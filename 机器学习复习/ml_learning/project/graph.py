import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

# --- 1. 数据加载 ---
# 假设 train.csv 放在当前目录下
train_df = pd.read_csv('train.csv', header=None)
num_features = 512
X_all = train_df.iloc[:, 0:num_features].values 
y_all = train_df.iloc[:, num_features].values 

# --- 2. 筛选样本以获得清晰的可视化效果 ---
# 100个类全画出来颜色会重叠。我们随机抽取 10 个类别展示其分布逻辑。
np.random.seed(42)
unique_classes = np.unique(y_all)
selected_classes = np.random.choice(unique_classes, size=10, replace=False)
mask = np.isin(y_all, selected_classes)

X_subset = X_all[mask]
y_subset = y_all[mask]

# --- 3. 数据预处理 ---
# t-SNE 对尺度非常敏感，必须先标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_subset)

# --- 4. 运行 t-SNE ---
# n_components=2: 降至2维
# perplexity: 关注局部还是全局结构，建议在 30-50
# learning_rate: 建议设为 'auto'
print(f"正在对类别 {selected_classes} 进行 t-SNE 降维计算...")
tsne = TSNE(
    n_components=2, 
    perplexity=40, 
    learning_rate='auto', 
    init='pca',      
    # 删除了 n_iter 参数，因为它在某些新版本中不再允许在初始化时传入
    random_state=42
)
X_tsne = tsne.fit_transform(X_scaled)

# --- 5. 绘制高质量图表 ---
plt.figure(figsize=(12, 8), dpi=100)
sns.set_style("whitegrid") # 使用清爽的背景

# 使用高对比度调色板
palette = sns.color_palette("husl", len(selected_classes))

scatter = sns.scatterplot(
    x=X_tsne[:, 0], 
    y=X_tsne[:, 1],
    hue=y_subset,
    palette=palette,
    legend='full',
    alpha=0.8,
    s=70,           # 点的大小
    edgecolor='w',  # 点的边缘颜色
    linewidth=0.5
)

# --- 6. 图表装饰 (直接用于报告) ---
plt.title('t-SNE Visualization: Evidence of High Linear Separability', fontsize=16, pad=20)
plt.xlabel('t-SNE Dimension 1', fontsize=12)
plt.ylabel('t-SNE Dimension 2', fontsize=12)

# 将图例放在外面防止遮挡点
plt.legend(title='Class Label', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)

# 添加简单的分析标注
plt.text(X_tsne[:, 0].min(), X_tsne[:, 1].min(), 
         "Note: Distinct clusters indicate high feature quality.", 
         fontsize=10, color='gray', style='italic')

plt.tight_layout()
plt.savefig('tsne_analysis.png') # 自动保存为图片
plt.show()

print("✅ 可视化图表 'tsne_analysis.png' 已生成！")