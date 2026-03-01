import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import warnings
import time

# 忽略警告
warnings.filterwarnings("ignore") 

# --- 1. 配置参数 ---
W_LR = 0.85
W_SVC = 0.15
N_SPLITS = 10
PCA_COMPONENTS = 0.98
# 定义多个种子，建议 3-5 个，越多越稳但耗时越长
SEEDS = [42 , 2025 , 888 , 24 , 2005 , 666 , 123 , 1314 , 520 , 77 , 1024] 

# --- 2. 数据加载 ---
print("📂 正在加载数据...")
train_df = pd.read_csv('train.csv', header=None) 
test_df = pd.read_csv('test.csv', header=None)

X_all = train_df.iloc[:, 0:512].values 
y_all = train_df.iloc[:, 512].values 
X_test_raw = test_df.values

# 最终存储所有种子预测概率的容器
final_test_probs = np.zeros((X_test_raw.shape[0], 100)) 

start_time = time.time()

print(f"🔥 启动多周知平均集成 | 种子列表: {SEEDS} | 比例: {W_LR}:{W_SVC}")
print("=" * 110)

# --- 3. 外层循环：随机种子 ---
for seed_idx, seed in enumerate(SEEDS, 1):
    seed_start_time = time.time()
    print(f"\n🌱 正在运行种子序列 [{seed_idx}/{len(SEEDS)}] (Seed: {seed})")
    print("-" * 110)
    print(f"{'折数':^5} | {'LR得分':^8} | {'SVM得分':^8} | {'融合得分':^8} | {'一致性':^7} | {'修正数*':^7}")
    
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
    seed_test_probs = np.zeros((X_test_raw.shape[0], 100))
    seed_stats = []

    # --- 内层循环：K折交叉验证 ---
    for fold, (train_index, val_index) in enumerate(skf.split(X_all, y_all), 1):
        X_tr, X_va = X_all[train_index], X_all[val_index]
        y_tr, y_va = y_all[train_index], y_all[val_index]
        
        # 特征工程 (保持种子一致性)
        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_tr)
        X_va_s = scaler.transform(X_va)
        X_te_s = scaler.transform(X_test_raw)
        
        pca = PCA(n_components=PCA_COMPONENTS, random_state=seed)
        X_tr_p = pca.fit_transform(X_tr_s)
        X_va_p = pca.transform(X_va_s)
        X_te_p = pca.transform(X_te_s)
        
        # 模型 A: LR
        lr = LogisticRegression(solver='saga', C=0.008, penalty='l2', max_iter=1000, n_jobs=-1, random_state=seed)
        lr.fit(X_tr_p, y_tr)
        p_lr_va = lr.predict_proba(X_va_p)
        
        # 模型 B: SVM
        base_svc = LinearSVC(C=0.01, dual=False, random_state=seed, max_iter=2000)
        svc = CalibratedClassifierCV(base_svc, cv=3) 
        svc.fit(X_tr_p, y_tr)
        p_svc_va = svc.predict_proba(X_va_p)
        
        # 融合与统计
        p_ens_va = (p_lr_va * W_LR) + (p_svc_va * W_SVC)
        y_pred_va = np.argmax(p_ens_va, axis=1)
        
        acc_lr = np.mean(np.argmax(p_lr_va, axis=1) == y_va)
        acc_svc = np.mean(np.argmax(p_svc_va, axis=1) == y_va)
        acc_ens = np.mean(y_pred_va == y_va)
        
        consistency = np.mean(np.argmax(p_lr_va, axis=1) == np.argmax(p_svc_va, axis=1))
        corrected = np.sum((np.argmax(p_lr_va, axis=1) != y_va) & (y_pred_va == y_va))
        wronged = np.sum((np.argmax(p_lr_va, axis=1) == y_va) & (y_pred_va != y_va))
        
        print(f"Fold {fold:02d} | {acc_lr:8.4f} | {acc_svc:8.4f} | {acc_ens:8.4f} | {consistency:7.2%} | {corrected-wronged:^7d}")
        
        # 累加当前种子的测试集概率
        seed_test_probs += ((lr.predict_proba(X_te_p) * W_LR) + (svc.predict_proba(X_te_p) * W_SVC)) / N_SPLITS
        seed_stats.append(acc_ens)

    # 将当前种子的结果贡献给全局
    final_test_probs += (seed_test_probs / len(SEEDS))
    
    seed_duration = (time.time() - seed_start_time) / 60
    print(f"✅ 种子 {seed} 完成 | 平均准确率: {np.mean(seed_stats):.5f} | 耗时: {seed_duration:.2f} min")

# --- 4. 总结报告 ---
total_duration = (time.time() - start_time) / 60
print("\n" + "=" * 110)
print(f"🏁 所有种子运行完毕！总耗时: {total_duration:.2f} 分钟")

# --- 5. 生成提交 ---
final_predictions = np.argmax(final_test_probs, axis=1)
output_name = f'submission_seeds_averaged_{len(SEEDS)}x.csv'
pd.DataFrame({'Id': np.arange(len(final_predictions)), 'Label': final_predictions}).to_csv(output_name, index=False)
print(f"✅ 最终提交文件已生成：{output_name}")