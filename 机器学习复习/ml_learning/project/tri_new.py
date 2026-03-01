import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.neural_network import MLPClassifier
import warnings

# 忽略警告
warnings.filterwarnings("ignore") 

# ==========================================
# 1. 数据加载
# ==========================================
print("📂 正在加载数据...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

num_features = 512
X_all = train_df.iloc[:, 0:num_features].values 
y_all = train_df.iloc[:, num_features].values 
X_test_raw = test_df.values

# ==========================================
# 2. 设置集成参数
# ==========================================
n_splits = 10
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# 用于存储累加的测试集排名分
all_test_ranks = np.zeros((X_test_raw.shape[0], 100)) 

fold_scores_ens = []

print(f"\n🚀 启动三路异构集成：LR(50%) + SVM(30%) + MLP(20%)")
print("-" * 75)
print(f"{'折数':^5} | {'LR得分':^8} | {'SVM得分':^8} | {'MLP得分':^8} | {'融合得分':^10} | {'提升度':^8}")
print("-" * 75)

# ==========================================
# 3. 核心 K 折循环
# ==========================================
for fold, (train_index, val_index) in enumerate(skf.split(X_all, y_all), 1):
    X_train_fold, X_val_fold = X_all[train_index], X_all[val_index]
    y_train_fold, y_val_fold = y_all[train_index], y_all[val_index]
    
    # 统一标准化
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train_fold)
    X_val_s = scaler.transform(X_val_fold)
    X_test_s = scaler.transform(X_test_raw)
    
    # 使用 0.99 PCA 保留足够信息给 MLP 学习
    pca = PCA(n_components=0.99, random_state=42)
    X_tr_p = pca.fit_transform(X_train_s)
    X_va_p = pca.transform(X_val_s)
    X_te_p = pca.transform(X_test_s)
    
    # --- 模型 A: 稳健的 LR ---
    lr = LogisticRegression(solver='saga', C=0.008, max_iter=1000, n_jobs=-1, random_state=42)
    lr.fit(X_tr_p, y_train_fold)
    
    # --- 模型 B: 线性 SVM ---
    base_svc = LinearSVC(C=0.01, dual=False, max_iter=2000, random_state=42)
    svc = CalibratedClassifierCV(base_svc, cv=3) 
    svc.fit(X_tr_p, y_train_fold)
    
    # --- 模型 C: 非线性 MLP (轻量级配置避免过拟合) ---
    mlp = MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=500, alpha=0.05, 
                        solver='adam', random_state=42, early_stopping=True)
    mlp.fit(X_tr_p, y_train_fold)
    
    # 获取验证集和测试集概率
    p_lr_v = lr.predict_proba(X_va_p)
    p_svc_v = svc.predict_proba(X_va_p)
    p_mlp_v = mlp.predict_proba(X_va_p)
    
    p_lr_te = lr.predict_proba(X_te_p)
    p_svc_te = svc.predict_proba(X_te_p)
    p_mlp_te = mlp.predict_proba(X_te_p)

    # --- 秩平均融合 (Rank Averaging) ---
    def get_rank(prob):
        return prob.argsort().argsort()

    # 验证集融合权重分配: LR 0.5, SVM 0.3, MLP 0.2
    res_v = (get_rank(p_lr_v) * 0.5 + get_rank(p_svc_v) * 0.3 + get_rank(p_mlp_v) * 0.2)
    y_pred_v = np.argmax(res_v, axis=1)
    
    # 计算得分
    acc_lr = np.mean(np.argmax(p_lr_v, axis=1) == y_val_fold)
    acc_svc = np.mean(np.argmax(p_svc_v, axis=1) == y_val_fold)
    acc_mlp = np.mean(np.argmax(p_mlp_v, axis=1) == y_val_fold)
    acc_ens = np.mean(y_pred_v == y_val_fold)
    improvement = acc_ens - max(acc_lr, acc_svc)
    
    fold_scores_ens.append(acc_ens)
    
    print(f"Fold {fold:2d} | {acc_lr:.4f} | {acc_svc:.4f} | {acc_mlp:.4f} | {acc_ens:10.4f} | {improvement:+.4f}")
    
    # --- 测试集排名分累加 ---
    all_test_ranks += (get_rank(p_lr_te) * 0.8 + get_rank(p_svc_te) * 0.1 + get_rank(p_mlp_te) * 0.1)

# ==========================================
# 4. 统计分析
# ==========================================
print("-" * 75)
print(f"💡 10-Fold 最终平均融合得分: {np.mean(fold_scores_ens):.4f} ✨")
print("-" * 75)

# ==========================================
# 5. 生成提交文件
# ==========================================
final_predictions = np.argmax(all_test_ranks, axis=1)
submission = pd.DataFrame({'Id': np.arange(len(final_predictions)), 'Label': final_predictions})
output_file = 'submission_triple_ensemble.csv'
submission.to_csv(output_file, index=False)
print(f"\n🎉 三路集成文件 '{output_file}' 已生成！")