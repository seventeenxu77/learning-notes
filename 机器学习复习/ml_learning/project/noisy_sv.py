# 加入噪音后准确率降低到了0.8840
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
import warnings
warnings.filterwarnings("ignore") 

# ----------------- 1. 数据加载与基础处理 -----------------
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)
num_features = 512

X_train_full = train_df.iloc[:, 0:num_features].values 
Y_train_full = train_df.iloc[:, num_features].values 
X_test = test_df.values

X_train, X_val, Y_train, Y_val = train_test_split(
    X_train_full, Y_train_full, test_size=0.2, random_state=42, stratify=Y_train_full 
)

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# PCA 降维 (建议尝试提高到 0.98 以保留更多细节)
pca = PCA(n_components=0.95, random_state=42)
X_train_pca = pca.fit_transform(X_train_scaled)
X_val_pca = pca.transform(X_val_scaled)
X_test_pca = pca.transform(X_test_scaled)

print(f"PCA 保留主成分数量: {pca.n_components_}")

# ----------------- 🌟 2. 增加高斯噪声增强 -----------------
def add_gaussian_noise(X, noise_level=0.01):
    """为矩阵注入随机高斯噪声"""
    sigma = np.std(X) * noise_level
    noise = np.random.normal(0, sigma, X.shape)
    return X + noise

print("\n--- 正在进行数据增强 ---")
# 生成带噪声的副本
X_train_pca_noisy = add_gaussian_noise(X_train_pca, noise_level=0.02)

# 方案：将原始降维数据与噪声数据合并，样本量翻倍
X_train_combined = np.vstack([X_train_pca, X_train_pca_noisy])
Y_train_combined = np.concatenate([Y_train, Y_train])

print(f"原始训练样本量: {X_train_pca.shape[0]}")
print(f"增强后训练样本量: {X_train_combined.shape[0]}")

# ----------------- 3. SVM 模型训练 (使用增强后的数据) -----------------
print("\n--- 3. SVM 训练 (带噪声增强) ---")

svc = LinearSVC(dual=False, max_iter=2000, random_state=42)
param_grid_svc = {'C': [0.01, 0.1, 1, 10]}

grid_search_svc = GridSearchCV(
    estimator=svc, 
    param_grid=param_grid_svc, 
    scoring='accuracy', 
    cv=2, 
    n_jobs=-1, 
    verbose=3
)

# 注意：这里使用的是增强后的 X_train_combined
grid_search_svc.fit(X_train_combined, Y_train_combined)

best_svc = grid_search_svc.best_estimator_
print(f"SVM 最佳参数: {grid_search_svc.best_params_}")

# 验证集评估 (验证集不加噪声！)
val_accuracy_svc = best_svc.score(X_val_pca, Y_val)
print(f"SVM 在验证集上的准确率: {val_accuracy_svc:.4f}")

# 生成提交文件
test_predictions_svc = best_svc.predict(X_test_pca)
submission_svc = pd.DataFrame({
    'Id': np.arange(len(test_predictions_svc)),
    'Label': test_predictions_svc
})
submission_svc.to_csv('submission_svc_noisy.csv', index=False)