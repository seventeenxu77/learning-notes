import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import warnings

warnings.filterwarnings("ignore")

# --- 1. 使用你日志中的最优参数 ---
W_LR = 0.85
W_SVC = 0.15
PCA_COMPONENTS = 0.98
SEED = 42 # 你可以根据日志换成那个“好运气”的种子

# --- 2. 加载数据 ---
print("📂 加载全量数据...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

X_train_full = train_df.iloc[:, 0:512].values
y_train_full = train_df.iloc[:, 512].values
X_test = test_df.values

# --- 3. 全量特征工程 ---
# 注意：Scaler和PCA必须在全量训练集上拟合
print("🧹 执行全量特征提取...")
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train_full)
X_test_s = scaler.transform(X_test)

pca = PCA(n_components=PCA_COMPONENTS, random_state=SEED)
X_train_p = pca.fit_transform(X_train_s)
X_test_p = pca.transform(X_test_s)

# --- 4. 全量模型重训练 ---
print(f"🔥 启动全量重训练模式 (无验证集消耗)...")

# 模型 A: LR (使用你调优后的 C=0.008)
lr = LogisticRegression(solver='saga', C=0.008, penalty='l2', max_iter=1000, n_jobs=-1, random_state=SEED)
lr.fit(X_train_p, y_train_full)

# 模型 B: SVC (使用你调优后的 C=0.01)
base_svc = LinearSVC(C=0.01, dual=False, random_state=SEED, max_iter=2000)
# 注意：即使是全量训练，CalibratedClassifierCV 内部仍需要 cv 来进行概率校准
svc = CalibratedClassifierCV(base_svc, cv=3) 
svc.fit(X_train_p, y_train_full)

# --- 5. 最终融合预测 ---
print("🧪 生成最终加权预测...")
test_probs_lr = lr.predict_proba(X_test_p)
test_probs_svc = svc.predict_proba(X_test_p)

final_probs = (test_probs_lr * W_LR) + (test_probs_svc * W_SVC)
final_preds = np.argmax(final_probs, axis=1)

# --- 6. 导出结果 ---
output_name = 'submission_full_data_best.csv'
pd.DataFrame({'Id': np.arange(len(final_preds)), 'Label': final_preds}).to_csv(output_name, index=False)
print(f"\n✅ 终极全量文件已生成：{output_name}")