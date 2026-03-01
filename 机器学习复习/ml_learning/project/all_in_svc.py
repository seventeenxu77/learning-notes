import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
import warnings

# 忽略警告
warnings.filterwarnings("ignore") 

print("--- 正在启动：全量数据重新拟合流程 ---")

# 1. 加载数据
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

num_features = 512
X_train_all = train_df.iloc[:, 0:num_features].values 
Y_train_all = train_df.iloc[:, num_features].values 
X_test = test_df.values

# 2. 全量标准化
# 此时我们不再划分 train/val，直接对全部 100% 训练数据进行 fit
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_all)
X_test_scaled = scaler.transform(X_test)

# 3. 全量 PCA 降维
# 保留 98% 方差，让模型接触到最完整的信息结构
pca = PCA(n_components=0.98, random_state=42)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

print(f"全量训练模式下，PCA 保留主成分数量: {pca.n_components_}")

# 4. 定义最终模型
# 使用你之前网格搜索出的最优参数：C=0.005, penalty='l2'
# 如果你之前的最佳参数是 0.01，请手动修改下面 C 的值
final_model = LogisticRegression(
    solver='saga', 
    max_iter=1000, 
    C=0.005,           # 这里填入你之前跑出的最佳 C 值
    penalty='l2',      # 这里填入你之前跑出的最佳惩罚项
    random_state=42,
    n_jobs=-1          # 开启全核计算
)

# 5. 在 100% 数据上进行拟合
print("正在使用 100% 训练数据拟合最终模型...")
final_model.fit(X_train_pca, Y_train_all)

# 6. 生成预测结果
print("正在预测测试集...")
test_predictions = final_model.predict(X_test_pca)

# 7. 保存提交文件
submission = pd.DataFrame({
    'Id': np.arange(len(test_predictions)),
    'Label': test_predictions
})

file_name = 'submission_final_full_fit.csv'
submission.to_csv(file_name, index=False)

print(f"\n✅ 成功！全量拟合文件 '{file_name}' 已生成。")
print("你可以将此文件上传 Kaggle，观察是否突破 0.90！")