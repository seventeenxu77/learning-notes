
### 机器学习第一次作业
---

Equivalence between LR and NB ：Please prove that NB and Logistic Regression are mathematically equivalent under certain conditions

---
当特征 $X$ 的条件概率分布 $P(X|Y)$ 属于指数族分布，且满足朴素贝叶斯的特征条件独立性假设时，朴素贝叶斯导出的后验概率 $P(Y|X)$ 与逻辑回归的函数形式等价。


#### 1. 逻辑回归 (LR) 的函数形式（假设）

LR 直接假设事件发生的对数几率是特征 $X$ 的线性函数：
不考虑X的先验分布，根据得到数据进行参数估计

$$P(Y=1|X) = \frac{1}{1 + e^{-\mathbf{w}^T \mathbf{X}'}}$$

$$\log \left( \frac{P(Y=1|X)}{P(Y=0|X)} \right)_{\text{LR}} = w_0 + \sum_{j=1}^{n} w_j X_j = \mathbf{w}^T \mathbf{X}'$$
得到了以上的线性形式

---
#### 2. 朴素贝叶斯对数几率的通用形式

朴素贝叶斯的决策基于对数几率（Log-Odds）：

$$\log \left( \frac{P(Y=1|X)}{P(Y=0|X)} \right) = \log \left( \frac{P(Y=1)}{P(Y=0)} \right) + \sum_{j=1}^{n} \log \left( \frac{P(X_j|Y=1)}{P(X_j|Y=0)} \right)$$

---

#### 分布形式的推导

##### a. 伯努利分布 (Bernoulli Naive Bayes)

适用于二元特征 $X_j \in \{0, 1\}$，设 $P(X_j|Y=k) = p_{jk}^{X_j}(1-p_{jk})^{1-X_j}$。

$$\log \left( \frac{P(X_j|Y=1)}{P(X_j|Y=0)} \right) = X_j \log \left( \frac{p_{j1}(1-p_{j0})}{p_{j0}(1-p_{j1})} \right) + \log \left( \frac{1-p_{j1}}{1-p_{j0}} \right)$$

$$\log \left( \frac{P(X_j|Y=1)}{P(X_j|Y=0)} \right) = w_j X_j + b_j$$

导出的对数几率是关于 $X$ 的线性函数 $\mathbf{w}^T \mathbf{X}'$，与 LR 形式等价。


---

##### B. 高斯分布 (Gaussian Naive Bayes)

适用于连续特征 $X_j \in \mathbb{R}$，设 $P(X_j|Y=k) \sim \mathcal{N}(\mu_{jk}, \sigma_{jk}^2)$。

$$\log \left( \frac{P(X_j|Y=1)}{P(X_j|Y=0)} \right)= \log \left( \frac{\sigma_{j0}}{\sigma_{j1}} \right) + \frac{1}{2} \left( \frac{(X_j - \mu_{j0})^2}{\sigma_{j0}^2} - \frac{(X_j - \mu_{j1})^2}{\sigma_{j1}^2} \right)$$
当方差相等时，即 $\sigma_{j1}^2 = \sigma_{j0}^2 = \sigma_j^2$，二次项 $X_j^2$ 才能被抵消。

在 $\sigma_{j1}^2 = \sigma_{j0}^2$ 的条件下：

$$\log \left( \frac{P(X_j|Y=1)}{P(X_j|Y=0)} \right)= X_j \left( \frac{\mu_{j1} - \mu_{j0}}{\sigma_j^2} \right) + \left( \frac{\mu_{j0}^2 - \mu_{j1}^2}{2\sigma_j^2} \right)$$

$$\log \left( \frac{P(X_j|Y=1)}{P(X_j|Y=0)} \right)= w_j X_j + b_j$$

在等方差的高斯假设下，NB 的对数几率是关于 $X$ 的线性函数 $\mathbf{w}^T \mathbf{X}'$，与 LR 形式等价。

---

在上述等价条件下，NB 推导出的对数几率是特征的线性组合：

$$\log \left( \frac{P(Y=1|X)}{P(Y=0|X)} \right) = \mathbf{w}^T \mathbf{X}'$$

这与逻辑回归直接假设的形式（Logit 函数）完全一致：

$$P(Y=1|X) = \frac{1}{1 + e^{-\mathbf{w}^T \mathbf{X}'}}$$

在一些满足指数族的条件独立性假设的特殊情况下，在决策边界上，两者是数学等价的。

---
---

  Select at least two data sets from the link (Data a) below and then investigate classification performances of LR, NB, LDA, Support Vector Machine (SVM), and neural networks (e.g., MLP) on the selected data sets.
  You may try different experimental settings, e.g., by varying the sample size of the training set, trying
data sets with different dimensions, and other configurations that may affect performance in your mind. You may also try different kernels for SVM.






---


下面比较五种经典分类模型（LR, NB, LDa, SVM, MLP）在不同数据集上的性能，并通过调整样本大小、特征维度和模型配置，下面是实验所得到的信息汇总表，代码在附录部分。

#### 1. 实验汇总表格

所有模型和配置下的性能指标（准确率按降序排列）
分别使用了三种数据集：a1a,a9a,w8a
**a1a**: training size | 1605 | feature |  123
**a9a**: training size | 32561 | feature |  123
**w8a**: training size | 49749 | feature |  300
| Experiment | Model | accuracy | F1-Score | Train Time (s) |
| :--- | :--- | :--- | :--- | :--- |
| w8a (High Dim/Large) (Baseline) | MLP | 0.9883 | 0.7868 | 3.97 |
| w8a (High Dim/Large) (Baseline) | SVM-Linear | 0.9863 | 0.7287 | 91.63 |
| w8a (High Dim/Large) (Baseline) | LR | 0.9862 | 0.7332 | 6.48 |
| w8a (High Dim/Large) (Baseline) | LDA | 0.9839 | 0.6938 | 0.93 |
| w8a (High Dim/Large) (Baseline) | NB | 0.9635 | 0.5492 | 0.14 |
| a9a (Low Dim/Large) (Baseline) | LR | 0.8505 | 0.6574 | 0.99 |
| a9a (Low Dim/Large) (Baseline) | SVM-Linear | 0.8485 | 0.6501 | 67.86 |
| a9a (Low Dim/Large) (Kernel Comparison) | SVM-Linear | 0.8485 | 0.6501 | 90.62 |
| a9a (Low Dim/Large) (Baseline) | LDA | 0.8475 | 0.6507 | 0.23 |
| a9a (Low Dim/Large) (Baseline) | MLP | 0.8461 | 0.6407 | 2.09 |
| a9a (Low Dim/Large) (Kernel Comparison) | SVM-RBF | 0.8457 | 0.6338 | 32.64 |
| a9a (Low Dim/Large) (Kernel Comparison) | SVM-Poly | 0.8410 | 0.6057 | 42.09 |
| a1a (Sample Ratio=0.8) | SVM-Linear | 0.8349 | 0.6490 | 0.12 |
| a1a (Sample Ratio=0.5) | LR | 0.8318 | 0.6250 | 0.01 |
| a1a (Low Dim/Small) (Baseline) | SVM-Linear | 0.8278 | 0.6210 | 0.08 |
| a1a (Low Dim/Small) (Baseline) | LR | 0.8237 | 0.6009 | 0.02 |
| a1a (Sample Ratio=0.8) | LR | 0.8224 | 0.6069 | 0.02 |
| a1a (Sample Ratio=0.5) | SVM-Linear | 0.8162 | 0.5931 | 0.03 |
| a1a (Low Dim/Small) (Baseline) | MLP | 0.8091 | 0.5741 | 0.17 |
| a1a (Low Dim/Small) (Baseline) | LDA | 0.7988 | 0.4260 | 0.05 |
| a1a (Sample Ratio=0.2) | SVM-Linear | 0.7975 | 0.5963 | 0.01 |
| a1a (Sample Ratio=0.2) | LR | 0.7944 | 0.6024 | 0.00 |
| a9a (Low Dim/Large) (Baseline) | NB | 0.4631 | 0.4618 | 0.03 |
| a1a (Low Dim/Small) (Baseline) | NB | 0.4004 | 0.4557 | 0.00 |

#### 2. 具体指标分析

##### 2.1. 数据集维度大小、数据量规模的影响

| 对比维度 | a1a (低维/小样本) | a9a (低维/大样本) | w8a (高维/大样本) |
| :--- | :--- | :--- | :--- |
| 最佳准确率 | 0.8278 (SVM-Linear) | 0.8505 (LR) | **0.9883 (MLP)** |
| NB 性能 | 0.4004 (极差) | 0.4631 (极差) | **0.9635 (优秀)** |
| SVM 耗时 | 0.08s | 67.86s | 91.63s |

1. **数据集规模 (a1a和a9a)：** a9a 的样本量远大于 a1a，所有模型的准确率普遍提升（例如 LR 提升约 $2.7$ 个百分点）。说明在一定程度上**更大的训练数据量**是提升模型性能直接有效的方法。

2. **维度(w8a)：** w8a的数据集质量极高，所有模型准确率都超过 $0.96$。

   * **NB 的适应性：** Naive Bayes 在 a1a/a9a 上由于**特征独立性假设**被破坏而表现不佳，但在 w8a 上的性能却大幅提升（高达 $0.9635$）。
   这可能意味着 w8a 的特征在高维空间中满足了更弱的条件独立性，或者数据本身具有高度可分离性，比如数据集本身具有**独立易分散**的特征，或者是因为**高纬度**的原因，使得特征之间的依赖性减弱。

   * **MLP 的优势：** 具有非线性能力的 **MLP** 在高维数据集 w8a 上表现最佳 ($0.9883$)，训练速度也比 SVM 快得多 ($3.97\text{s}$ 远低于 $91.63\text{s}$)。

3. **计算复杂度：** **SVM** 即使使用了线性核，其训练时间复杂度仍高，在大规模数据集 a9a 和 w8a 上耗时最长（超过一分钟）。对于大型任务，**LR** 和 **MLP** 是更有效率的选择。

##### 2.2. 训练集样本大小测试
这里以**a1a数据集**为例来进行测试：

| 训练比例 | 训练样本数 | LR 准确率 | SVM-Linear 准确率 |
| :--- | :--- | :--- | :--- |
| 20% | 256 | 0.7944 | 0.7975 |
| 50% | 642 | **0.8318** | 0.8162 |
| 80% | 1027 | 0.8224 | **0.8349** |

1. **正确率趋势：** $20\%$样本比例正确率约为0.79，$50\%$ 比例正确率约为0.83，提升比较明显，表明模型在训练初期的学习曲线非常陡峭，数据量带来的边际效益显著。
当训练样本数继续增加到 80% 时，准确率反而略有下降（0.8224），这可能暗示了 LR 模型对 a1a 数据集的过拟合敏感性，或者其性能瓶颈出现在 50% 左右。

2. **LR与SVM模型：**

   * 在小样本量（$20\%$）下，LR 和 SVM 性能相似。

   * 当样本量增加到 $80\%$ 时，**SVM-Linear** 超过 LR ($0.8349$ vs $0.8224$)。这表明 SVM 更能利用增加的数据来精确确定最优的决策边界，在高样本量下展现出更好的泛化能力。

##### 2.3. SVM 核函数
这里以**a9a数据集**为例来进行测试：

| 模型 | 准确率 (accuracy) | F1-Score | 训练时间 (s) |
| :--- | :--- | :--- | :--- |
| **SVM-Linear** | **0.8485** | **0.6501** | 90.62 |
| SVM-RBF | 0.8457 | 0.6338 | **32.64** |
| SVM-Poly | 0.8410 | 0.6057 | 42.09 |

1. **核函数性能：**
   **线性核** 实现了最佳性能，高于 RBF 和 Poly 核。这强烈暗示 a9a 数据集在特征标准化后，数据在特征空间中具有**良好的线性可分性**。在这种情况下，非线性核只会增加模型复杂度和训练时间，容易导致过拟合或收敛困难。

2. **泛化：**

   * 尽管线性核的性能最高，但它的训练时间也最长（$90.62\text{s}$）。
   * RBF 核的性能下降幅度很小（准确率仅从 $0.8485$ 降至 $0.8457$）。更重要的是，它的 F1-Score 也只略微下降（从 $0.6501$ 降至 $0.6338$），在保持整体准确率的同时，表示其在对少数类别的识别能力上（即精确率和召回率的平衡）也保持了相对高的水准。
   * RBF 核虽然性能略有损失，但训练时间大幅减少（降至 $32.64 \text{s}$）。鉴于性能差异微小，RBF 核提供了一个在性能、少数类别识别能力（F1-Score）和计算效率之间的良好折中方案，在**资源有限或需要快速迭代**的场景中，它将是更优的选择。

##### 3. 报告信息总结

数据量和特征维度（w8a）对模型性能有直接明显的作用。w8a 相比其他两个数据集在正确率上领先不少。
 **MLP** 在高维、高信息量的数据集 (w8a) 上表现出卓越的准确率和合理的训练速度，是该任务的最佳分类器。
如果选择 SVM，应优先考虑**线性核**以获得最高准确率，或选择 **RBF 核**以平衡性能和计算效率。对于 a9a 这类线性可分性好的数据集，不应盲目使用非线性核，否则会出现正确率偏低等问题。



#### 附录代码

```python
import numpy as np
import pandas as pd
import time
import requests
import io

from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score
from collections import defaultdict

DATASET_URLS = {
    "A1A (Low Dim/Small)": "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/a1a",
    "A9A (Low Dim/Large)": "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/a9a",
    "W8A (High Dim/Large)": "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/w8a" 
}

BASE_MODELS = {
    "Logistic Regression (LR)": LogisticRegression(solver='liblinear', random_state=42, max_iter=1000),
    "Naive Bayes (NB)": GaussianNB(),
    "Linear Discriminant Analysis (LDA)": LDA(),
    "Support Vector Machine (SVM-Linear)": SVC(kernel='linear', random_state=42, gamma='auto'),
    "Neural Networks (MLP)": MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42, early_stopping=True)
}

all_results = defaultdict(dict)

def load_and_preprocess_data(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return np.array([]), np.array([]) 
    data_io = io.BytesIO(response.content)
    X_sparse, y = load_svmlight_file(data_io)
    X = X_sparse.toarray()
    
    scaler = StandardScaler()
    X = scaler.fit_transform(X) 
    return X, y

def evaluate_model(model, X_train, y_train, X_test, y_test):
    try:
        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='binary', zero_division=0)
        
        return {
            'Accuracy': accuracy,
            'F1-Score': f1,
            'Train Time (s)': training_time
        }
    except Exception as e:
        print(f"Error: {e}")
        return {'Accuracy': np.nan, 'F1-Score': np.nan, 'Train Time (s)': np.nan, 'Error': str(e)}

def run_experiment_set(dataset_name, X, y, experiment_tag, models_to_run):
    if X.size == 0:
        print(f"实验集 {dataset_name}load error。")
        return
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    for name, model_instance in models_to_run.items():
        model = type(model_instance)(**model_instance.get_params())
        results = evaluate_model(model, X_train, y_train, X_test, y_test)
        
        full_tag = f"{dataset_name} ({experiment_tag})"
        all_results[full_tag][name] = results
        
        acc = results['Accuracy']
        time_sec = results['Train Time (s)']
        print(f"     Accuracy: {acc:.4f}, Time: {time_sec:.2f}s")


for name, url in DATASET_URLS.items():
    X_data, y_data = load_and_preprocess_data(url)
    run_experiment_set(name, X_data, y_data, "Baseline", BASE_MODELS)


X_A1A, y_A1A = load_and_preprocess_data(DATASET_URLS["A1A (Low Dim/Small)"])

if X_A1A.size > 0:
    TEST_SIZE_A1A = 0.2
    X_train_full, X_test, y_train_full, y_test = train_test_split(
        X_A1A, y_A1A, test_size=TEST_SIZE_A1A, random_state=42
    )
    
    for sample_ratio in [0.2, 0.5, 0.8]:
        train_size = int(len(X_train_full) * sample_ratio)
        X_train_sub = X_train_full[:train_size]
        y_train_sub = y_train_full[:train_size]
        
        sample_models = {
            "LR": LogisticRegression(solver='liblinear', random_state=42, max_iter=500),
            "SVM-Linear": SVC(kernel='linear', random_state=42, gamma='auto')
        }
        {sample_ratio:.1f}, N_train={len(X_train_sub)}) ---")
        for name, model_instance in sample_models.items():
            model = type(model_instance)(**model_instance.get_params())
            results = evaluate_model(model, X_train_sub, y_train_sub, X_test, y_test)
            full_tag = f"A1A (Sample Ratio={sample_ratio:.1f})"
            all_results[full_tag][name] = results
            print(f"  -> {name} Acc: {results['Accuracy']:.4f}")


X_A9A, y_A9A = load_and_preprocess_data(DATASET_URLS["A9A (Low Dim/Large)"])

if X_A9A.size > 0:
    SVM_MODELS = {
        "SVM (Linear Kernel)": SVC(kernel='linear', random_state=42, gamma='auto'),
        "SVM (RBF Kernel)": SVC(kernel='rbf', random_state=42, gamma='scale'),
        "SVM (Poly Kernel)": SVC(kernel='poly', degree=3, random_state=42, gamma='auto')
    }
    
    run_experiment_set("A9A (Low Dim/Large)", X_A9A, y_A9A, "Kernel Comparison", SVM_MODELS)


df_list = []
for experiment_tag, model_results in all_results.items():
    for model_name, metrics in model_results.items():
        row = {'Experiment': experiment_tag, 'Model': model_name}
        row.update(metrics)
        df_list.append(row)

final_df = pd.DataFrame(df_list)
if not final_df.empty:
    print(final_df.sort_values(by='Accuracy', ascending=False)[['Experiment', 'Model', 'Accuracy', 'F1-Score', 'Train Time (s)']].to_markdown(index=False, floatfmt=".4f"))
else:
    print("error：无生成结果。")


```
