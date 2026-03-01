import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import warnings

# 忽略警告
warnings.filterwarnings("ignore") 

# ==========================================
# 1. 功能函数：特征交互增强
# ==========================================
def extract_interaction_features(X):
    """
    通过行级统计量构造特征交互，增强线性模型的捕捉能力
    """
    # 基础统计量交互
    mean_f = np.mean(X, axis=1).reshape(-1, 1)
    std_f = np.std(X, axis=1).reshape(-1, 1)
    max_f = np.max(X, axis=1).reshape(-1, 1)
    min_f = np.min(X, axis=1).reshape(-1, 1)
    # L2 范数（代表向量的长度/能量，是隐形的平方交互）
    l2_f = np.linalg.norm(X, axis=1).reshape(-1, 1)
    
    return np.hstack([X, mean_f, std_f, max_f, min_f, l2_f])

# ==========================================
# 2. 数据加载与初始增强
# ==========================================
print("📂 正在加载数据并注入交互特征...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

num_features = 512
X_raw = train_df.iloc[:, 0:num_features].values 
y_all = train_df.iloc[:, num_features].values 
X_test_raw = test_df.values

# 注入行级交互特征
X_all = extract_interaction_features(X_raw)
X_test_all = extract_interaction_features(X_test_raw)

# ==========================================
# 3. 阶段一：10-Fold 交叉验证 (带主成分交互)
# ==========================================
n_splits = 10
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

all_test_probs = np.zeros((X_test_all.shape[0], 100)) 
fold_scores = []

print(f"\n🚀 启动第一阶段：{n_splits}-Fold 交互增强训练...")

for fold, (train_idx, val_idx) in enumerate(skf.split(X_all, y_all), 1):
    X_train_f, X_val_f = X_all[train_idx], X_all[val_idx]
    y_train_f, y_val_f = y_all[train_idx], y_all[val_idx]
    
    # 标准化
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_train_f)
    X_va_s = scaler.transform(X_val_f)
    X_te_s = scaler.transform(X_test_all)
    
    # PCA 降维
    pca = PCA(n_components=0.985, random_state=42)
    X_tr_p = pca.fit_transform(X_tr_s)
    X_va_p = pca.transform(X_va_s)
    X_te_p = pca.transform(X_te_s)
    
    # --- 特征交互升级：主成分二阶项 ---
    # 针对 PCA 前 3 维构造交叉乘积 (x1*x2, x1*x3, x2*x3)
    poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
    X_tr_poly = poly.fit_transform(X_tr_p[:, :3]) 
    X_va_poly = poly.transform(X_va_p[:, :3])
    X_te_poly = poly.transform(X_te_p[:, :3])
    
    # 拼接原始 PCA 特征与交互项
    X_tr_final = np.hstack([X_tr_p, X_tr_poly])
    X_va_final = np.hstack([X_va_p, X_va_poly])
    X_te_final = np.hstack([X_te_p, X_te_poly])
    
    # 模型训练
    lr = LogisticRegression(solver='saga', C=0.0085, max_iter=1200, n_jobs=-1, random_state=42)
    lr.fit(X_tr_final, y_train_f)
    
    svc = CalibratedClassifierCV(LinearSVC(C=0.012, dual=False, max_iter=2500, random_state=42), cv=3)
    svc.fit(X_tr_final, y_train_f)
    
    # 融合评估
    p_lr_v = lr.predict_proba(X_va_final)
    p_svc_v = svc.predict_proba(X_va_final)
    p_ens_v = (p_lr_v * 0.58 + p_svc_v * 0.42) # 微调比例
    acc = np.mean(np.argmax(p_ens_v, axis=1) == y_val_f)
    fold_scores.append(acc)
    
    # 预测积累
    all_test_probs += (lr.predict_proba(X_te_final) * 0.55 + svc.predict_proba(X_te_final) * 0.45) / n_splits
    print(f"   Fold {fold} 完成, 交互增强准确率: {acc:.4f}")

print(f"\n✅ 阶段一平均 CV 得分: {np.mean(fold_scores):.4f}")

# ==========================================
# 4. 阶段二：高置信度伪标签重训
# ==========================================
max_probs = np.max(all_test_probs, axis=1)
pseudo_labels = np.argmax(all_test_probs, axis=1)
threshold = 0.96 # 提高阈值至 0.96，确保加入的都是极高置信度样本
mask = max_probs > threshold

X_pseudo = X_test_all[mask]
y_pseudo = pseudo_labels[mask]

print(f"\n🔍 筛选出 {len(y_pseudo)} 个极高置信度样本进行终极进化...")

if len(y_pseudo) > 50:
    X_comb = np.vstack([X_all, X_pseudo])
    y_comb = np.concatenate([y_all, y_pseudo])
    
    # 全量重训特征工程
    final_scaler = StandardScaler()
    X_comb_s = final_scaler.fit_transform(X_comb)
    X_te_s_final = final_scaler.transform(X_test_all)
    
    final_pca = PCA(n_components=0.988, random_state=42) # 稍微增加方差保留
    X_comb_p = final_pca.fit_transform(X_comb_s)
    X_te_p_f = final_pca.transform(X_te_s_final)
    
    # PCA 前 3 维二阶交互
    final_poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
    X_comb_poly = final_poly.fit_transform(X_comb_p[:, :3])
    X_te_poly_f = final_poly.transform(X_te_p_f[:, :3])
    
    X_comb_final = np.hstack([X_comb_p, X_comb_poly])
    X_te_final_final = np.hstack([X_te_p_f, X_te_poly_f])
    
    # 终极拟合
    final_lr = LogisticRegression(solver='saga', C=0.008, max_iter=1500, n_jobs=-1)
    final_svc = CalibratedClassifierCV(LinearSVC(C=0.01, dual=False, max_iter=3000), cv=5) # 增加校准折数
    
    final_lr.fit(X_comb_final, y_comb)
    final_svc.fit(X_comb_final, y_comb)
    
    final_res = (final_lr.predict_proba(X_te_final_final) * 0.55 + final_svc.predict_proba(X_te_final_final) * 0.45)
    final_predictions = np.argmax(final_res, axis=1)
    print("✨ 特征交互+伪标签 终极进化完成！")
else:
    final_predictions = np.argmax(all_test_probs, axis=1)

# ==========================================
# 5. 生成提交
# ==========================================
submission = pd.DataFrame({'Id': np.arange(len(final_predictions)), 'Label': final_predictions})
submission.to_csv('submission_interaction_v1.csv', index=False)
print("\n🎉 优化版文件已生成：'submission_interaction_v1.csv'")