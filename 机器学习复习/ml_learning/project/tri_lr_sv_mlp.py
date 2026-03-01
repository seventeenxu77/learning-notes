import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import warnings

warnings.filterwarnings("ignore")

# --- 1. 数据准备 ---
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)
X_all = train_df.iloc[:, 0:512].values 
y_all = train_df.iloc[:, 512].values 
X_test_raw = test_df.values

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_all)
X_test_scaled = scaler.transform(X_test_raw)

# PCA 降维 (用于 LR 和 SVM)
pca = PCA(n_components=0.98, random_state=42)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

# 存储测试集概率矩阵 (100个类别的预测概率)
prob_lr = np.zeros((len(X_test_raw), 100))
prob_svm = np.zeros((len(X_test_raw), 100))
prob_mlp = np.zeros((len(X_test_raw), 100))

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# --- 2. 训练 LR 和 SVM (10折交叉验证) ---
print("📦 开始训练 LR 和 SVM (10-Fold)...")
for i, (train_idx, val_idx) in enumerate(skf.split(X_train_pca, y_all)):
    X_tr, X_va = X_train_pca[train_idx], X_train_pca[val_idx]
    y_tr, y_va = y_all[train_idx], y_all[val_idx]

    # LR 模型
    lr = LogisticRegression(C=0.01, penalty='l2', solver='lbfgs', max_iter=1000)
    lr.fit(X_tr, y_tr)
    prob_lr += lr.predict_proba(X_test_pca)  / 10.0

    # SVM 模型 (注意：必须设置 probability=True 才能融合)
    # 使用 SVC 因为 LinearSVC 不支持概率输出
    svm = SVC(C=0.1, kernel='linear', probability=True, random_state=42)
    svm.fit(X_tr, y_tr)
    prob_svm += svm.predict_proba(X_test_pca) / 10.0
    print(f"  - 第 {i+1}/10 折完成")

# --- 3. 训练 MLP (3种子深层集成) ---
print("\n🧠 开始训练 MLP (3-Seed Ensemble)...")
seeds = [42, 123, 2024]
noise_factor = 0.02

for i, seed in enumerate(seeds):
    np.random.seed(seed)
    # 给 MLP 输入带噪声的原始 512 维特征
    X_train_noisy = X_train_scaled + noise_factor * np.random.normal(0, 1, X_train_scaled.shape)
    
    mlp = MLPClassifier(
        hidden_layer_sizes=(1024, 512), 
        alpha=1.0, 
        batch_size=128, 
        learning_rate_init=0.0002,
        max_iter=500, 
        early_stopping=True,
        n_iter_no_change=50,
        random_state=seed,
        verbose=False
    )
    mlp.fit(X_train_noisy, y_all)
    prob_mlp += mlp.predict_proba(X_test_scaled) / len(seeds)
    print(f"  - 第 {i+1}/3 个种子完成")

# --- 4. 终极加权融合 (Soft Voting) ---
# 权重分配：给予最稳健的 LR 和 SVM 更高权重，MLP 作为非线性补位
w_lr = 0.45
w_svm = 0.40
w_mlp = 0.15



final_probs = (w_lr * prob_lr) + (w_svm * prob_svm) + (w_mlp * prob_mlp)
final_predictions = np.argmax(final_probs, axis=1)

# --- 5. 生成提交文件 ---
submission = pd.DataFrame({
    'Id': np.arange(len(final_predictions)),
    'Label': final_predictions
})
submission.to_csv('submission_trinity_final.csv', index=False)
print("\n✅ 终极集成预测完成！文件 'submission_trinity_final.csv' 已生成。")