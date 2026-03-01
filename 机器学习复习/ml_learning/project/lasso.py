import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
import warnings
import time

warnings.filterwarnings("ignore") 

# --- 1. 加载数据 ---
print("📂 正在加载数据并准备双路径线性空间...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)
X_all = train_df.iloc[:, 0:512].values 
y_all = train_df.iloc[:, 512].values 
X_test_raw = test_df.values

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
all_test_ranks = np.zeros((X_test_raw.shape[0], 100)) 

print("\n🚀 启动 SAGA 双正则集成：L2 (全局稳健) + L1 (稀疏去噪)")
print("=" * 85)
print(f"{'折数':^5} | {'L2得分':^8} | {'L1得分':^8} | {'融合得分':^8} | {'净增益':^8}")
print("-" * 85)

start_total = time.time()

for fold, (train_index, val_index) in enumerate(skf.split(X_all, y_all), 1):
    X_tr, X_va = X_all[train_index], X_all[val_index]
    y_tr, y_va = y_all[train_index], y_all[val_index]
    
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_va_s = scaler.transform(X_va)
    X_te_s = scaler.transform(X_test_raw)
    
    pca = PCA(n_components=0.985, random_state=42)
    X_tr_p = pca.fit_transform(X_tr_s)
    X_va_p = pca.transform(X_va_s)
    X_te_p = pca.transform(X_te_s)
    
    # 路径 A: L2 正则 (你的基础分来源)
    lr_l2 = LogisticRegression(solver='saga', penalty='l2', C=0.008, max_iter=1000, n_jobs=-1, random_state=42)
    lr_l2.fit(X_tr_p, y_tr)
    
    # 路径 B: L1 正则 (奇兵：强制压缩噪声维度)
    # C=0.02 稍微放宽一点点，避免 L1 过于激进导致信息丢失
    lr_l1 = LogisticRegression(solver='saga', penalty='l1', C=0.02, max_iter=1000, n_jobs=-1, random_state=42)
    lr_l1.fit(X_tr_p, y_tr)
    
    # 概率获取
    p_l2_v = lr_l2.predict_proba(X_va_p)
    p_l1_v = lr_l1.predict_proba(X_va_p)
    
    def get_rank(prob): return prob.argsort().argsort()
    
    # 融合：L2 (85%) + L1 (15%) 
    # 这是一个非常安全的微调比例，旨在 L2 犹豫时由 L1 提供“精简维度”下的见解
    res_v = get_rank(p_l2_v) * 0.85 + get_rank(p_l1_v) * 0.15
    y_pred_v = np.argmax(res_v, axis=1)
    
    acc_l2 = np.mean(np.argmax(p_l2_v, axis=1) == y_va)
    acc_l1 = np.mean(np.argmax(p_l1_v, axis=1) == y_va)
    acc_ens = np.mean(y_pred_v == y_va)
    
    print(f"Fold {fold:2d} | {acc_l2:8.4f} | {acc_l1:8.4f} | {acc_ens:8.4f} | {acc_ens-acc_l2:+.5f}")
    
    # 测试集同步累加
    all_test_ranks += (get_rank(lr_l2.predict_proba(X_te_p)) * 0.85 + 
                       get_rank(lr_l1.predict_proba(X_te_p)) * 0.15)

print("-" * 85)
final_predictions = np.argmax(all_test_ranks, axis=1)
pd.DataFrame({'Id': np.arange(len(final_predictions)), 'Label': final_predictions}).to_csv('submission_l1l2_saga.csv', index=False)
print(f"✅ 终极双正则文件已生成！总耗时: {(time.time()-start_total)/60:.2f} 分钟")