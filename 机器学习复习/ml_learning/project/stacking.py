import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score
import warnings

warnings.filterwarnings("ignore")

# --- 1. 数据加载 ---
print("📂 正在加载数据...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)
X_all = train_df.iloc[:, 0:512].values 
y_all = train_df.iloc[:, 512].values 
X_test_raw = test_df.values

# --- 2. 准备 Stacking ---
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# 存储训练集的元特征 (Out-of-Fold Predictions)
oof_probs = np.zeros((X_all.shape[0], 200)) # 2模型 x 100类
# 存储测试集的元特征
test_probs_lr = np.zeros((X_test_raw.shape[0], 100))
test_probs_svc = np.zeros((X_test_raw.shape[0], 100))

print("\n🚀 启动 Stacking 模式：提取元特征 (OOF)...")
print("-" * 50)

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
    
    # 基础模型
    lr = LogisticRegression(solver='saga', C=0.008, max_iter=1000, n_jobs=-1)
    svc = CalibratedClassifierCV(LinearSVC(C=0.01, dual=False), cv=3, method='isotonic')
    
    lr.fit(X_tr_p, y_tr)
    svc.fit(X_tr_p, y_tr)
    
    # 填充元特征 (验证集预测)
    p_lr_v = lr.predict_proba(X_va_p)
    p_svc_v = svc.predict_proba(X_va_p)
    oof_probs[val_index, 0:100] = p_lr_v
    oof_probs[val_index, 100:200] = p_svc_v
    
    # 测试集预测累加
    test_probs_lr += lr.predict_proba(X_te_p) / 10
    test_probs_svc += svc.predict_proba(X_te_p) / 10
    
    # 打印单折基础模型效果
    acc_lr = accuracy_score(y_va, np.argmax(p_lr_v, axis=1))
    print(f"Fold {fold:2d} | LR Acc: {acc_lr:.4f} | 元特征提取完成")

# 拼接测试集元特征
test_meta_features = np.hstack([test_probs_lr, test_probs_svc])

# --- 3. 训练元分类器 ---
print("\n" + "="*50)
print("📝 正在训练元分类器 (Meta-Classifier)...")

# 移除 multi_class 参数，改用更稳健的超参数
meta_model = LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs', n_jobs=-1)
meta_model.fit(oof_probs, y_all)

# --- 4. 信心监控输出 ---
print("-" * 50)
# 拟合度
train_meta_acc = meta_model.score(oof_probs, y_all)
print(f"📊 元分类器训练集拟合准确率: {train_meta_acc:.5f}")

# 模型差异性监控 (相关性越低，Stacking 潜力越大)
corr = np.corrcoef(oof_probs[:, 0:100].flatten(), oof_probs[:, 100:200].flatten())[0,1]
print(f"🔗 LR 与 SVM 预测相关性: {corr:.4f}")
print("="*50)

# --- 5. 最终预测与生成 ---
final_predictions = meta_model.predict(test_meta_features)

output_file = 'submission_stacking_final.csv'
pd.DataFrame({
    'Id': np.arange(len(final_predictions)),
    'Label': final_predictions
}).to_csv(output_file, index=False)

print(f"\n✅ 终极 Stacking 集成文件 '{output_file}' 已生成！")