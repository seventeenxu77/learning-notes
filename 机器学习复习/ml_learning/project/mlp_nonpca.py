import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import warnings

# 忽略警告
warnings.filterwarnings("ignore")

# --- 1. 数据加载 ---
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

num_features = 512
X_all = train_df.iloc[:, 0:num_features].values 
y_all = train_df.iloc[:, num_features].values 
X_test_raw = test_df.values

# --- 2. 划分验证集 (8:2) ---
X_train, X_val, y_train, y_val = train_test_split(
    X_all, y_all, test_size=0.2, random_state=42, stratify=y_all
)

# --- 3. 标准化 (必须在注入噪声前完成) ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test_raw)

# --- 4. 注入高斯噪声 (数据增强) ---
# noise_factor 决定了噪声的强度。0.05 是一个稳健的起点。
# 仅对训练集加噪，验证集和测试集保持“干净”。
noise_factor = 0.02
X_train_noisy = X_train_scaled + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=X_train_scaled.shape)

print(f"输入特征维度: {X_train_noisy.shape[1]} (未降维)")
print(f"注入噪声强度: {noise_factor}")

# --- 5. 构建 MLP 模型 ---
# hidden_layer_sizes: 既然输入是 512 维，隐藏层需要足够宽来容纳信息。
# alpha: 较大的 L2 正则化系数 (如 0.1 或 0.5) 配合噪声共同防止过拟合。
# early_stopping: 必须开启，防止模型在噪声数据上训练过头。
mlp = MLPClassifier(
    hidden_layer_sizes=(512, 256), 
    activation='relu', 
    solver='adam', 
    alpha=0.5,                # 调高正则化，从 0.1 -> 0.5
    learning_rate_init=0.0005, # 调低学习率，从 0.001 -> 0.0005，更细腻地寻找最优解
    max_iter=1000,             # 给它更多迭代机会
    early_stopping=True, 
    n_iter_no_change=20,       # 容忍度调高，不要太早停止
    random_state=42,
    verbose=True
)

# --- 6. 训练与评估 ---
print("\n开始训练带噪声的 MLP 模型...")
mlp.fit(X_train_noisy, y_train)

# 验证集评估 (注意：评估使用的是没有噪声的干净数据 X_val_scaled)
val_accuracy = mlp.score(X_val_scaled, y_val)
train_accuracy = mlp.score(X_train_noisy, y_train)

print("\n" + "="*30)
print(f"💡 训练集准确率 (带噪): {train_accuracy:.4f}")
print(f"💡 验证集准确率 (干净): {val_accuracy:.4f}")
print("="*30)

# --- 7. 生成提交文件 ---
test_predictions = mlp.predict(X_test_scaled)
submission = pd.DataFrame({
    'Id': np.arange(len(test_predictions)),
    'Label': test_predictions
})
submission.to_csv('submission_mlp_noise_raw.csv', index=False)
print("\n✅ 文件 'submission_mlp_noise_raw.csv' 已生成！")