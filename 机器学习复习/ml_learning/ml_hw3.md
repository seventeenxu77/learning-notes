### 机器学习第二次作业
---
##### 习题 1. 证明 ReLU 激活函数满足正系数齐次性质，即对于 \( c \in R^+ \)，
\[
\text{ReLU}(cx) = c \cdot \text{ReLU}(x)
\]

---


##### 证明：

ReLU 激活函数定义： $\text{ReLU}(z) = \max(0, z)$。

假设 $\mathbf{x}$ 是一个实数（或向量），$c$ 是一个正实数，即 $c > 0$。

1.  当 $\mathbf{x} \ge 0$ 时，$c\mathbf{x} \ge 0$，$\text{ReLU}(\mathbf{x}) = \mathbf{x}$ 
所以$\text{ReLU}(c\mathbf{x}) = c\mathbf{x} = c \cdot \text{ReLU}(\mathbf{x})$。

2. 当 $\mathbf{x} < 0$ 时，$c\mathbf{x} < 0$，$\text{ReLU}(c\mathbf{x}) = 0$
所以，$\text{ReLU}(c\mathbf{x}) = 0 = c \cdot 0 = c \cdot \text{ReLU}(\mathbf{x})$。

即对于 $c \in \mathbb{R}^+$，都有 $\text{ReLU}(c\mathbf{x}) = c \cdot \text{ReLU}(\mathbf{x})$，所以ReLU 激活函数满足正系数齐次性质

---
##### 习题2.考虑卷积神经网络。如果卷积核K是3x3矩阵,经过两个卷积运算得到特征图的感受野是多大？

---

对于连续 $L$ 层卷积，第 $L$ 层的感受野 $RF_L$ 依赖于前一层感受野 $RF_{L-1}$ 和本层卷积核大小 $K_L$，这里假设步长为1符合最简单的情况。

$$\text{RF}_L = \text{RF}_{L-1} + (K_L - 1) \times J_{L-1}$$

其中 $J_{L-1}$ 是前一层的有效步幅， $J_0=1$

**第一层卷积 (L=1)：**

$$\text{RF}_1 = \text{RF}_0 + (K_1 - 1) \times J_0= 1 + (3 - 1) \times 1 = 3$$

**第二层卷积 (L=2)：**

第一层的有效步幅：$J_1 = J_0 \times S_1 = 1 \times 1 = 1$

$$\text{RF}_2 = \text{RF}_1 + (K_2 - 1) \times J_1= 3 + (3 - 1) \times 1 = 5$$


经过两次 $3 \times 3$ 卷积运算后（默认步长为 1），特征图的感受野大小是 **$5 \times 5$**。
***
##### 习题 3. 考虑一个隐含层的感知器网络

 - 输入向量: $\boldsymbol{x} \in R^p$
- $\boldsymbol{s} = \boldsymbol{W}_1\boldsymbol{x} + \boldsymbol{b}_1 \in R^m$
- $\boldsymbol{z} = \text{ReLU}(\boldsymbol{s}) \in R^m$
- $\boldsymbol{u} = \boldsymbol{W}_2\boldsymbol{z} + \boldsymbol{b}_2 \in R^n$
- 损失函数: $L = \text{CrossEntropy}(\boldsymbol{y}, \text{soft max}(\boldsymbol{u}))$

请详细推导计算参数的局部梯度。
***
交叉熵损失 $L = \text{CrossEntropy}(\boldsymbol{y}, \hat{\boldsymbol{y}}) = -\sum_{k=1}^n y_k \ln \hat{y}_k$


计算损失 $L$ 对输出层净输入 $u_k$ 的导数（局部误差）：


已知$$L = -\sum_{l} y_l \ln \hat{y}_l \quad \hat{y}_l = \frac{e^{u_l}}{\sum_{i} e^{u_i}}$$

链式法则$$\frac{\partial L}{\partial u_k} = \sum_{l=1}^n \frac{\partial L}{\partial \hat{y}_l} \cdot \frac{\partial \hat{y}_l}{\partial u_k}$$
两个部分
$$\frac{\partial L}{\partial \hat{y}_l} = -\frac{y_l}{\hat{y}_l}$$

$$\frac{\partial \hat{y}_l}{\partial u_k} = \hat{y}_l (\delta_{lk} - \hat{y}_k)$$
$$\left( \text{推导自: } \begin{cases} l=k: \frac{\partial \hat{y}_k}{\partial u_k} = \hat{y}_k(1-\hat{y}_k) \\ l\neq k: \frac{\partial \hat{y}_l}{\partial u_k} = -\hat{y}_l \hat{y}_k \end{cases} \right)$$

$$\frac{\partial L}{\partial u_k} = \sum_{l=1}^n \left(-\frac{y_l}{\hat{y}_l}\right) \cdot \hat{y}_l (\delta_{lk} - \hat{y}_k)$$
代入
$$\frac{\partial L}{\partial u_k} = -\sum_{l=1}^n y_l (\delta_{lk} - \hat{y}_k)= -\sum_{l} y_l \delta_{lk} + \hat{y}_k \sum_{l} y_l$$


由于$\sum_{l} y_l = 1$ 和 $\sum_{l} y_l \delta_{lk} = y_k$
$$\delta_k^{(2)}=\frac{\partial L}{\partial u_k} = \hat{y}_k - y_k$$

---

##### 输出层参数 $\boldsymbol{W}_2$ 和 $\boldsymbol{b}_2$ 的局部梯度

$W_{kj}^{(2)}$ 表示隐含层第 $j$ 个节点到输出层第 $k$ 个节点的权重。
净输入 $u_k$ 关于 $W_{kj}^{(2)}$ 的导数：
$$u_k = \sum_{j=1}^m W_{kj}^{(2)} z_j + b_{k2} \implies \frac{\partial u_k}{\partial W_{kj}^{(2)}} = z_j$$
$$\frac{\partial L}{\partial W_{kj}^{(2)}} = \frac{\partial L}{\partial u_k} \cdot \frac{\partial u_k}{\partial W_{kj}^{(2)}} = \delta_k^{(2)} \cdot z_j = (\hat{y}_k - y_k) z_j$$

##### 偏置 $\boldsymbol{b}_2$ 的梯度 $\frac{\partial L}{\partial b_{k2}}$
$$u_k = \sum_{j=1}^m W_{kj}^{(2)} z_j + b_{k2} \implies \frac{\partial u_k}{\partial b_{k2}} = 1$$
$$\frac{\partial L}{\partial b_{k2}} = \frac{\partial L}{\partial u_k} \cdot \frac{\partial u_k}{\partial b_{k2}} = \delta_k^{(2)} \cdot 1 = \hat{y}_k - y_k$$

##### 隐含层参数 $\boldsymbol{W}_1$ 和 $\boldsymbol{b}_1$ 的局部梯度

损失 $L$ 通过 $u_k$ 和 $z_j$ 传到 $s_j$：
$$\delta_j^{(1)} = \frac{\partial L}{\partial s_j} = \frac{\partial L}{\partial z_j} \cdot \frac{\partial z_j}{\partial s_j}$$

- **$\frac{\partial L}{\partial z_j}$**
  $L$ 通过所有输出层净输入 $u_k$ 传递到 $z_j$：
  $$\frac{\partial L}{\partial z_j} = \sum_{k=1}^n \frac{\partial L}{\partial u_k} \cdot \frac{\partial u_k}{\partial z_j} = \sum_{k=1}^n \delta_k^{(2)} \cdot W_{kj}^{(2)}$$
  （因为 $u_k = \sum_{j'=1}^m W_{k j'}^{(2)} z_{j'} + b_{k2}$，故 $\frac{\partial u_k}{\partial z_j} = W_{kj}^{(2)}$）

- **$\frac{\partial z_j}{\partial s_j}$**
  即 ReLU 激活函数的导数：
  $$\frac{\partial z_j}{\partial s_j} = \mathbb{I}(s_j > 0)$$
  （其中 $\mathbb{I}(\cdot)$ 当括号内条件成立时为 1，否则为 0。）

- $\delta_j^{(1)}$：
  $$\delta_j^{(1)} = \left( \sum_{k=1}^n \delta_k^{(2)} W_{kj}^{(2)} \right) \cdot \mathbb{I}(s_j > 0)$$
  代入 $\delta_k^{(2)} = \hat{y}_k - y_k$：
  $$\delta_j^{(1)} = \left( \sum_{k=1}^n (\hat{y}_k - y_k) W_{kj}^{(2)} \right) \cdot \mathbb{I}(s_j > 0)$$

##### 2.1 权重 $\boldsymbol{W}_1$ 的梯度 $\frac{\partial L}{\partial W_{ji}^{(1)}}$
$W_{ji}^{(1)}$ 表示输入层第 $i$ 个节点到隐含层第 $j$ 个节点的权重。
净输入 $s_j$ 关于 $W_{ji}^{(1)}$ 的导数：
$$s_j = \sum_{i=1}^p W_{ji}^{(1)} x_i + b_{j1} \implies \frac{\partial s_j}{\partial W_{ji}^{(1)}} = x_i$$
$$\frac{\partial L}{\partial W_{ji}^{(1)}} = \frac{\partial L}{\partial s_j} \cdot \frac{\partial s_j}{\partial W_{ji}^{(1)}} = \delta_j^{(1)} \cdot x_i = \left( \sum_{k=1}^n (\hat{y}_k - y_k) W_{kj}^{(2)} \right) \mathbb{I}(s_j > 0) x_i$$

##### 2.2 偏置 $\boldsymbol{b}_1$ 的梯度 $\frac{\partial L}{\partial b_{j1}}$
净输入 $s_j$ 关于 $b_{j1}$ 的导数：
$$s_j = \sum_{i=1}^p W_{ji}^{(1)} x_i + b_{j1} \implies \frac{\partial s_j}{\partial b_{j1}} = 1$$
$$\frac{\partial L}{\partial b_{j1}} = \frac{\partial L}{\partial s_j} \cdot \frac{\partial s_j}{\partial b_{j1}} = \delta_j^{(1)} \cdot 1 = \left( \sum_{k=1}^n (\hat{y}_k - y_k) W_{kj}^{(2)} \right) \mathbb{I}(s_j > 0)$$

| 参数 | 梯度公式 |
| :---: | :---: |
| **输出层权重** $W_{kj}^{(2)}$ | $$\frac{\partial L}{\partial W_{kj}^{(2)}} = (\hat{y}_k - y_k) z_j$$ |
| **输出层偏置** $b_{k2}$ | $$\frac{\partial L}{\partial b_{k2}} = \hat{y}_k - y_k$$ |
| **隐含层权重** $W_{ji}^{(1)}$ | $$\frac{\partial L}{\partial W_{ji}^{(1)}} = \left( \sum_{k=1}^n (\hat{y}_k - y_k) W_{kj}^{(2)} \right) \mathbb{I}(s_j > 0) x_i$$ |
| **隐含层偏置** $b_{j1}$ | $$\frac{\partial L}{\partial b_{j1}} = \left( \sum_{k=1}^n (\hat{y}_k - y_k) W_{kj}^{(2)} \right) \mathbb{I}(s_j > 0)$$ |