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
# 2. 参数设置
# ==========================================
n_splits = 10
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# 用于存储累加的测试集排名分
all_test_ranks = np.zeros((X_test_raw.shape[0], 100)) 

fold_scores_lr = []
fold_scores_svc = []
fold_scores_ens = []

print(f"\n🚀 启动终极冲刺：10-Fold + 秩平均融合 (Rank Averaging)...")
print("-" * 70)
print(f"{'折数':^5} | {'LR 得分':^10} | {'SVM 得分':^10} | {'融合(Rank)':^12} | {'提升度':^8}")
print("-" * 70)

# ==========================================
# 3. 核心 K 折循环
# ==========================================
for fold, (train_index, val_index) in enumerate(skf.split(X_all, y_all), 1):
    X_train_fold, X_val_fold = X_all[train_index], X_all[val_index]
    y_train_fold, y_val_fold = y_all[train_index], y_all[val_index]
    
    # 统一标准化
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train_fold)
    X_val_s = scaler.transform(X_val_fold)
    X_test_s = scaler.transform(X_test_raw)
    
    # 使用统一的高精度特征空间
    pca = PCA(n_components=0.99, random_state=42)
    X_tr_p = pca.fit_transform(X_train_s)
    X_va_p = pca.transform(X_val_s)
    X_te_p = pca.transform(X_test_s)
    
    # --- 模型 A: LR ---
    lr = LogisticRegression(solver='saga', C=0.008, max_iter=1000, n_jobs=-1, random_state=42)
    lr.fit(X_tr_p, y_train_fold)
    
    # --- 模型 B: SVM ---
    base_svc = LinearSVC(C=0.01, dual=False, max_iter=2000, random_state=42)
    svc = CalibratedClassifierCV(base_svc, cv=3) 
    svc.fit(X_tr_p, y_train_fold)
    
    # --- 获取概率预测 ---
    p_lr_v = lr.predict_proba(X_va_p)
    p_svc_v = svc.predict_proba(X_va_p)
    
    p_lr_te = lr.predict_proba(X_te_p)
    p_svc_te = svc.predict_proba(X_te_p)

    # --- 核心：秩平均 (Rank Averaging) ---
    # argsort().argsort() 可以得到每个样本中类别的排名 (0-99)
    # 这样消除了概率绝对值的偏差
    rank_lr_v = p_lr_v.argsort().argsort()
    rank_svc_v = p_svc_v.argsort().argsort()
    
    rank_lr_te = p_lr_te.argsort().argsort()
    rank_svc_te = p_svc_te.argsort().argsort()
    
    # 验证集融合评估 (权重 0.7 LR + 0.3 SVM)
    # 给 LR 更高权重是因为它单模最强，SVM 仅作辅助修正
    res_v = (rank_lr_v * 0.7 + rank_svc_v * 0.3)
    y_pred_v = np.argmax(res_v, axis=1)
    
    # 分数统计
    acc_lr = np.mean(np.argmax(p_lr_v, axis=1) == y_val_fold)
    acc_svc = np.mean(np.argmax(p_svc_v, axis=1) == y_val_fold)
    acc_ens = np.mean(y_pred_v == y_val_fold)
    improvement = acc_ens - acc_lr
    
    fold_scores_lr.append(acc_lr)
    fold_scores_svc.append(acc_svc)
    fold_scores_ens.append(acc_ens)
    
    print(f"Fold {fold:2d} | {acc_lr:10.4f} | {acc_svc:10.4f} | {acc_ens:12.4f} | {improvement:+.4f}")
    
    # --- 测试集排名分累加 ---
    all_test_ranks += (rank_lr_te * 0.7 + rank_svc_te * 0.3)

# ==========================================
# 4. 统计结果
# ==========================================
print("-" * 70)
print(f"💡 平均得分 | LR: {np.mean(fold_scores_lr):.4f} | 融合(Rank): {np.mean(fold_scores_ens):.4f} ✨")
print("-" * 70)

# ==========================================
# 5. 生成提交文件
# ==========================================
final_predictions = np.argmax(all_test_ranks, axis=1)

submission = pd.DataFrame({
    'Id': np.arange(len(final_predictions)),
    'Label': final_predictions
})
output_file = 'submission_rank_ensemble.csv'
submission.to_csv(output_file, index=False)

print(f"\n🎉 秩平均融合文件 '{output_file}' 已生成！建议立即提交。")