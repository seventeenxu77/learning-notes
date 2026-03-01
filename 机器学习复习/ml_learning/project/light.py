import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
import lightgbm as lgb  # 确保你的文件名不叫 lightgbm.py
from sklearn.metrics import accuracy_score
import warnings
import time

warnings.filterwarnings("ignore")

# --- 1. 加载数据 ---
print("📂 正在加载数据...")
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)
X_all = train_df.iloc[:, 0:512].values 
y_all = train_df.iloc[:, 512].values 
X_test_raw = test_df.values

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
all_test_ranks = np.zeros((X_test_raw.shape[0], 100))

print("\n🔥 异构集成 (LR + LGBM) | 目标: 纠偏线性盲区")
print("=" * 115)
print(f"{'折数':^5} | {'LR得分':^8} | {'LGBM得分':^8} | {'相关性':^8} | {'分歧率':^7} | {'修正':^4} | {'融合得分':^8} | {'增益':^7}")
print("-" * 115)

start_total = time.time()

for fold, (train_index, val_index) in enumerate(skf.split(X_all, y_all), 1):
    X_tr, X_va = X_all[train_index], X_all[val_index]
    y_tr, y_va = y_all[train_index], y_all[val_index]
    
    # --- 模型 A: LR (线性基石) ---
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_va_s = scaler.transform(X_va)
    X_te_s = scaler.transform(X_test_raw)
    
    pca = PCA(n_components=0.985, random_state=42)
    X_tr_p = pca.fit_transform(X_tr_s)
    X_va_p = pca.transform(X_va_s)
    X_te_p = pca.transform(X_te_s)
    
    lr = LogisticRegression(solver='saga', C=0.008, max_iter=1000, n_jobs=-1, random_state=42)
    lr.fit(X_tr_p, y_tr)
    p_lr_v = lr.predict_proba(X_va_p)
    
    # --- 模型 B: LightGBM (局部非线性专家) ---
    # 增加 boosting 轮数到 150，降低学习率
    dtrain = lgb.Dataset(X_tr, label=y_tr)
    lgb_params = {
        'objective': 'multiclass',
        'num_class': 100,
        'metric': 'multi_logloss',
        'learning_rate': 0.03, # 降低步长，学习更精细
        'num_leaves': 45,      # 增加叶子节点，捕捉更复杂的非线性
        'feature_fraction': 0.8,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'lambda_l1': 0.1,      # 增加 L1 正则，防止过拟合
        'verbosity': -1,
        'seed': 42
    }
    lgb_model = lgb.train(lgb_params, dtrain, num_boost_round=150)
    p_lgb_v = lgb_model.predict(X_va)
    
    # --- 融合统计 ---
    def get_rank(prob): return prob.argsort().argsort()
    
    # 权重 0.7:0.3
    res_v = get_rank(p_lr_v) * 0.7 + get_rank(p_lgb_v) * 0.3
    y_pred_v = np.argmax(res_v, axis=1)
    
    # 指标统计
    pred_lr_v = np.argmax(p_lr_v, axis=1)
    pred_lgb_v = np.argmax(p_lgb_v, axis=1)
    
    acc_lr = accuracy_score(y_va, pred_lr_v)
    acc_lgb = accuracy_score(y_va, pred_lgb_v)
    acc_ens = accuracy_score(y_va, y_pred_v)
    
    corr = np.corrcoef(p_lr_v.flatten(), p_lgb_v.flatten())[0,1]
    disagreement = np.mean(pred_lr_v != pred_lgb_v)
    net_corr = np.sum((pred_lr_v != y_va) & (y_pred_v == y_va)) - \
               np.sum((pred_lr_v == y_va) & (y_pred_v != y_va))
    
    print(f"Fold {fold:2d} | {acc_lr:8.4f} | {acc_lgb:8.4f} | {corr:8.4f} | {disagreement:7.1%} | {net_corr:^4d} | {acc_ens:8.4f} | {acc_ens-acc_lr:+.4f}")
    
    all_test_ranks += (get_rank(lr.predict_proba(X_te_p)) * 0.7 + 
                       get_rank(lgb_model.predict(X_test_raw)) * 0.3)

print("-" * 115)
final_predictions = np.argmax(all_test_ranks, axis=1)
pd.DataFrame({'Id': np.arange(len(final_predictions)), 'Label': final_predictions}).to_csv('submission_lgbm_hybrid.csv', index=False)
print(f"✅ 异构融合完成！耗时: {(time.time()-start_total)/60:.2f} min")