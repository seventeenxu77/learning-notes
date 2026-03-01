import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.linear_model import LogisticRegression 
import warnings

# 忽略警告
warnings.filterwarnings("ignore") 

# --- 1. 数据加载 ---
train_df = pd.read_csv('train.csv', header=None)
test_df = pd.read_csv('test.csv', header=None)

num_features = 512
X_all = train_df.iloc[:, 0:num_features].values 
y_all = train_df.iloc[:, num_features].values 
X_test = test_df.values

# --- 2. 设置 K 折参数 ---
# 使用 5 折通常是性能和速度的最佳平衡点
n_splits = 10
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# 用于存储 5 次模型预测的概率分布 (N行 x 100个类别)
all_test_probs = np.zeros((X_test.shape[0], 100)) 

# 用于记录每一折的本地验证分数，帮你监控模型稳不稳
fold_scores = []

# --- 3. 核心 K 折循环 ---
fold = 1
for train_index, val_index in skf.split(X_all, y_all):
    print(f"\n🚀 正在处理第 {fold}/{n_splits} 折...")
    
    # 划分本折的训练集和验证集
    X_train_fold, X_val_fold = X_all[train_index], X_all[val_index]
    y_train_fold, y_val_fold = y_all[train_index], y_all[val_index]
    
    # --- 独立标准化与 PCA (防止数据泄露) ---
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_fold)
    X_val_scaled = scaler.transform(X_val_fold)
    X_test_scaled = scaler.transform(X_test)
    
    # 使用你之前发现的最佳 PCA 保留比例 0.98
    pca = PCA(n_components=0.98, random_state=42)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_val_pca = pca.transform(X_val_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    
    # --- 训练逻辑回归 ---
    # 使用你之前跑出的最强参数 C=0.005, penalty='l2'
    model = LogisticRegression(
        solver='saga', 
        C=0.008, 
        penalty='l2', 
        max_iter=1000,  
        random_state=42, 
        n_jobs=-1
    )
    model.fit(X_train_pca, y_train_fold)
    
    # --- 评估与概率累加 ---
    val_acc = model.score(X_val_pca, y_val_fold)
    fold_scores.append(val_acc)
    print(f"   - 第 {fold} 折验证集准确率: {val_acc:.4f}")
    
    # 关键步骤：获取测试集的概率矩阵（而非直接预测分类）
    all_test_probs += model.predict_proba(X_test_pca)
    
    fold += 1

# --- 4. 结果集成 ---
print("\n" + "="*30)
print(f"💡 平均交叉验证准确率: {np.mean(fold_scores):.4f} (+/- {np.std(fold_scores):.4f})")

# 将 5 次概率取平均，得出最终的“集体意见”
final_probs = all_test_probs / n_splits
# 选取平均概率最大的那个索引作为分类结果
final_predictions = np.argmax(final_probs, axis=1)

# --- 5. 生成提交文件 ---
submission = pd.DataFrame({
    'Id': np.arange(len(final_predictions)),
    'Label': final_predictions
})
file_name = 'submission_kfold  .csv'
submission.to_csv(file_name, index=False)

print(f"\n✅ 终极集成文件 '{file_name}' 已生成！")