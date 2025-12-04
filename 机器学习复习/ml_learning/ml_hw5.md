### 机器学习第五次作业
---
##### 习题：设训练数据 \( D = \{(x_i, y_i)\}_{i=1}^N \)，记 \( X = \{x_i\}_{i=1}^N, Y = \{y_i\}_{i=1}^N \)。

---

##### 1. 证明线性回归模型和 KNN 模型的解可以表示为以下形式
$$\hat{f}(x_0) = \sum_{i=1}^N l_i(x_0, X) y_i$$其中，权重 \( l_i(x_0, X) \) 不依赖于 \( y_i \)。

---

**线性模型**

线性回归权重解为：
$$\hat{\mathbf{w}} = (X^T X)^{-1} X^T \mathbf{y}$$
对于一个输入点$x_0,$，其预测值 $\hat{f}(x_0) = x_0 \hat{\mathbf{w}}= x_0 (X^T X)^{-1} X^T \mathbf{y}$



令$$\mathbf{l}^T = x_0 (X^T X)^{-1} X^T$$

$$\hat{f}(x_0) = \mathbf{l}^T \mathbf{y}$$

将内积展开为求和形式，其中 $\mathbf{l}^T$ 的第 $i$ 个元素即为 $l_i(x_0, X)$：
    $$\hat{f}(x_0) = \sum_{i=1}^{N} l_i(x_0, X) y_i$$
权重由X的元素构成，不涉及y

**KNN模型**

$$\hat{f}(x_0) = \frac{1}{K} \sum_{i \in \mathcal{N}_K(x_0)} y_i$$
定义权重 $l_i(x_0, X)$ 如下：
$$l_i(x_0, X) = \begin{cases} \frac{1}{K} & \text{if } x_i \in \mathcal{N}_K(x_0) \\ 0 & \text{otherwise} \end{cases}$$

$$\hat{f}(x_0) = \sum_{i=1}^{N} l_i(x_0, X) y_i = \sum_{i \in \mathcal{N}_K(x_0)} \frac{1}{K} y_i + \sum_{i \notin \mathcal{N}_K(x_0)} 0 \cdot y_i$$

$$\hat{f}(x_0) = \frac{1}{K} \sum_{i \in \mathcal{N}_K(x_0)} y_i$$

权重 $l_i(x_0, X)$ 的取值完全取决于 $x_0$ 与训练集 $X$ 中各点的位置关系比如距离等，不依赖于 $y_i$。

---

##### 2. 请给出条件均方误差的偏差和方差分解$$\mathrm{E}_{Y|X}(f(x_0) - \hat{f}(x_0))^2.$$对于线性回归问题，证明$$\mathrm{Var}_{Y|X}(\hat{f}(x_0)) = \sigma^2 \sum_{i=1}^N l_i^2(x_0, X).$$

---
**条件均方误差分解**
用$D$取代$Y|X$,同时令$\mu =E_D[\hat{f}(x_0)]$

原式$= E_D\left[ \left( (f(x_0) - E_D[\hat{f}(x_0)]) + (E_D[\hat{f}(x_0)] - \hat{f}(x_0)) \right)^2 \right]$

$$= E_D[(f(x_0) - \mu)^2] + 2 E_D[(f(x_0) - \mu)(\mu - \hat{f}(x_0))]$$

$$+ E_D[(\mu - \hat{f}(x_0))^2]$$
偏差项：

$$E_D[(f(x_0) - \mu)^2] = (f(x_0) - \mu)^2 $$

$$= \left(f(x_0) - E_D[\hat{f}(x_0)]\right)^2= {\text{Bias}^2(x_0)}$$

交叉项

$$2 (f(x_0) - \mu) E_D[\mu - \hat{f}(x_0)] = 2 (f(x_0) - \mu) (\mu - E_D[\hat{f}(x_0)])  = 0$$

方差项

$$E_D[(\mu - \hat{f}(x_0))^2] = E_D\left[\left(\hat{f}(x_0) - E_D[\hat{f}(x_0)]\right)^2\right] = {\text{Variance}(x_0)}$$

**线性回归证明**
第一问已经证明：
$$\hat{f}(x_0) = \sum_{i=1}^{N} l_i(x_0, X) y_i$$

假设训练数据 $y_i$ 是由真实函数值 $f(x_i)$ 加上一个随机噪声 $\epsilon_i$ 生成的：
$$y_i = f(x_i) + \epsilon_i$$

$E[\epsilon_i] = 0，\text{Var}(\epsilon_i) = \sigma^2$
$$\text{Var}(y_i) = \text{Var}(f(x_i) + \epsilon_i) = \text{Var}(\epsilon_i) = \sigma^2$$
由于$y_i$独立同分布：
$$\text{Var}_{Y|X}(\hat{f}(x_0)) = \text{Var}\left( \sum_{i=1}^{N} l_i(x_0, X) y_i \right)= \sum_{i=1}^{N} \left( l_i(x_0, X) \right)^2 \text{Var}(y_i)$$

$$= \sum_{i=1}^{N} l_i^2(x_0, X) \sigma^2= \sigma^2 \sum_{i=1}^{N} l_i^2(x_0, X)$$

---

##### 3. 给出（无条件）均方误差的偏差和方差分解$$\mathrm{E}_{X,Y}(f(x_0) - \hat{f}(x_0))^2.$$对于线性回归问题，证明
$$\mathrm{Var}_{X,Y}(\hat{f}(x_0)) = E_X\left[\sigma^2 \sum_{i=1}^N l_i(x_0, X)^2\right]$$

$$+ \mathrm{Var}_X\left[\sum_{i=1}^N l_i(x_0, X) f(x_i)\right].$$

---
只需将问题2的条件均方误差外面做x的期望处理即可：
$$= E_{X}\left[ E_{Y|X}\left[(f(x_0) - \hat{f}(x_0))^2 \mid X=x_0\right] \right]$$


$$= E_{X}\left[ \text{Bias}^2(x_0) \right] + E_{X}\left[ \text{Variance}(x_0) \right]$$



**线性回归证明**


使用全方差公式：
$$\text{Var}(Z) = E_X[\text{Var}(Z|X)] + \text{Var}_X[E[Z|X]]$$



$$\text{Var}_{X,Y}(\hat{f}(x_0)) = E_X[\text{Var}_{Y|X}(\hat{f}(x_0))] + \text{Var}_X[E_{Y|X}(\hat{f}(x_0))]$$

由于$\text{Var}_{Y|X}(\hat{f}(x_0)) = \sigma^2 \sum_{i=1}^{N} l_i^2(x_0, X)$
第一项：

$$E_X[\text{Var}_{Y|X}(\hat{f}(x_0))] = E_X\left[\sigma^2 \sum_{i=1}^{N} l_i^2(x_0, X)\right]$$


第二项内部条件期望：

$$E_{Y|X}(\hat{f}(x_0)) = E_{Y|X}\left[\sum_{i=1}^{N} l_i(x_0, X) y_i\right]$$

将期望符号移入求和：
$$E_{Y|X}(\hat{f}(x_0)) = \sum_{i=1}^{N} l_i(x_0, X) E_{Y|X}[y_i]$$

由于 $y_i = f(x_i) + \epsilon_i$，且 $E[\epsilon_i]=0$：
$$E_{Y|X}[y_i] = E[f(x_i) + \epsilon_i] = f(x_i) + E[\epsilon_i] = f(x_i)$$

代回条件期望公式：
$$E_{Y|X}(\hat{f}(x_0)) = \sum_{i=1}^{N} l_i(x_0, X) f(x_i)$$

求方差得到第二项
$$\text{Var}_X[E_{Y|X}(\hat{f}(x_0))] = \text{Var}_X\left[\sum_{i=1}^{N} l_i(x_0, X) f(x_i)\right]$$
合并一二两项：

$$\text{Var}_{X,Y}(\hat{f}(x_0)) = E_X\left[\sigma^2 \sum_{i=1}^{N} l_i^2(x_0, X)\right] $$

$$+ \text{Var}_X\left[\sum_{i=1}^{N} l_i(x_0, X) f(x_i)\right]$$

---

##### 4.讨论上述两种情况下平方偏置和方差之间的关系。

---

有条件分解和无条件分解之间的关系是通过对输入特征 $X$ 取期望建立起来的，主要是模型误差在特定点 $x_0$ 和在整个数据分布上的不同表现。


**情况1**，**特定点$x_0$**;
偏差 $\text{Bias}(x_0)$ 和方差 $\text{Variance}(x_0)$ 都是关于特定点 $x_0$ 的函数。这意味着模型的拟合能力和稳定性在输入空间的不同区域可能不同。
    模型的复杂度（例如线性回归中的特征数量、KNN 中的 $1/K$）是一些复杂度的控制参数。
    模型越简单： 偏差越高欠拟合风险增高，方差越低越稳定。
主要衡量了在给定 $x_0$ 下，模型选择带来的**全部误差**
反映的是直接的局部样本的偏差-方差权衡

**情况2**，**整个输入空间**上的平均表现。


整个误差是对所有输入点 $x_0$ 上的局部偏差和方差进行平均得到的结果。反映了模型在整个数据分布上的**平均性能**。
平均偏差平方 $E_X[\text{Bias}^2(x_0)]$衡量模型在整个输入空间上系统性地偏离真实函数的程度。
平均方差 $E_X[\text{Variance}(x_0)]$：衡量模型在整个输入空间上平均的稳定性。
主要体现的是模型的泛化性

反映的是全局平均值的偏差-方差权衡


共同点就是偏差-方差分解的本质关系（复杂模型低偏差高方差，简单模型高偏差低方差）在这两种情况下都成立。区别在于，条件分解分析的是局部原因，无条件分解分析的是全局结果。
