import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

train_df = pd.read_csv('train.csv', header=None)
# 每个图像表示为一个 512 维向量 [cite: 8]
X_all = train_df.iloc[:, 0:512].values 
y_all = train_df.iloc[:, 512].values 

# --- 2. 类别分布分析 (Understand the distribution of classes) [cite: 20] ---
plt.figure(figsize=(16, 6))
# 共有 100 个预定义的类别 [cite: 5]
sns.countplot(x=y_all, palette="viridis")
plt.title("Distribution of 100 Image Categories", fontsize=15)
plt.xlabel("Class ID", fontsize=12)
plt.ylabel("Sample Count", fontsize=12)
plt.xticks(rotation=90, fontsize=8) 
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# --- 3. 稀疏性分析 (Analyze the sparsity of the data) [cite: 21] ---
# 严格零值占比
zero_ratio = np.sum(X_all == 0) / X_all.size
# 准零值占比（考虑预提取特征中的极小值）
quasi_threshold = 1e-5
quasi_zero_ratio = np.sum(np.abs(X_all) < quasi_threshold) / X_all.size

print(f"📊 数据稀疏性分析报告:")
print(f"   - 原始特征维度: 512 [cite: 8]")
print(f"   - 样本总数: {len(X_all)} [cite: 7]")
print(f"   - 严格稀疏度 (Exact Zeros): {zero_ratio:.4%}")
print(f"   - 准稀疏度 (Values < {quasi_threshold}): {quasi_zero_ratio:.4%}")

# --- 4. 特征数值分布可视化 (Understand the feature space) [cite: 20] ---
plt.figure(figsize=(10, 5))
plt.hist(X_all.flatten(), bins=100, color='skyblue', edgecolor='black', log=True)
plt.title("Global Distribution of Feature Values (Log Scale)", fontsize=14)
plt.xlabel("Feature Value")
plt.ylabel("Frequency (Log)")
plt.show()

# --- 5. 降维影响分析 (Dimensionality Reduction Analysis - PCA) [cite: 23, 24] ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_all)

pca_full = PCA().fit(X_scaled)
cum_variance = np.cumsum(pca_full.explained_variance_ratio_)

# 找到解释 98% 方差所需的组件数 [cite: 25]
n_components_98 = np.where(cum_variance >= 0.98)[0][0] + 1

plt.figure(figsize=(10, 6))
plt.plot(cum_variance, linewidth=2, color='red')
plt.axhline(y=0.98, color='k', linestyle='--', label='98% Variance Threshold')
plt.axvline(x=n_components_98, color='g', linestyle=':', label=f'{n_components_98} Components')
plt.title("PCA Cumulative Explained Variance", fontsize=14)
plt.xlabel("Number of Principal Components")
plt.ylabel("Cumulative Variance Ratio")
plt.legend()
plt.grid(True)
plt.show()

print(f"📉 降维讨论依据:")
print(f"   - 解释 98% 方差仅需 {n_components_98} 个主成分。")
print(f"   - 结论：数据在 512 维空间中存在显著的线性冗余。 [cite: 25]")