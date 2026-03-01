import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

# --- 1. 加载数据 ---
print("🚀 正在加载数据进行特征空间分析...")
train_df = pd.read_csv('train.csv', header=None)
X_all = train_df.iloc[:, 0:512].values
y_all = train_df.iloc[:, 512].values

# --- 2. 类别分布实验 (Class Distribution) ---
print("📊 正在分析类别分布...")
class_counts = pd.Series(y_all).value_counts().sort_index()

plt.figure(figsize=(20, 6))
sns.barplot(x=class_counts.index, y=class_counts.values, palette="viridis")
plt.axhline(y=len(y_all)/100, color='r', linestyle='--', label='Average count')
plt.title('Distribution of 100 Classes in Training Set', fontsize=15)
plt.xlabel('Class ID (0-99)')
plt.ylabel('Number of Samples')
plt.xticks(ticks=range(0, 100, 5), labels=range(0, 100, 5))
plt.legend()
plt.savefig('class_distribution.png', dpi=300)
plt.show()

# --- 3. 特征相关性分析 (Correlation Matrix) ---
print("🌡️ 正在生成特征相关性热力图 (前50维)...")
# 选取前50个特征进行观察，因为512维太多无法直接显示
X_subset = pd.DataFrame(X_all[:, :50])
corr_matrix = X_subset.corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, cmap='RdBu_r', center=0, annot=False)
plt.title('Correlation Matrix of First 50 Features', fontsize=15)
plt.savefig('correlation_heatmap.png', dpi=300)
plt.show()

# --- 4. 数据稀疏性分析 (Sparsity Analysis) ---
print("🌵 正在分析数据稀疏性...")
# 定义稀疏阈值（接近0的值）
sparsity_threshold = 1e-6
sparsity = np.mean(np.abs(X_all) < sparsity_threshold)
print(f"👉 整体数据稀疏度 (Sparsity): {sparsity:.2%}")

# --- 5. t-SNE 高维分布可视化 ---
print("🌈 正在运行 t-SNE 可视化 (约需1-2分钟)...")
# 为了速度，抽取3000个样本进行可视化
sample_indices = np.random.choice(len(X_all), 3000, replace=False)
X_sample = X_all[sample_indices]
y_sample = y_all[sample_indices]

# 标准化是 t-SNE 的必要步骤
X_sample_scaled = StandardScaler().fit_transform(X_sample)

tsne = TSNE(n_components=2, perplexity=30, random_state=42, init='pca', learning_rate='auto')
X_embedded = tsne.fit_transform(X_sample_scaled)

plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=y_sample, cmap='tab20', s=15, alpha=0.6)
plt.colorbar(scatter, label='Class ID')
plt.title('t-SNE Visualization of Feature Space (3000 Samples)', fontsize=15)
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.savefig('tsne_visualization.png', dpi=300)
plt.show()

print("✅ 实验完成！图片已保存为: class_distribution.png, correlation_heatmap.png, tsne_visualization.png")