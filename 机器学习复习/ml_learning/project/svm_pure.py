import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import warnings
import time

# 忽略警告，保持控制台整洁
warnings.filterwarnings("ignore") 

# --- 1. 配置参数 ---
N_SPLITS = 10           # K折交叉验证
PCA_COMPONENTS = 0.98   # PCA保留98%的方差
RANDOM_STATE = 42

# --- 2. 数据加载 ---
print("📂 正在加载数据...")
try:
    train_df = pd.read_csv('train.csv', header=None)
    test_df = pd.read_csv('test.csv', header=None)
except FileNotFoundError:
    print("❌ 错误：找不到 train.csv 或 test.csv 文件，请检查路径。")
    exit()

X_all = train_df.iloc[:, 0:512].values 
y_all = train_df.iloc[:, 512].values 
X_test_raw = test_df.values

# 初始化交叉验证和概率存储矩阵 (N个测试样本 x 100个类别)
skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
all_test_probs = np.zeros((X_test_raw.shape[0], 100)) 

fold_scores = []

print(f"\n⚡ 启动纯 SVM 训练模式 (n_splits={N_SPLITS})")
print("=" * 60)
print(f"{'折数':^10} | {'SVM 验证集准确率':^20} | {'耗时':^10}")
print("-" * 60)

total_start_time = time.time()

# --- 3. 核心 K 折循环 ---
for fold, (train_index, val_index) in enumerate(skf.split(X_all, y_all), 1):
    fold_start = time.time()
    
    # 划分训练/验证集
    X_tr, X_va = X_all[train_index], X_all[val_index]
    y_tr, y_va = y_all[train_index], y_all[val_index]
    
    # --- 特征工程 ---
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_va_s = scaler.transform(X_va)
    X_te_s = scaler.transform(X_test_raw)
    
    pca = PCA(n_components=PCA_COMPONENTS, random_state=RANDOM_STATE)
    X_tr_p = pca.fit_transform(X_tr_s)
    X_va_p = pca.transform(X_va_s)
    X_te_p = pca.transform(X_te_s)
    
    # --- 训练线性 SVM (带概率校准) ---
    # 使用 CalibratedClassifierCV 是为了获取 predict_proba 接口
    base_svc = LinearSVC(C=0.009, dual=False, random_state=RANDOM_STATE, max_iter=2000)
    svc = CalibratedClassifierCV(base_svc, cv=3) 
    svc.fit(X_tr_p, y_tr)
    
    # --- 评估 ---
    acc_svc = svc.score(X_va_p, y_va)
    fold_scores.append(acc_svc)
    
    fold_end = time.time()
    print(f"Fold {fold:02d} | {acc_svc:^20.4f} | {fold_end - fold_start:8.2f}s")
    
    # --- 预测测试集并累加概率 ---
    all_test_probs += svc.predict_proba(X_te_p) / N_SPLITS

# --- 4. 统计总结 ---
avg_acc = np.mean(fold_scores)
std_acc = np.std(fold_scores)
total_duration = (time.time() - total_start_time) / 60

print("-" * 60)
print(f"📊 10-Fold 平均准确率: {avg_acc:.5f} (±{std_acc:.5f})")
print(f"⌛ 任务总耗时: {total_duration:.2f} 分钟")
print("=" * 60)

# --- 5. 生成提交文件 ---
final_predictions = np.argmax(all_test_probs, axis=1)
submission = pd.DataFrame({
    'Id': np.arange(len(final_predictions)),
    'Label': final_predictions
})

output_file = 'submission_pure_svm.csv'
submission.to_csv(output_file, index=False)

print(f"\n✅ 纯 SVM 预测文件 '{output_file}' 已生成，去上传试试吧！")