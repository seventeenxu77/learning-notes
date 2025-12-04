### 机器学习第七次作业
---
##### Problem 1.
Given training data \( \{x_i\}_{i=1}^N, x_i \in R^p \), \( \Sigma \) is its covariance matrix with eigenvectors \( \{\mathbf{v}_j\}_{j=1}^p \) and eigenvalues \( \lambda_1 > \lambda_2 > \mathrm{L} > \lambda_p \). Given an eigenvector \( \mathbf{v}_j \), the projection of data to eigenvector \( \mathbf{v}_j \) subspace is defined by:
$$\hat{\mu}_j, \{\hat{\beta}_{ji}\}_{i=1}^N = \arg \min \sum_{i=1}^N \left\|x_i - \mu - \mathbf{v}_j \beta_{ji}\right\|^2, \text{ where } \mathbf{v}_j^T \mathbf{v}_j = 1.$$

1. Derive the solution to the optimal problem.

2. Prove that \( \sum_{i=1}^N \left\|x_i - \hat{\mu}_k - \mathbf{v}_k \hat{\beta}_{ki}\right\|^2 < \sum_{i=1}^N \left\|x_i - \hat{\mu}_j - \mathbf{v}_j \hat{\beta}_{ji}\right\|^2 \), if \( k < l \).

---


1.

求解$\mu$:

$$
\frac{\partial J}{\partial \boldsymbol{\mu}} = \sum_{i=1}^{N} \frac{\partial}{\partial \boldsymbol{\mu}} \left(\mathbf{x}_{i}-\boldsymbol{\mu}-\mathbf{v}_{j} \beta_{j i}\right)^{\mathrm{T}} \left(\mathbf{x}_{i}-\boldsymbol{\mu}-\mathbf{v}_{j} \beta_{j i}\right)
$$


$$
\frac{\partial J}{\partial \boldsymbol{\mu}} = \sum_{i=1}^{N} \left[-2 (\mathbf{x}_{i}-\boldsymbol{\mu}-\mathbf{v}_{j} \beta_{j i})\right] = 0
$$

$$
N\boldsymbol{\mu} = \sum_{i=1}^{N} \mathbf{x}_{i} - \mathbf{v}_{j} \sum_{i=1}^{N} \beta_{j i}
$$

假设投影居中，所以$\sum_{i=1}^{N} \beta_{j i} = 0$

$$
N\boldsymbol{\mu} =  \frac{1}{N} \sum_{i=1}^{N} \mathbf{x}_{i} = \bar{\mathbf{x}}
$$

---

2. 求解 $\left\{\hat{\beta}_{j i}\right\}_{i=1}^{N}$ 

令 $\mathbf{y}_i = \mathbf{x}_i - \hat{\boldsymbol{\mu}}_{j} = \mathbf{x}_i - \bar{\mathbf{x}}$。目标函数变为：

$$
J'(\left\{\beta_{j i}\right\}) = \sum_{i=1}^{N}\left\|\mathbf{y}_{i}-\mathbf{v}_{j} \beta_{j i}\right\|^{2}
$$

独立 $\beta_{j i}$ 求导，并令其为零：

$$
\frac{\partial J'}{\partial \beta_{j i}} = \frac{\partial}{\partial \beta_{j i}} (\mathbf{y}_{i}-\mathbf{v}_{j} \beta_{j i})^{\mathrm{T}} (\mathbf{y}_{i}-\mathbf{v}_{j} \beta_{j i}) = 0
$$

$$
\frac{\partial}{\partial \beta_{j i}} (\mathbf{y}_{i}^{\mathrm{T}}\mathbf{y}_{i} - 2\beta_{j i} \mathbf{v}_{j}^{\mathrm{T}}\mathbf{y}_{i} + \beta_{j i}^{2} \mathbf{v}_{j}^{\mathrm{T}}\mathbf{v}_{j}) = 0
$$

由于 $\mathbf{v}_{j}^{\mathrm{T}} \mathbf{v}_{j} = 1$:



$$
\hat{\beta}_{j i} = \mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i} = \mathbf{v}_{j}^{\mathrm{T}} (\mathbf{x}_{i} - \bar{\mathbf{x}})
$$


---


2.

将 $\hat{\boldsymbol{\mu}}$ 和 $\hat{\beta}$ 代入目标函数。




$$
E_j = \sum_{i=1}^{N}\left\|\mathbf{y}_{i}-\mathbf{v}_{j} (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i})\right\|^{2}
$$

由于向量 $\mathbf{v}_{j} (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i})$ 是 $\mathbf{y}_{i}$ 在 $\mathbf{v}_{j}$ 上的投影，其中后面表示的数值，指的是投影长度。误差向量 $\mathbf{y}_{i}-\mathbf{v}_{j} (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i})$ 与 $\mathbf{v}_{j}$ 正交。使用勾股定理：

$$
\|\mathbf{y}_{i}\|^2 = \|\mathbf{v}_{j} (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i})\|^2 + \|\mathbf{y}_{i}-\mathbf{v}_{j} (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i})\|^2
$$

$$
\|\mathbf{y}_{i}-\mathbf{v}_{j} \hat{\beta}_{j i}\|^2 = \|\mathbf{y}_{i}\|^2 - \|\mathbf{v}_{j} \hat{\beta}_{j i}\|^2
$$

由于 $\mathbf{v}_j$ 是单位向量 ($\|\mathbf{v}_j\|=1$)，且 $\hat{\beta}_{j i}$ 是标量：
$$
\|\mathbf{v}_{j} \hat{\beta}_{j i}\|^2 = \hat{\beta}_{j i}^2 \|\mathbf{v}_{j}\|^2 = \hat{\beta}_{j i}^2= (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i})^2
$$

$$
E_j = \sum_{i=1}^{N} \left( \|\mathbf{y}_{i}\|^2 - (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i})^2 \right) = \sum_{i=1}^{N} \|\mathbf{y}_{i}\|^2 - \sum_{i=1}^{N} (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i})^2
$$

将第二项写成协方差矩阵的形式：

$$
\sum_{i=1}^{N} (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i})^2 = \sum_{i=1}^{N} (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{y}_{i}) (\mathbf{y}_{i}^{\mathrm{T}} \mathbf{v}_{j}) = \mathbf{v}_{j}^{\mathrm{T}} \left( \sum_{i=1}^{N} \mathbf{y}_{i} \mathbf{y}_{i}^{\mathrm{T}} \right) \mathbf{v}_{j}
$$

$$
\mathbf{v}_{j}^{\mathrm{T}} \left( \sum_{i=1}^{N} \mathbf{y}_{i} \mathbf{y}_{i}^{\mathrm{T}} \right) \mathbf{v}_{j} \approx N \cdot \mathbf{v}_{j}^{\mathrm{T}} \Sigma \mathbf{v}_{j}
$$

代入特征值方程 $\Sigma \mathbf{v}_j = \lambda_j \mathbf{v}_j$:

$$
N \cdot \mathbf{v}_{j}^{\mathrm{T}} \Sigma \mathbf{v}_{j} = N \cdot \mathbf{v}_{j}^{\mathrm{T}} (\lambda_j \mathbf{v}_{j}) = N \lambda_j (\mathbf{v}_{j}^{\mathrm{T}} \mathbf{v}_{j}) = N \lambda_j
$$

重构误差 $E_j$ 的表达式近似为：

$$
E_j \approx \sum_{i=1}^{N} \|\mathbf{y}_{i}\|^2 - N \lambda_j
$$

因此
$$
\sum_{i=1}^{N}\left\|\mathbf{x}_{i}-\hat{\boldsymbol{\mu}}_{k}-\mathbf{v}_{k} \hat{\beta}_{k i}\right\|^{2} < \sum_{i=1}^{N}\left\|\mathbf{x}_{i}-\hat{\boldsymbol{\mu}}_{l}-\mathbf{v}_{l} \hat{\beta}_{l i}\right\|^{2}, \quad \text{如果 } k < l
$$

---
### Problem 2.
Please derive gradient descent algorithm for ICA model by minimizing the KL divergence between the joint probability density function \( p(\mathbf{x}) \) and its factored probability density function \( q(\mathbf{x}) = q_1(x_1)q_2(x_2)\dots q_n(x_n) \) in detail.

---

已知分离矩阵W，将观测数据x线性变换为独立成分y：
$$
\mathbf{y} = \mathbf{W}\mathbf{x}
$$

$$
H(\mathbf{y}) = H(\mathbf{x}) + \log|\det(\mathbf{W})|
$$

$$
KL(\mathbf{W}) = \int p(\mathbf{y}) \log \frac{p(\mathbf{y})}{\prod_{k=1}^{K} p_k(y_k)} d\mathbf{y}
$$

$$
KL(\mathbf{W}) = -H(\mathbf{y}) - \sum_{k=1}^{K} \int p(\mathbf{y}) \log p_k(y_k) d\mathbf{y}
$$

将 $H(\mathbf{y})$ 替换为 $H(\mathbf{x}) + \log|\det(\mathbf{W})|$：

$$
KL(\mathbf{W}) = -H(\mathbf{x}) - \log|\det(\mathbf{W})| - \sum_{k=1}^{K} \mathbf{E} [\log p_k(y_k)]
$$
最大化这个函数：
$$
\mathcal{L}(\mathbf{W}) = \log|\det(\mathbf{W})| + \sum_{k=1}^{K} \mathbf{E} [\log p_k(y_k)]
$$

$$
\Delta \mathbf{W} \propto -\frac{\partial KL(\mathbf{W})}{\partial \mathbf{W}} = \frac{\partial \mathcal{L}(\mathbf{W})}{\partial \mathbf{W}}
$$

$$
\nabla \mathcal{L}(\mathbf{W}) = \frac{\partial}{\partial \mathbf{W}} \log|\det(\mathbf{W})| + \frac{\partial}{\partial \mathbf{W}} \sum_{k=1}^{K} \mathbf{E} [\log p_k(y_k)]
$$
第一个部分的梯度为$\mathbf{W}^{-\mathrm{T}}$,算第二部分：

定义非线性函数 $\boldsymbol{\varphi}(\mathbf{y})$：
$$
\boldsymbol{\varphi}(\mathbf{y}) = \left[ \frac{\partial \log p_1(y_1)}{\partial y_1}, \ldots, \frac{\partial \log p_K(y_K)}{\partial y_K} \right]^{\mathrm{T}}
$$

$$
\frac{\partial}{\partial \mathbf{W}} \sum_{k=1}^{K} \mathbf{E} [\log p_k(y_k)] = \mathbf{E}_{\mathbf{x}} \left[ \boldsymbol{\varphi}(\mathbf{y}) \mathbf{x}^{\mathrm{T}} \right]
$$


将 $\mathbf{x}^{\mathrm{T}}$ 替换为 $(\mathbf{W}^{-1}\mathbf{y})^{\mathrm{T}} = \mathbf{y}^{\mathrm{T}}\mathbf{W}^{-\mathrm{T}}$：
$$
\nabla \mathcal{L}(\mathbf{W}) = \mathbf{W}^{-\mathrm{T}} + \mathbf{E} \left[ \boldsymbol{\varphi}(\mathbf{y}) \mathbf{y}^{\mathrm{T}}\mathbf{W}^{-\mathrm{T}} \right]
$$

$$
\nabla \mathcal{L}(\mathbf{W}) = \left( \mathbf{I} + \mathbf{E} \left[ \boldsymbol{\varphi}(\mathbf{y}) \mathbf{y}^{\mathrm{T}} \right] \right) \mathbf{W}^{-\mathrm{T}}
$$


加入自然梯度
$$
\tilde{\nabla} \mathcal{L}(\mathbf{W}) = \left( \mathbf{I} + \mathbf{E} \left[ \boldsymbol{\varphi}(\mathbf{y}) \mathbf{y}^{\mathrm{T}} \right] \right) \mathbf{W}^{-\mathrm{T}} \cdot (\mathbf{W}^{\mathrm{T}}\mathbf{W})
$$


$$
\tilde{\nabla} \mathcal{L}(\mathbf{W}) = \left( \mathbf{I} + \mathbf{E} \left[ \boldsymbol{\varphi}(\mathbf{y}) \mathbf{y}^{\mathrm{T}} \right] \right) \mathbf{W}
$$
