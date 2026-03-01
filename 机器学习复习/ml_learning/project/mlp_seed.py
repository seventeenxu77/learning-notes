import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import warnings

# 忽略所有警告
warnings.filterwarnings("ignore")

# --- 1. 数据加载与基础处理 ---
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

num_features = 512
X_all = train_df.iloc[:, 0:num_features].values 
y_all = train_df.iloc[:, num_features].values 
X_test_raw = test_df.values

# 划分验证集 (8:2)
X_train, X_val, y_train, y_val = train_test_split(
    X_all, y_all, test_size=0.2, random_state=42, stratify=y_all
)

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test_raw)

# --- 2. 核心设置 ---
noise_factor = 0.02          # 黄金噪声强度
seeds = [42, 123, 2024]      # 三个不同的随机种子，用于模型集成
all_test_probs = []          # 存储测试集预测概率
all_val_scores = []          # 存储验证集得分

# --- 3. 多种子模型训练循环 ---
for i, seed in enumerate(seeds):
    print(f"\n🔥 正在启动第 {i+1}/3 轮训练 (随机种子: {seed})")
    
    # 为每一轮训练注入独立随机噪声，增加数据的多样性
    np.random.seed(seed)
    X_train_noisy = X_train_scaled + noise_factor * np.random.normal(0, 1, X_train_scaled.shape)
    
    # 配置强化版 MLP
    mlp = MLPClassifier(
        hidden_layer_sizes=(1024, 512), # 拓宽加深架构
        activation='relu',
        solver='adam',
        alpha=1.0,                    # 强正则化，对抗 512 维噪声
        batch_size=128,               # 较小 Batch Size 增强泛化能力
        learning_rate_init=0.0002,     # 极低学习率，进行“精耕细作”
        max_iter=2000,
        early_stopping=True,
        n_iter_no_change=50,          # 提高容忍度，让模型磨合更久
        tol=1e-5,
        random_state=seed,
        verbose=True                  # 打印 Loss，监控收敛
    )
    
    # 训练模型
    mlp.fit(X_train_noisy, y_train)
    
    # 记录当前模型的表现
    val_acc = mlp.score(X_val_scaled, y_val)
    all_val_scores.append(val_acc)
    
    # 收集测试集预测概率 (Soft Voting)
    all_test_probs.append(mlp.predict_proba(X_test_scaled))
    
    print(f"✅ 第 {i+1} 轮验证集准确率: {val_acc:.4f}")

# --- 4. 集成结果处理 ---
# 对三个模型的概率取平均值
final_test_probs = np.mean(all_test_probs, axis=0)
final_predictions = np.argmax(final_test_probs, axis=1)

print("\n" + "="*40)
print(f"💡 种子集成平均验证集得分: {np.mean(all_val_scores):.4f}")
print(f"💡 各种子最高得分: {np.max(all_val_scores):.4f}")
print("="*40)

# --- 5. 生成最终提交文件 ---
submission = pd.DataFrame({
    'Id': np.arange(len(final_predictions)),
    'Label': final_predictions
})
output_name = 'submission_mlp_deep_ensemble.csv'
submission.to_csv(output_name, index=False)
print(f"\n🚀 终极集成预测完成！文件 '{output_name}' 已生成。")