import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import accuracy_score
import warnings

# 忽略警告
warnings.filterwarnings("ignore") 

# --- 1. 数据加载 ---
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

num_features = 512
X_train_full = train_df.iloc[:, 0:num_features].values 
Y_train_full = train_df.iloc[:, num_features].values 
X_test = test_df.values

# --- 2. 数据划分 (8:2 比例) ---
X_train, X_val, Y_train, Y_val = train_test_split(
    X_train_full, 
    Y_train_full, 
    test_size=0.2, 
    random_state=42, 
    stratify=Y_train_full 
)

# --- 3. 标准化 ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# --- 4. PCA 降维 (保留 95% 方差) ---
pca = PCA(n_components=0.98, random_state=42)
X_train_pca = pca.fit_transform(X_train_scaled)
X_val_pca = pca.transform(X_val_scaled)
X_test_pca = pca.transform(X_test_scaled)

print(f"PCA 选择保留的主成分数量: {pca.n_components_}")

# --- 5. 模型训练 - 多分类逻辑回归 ---
# 使用 saga 求解器，适合大数据集和多分类
log_reg = LogisticRegression(solver='saga', max_iter=1000, random_state=42) 

# 超参数搜索空间
param_grid = {
    'penalty': ['l1', 'l2'], 
    'C': [0.001, 0.005, 0.01]
}

# GridSearchCV (cv=2 是拿到 0.8968 的关键参数之一)
grid_search_lr = GridSearchCV(
    estimator=log_reg, 
    param_grid=param_grid, 
    scoring='accuracy', 
    cv=2, 
    verbose=3, 
    n_jobs=-1
)

grid_search_lr.fit(X_train_pca, Y_train) 

# --- 6. 评估与生成结果 ---
best_lr = grid_search_lr.best_estimator_
val_accuracy_lr = best_lr.score(X_val_pca, Y_val)

print(f"\n最佳参数: {grid_search_lr.best_params_}")
print(f"验证集准确率: {val_accuracy_lr:.4f}")

# 生成 Kaggle 提交文件
test_predictions = best_lr.predict(X_test_pca)
submission = pd.DataFrame({
    'Id': np.arange(len(test_predictions)),
    'Label': test_predictions
})
submission.to_csv('submission_baseline.csv', index=False)