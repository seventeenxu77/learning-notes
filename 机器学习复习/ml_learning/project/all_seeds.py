import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import warnings
import time

warnings.filterwarnings("ignore")

# --- 1. 核心黄金配置 ---
W_LR, W_SVC = 0.85, 0.15      # 经过验证的最佳比例
PCA_COMPONENTS = 0.98         # 经过验证的黄金降维点
SEEDS = [42, 666, 888, 123, 2025] # 5个不同种子，覆盖不同的初始化空间
N_CLASSES = 100

# --- 2. 加载数据 ---
print("📂 正在加载数据...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

X_train_full = train_df.iloc[:, 0:512].values
y_train_full = train_df.iloc[:, 512].values
X_test_raw = test_df.values

# 预先缩放（全局缩放对全量训练更稳）
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train_full)
X_test_s = scaler.transform(X_test_raw)

# 准备累加器
final_test_probs = np.zeros((len(X_test_raw), N_CLASSES))

print(f"\n🚀 启动 {len(SEEDS)} 种子全量集成方案...")
print("=" * 60)

start_time = time.time()

for i, seed in enumerate(SEEDS, 1):
    fold_start = time.time()
    
    # --- PCA 降维 (每个种子略有不同) ---
    pca = PCA(n_components=PCA_COMPONENTS, random_state=seed)
    X_train_p = pca.fit_transform(X_train_s)
    X_test_p = pca.transform(X_test_s)
    
    # --- 模型 A: LR ---
    lr = LogisticRegression(solver='saga', C=0.008, max_iter=1000, n_jobs=-1, random_state=seed)
    lr.fit(X_train_p, y_train_full)
    p_lr = lr.predict_proba(X_test_p)
    
    # --- 模型 B: SVC ---
    base_svc = LinearSVC(C=0.01, dual=False, random_state=seed, max_iter=2000)
    svc = CalibratedClassifierCV(base_svc, cv=3) # 内置3折校准
    svc.fit(X_train_p, y_train_full)
    p_svc = svc.predict_proba(X_test_p)
    
    # --- 权重融合并累加 ---
    current_probs = (p_lr * W_LR) + (p_svc * W_SVC)
    final_test_probs += current_probs / len(SEEDS)
    
    print(f"✅ Seed {seed:4d} (Iter {i}/{len(SEEDS)}) 完成 | 耗时: {time.time()-fold_start:.1f}s")

# --- 3. 生成提交 ---
final_preds = np.argmax(final_test_probs, axis=1)
output_name = 'submission_seeds_ensemble_no_pseudo.csv'
pd.DataFrame({'Id': np.arange(len(final_preds)), 'Label': final_preds}).to_csv(output_name, index=False)

print("=" * 60)
print(f"✨ 所有种子集成完毕！总耗时: {(time.time()-start_time)/60:.2f} 分钟")
print(f"🏆 最终产出文件：{output_name}")