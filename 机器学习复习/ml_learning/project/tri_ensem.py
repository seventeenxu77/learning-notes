import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, classification_report, log_loss
import warnings
import time

# 忽略不必要的警告
warnings.filterwarnings("ignore") 

# --- 1. 配置参数 ---
W_LR = 0.75    
W_SVC = 0.15   
W_RIDGE = 0.10 
N_SPLITS = 10
PCA_COMPONENTS = 0.98 

def calculate_entropy(probs):
    """计算预测结果的熵，熵越低代表模型越自信"""
    return -np.mean(np.sum(probs * np.log(probs + 1e-12), axis=1))

# --- 2. 数据加载 ---
print("📂 [1/5] 正在加载数据...")
train_df = pd.read_csv('train.csv', header=None) 
test_df = pd.read_csv('test.csv', header=None)

X_all = train_df.iloc[:, 0:512].values 
y_all = train_df.iloc[:, 512].values 
X_test_raw = test_df.values

skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=42)
all_test_probs = np.zeros((X_test_raw.shape[0], 100)) 

# 存储所有折的详细统计
detailed_stats = []

print(f"\n⚔️ [2/5] 启动诊断模式：LR({W_LR}) + SVM({W_SVC}) + Ridge({W_RIDGE})")
print("=" * 130)
header = f"{'折数':^4} | {'LR ACC':^8} | {'SVM ACC':^8} | {'Ridge ACC':^9} | {'融合 ACC':^8} | {'增益':^8} | {'LR熵':^6} | {'一致性(L-S)':^9}"
print(header)
print("-" * 130)

start_time = time.time()

for fold, (train_index, val_index) in enumerate(skf.split(X_all, y_all), 1):
    X_tr, X_va = X_all[train_index], X_all[val_index]
    y_tr, y_va = y_all[train_index], y_all[val_index]
    
    # --- 特征工程 ---
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_va_s = scaler.transform(X_va)
    X_te_s = scaler.transform(X_test_raw)
    
    pca = PCA(n_components=PCA_COMPONENTS, random_state=42)
    X_tr_p = pca.fit_transform(X_tr_s)
    X_va_p = pca.transform(X_va_s)
    X_te_p = pca.transform(X_te_s)
    
    # --- 模型 A: LR ---
    lr = LogisticRegression(solver='saga', C=0.008, penalty='l2', max_iter=1000, n_jobs=-1, random_state=666)
    lr.fit(X_tr_p, y_tr)
    p_lr_va = lr.predict_proba(X_va_p)
    p_lr_te = lr.predict_proba(X_te_p)
    
    # --- 模型 B: SVC ---
    base_svc = LinearSVC(C=0.01, dual=False, random_state=42, max_iter=2000)
    svc = CalibratedClassifierCV(base_svc, cv=3) 
    svc.fit(X_tr_p, y_tr)
    p_svc_va = svc.predict_proba(X_va_p)
    p_svc_te = svc.predict_proba(X_te_p)

    # --- 模型 C: Ridge ---
    base_ridge = RidgeClassifier(alpha=1.0, random_state=42)
    ridge = CalibratedClassifierCV(base_ridge, cv=3)
    ridge.fit(X_tr_p, y_tr)
    p_ridge_va = ridge.predict_proba(X_va_p)
    p_ridge_te = ridge.predict_proba(X_te_p)
    
    # --- 融合与诊断 ---
    p_ens_va = (p_lr_va * W_LR) + (p_svc_va * W_SVC) + (p_ridge_va * W_RIDGE)
    y_pred_va = np.argmax(p_ens_va, axis=1)
    
    # 计算各项指标
    acc_lr = accuracy_score(y_va, np.argmax(p_lr_va, axis=1))
    acc_svc = accuracy_score(y_va, np.argmax(p_svc_va, axis=1))
    acc_ridge = accuracy_score(y_va, np.argmax(p_ridge_va, axis=1))
    acc_ens = accuracy_score(y_va, y_pred_va)
    
    # 诊断数据
    ent_lr = calculate_entropy(p_lr_va)
    cons_ls = np.mean(np.argmax(p_lr_va, axis=1) == np.argmax(p_svc_va, axis=1))
    gain = acc_ens - acc_lr
    
    print(f"F{fold:02d} | {acc_lr:.5f} | {acc_svc:.5f} | {acc_ridge:.5f} | {acc_ens:.5f} | {gain:+.5f} | {ent_lr:.3f} | {cons_ls:.2%}")
    
    detailed_stats.append({
        'fold': fold, 'lr': acc_lr, 'svc': acc_svc, 'ridge': acc_ridge, 'ens': acc_ens,
        'loss': log_loss(y_va, p_ens_va)
    })
    
    # 累加测试集概率
    all_test_probs += ((p_lr_te * W_LR) + (p_svc_te * W_SVC) + (p_ridge_te * W_RIDGE)) / N_SPLITS

# --- 4. 深度报告 ---
print("\n📊 [3/5] 训练总结报告")
print("-" * 60)
df_stats = pd.DataFrame(detailed_stats)
print(f"平均准确率: {df_stats['ens'].mean():.6f} (±{df_stats['ens'].std():.4f})")
print(f"平均 LogLoss: {df_stats['loss'].mean():.6f}")
print(f"最大单折准确率: {df_stats['ens'].max():.6f}")
print(f"模型分歧度 (LR vs SVM): {1 - cons_ls:.2%}")

# --- 5. 提交准备 ---
print("\n💾 [4/5] 正在生成提交文件...")
final_predictions = np.argmax(all_test_probs, axis=1)
pd.DataFrame({'Id': np.arange(len(final_predictions)), 'Label': final_predictions}).to_csv('submission_pro_triple.csv', index=False)

print(f"\n✅ [5/5] 完成！总耗时: {(time.time() - start_time)/60:.2f} 分钟")