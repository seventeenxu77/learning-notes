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
# # 画二维图==========================================================================
# def plot_pca_2d(X_pca, y, title="PCA 2D Visualization"):
#     plt.figure(figsize=(12, 8))
    
#     # 选取 PCA 的前两个维度
#     # X_pca[:, 0] 是第一主成分，X_pca[:, 1] 是第二主成分
#     sns.scatterplot(
#         x=X_pca[:, 0], 
#         y=X_pca[:, 1], 
#         hue=y, 
#         palette="viridis", 
#         legend=None,  # 100个类别图例太乱，暂时关闭
#         alpha=0.6
#     )
    
#     plt.title(title)
#     plt.xlabel("First Principal Component")
#     plt.ylabel("Second Principal Component")
#     plt.grid(True)
#     plt.show()
# # 画图================================================
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')

# # 选取前三个主成分
# ax.scatter(X_val_pca[:, 0], X_val_pca[:, 1], X_val_pca[:, 2], c=Y_val, cmap='viridis', s=10)

# ax.set_title("PCA 3D Visualization")
# ax.set_xlabel("PC1")
# ax.set_ylabel("PC2")
# ax.set_zlabel("PC3")
# plt.show()
# # 调用函数：绘制验证集的降维分布图
# plot_pca_2d(X_val_pca, Y_val, "PCA Visualization of Validation Set (100 Classes)")
# ==================== [ 第二部分：模型训练 - 多分类逻辑回归 ] ====================

# # 1.1 定义模型和超参数搜索空间
# # 由于有 100 个类别，使用 'lbfgs' 或 'saga' 作为求解器
# # C 是正则化强度的倒数，C 越小，正则化越强
# # multi_class='multinomial' 启用多分类模式
# log_reg = LogisticRegression(solver='saga', max_iter=1000, random_state=42) 

# # 定义超参数网格：尝试 L1 和 L2 正则化，以及不同的正则化强度 C
# param_grid = {
#     'penalty': ['l1', 'l2'], 
#     'C': [0.01, 0.1, 1.0, 10.0] # C 的搜索范围
# }
# # param_grid = {'C': [0.1], 'penalty': ['l2']} # 快速测试用
# # 1.2 使用 GridSearchCV 进行超参数调优 (模型评估和选择方法一)
# # 在 X_train_pca 上进行训练，并使用内置的交叉验证进行内部评估
# # cv=3 表示 3 折交叉验证
# grid_search_lr = GridSearchCV(
#     estimator=log_reg, 
#     param_grid=param_grid, 
#     scoring='accuracy', 
#     cv=2, 
#     verbose=3, 
#     n_jobs=-1
# )

# # 使用降维后的训练集拟合网格搜索
# grid_search_lr.fit(X_train_pca, Y_train) 

# # 1.3 提取最佳模型和结果
# best_lr = grid_search_lr.best_estimator_
# best_params_lr = grid_search_lr.best_params_

# print(f"\n最佳逻辑回归参数: {best_params_lr}")

# # 1.4 在验证集上进行最终评估
# Y_val_pred_lr = best_lr.predict(X_val_pca)
# val_accuracy_lr = accuracy_score(Y_val, Y_val_pred_lr)

# print(f"逻辑回归在验证集上的准确率: {val_accuracy_lr:.4f}")

# # 1.5 模型的鲁棒性评估：交叉验证 (模型评估和选择方法二)
# # 使用全量训练集（降维后）进行 K-Fold 评估，以获得更稳健的泛化能力估计
# # 这里使用 X_train_full_pca 对应完整训练集
# print("\n--- 鲁棒性评估 (5-Fold Cross-Validation) ---")
# # 注意：在GridSearch内部已经使用了交叉验证，但这里展示如何独立进行CV。
# # 重新将完整训练集进行降维
# X_train_full_scaled = scaler.transform(X_train_full)
# X_train_full_pca = pca.transform(X_train_full_scaled)

# cv_scores = cross_val_score(
#     best_lr, 
#     X_train_full_pca, 
#     Y_train_full, 
#     cv=5, 
#     scoring='accuracy', 
#     n_jobs=-1
# )

# print(f"5-Fold CV 准确率: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
# # # 1. 使用逻辑回归模型对测试集进行预测
# # test_predictions = best_lr.predict(X_test_pca)

# # # 2. 创建 DataFrame，确保列名完全符合要求
# # submission = pd.DataFrame({
# #     'Id': np.arange(len(test_predictions)), # 生成 0 到 9999 的 ID
# #     'Label': test_predictions               # 填入预测结果
# # })

# # # 3. 保存为 csv 文件，index=False 表示不保存 DataFrame 自带的索引行
# # submission.to_csv('submission_lr.csv', index=False)

# # print("\n符合格式的提交文件 'submission_lr.csv' 已生成！")


# ==================== [ 第三部分：下一个模型（待补充） ] ====================

# # 接下来您可以继续添加第二个模型 (例如：Linear SVM) 的训练和评估代码。
# # ...


# # 2.1 初始化模型
# # dual=False 是为了加速样本量大于特征数的情况
# # multi_class='ovr' (One-vs-Rest) 处理 100 分类
# svc = LinearSVC(dual=False, max_iter=2000, random_state=42)

# # 2.2 定义超参数网格
# # C 是 SVM 的惩罚参数：C 越大，对错误分类的容忍度越低（易过拟合）；C 越小，间隔越大（泛化性好）
# param_grid_svc = {
#     'C': [0.001, 0.01, 0.1, 1, 10]
# }

# # 2.3 网格搜索与交叉验证
# grid_search_svc = GridSearchCV(
#     estimator=svc, 
#     param_grid=param_grid_svc, 
#     scoring='accuracy', 
#     cv=2,          # 保持与逻辑回归一致的折数方便对比
#     n_jobs=-1, 
#     verbose=3
# )

# print("开始 SVM 网格搜索训练...")
# grid_search_svc.fit(X_train_pca, Y_train)

# # 2.4 提取最佳模型
# best_svc = grid_search_svc.best_estimator_
# print(f"\nSVM 最佳参数: {grid_search_svc.best_params_}")

# # 2.5 验证集评估
# val_accuracy_svc = best_svc.score(X_val_pca, Y_val)
# print(f"SVM 在验证集上的准确率: {val_accuracy_svc:.4f}")

# # 2.6 生成针对 SVM 的 Kaggle 提交文件
# test_predictions_svc = best_svc.predict(X_test_pca)
# submission_svc = pd.DataFrame({
#     'Id': np.arange(len(test_predictions_svc)),
#     'Label': test_predictions_svc
# })
# submission_svc.to_csv('submission_svc.csv', index=False)
# print("提交文件 'submission_svc.csv' 已生成！")

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