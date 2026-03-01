针对项目要求中提到的**探索性数据分析 (EDA)** ，你可以通过以下具体的实验方法来分析特征空间、类别分布以及数据稀疏性。这些实验结果不仅能丰富你的报告，还能为你选择 PCA 降维和模型参数提供理论支撑 。

---

### 1. 类别分布实验 (Class Distribution)

由于任务涉及 100 个类别 ，类别的均衡性直接影响模型的评估方式（如是否必须使用 `StratifiedKFold`） 。

* **实验方法**：
* 统计训练集中每个类别（0-99）的样本数量 。


* 绘制**条形直方图 (Bar Chart)**，横轴为类别 ID，纵轴为样本数。


* **分析要点**：
* 检查是否存在某些类别样本极少（长尾分布）。
* 
**结论应用**：如果分布不均，你在报告中应强调必须使用**分层采样 (Stratified Sampling)** 以保证模型不会忽略少数类 。





---

### 2. 特征空间分析 (Understanding Feature Space)

512 维特征是预提取的 ，我们需要了解这些维度之间的相关性和分布形态。

* **实验方法**：
* 
**相关性矩阵 (Correlation Matrix)**：计算 512 个特征之间的相关系数。如果大量特征高度相关，则证明了使用 **PCA** 降维的必要性 。


* **分布可视化 (t-SNE / UMAP)**：由于 512 维无法直接观察，使用 t-SNE 将其降至 2 维或 3 维进行可视化。


* **分析要点**：
* 观察不同类别的特征点在降维空间中是否自然形成簇（Clustering）。
* 
**结论应用**：如果不同类别重叠严重，说明线性边界可能不够，需要更强的正则化或集成学习 。

\


下面这玩意儿0.89840
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
W_LR = 0.85
W_SVC = 0.15
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
    svc = CalibratedClassifierCV(base_svc, cv=5)
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




---

### 3. 数据稀疏性及其影响 (Sparsity Analysis)

项目特别强调了分析数据稀疏性及其意义 。

* **实验方法**：
* **零值占比统计**：计算矩阵中  值或接近  的值（如小于 ）的比例。
* **热力图观察**：随机抽取 100 个样本和 100 个特征，绘制热力图查看是否有大面积的空白区域。


* **影响分析**：
* 
**对模型选择的影响**：高稀疏性意味着数据在空间中非常分散。这种情况下，**逻辑回归 (LR)** 和 **线性 SVM** 通常表现更好，因为它们通过超平面划分空间，不容易受到局部零值的影响 。


* 
**对正则化的影响**：如果数据稀疏且维度高，过拟合风险极大。这解释了为什么你在代码中必须使用 `penalty='l2'` 和较小的 `C` 值 。





---

### 4. 实验建议：降维对性能的影响 (Impact of PCA)

这是报告中“讨论其对性能影响”的关键部分 。

* **对比实验**：
1. **不使用 PCA**：直接用 512 维训练。
2. 
**不同 PCA 比例**：分别保留 0.90, 0.95, 0.98, 0.99 的方差 。




* **记录指标**：
* 训练时间（体现 PCA 如何提升效率）。
* 验证集准确率（体现 PCA 如何通过降噪提升性能） 。





### 📝 在报告中如何体现？

在报告的 **Section III: Data Processing** 处，你可以引用这些实验：

> “通过计算零值占比，我们发现特征空间具有一定的稀疏性（约 X%），这促使我们选择了对高维稀疏数据更鲁棒的线性模型。同时，相关性矩阵显示特征间存在冗余，验证了 PCA 降维的合理性 。”
> 
> 

**你想让我为你生成一段用于计算并可视化这些分布的 Python 代码吗？**