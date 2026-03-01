import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD  # 核心替换
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import warnings
import time

warnings.filterwarnings("ignore")

# --- 1. 配置参数 ---
W_LR, W_SVC = 0.85, 0.15
N_SPLITS = 10
SVD_COMPONENTS = 80  # SVD通常需要指定具体的维度，256是一个兼顾信息与压缩的黄金点
SEED = 42            
TOP_K_PSEUDO = 800 

# --- 2. 数据加载 ---
print("📂 正在加载数据...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

X_train_orig = train_df.iloc[:, 0:512].values
y_train_orig = train_df.iloc[:, 512].values
X_test_raw = test_df.values

# ==========================================
# 阶段 1: 基础预测
# ==========================================
print(f"\n--- 阶段 1: 基础预测 (使用 TruncatedSVD 提取特征) ---")

skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
initial_test_probs = np.zeros((X_test_raw.shape[0], 100))
stage1_accs = []

for fold, (tr_idx, va_idx) in enumerate(skf.split(X_train_orig, y_train_orig), 1):
    X_tr, X_va = X_train_orig[tr_idx], X_train_orig[va_idx]
    y_tr, y_va = y_train_orig[tr_idx], y_train_orig[va_idx]
    
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_va_s = scaler.transform(X_va)
    X_te_s = scaler.transform(X_test_raw)
    
    # 替换 PCA 为 TruncatedSVD
    svd = TruncatedSVD(n_components=SVD_COMPONENTS, random_state=SEED)
    X_tr_p = svd.fit_transform(X_tr_s)
    X_va_p = svd.transform(X_va_s)
    X_te_p = svd.transform(X_te_s)
    
    if fold == 1:
        print(f"📌 SVD 降维完成：512维 -> {X_tr_p.shape[1]}维 (解释方差比: {np.sum(svd.explained_variance_ratio_):.4f})")

    lr = LogisticRegression(solver='saga', C=0.008, max_iter=1000, n_jobs=-1, random_state=SEED)
    lr.fit(X_tr_p, y_tr)
    svc = CalibratedClassifierCV(LinearSVC(C=0.01, dual=False, random_state=SEED), cv=3)
    svc.fit(X_tr_p, y_tr)
    
    p_ens_va = (lr.predict_proba(X_va_p) * W_LR) + (svc.predict_proba(X_va_p) * W_SVC)
    stage1_accs.append(np.mean(np.argmax(p_ens_va, axis=1) == y_va))
    
    initial_test_probs += (lr.predict_proba(X_te_p) * W_LR + svc.predict_proba(X_te_p) * W_SVC) / N_SPLITS
    print(f"Fold {fold:02d} | 验证集 ACC: {stage1_accs[-1]:.4f}")

# --- 核心：精英筛选逻辑 ---
sorted_probs = np.sort(initial_test_probs, axis=1)
margins = sorted_probs[:, -1] - sorted_probs[:, -2]
pseudo_labels = np.argmax(initial_test_probs, axis=1)

threshold = np.partition(margins, -TOP_K_PSEUDO)[-TOP_K_PSEUDO]
mask = margins >= threshold

X_pseudo = X_test_raw[mask][:TOP_K_PSEUDO]
y_pseudo = pseudo_labels[mask][:TOP_K_PSEUDO]

print(f"\n📢 筛选完成！动态差值阈值: {threshold:.4f}")
print(f"   --> 选定的伪标签数量: {len(y_pseudo)}")

# ==========================================
# 阶段 2: 增强训练
# ==========================================
print(f"\n--- 阶段 2: 伪标签增强训练 (TruncatedSVD) ---")
print("-" * 110)
print(f"{'折数':^5} | {'新得分':^8} | {'净增益':^8} | {'状态':^7}")
print("-" * 110)

final_test_probs = np.zeros((X_test_raw.shape[0], 100))
stage2_accs = []
skf_final = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)

for fold, (tr_idx, va_idx) in enumerate(skf_final.split(X_train_orig, y_train_orig), 1):
    X_tr_fold = np.vstack([X_train_orig[tr_idx], X_pseudo])
    y_tr_fold = np.concatenate([y_train_orig[tr_idx], y_pseudo])
    X_va_fold = X_train_orig[va_idx]
    y_va_fold = y_train_orig[va_idx]
    
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr_fold)
    X_va_s = scaler.transform(X_va_fold)
    X_te_s = scaler.transform(X_test_raw)
    
    # 替换 PCA 为 TruncatedSVD
    svd = TruncatedSVD(n_components=SVD_COMPONENTS, random_state=SEED)
    X_tr_p = svd.fit_transform(X_tr_s)
    X_va_p = svd.transform(X_va_s)
    X_te_p = svd.transform(X_te_s)
    
    lr = LogisticRegression(solver='saga', C=0.008, max_iter=1000, n_jobs=-1, random_state=SEED)
    lr.fit(X_tr_p, y_tr_fold)
    svc = CalibratedClassifierCV(LinearSVC(C=0.01, dual=False, random_state=SEED), cv=3)
    svc.fit(X_tr_p, y_tr_fold)
    
    p_ens_va = (lr.predict_proba(X_va_p) * W_LR) + (svc.predict_proba(X_va_p) * W_SVC)
    acc_ens = np.mean(np.argmax(p_ens_va, axis=1) == y_va_fold)
    stage2_accs.append(acc_ens)
    
    gain = acc_ens - stage1_accs[fold-1]
    status = "🔥 提升" if gain > 0 else "❄️ 退步"
    print(f"Fold {fold:02d} | {acc_ens:8.4f} | {gain:+.5f} | {status}")
    
    final_test_probs += (lr.predict_proba(X_te_p) * W_LR + svc.predict_proba(X_te_p) * W_SVC) / N_SPLITS

print("-" * 110)
print(f"📊 阶段 1 均分: {np.mean(stage1_accs):.5f} | 阶段 2 均分: {np.mean(stage2_accs):.5f}")
print(f"✨ 预估线上增益: {np.mean(stage2_accs) - np.mean(stage1_accs):+.5f}")

final_preds = np.argmax(final_test_probs, axis=1)
pd.DataFrame({'Id': np.arange(len(final_preds)), 'Label': final_preds}).to_csv('submission_svd_pseudo.csv', index=False)
print("\n✅ 结果已生成：submission_svd_pseudo.csv")