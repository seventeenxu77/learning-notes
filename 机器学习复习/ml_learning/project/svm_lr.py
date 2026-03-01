import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import warnings

# 忽略警告，保持控制台整洁
warnings.filterwarnings("ignore") 

# --- 1. 数据加载 ---
# 确保 train.csv 和 test.csv 在同一目录下
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

num_features = 512
X_all = train_df.iloc[:, 0:num_features].values 
y_all = train_df.iloc[:, num_features].values 
X_test = test_df.values

# --- 2. 设置集成参数 ---
n_splits = 10
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# 用于存储累加的测试集概率（N行 x 100个类别）
all_test_probs = np.zeros((X_test.shape[0], 100)) 

# 记录各折得分，用于最后分析
fold_scores_lr = []
fold_scores_svc = []
fold_scores_ensemble = []

# --- 3. 核心 K 折循环 ---
fold = 1
for train_index, val_index in skf.split(X_all, y_all):
    print(f"\n🚀 正在处理第 {fold}/{n_splits} 折...")
    
    # 划分训练/验证集
    X_train_fold, X_val_fold = X_all[train_index], X_all[val_index]
    y_train_fold, y_val_fold = y_all[train_index], y_all[val_index]
    
    # --- 统一的特征工程 (PCA 0.98) ---
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_fold)
    X_val_scaled = scaler.transform(X_val_fold)
    X_test_scaled = scaler.transform(X_test)
    
    pca = PCA(n_components=0.98, random_state=42)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_val_pca = pca.transform(X_val_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    
    # --- 模型 A: 强力逻辑回归 (LR) ---
    lr = LogisticRegression(
        solver='saga', 
        C=0.008, 
        penalty='l2', 
        max_iter=1000, 
        random_state=42, 
        n_jobs=-1
    )
    lr.fit(X_train_pca, y_train_fold)
    
    # --- 模型 B: 线性 SVM (带概率校准) ---
    # SVM 的决策边界和 LR 互补，能处理 LR 难以确定的边缘样本
    base_svc = LinearSVC(C=0.01, dual=False, random_state=42, max_iter=2000)
    # CalibratedClassifierCV 让原本不支持概率输出的 LinearSVC 能够输出 predict_proba
    svc = CalibratedClassifierCV(base_svc, cv=3) 
    svc.fit(X_train_pca, y_train_fold)
    
    # --- 计算验证集得分（监控融合效果） ---
    p_lr_val = lr.predict_proba(X_val_pca)
    p_svc_val = svc.predict_proba(X_val_pca)
    
    # 融合概率：50% LR + 50% SVM
    p_ens_val = (p_lr_val + p_svc_val) / 2
    y_pred_ens = np.argmax(p_ens_val, axis=1)
    
    acc_lr = lr.score(X_val_pca, y_val_fold)
    acc_svc = svc.score(X_val_pca, y_val_fold)
    acc_ens = np.mean(y_pred_ens == y_val_fold)
    
    fold_scores_lr.append(acc_lr)
    fold_scores_svc.append(acc_svc)
    fold_scores_ensemble.append(acc_ens)
    
    print(f"   - LR: {acc_lr:.4f} | SVM: {acc_svc:.4f} | 混合融合: {acc_ens:.4f}")
    
    # --- 预测测试集并累加概率 ---
    p_lr_test = lr.predict_proba(X_test_pca)
    p_svc_test = svc.predict_proba(X_test_pca)
    all_test_probs += (p_lr_test + p_svc_test) / 2
    
    fold += 1

# --- 4. 最终统计分析 ---
print("\n" + "="*45)
print(f"💡 10-Fold LR  平均准确率: {np.mean(fold_scores_lr):.4f}")
print(f"💡 10-Fold SVM 平均准确率: {np.mean(fold_scores_svc):.4f}")
print(f"💡 10-Fold 融合平均准确率: {np.mean(fold_scores_ensemble):.4f} ✨")
print(f"   (融合标准差: {np.std(fold_scores_ensemble):.4f})")
print("="*45)

# --- 5. 生成最终提交文件 ---
final_probs = all_test_probs / n_splits
final_predictions = np.argmax(final_probs, axis=1)

submission = pd.DataFrame({
    'Id': np.arange(len(final_predictions)),
    'Label': final_predictions
})
output_file = 'submission_lr_svm_ensemble.csv'
submission.to_csv(output_file, index=False)

print(f"\n✅ 终极混合集成文件 '{output_file}' 已生成")