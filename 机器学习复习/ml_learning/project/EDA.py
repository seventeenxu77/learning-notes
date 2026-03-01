import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 加载数据
# 假设你的训练数据最后一列是标签 [cite: 8]
train_df = pd.read_csv('train.csv', header=None)
y_train = train_df.iloc[:, 512].values 

# 2. 统计每个类别的数量
class_counts = pd.Series(y_train).value_counts().sort_index()

# 3. 绘图
plt.figure(figsize=(20, 6))
sns.barplot(x=class_counts.index, y=class_counts.values, palette="viridis")

# 添加标题和标签
plt.title('Distribution of 100 Classes in Training Set', fontsize=16)
plt.xlabel('Class ID (0-99)', fontsize=12)
plt.ylabel('Number of Samples', fontsize=12)

# 设置横轴刻度，确保 0-99 都能看到
plt.xticks(ticks=range(0, 100, 5), labels=range(0, 100, 5))

# 绘制平均线，辅助观察不平衡程度
plt.axhline(y=len(y_train)/100, color='r', linestyle='--', label='Average count')
plt.legend()

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 4. 打印简单的统计分析
print(f"总样本数: {len(y_train)}")
print(f"最大类别样本数: {class_counts.max()} (类别 {class_counts.idxmax()})")
print(f"最小类别样本数: {class_counts.min()} (类别 {class_counts.idxmin()})")
print(f"样本数标准差: {class_counts.std():.2f}")