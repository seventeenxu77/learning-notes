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
import seaborn as sns
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
# ==================== [ 第二部分：模型训练 - 多分类逻辑回归 ] ====================

# 1.1 定义模型和超参数搜索空间
# 由于有 100 个类别，使用 'lbfgs' 或 'saga' 作为求解器
# C 是正则化强度的倒数，C 越小，正则化越强
# multi_class='multinomial' 启用多分类模式
log_reg = LogisticRegression(solver='saga', max_iter=1000, random_state=42) 

# 定义超参数网格：尝试 L1 和 L2 正则化，以及不同的正则化强度 C
param_grid = {
    'penalty': ['l1', 'l2'], 
    'C': [0.01, 0.1, 1.0, 10.0] # C 的搜索范围
}
# param_grid = {'C': [0.1], 'penalty': ['l2']} # 快速测试用
# 1.2 使用 GridSearchCV 进行超参数调优 (模型评估和选择方法一)
# 在 X_train_pca 上进行训练，并使用内置的交叉验证进行内部评估
# cv=3 表示 3 折交叉验证
grid_search_lr = GridSearchCV(
    estimator=log_reg, 
    param_grid=param_grid, 
    scoring='accuracy', 
    cv=2, 
    verbose=3, 
    n_jobs=-1
)

# 使用降维后的训练集拟合网格搜索
grid_search_lr.fit(X_train_pca, Y_train) 

# 1.3 提取最佳模型和结果
best_lr = grid_search_lr.best_estimator_
best_params_lr = grid_search_lr.best_params_

print(f"\n最佳逻辑回归参数: {best_params_lr}")

# 1.4 在验证集上进行最终评估
Y_val_pred_lr = best_lr.predict(X_val_pca)
val_accuracy_lr = accuracy_score(Y_val, Y_val_pred_lr)

print(f"逻辑回归在验证集上的准确率: {val_accuracy_lr:.4f}")

# 1.5 模型的鲁棒性评估：交叉验证 (模型评估和选择方法二)
# 使用全量训练集（降维后）进行 K-Fold 评估，以获得更稳健的泛化能力估计
# 这里使用 X_train_full_pca 对应完整训练集
print("\n--- 鲁棒性评估 (5-Fold Cross-Validation) ---")
# 注意：在GridSearch内部已经使用了交叉验证，但这里展示如何独立进行CV。
# 重新将完整训练集进行降维
X_train_full_scaled = scaler.transform(X_train_full)
X_train_full_pca = pca.transform(X_train_full_scaled)

cv_scores = cross_val_score(
    best_lr, 
    X_train_full_pca, 
    Y_train_full, 
    cv=5, 
    scoring='accuracy', 
    n_jobs=-1
)

print(f"5-Fold CV 准确率: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
# 1. 使用逻辑回归模型对测试集进行预测
test_predictions = best_lr.predict(X_test_pca)

# 2. 创建 DataFrame，确保列名完全符合要求
submission = pd.DataFrame({
    'Id': np.arange(len(test_predictions)), # 生成 0 到 9999 的 ID
    'Label': test_predictions               # 填入预测结果
})

# 3. 保存为 csv 文件，index=False 表示不保存 DataFrame 自带的索引行
submission.to_csv('submission_lr.csv', index=False)

print("\n符合格式的提交文件 'submission_lr.csv' 已生成！")


