import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import SVC
import warnings
import time

warnings.filterwarnings("ignore") 

# --- 1. 数据加载 ---
print("📂 正在加载数据并初始化 512 维特征空间...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)
X_all = train_df.iloc[:, 0:512].values 
y_all = train_df.iloc[:, 512].values 
X_test_raw = test_df.values

# --- 2. 参数设置 ---
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
all_test_ranks = np.zeros((X_test_raw.shape[0], 100)) 
fold_stats = []

# 比例配置
W_LR = 0.65
W_RBF = 0.35

print(f"\n🔥 启动黄金比例异构集成：LR ({W_LR:.2f}) + RBF-SVM ({W_RBF:.2f})")
print(f"目标：利用非线性核的 35% 话语权突破线性天花板")
print("=" * 105)
print(f"{'折数':^5} | {'LR得分':^8} | {'RBF得分':^8} | {'一致性':^7} | {'修正数*':^7} | {'融合得分':^8} | {'净增益':^8}")
print("-" * 105)

start_total = time.time()

for fold, (train_index, val_index) in enumerate(skf.split(X_all, y_all), 1):
    X_tr, X_va = X_all[train_index], X_all[val_index]
    y_tr, y_va = y_all[train_index], y_all[val_index]
    
    # 标准化与 PCA 0.985
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_va_s = scaler.transform(X_va)
    X_te_s = scaler.transform(X_test_raw)
    
    pca = PCA(n_components=0.985, random_state=42)
    X_tr_p = pca.fit_transform(X_tr_s)
    X_va_p = pca.transform(X_va_s)
    X_te_p = pca.transform(X_te_s)
    
    # 模型训练
    lr = LogisticRegression(solver='saga', C=0.008, max_iter=1000, n_jobs=-1, random_state=42)
    lr.fit(X_tr_p, y_tr)
    
    rbf_svc = SVC(kernel='rbf', C=1.5, gamma='scale', probability=True, random_state=42)
    rbf_svc.fit(X_tr_p, y_tr)
    
    def get_rank(prob): return prob.argsort().argsort()
    
    # 概率与排名计算
    p_lr_v = lr.predict_proba(X_va_p)
    p_svc_v = rbf_svc.predict_proba(X_va_p)
    
    rank_lr_v = get_rank(p_lr_v)
    rank_svc_v = get_rank(p_svc_v)
    
    # 融合决策
    res_v = rank_lr_v * W_LR + rank_svc_v * W_RBF
    y_pred_v = np.argmax(res_v, axis=1)
    
    # 统计分析
    pred_lr_v = np.argmax(p_lr_v, axis=1)
    pred_svc_v = np.argmax(p_svc_v, axis=1)
    
    # 计算修正数：即 LR 预测错、但融合后预测对的样本数量
    corrected = np.sum((pred_lr_v != y_va) & (y_pred_v == y_va))
    wronged = np.sum((pred_lr_v == y_va) & (y_pred_v != y_va))
    net_correction = corrected - wronged
    
    agreement = np.mean(pred_lr_v == pred_svc_v)
    acc_lr = np.mean(pred_lr_v == y_va)
    acc_svc = np.mean(pred_svc_v == y_va)
    acc_ens = np.mean(y_pred_v == y_va)
    gain = acc_ens - acc_lr
    
    print(f"Fold {fold:2d} | {acc_lr:8.4f} | {acc_svc:8.4f} | {agreement:7.2%} | {net_correction:^7d} | {acc_ens:8.4f} | {gain:+.4f}")
    
    # 测试集同步累加
    all_test_ranks += (get_rank(lr.predict_proba(X_te_p)) * W_LR + 
                       get_rank(rbf_svc.predict_proba(X_te_p)) * W_RBF)
    fold_stats.append(acc_ens)

print("-" * 105)
print(f"📊 最终平均验证集得分: {np.mean(fold_stats):.5f}")
print(f"⌛ 总计算耗时: {(time.time() - start_total)/60:.2f} 分钟")

# --- 3. 生成提交 ---
final_predictions = np.argmax(all_test_ranks, axis=1)
output_file = 'submission_rbf_final_gold.csv'
pd.DataFrame({'Id': np.arange(len(final_predictions)), 'Label': final_predictions}).to_csv(output_file, index=False)

print(f"\n✅ 终极版文件 '{output_file}' 已生成。")
print("💡 提示：如果修正数为正，说明 RBF-SVM 成功协助 LR 找回了丢失的样本点。")