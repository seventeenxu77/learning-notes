import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.neural_network import MLPClassifier
import warnings

# 忽略警告
warnings.filterwarnings("ignore") 

# --- 1. 数据加载 ---
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

num_features = 512
X_all = train_df.iloc[:, 0:num_features].values 
y_all = train_df.iloc[:, num_features].values 
X_test = test_df.values

# --- 2. 设置 K 折参数 ---
n_splits = 10
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# 用于存储最终融合的概率
all_test_probs = np.zeros((X_test.shape[0], 100)) 

# 记录分数
fold_scores_lr = []
fold_scores_mlp = []
fold_scores_ensemble = []

# --- 3. 核心 K 折循环 ---
fold = 1
for train_index, val_index in skf.split(X_all, y_all):
    print(f"\n🚀 正在处理第 {fold}/{n_splits} 折...")
    
    # 数据切分
    X_train_fold, X_val_fold = X_all[train_index], X_all[val_index]
    y_train_fold, y_val_fold = y_all[train_index], y_all[val_index]
    
    # 标准化与 PCA
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_fold)
    X_val_scaled = scaler.transform(X_val_fold)
    X_test_scaled = scaler.transform(X_test)
    
    pca = PCA(n_components=0.98, random_state=42)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_val_pca = pca.transform(X_val_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    
    # --- 模型 A: 逻辑回归 (LR) ---
    # 使用你之前验证的最强参数
    lr = LogisticRegression(solver='saga', C=0.008, penalty='l2', max_iter=1000, random_state=42, n_jobs=-1)
    lr.fit(X_train_pca, y_train_fold)
    
    # --- 模型 B: 多层感知机 (MLP) ---
    # 增加 alpha 正则化防止过拟合，设置两层隐藏层捕捉非线性特征
    mlp = MLPClassifier(hidden_layer_sizes=(256, 128), alpha=0.05, max_iter=500, random_state=42)
    mlp.fit(X_train_pca, y_train_fold)
    
    # --- 概率融合 ---
    prob_lr_val = lr.predict_proba(X_val_pca)
    prob_mlp_val = mlp.predict_proba(X_val_pca)
    
    # 在验证集上测试融合效果 (权重的配比可以微调，这里推荐 LR:MLP = 0.6:0.4)
    ensemble_val_probs = 0.6 * prob_lr_val + 0.4 * prob_mlp_val
    ensemble_val_labels = np.argmax(ensemble_val_probs, axis=1)
    
    # 记录各方表现
    acc_lr = lr.score(X_val_pca, y_val_fold)
    acc_mlp = mlp.score(X_val_pca, y_val_fold)
    acc_ens = np.mean(ensemble_val_labels == y_val_fold)
    
    fold_scores_lr.append(acc_lr)
    fold_scores_mlp.append(acc_mlp)
    fold_scores_ensemble.append(acc_ens)
    
    print(f"   - LR 分数: {acc_lr:.4f} | MLP 分数: {acc_mlp:.4f} | 融合分数: {acc_ens:.4f}")
    
    # 累加测试集概率
    prob_lr_test = lr.predict_proba(X_test_pca)
    prob_mlp_test = mlp.predict_proba(X_test_pca)
    all_test_probs += (0.6 * prob_lr_test + 0.4 * prob_mlp_test)
    
    fold += 1

# --- 4. 统计与生成 ---
print("\n" + "="*40)
print(f"💡 LR 平均分: {np.mean(fold_scores_lr):.4f}")
print(f"💡 MLP 平均分: {np.mean(fold_scores_mlp):.4f}")
print(f"💡 融合平均分: {np.mean(fold_scores_ensemble):.4f}")

# 最终预测
final_predictions = np.argmax(all_test_probs / n_splits, axis=1)

submission = pd.DataFrame({
    'Id': np.arange(len(final_predictions)),
    'Label': final_predictions
})
submission.to_csv('submission_lr_mlp_ensemble.csv', index=False) 
print("\n✅ 终极混合集成文件已生成！快去提交吧！")