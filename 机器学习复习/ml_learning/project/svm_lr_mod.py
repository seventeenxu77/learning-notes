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
# 在这里快速调整比例 (建议和为1.0)
W_LR = 0.8  
W_SVC = 0.2
N_SPLITS = 10
PCA_COMPONENTS = 0.98  # 之前实验证明 0.985 效果通常更好

# --- 2. 数据加载 ---
print("📂 正在加载数据并准备特征空间...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

X_all = train_df.iloc[:, 0:512].values 
y_all = train_df.iloc[:, 512].values 
X_test_raw = test_df.values

skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=42)
all_test_probs = np.zeros((X_test_raw.shape[0], 100)) 

# 用于存储统计数据
stats = []

print(f"\n🔥 启动异构集成：LR ({W_LR:.2f}) + SVM ({W_SVC:.2f})")
print("=" * 110)
print(f"{'折数':^5} | {'LR得分':^8} | {'SVM得分':^8} | {'融合得分':^8} | {'一致性':^7} | {'修正数*':^7} | {'增益':^8}")
print("-" * 110)

start_time = time.time()

for fold, (train_index, val_index) in enumerate(skf.split(X_all, y_all), 1):
    X_tr, X_va = X_all[train_index], X_all[val_index]
    y_tr, y_va = y_all[train_index], y_all[val_index]
    
    # --- 特征工程 ---
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_va_s = scaler.transform(X_va)
    X_te_s = scaler.transform(X_test_raw)
    
    pca = PCA(n_components=PCA_COMPONENTS, random_state=42)
    X_tr_p = pca.fit_transform(X_tr_s)
    X_va_p = pca.transform(X_va_s)
    X_te_p = pca.transform(X_te_s)
    
    # --- 模型 A: LR ---
    lr = LogisticRegression(solver='saga', C=0.008, penalty='l2', max_iter=1000, n_jobs=-1, random_state=42)
    lr.fit(X_tr_p, y_tr)
    p_lr_va = lr.predict_proba(X_va_p)
    
    # --- 模型 B: Calibrated LinearSVC ---
    base_svc = LinearSVC(C=0.01, dual=False, random_state=42, max_iter=2000)
    svc = CalibratedClassifierCV(base_svc, cv=3) 
    svc.fit(X_tr_p, y_tr)
    p_svc_va = svc.predict_proba(X_va_p)
    
    # --- 权重融合 ---
    # 使用 Soft Voting 加权融合
    p_ens_va = (p_lr_va * W_LR) + (p_svc_va * W_SVC)
    y_pred_va = np.argmax(p_ens_va, axis=1)
    
    # --- 深度统计分析 ---
    pred_lr = np.argmax(p_lr_va, axis=1)
    pred_svc = np.argmax(p_svc_va, axis=1)
    
    acc_lr = np.mean(pred_lr == y_va)
    acc_svc = np.mean(pred_svc == y_va)
    acc_ens = np.mean(y_pred_va == y_va)
    
    # 模型一致性：两个模型预测结果相同的比例
    consistency = np.mean(pred_lr == pred_svc)
    # 修正数：LR判错但融合后判对的样本数 - LR判对但融合后判错的样本数
    corrected = np.sum((pred_lr != y_va) & (y_pred_va == y_va))
    wronged = np.sum((pred_lr == y_va) & (y_pred_va != y_va))
    net_correction = corrected - wronged
    
    print(f"Fold {fold:02d} | {acc_lr:8.4f} | {acc_svc:8.4f} | {acc_ens:8.4f} | {consistency:7.2%} | {net_correction:^7d} | {acc_ens-acc_lr:+.5f}")
    
    stats.append([acc_lr, acc_svc, acc_ens])
    
    # 累加测试集概率
    all_test_probs += ((lr.predict_proba(X_te_p) * W_LR) + (svc.predict_proba(X_te_p) * W_SVC)) / N_SPLITS

# --- 4. 总结报告 ---
stats_arr = np.array(stats)
print("-" * 110)
print(f"📊 平均表现: LR: {np.mean(stats_arr[:,0]):.5f} | SVM: {np.mean(stats_arr[:,1]):.5f} | 最终融合: {np.mean(stats_arr[:,2]):.5f}")
print(f"✨ 融合总增益: {np.mean(stats_arr[:,2]) - np.mean(stats_arr[:,0]):+.5f}")
print(f"⌛ 总耗时: {(time.time() - start_time)/60:.2f} 分钟")

# --- 5. 生成提交 ---
final_predictions = np.argmax(all_test_probs, axis=1)
pd.DataFrame({'Id': np.arange(len(final_predictions)), 'Label': final_predictions}).to_csv('submission_lr_svm_weighted.csv', index=False)
print("\n✅ 提交文件已生成：submission_lr_svm_weighted.csv")