import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import warnings

# 忽略警告
warnings.filterwarnings("ignore") 

# ==========================================
# 1. 数据加载
# ==========================================
print("📂 正在加载数据...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

num_features = 512
X_all = train_df.iloc[:, 0:num_features].values 
y_all = train_df.iloc[:, num_features].values 
X_test_raw = test_df.values

# ==========================================
# 2. 阶段一：10-Fold 交叉验证（监控独立表现）
# ==========================================
n_splits = 10
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

all_test_probs = np.zeros((X_test_raw.shape[0], 100)) 
fold_scores_lr = []
fold_scores_svc = []
fold_scores_ens = []

print(f"\n🚀 启动第一阶段：{n_splits}-Fold 集成训练...")

for fold, (train_idx, val_idx) in enumerate(skf.split(X_all, y_all), 1):
    X_train_f, X_val_f = X_all[train_idx], X_all[val_idx]
    y_train_f, y_val_f = y_all[train_idx], y_all[val_idx]
    
    # 特征工程 (提高到 0.99 以保留更多微小特征)
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_train_f)
    X_va_s = scaler.transform(X_val_f)
    X_te_s = scaler.transform(X_test_raw)
    
    pca = PCA(n_components=0.99, random_state=42)
    X_tr_p = pca.fit_transform(X_tr_s)
    X_va_p = pca.transform(X_va_s)
    X_te_p = pca.transform(X_te_s)
    
    # 模型 A: Logistic Regression (权重 0.6)
    lr = LogisticRegression(solver='saga', C=0.008, max_iter=1000, n_jobs=-1, random_state=42)
    lr.fit(X_tr_p, y_train_f)
    
    # 模型 B: Calibrated SVM (权重 0.4)
    base_svc = LinearSVC(C=0.01, dual=False, max_iter=2000, random_state=42)
    svc = CalibratedClassifierCV(base_svc, cv=3)
    svc.fit(X_tr_p, y_train_f)
    
    # 验证集评估
    p_lr_v = lr.predict_proba(X_va_p)
    p_svc_v = svc.predict_proba(X_va_p)
    
    # 融合预测 (基于 LR 和 SVM 的不同表现手动调权)
    p_ens_v = (p_lr_v * 0.6 + p_svc_v * 0.4)
    
    acc_lr = np.mean(np.argmax(p_lr_v, axis=1) == y_val_f)
    acc_svc = np.mean(np.argmax(p_svc_v, axis=1) == y_val_f)
    acc_ens = np.mean(np.argmax(p_ens_v, axis=1) == y_val_f)
    
    fold_scores_lr.append(acc_lr)
    fold_scores_svc.append(acc_svc)
    fold_scores_ens.append(acc_ens)
    
    # 核心日志：让你看清谁在出力
    print(f"   Fold {fold:2d} | LR: {acc_lr:.4f} | SVM: {acc_svc:.4f} | 融合: {acc_ens:.4f}")
    
    # 累加测试集概率
    all_test_probs += (lr.predict_proba(X_te_p) * 0.6 + svc.predict_proba(X_te_p) * 0.4) / n_splits

print("-" * 50)
print(f"✅ 平均表现 | LR: {np.mean(fold_scores_lr):.4f} | SVM: {np.mean(fold_scores_svc):.4f} | 融合: {np.mean(fold_scores_ens):.4f}")

# ==========================================
# 3. 阶段二：伪标签 (阈值下调至 0.80 以激活进化)
# ==========================================
print("\n🔍 启动第二阶段：伪标签筛选...")

max_probs = np.max(all_test_probs, axis=1)
pseudo_labels = np.argmax(all_test_probs, axis=1)

# 将阈值降至 0.80，确保能筛选出足够样本覆盖测试集分布
threshold = 0.80 
mask = max_probs > threshold

X_pseudo = X_test_raw[mask]
y_pseudo = pseudo_labels[mask]

print(f"📈 发现高置信度样本: {len(y_pseudo)} 个")

if len(y_pseudo) > 100:
    print("🧬 正在合并数据集并进行终极全量重训...")
    X_combined = np.vstack([X_all, X_pseudo])
    y_combined = np.concatenate([y_all, y_pseudo])
    
    final_scaler = StandardScaler()
    X_comb_s = final_scaler.fit_transform(X_combined)
    X_te_s_final = final_scaler.transform(X_test_raw)
    
    # 终极训练使用更高维度的 PCA (0.995)
    final_pca = PCA(n_components=0.995, random_state=42)
    X_comb_p = final_pca.fit_transform(X_comb_s)
    X_te_p_final = final_pca.transform(X_te_s_final)
    
    final_lr = LogisticRegression(solver='saga', C=0.008, max_iter=1000, n_jobs=-1)
    final_svc = CalibratedClassifierCV(LinearSVC(C=0.01, dual=False, max_iter=2000), cv=3)
    
    final_lr.fit(X_comb_p, y_combined)
    final_svc.fit(X_comb_p, y_combined)
    
    # 最终输出稍微偏向 LR 一点点 (0.55/0.45)
    res_probs = (final_lr.predict_proba(X_te_p_final) * 0.55 + final_svc.predict_proba(X_te_p_final) * 0.45)
    final_predictions = np.argmax(res_probs, axis=1)
    print("✨ 终极重训完成！")
else:
    print("⚠️ 满足条件的样本不足，维持第一阶段结果。")
    final_predictions = np.argmax(all_test_probs, axis=1)

# ==========================================
# 4. 生成提交文件
# ==========================================
submission = pd.DataFrame({'Id': np.arange(len(final_predictions)), 'Label': final_predictions})
submission.to_csv('submission_ultra_final.csv', index=False)
print("\n🎉 最终文件 'submission_ultra_final.csv' 已生成！")