from sklearn.svm import LinearSVC
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
print("\n--- 2. 线性支持向量机 (Linear SVM) ---")

# 2.1 初始化模型
# dual=False 是为了加速样本量大于特征数的情况
# multi_class='ovr' (One-vs-Rest) 处理 100 分类
svc = LinearSVC(dual=False, max_iter=2000, random_state=42)

# 2.2 定义超参数网格
# C 是 SVM 的惩罚参数：C 越大，对错误分类的容忍度越低（易过拟合）；C 越小，间隔越大（泛化性好）
param_grid_svc = {
    'C': [0.001, 0.01, 0.1, 1, 10]
}

# 2.3 网格搜索与交叉验证
grid_search_svc = GridSearchCV(
    estimator=svc, 
    param_grid=param_grid_svc, 
    scoring='accuracy', 
    cv=2,          # 保持与逻辑回归一致的折数方便对比
    n_jobs=-1, 
    verbose=3
)

print("开始 SVM 网格搜索训练...")
grid_search_svc.fit(X_train_pca, Y_train)

# 2.4 提取最佳模型
best_svc = grid_search_svc.best_estimator_
print(f"\nSVM 最佳参数: {grid_search_svc.best_params_}")

# 2.5 验证集评估
val_accuracy_svc = best_svc.score(X_val_pca, Y_val)
print(f"SVM 在验证集上的准确率: {val_accuracy_svc:.4f}")

# 2.6 生成针对 SVM 的 Kaggle 提交文件
test_predictions_svc = best_svc.predict(X_test_pca)
submission_svc = pd.DataFrame({
    'Id': np.arange(len(test_predictions_svc)),
    'Label': test_predictions_svc
})
submission_svc.to_csv('submission_svc.csv', index=False)
print("提交文件 'submission_svc.csv' 已生成！")