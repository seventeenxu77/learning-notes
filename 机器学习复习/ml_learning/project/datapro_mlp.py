import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression # 逻辑回归模型
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings("ignore") # 忽略所有警告
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
# data process
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv',    header=None)

num_features = 512

# training set
X_train_full = train_df.iloc[:, 0:num_features].values 
Y_train_full = train_df.iloc[:, num_features].values 

# testing set
X_test = test_df.values


# 按照8:2的比例划分training set和test set
X_train, X_val, Y_train, Y_val = train_test_split(
    X_train_full, 
    Y_train_full, 
    test_size=0.2, 
    random_state=42, 
    stratify=Y_train_full 
)

print(f"\ntraining set sample: {X_train.shape[0]}")
print(f"testing set sample: {X_val.shape[0]}")

#standardization
scaler = StandardScaler()#均值0，方差1

X_train_scaled = scaler.fit_transform(X_train) #training set fit


X_val_scaled = scaler.transform(X_val)#不拟合，防止test的数据特征泄露
X_test_scaled = scaler.transform(X_test) #最后test数据同样处理


#PCA
pca = PCA(n_components=0.95, random_state=42)#保留 95% 的方差，降维k由PCA自动确定

# 仅用训练集的标准化数据拟合 PCA 模型
X_train_pca = pca.fit_transform(X_train_scaled)

# 使用已拟合的 PCA 模型转换验证集和测试集
X_val_pca = pca.transform(X_val_scaled)
X_test_pca = pca.transform(X_test_scaled)

print(f"PCA 选择保留的主成分数量: {pca.n_components_}")
print(f"降维后的训练集特征维度: {X_train_pca.shape}")

# ==================== [ 第四部分：多层感知机 (MLP) ] ====================
print("\n--- 4. 深度学习方法：多层感知器 (MLP) ---")

# 4.1 初始化模型
# hidden_layer_sizes=(256, 128): 设置两个隐藏层，第一层 256 个神经元，第二层 128 个
# activation='relu': 使用最主流的 ReLU 激活函数
# solver='adam': 深度学习中最常用的优化器，自适应调整学习率
# early_stopping=True: 自动划分出一部分验证集，如果分数连续几轮不提升就停止训练，防止过拟合
mlp = MLPClassifier(max_iter=500, random_state=42, early_stopping=True)

# 4.2 定义超参数网格
# alpha: L2 正则化项系数（防止神经元权重过大）
# learning_rate_init: 初始学习率，控制每次更新步子的大小
param_grid_mlp = {
    'hidden_layer_sizes': [(256, 128), (512,)],
    'alpha': [0.0001, 0.001],
    'learning_rate_init': [0.001, 0.01]
}

# 4.3 网格搜索
grid_search_mlp = GridSearchCV(
    estimator=mlp, 
    param_grid=param_grid_mlp, 
    scoring='accuracy', 
    cv=2, 
    n_jobs=-1, 
    verbose=3
)

print("开始 MLP 神经网络训练（深度学习方法）...")
grid_search_mlp.fit(X_train_pca, Y_train)

# 4.4 提取最佳模型
best_mlp = grid_search_mlp.best_estimator_
print(f"\nMLP 最佳参数: {grid_search_mlp.best_params_}")

# 4.5 验证集评估
val_accuracy_mlp = best_mlp.score(X_val_pca, Y_val)
print(f"MLP 在验证集上的准确率: {val_accuracy_mlp:.4f}")

# 4.6 生成针对 MLP 的 Kaggle 提交文件
test_predictions_mlp = best_mlp.predict(X_test_pca)
submission_mlp = pd.DataFrame({
    'Id': np.arange(len(test_predictions_mlp)),
    'Label': test_predictions_mlp
})
submission_mlp.to_csv('submission_mlp.csv', index=False)
print("提交文件 'submission_mlp.csv' 已生成！")