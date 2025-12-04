### 机器学习第四次作业
---
#### 一：判别是非题
##### 1.当训练数据量充分大时，贝叶斯信息准则（BIC）选择的模型比Akaike信息准则（AIC）更加简单。

---

正确，BIC使用klog(n)而AIC使用2k，所以当样本足够多，BIC对参数惩罚更重，选择模型更简单

---
##### 2.对于两类分类问题，两类样本服从高斯分布，具有不同的均值和相同的方差。当其中一类训练样本数大于另外一类时，则其后验概率的判别分界面不是线性的。
---
错误，根据朴素贝叶斯对数几率，代入两种分类的分布数学形式时
$$\log \left( \frac{P(Y=1|X)}{P(Y=0|X)} \right)$$
由于两个分类的方差相同，所以二次项可以被消除，得到线性的分界面，是否形成线性分界面和样本数量无关，和两个分类分别的方差有关

---
#### 二：
##### 假设统计模型 \( Y = f(X) + \varepsilon \)，其中误差 \( \varepsilon \propto N(0, \sigma_\varepsilon^2) \)。请推导在均方误差损失的条件下，回归函数的理论解为 \( f(x) = E_Y[y \mid X = x] \)。

---
均方误差损失条件下，期望预测损失即为下面的形式，转为条件概率
$$\text{EPE}(f) = E_{\mathbf{X}, Y}[(Y - f(\mathbf{X}))^2]$$


$$\text{EPE}(f) = E_X [ E_{Y|X} [(Y - f(X))^2 | X] ]$$

为了最小化 $\text{EPE}(f)$，对内部期望逐点极小化。对于任何$X=x$，最优预测值 $f(x)$ 记为常数 $c$(毕竟f仅有变量x，x确定fx确定)

$$f(x) = \arg \min_{c} E_{Y|X} [(Y - c)^2 | X = x]$$

设目标函数 $g(c) = E[(Y - c)^2 | X = x]$。对c求导。

$$\frac{\partial g(c)}{\partial c} = \frac{\partial}{\partial c} E[(Y - c)^2 | X = E \left[ \frac{\partial}{\partial c} (Y - c)^2 | X = x \right]$$

$$\frac{\partial g(c)}{\partial c} = E \left[ 2(Y - c) \cdot (-1) | X = x \right] = -2 E [Y - c | X = x]$$

令导数等于零，寻找极值点 $c^*$：

$$-2 E [Y - c^* | X = x] = 0$$

$$E [Y - c^* | X = x] = 0$$


$$E [Y | X = x] - E [c^* | X = x] = 0$$
由于c*和x取值无关，是预先确定的函数值，所以c的值和x无关，期望也无关
$$E [Y | X = x] - c^* = 0$$


$$c^* = E [Y | X = x]$$
即\( f(x) = E_Y[y \mid X = x] \)

---

#### 三、神经网络与深度学习
##### 以深度卷积神经网络为例，讨论哪些模型参数可以用于模型选择的参数。如何对深度卷积网络进行模型正则化，避免模型对训练数据的过度拟合。
**网络的层数(layer)**：深度增加，会一定程度上增加表达力，太深有过拟合风险。
**神经元数量(neuron)**：可以用来确定模型宽度，提取更多特征，越多可能有过拟合风险。
**卷积核大小规模(convolution kernel)**:会影响捕获特征范围和感受野。
**激活函数的选择(activation function)**:非线性程度。
**池化类型和大小(pooling)**:池化类型和大小。
**随即失活概率(dropout)**：以一定概率让神经元停止工作。
**训练轮数(training epoch)**：模型训练迭代次数，过长可能导致过拟合


**权重正则化（Weight Regularization）**
损失函数里面加上权重的正则项，比如L2正则向损失函数中添加所有权重平方的和$W^2$，L1正则向损失函数中添加所有权重绝对值的和$|W|$。
这样会迫使模型倾向选择更小的权重，而不会出现某个权重异常大而导致的过拟合而导致的方差过大。


**随机失活（Dropout）**
在训练过程中，随机地（以一定概率 $p$）让神经元停止工作。
防止神经元形成过于复杂的相互依赖关系而导致的过拟合。

**早停法（Early Stopping）**
当验证集损失开始增加，则停止训练，防止在验证集上达到最小后继续拟合训练数据，按照训练轮数epoch进行调整

**批量归一化（Batch Normalization, BN）**
对每一层的输入进行归一化操作，使其均值为 0，方差为 1。
稳定每一层的输入分布，防止局部噪音影响权重训练导致过拟合，可以减少对其他正则化方法（如 Dropout）的依赖。

**其他**
网络层数越深，每层神经元数量越多，都会增加过拟合的风险，所以要选择合理的神经元数量和层数规模，不是越深越多越好。

---

#### 四、(极大似然与极大后验)
##### 1. 假设统计模型 \( Y = f(X, \beta) + \varepsilon \)，其中误差 \( \varepsilon \propto N(0, \sigma_\varepsilon^2) \)。如何定义其回归问题的似然函数 \( p(y \mid x, \beta) \)，并证明其极大似然的解等价于预测模型均方误差极小问题。

---

由于 $Y = f(X, \beta) + \varepsilon$ 且 $\varepsilon \sim N(0, \sigma_\varepsilon^2)$，所以 $Y$ 是一个随机变量，其均值为 $f(X, \beta)$，方差为 $\sigma_\varepsilon^2$。

因此，给定 $x$ 和参数 $\beta$，条件概率 $p(y \mid x, \beta)$ 服从高斯分布

$$p(y \mid x, \beta) = N(f_{\beta}(x), \sigma^2)$$

$$p(y \mid x, \beta) = \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{(y - f_{\beta}(x))^2}{2\sigma^2}\right)$$

根据样本数据独立同分布，所以似然函数：

$$L(\theta) = \prod_{i=1}^{N} p(y_i \mid x_i, \beta) = \prod_{i=1}^{N} \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{(y_i - f_{\beta}(x_i))^2}{2\sigma^2}\right)$$
取对数：

$$l(\theta) = \ln \left( \prod_{i=1}^{N} \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{(y_i - f_{\beta}(x_i))^2}{2\sigma^2}\right) \right)$$

$$l(\theta) = \sum_{i=1}^{N} \left[ \ln\left(\frac{1}{\sqrt{2\pi}\sigma}\right) - \frac{(y_i - f_{\beta}(x_i))^2}{2\sigma^2} \right]$$

$$l(\theta) = -N \ln(\sqrt{2\pi}\sigma) - \frac{1}{2\sigma^2} \sum_{i=1}^{N} (y_i - f_{\beta}(x_i))^2$$

$$\hat{\beta} = \arg \max_{\beta} \left[ -N \ln(\sqrt{2\pi}\sigma) - \frac{1}{2\sigma^2} \sum_{i=1}^{N} (y_i - f_{\beta}(x_i))^2 \right]$$
丢掉常数和多余的系数

$$\hat{\beta} = \arg \min_{\beta} \left[ \sum_{i=1}^{N} (y_i - f_{\beta}(x_i))^2 \right]$$


因此，在误差服从 $N(0, \sigma_\varepsilon^2)$ 假设下，回归问题的极大似然估计解等价于均方误差极小化问题的解。

---
##### 2. 设回归模型的参数先验 \( p(\beta) = N(0, \tau I) \)，证明在上一小题的假设条件下，模型参数的后验概率 \( p(\beta \mid y, x) \) 也是高斯分布。
---
贝叶斯，然后换成向量形式：

$$p(\beta | Y, X) \propto p(Y | X, \beta) \cdot p(\beta)$$


$$p(Y | X, \beta) \propto \exp \left\{ -\frac{1}{2\sigma_{\varepsilon}^2} (Y - f(X, \beta))^T (Y - f(X, \beta)) \right\}$$

参数 $\beta$ 的先验分布是均值为 0、协方差矩阵为 $\tau I$ 的高斯分布 $N(0, \tau I)$。

$$p(\beta) = \frac{1}{\sqrt{(2\pi)^P |\tau I|}} \exp \left\{ -\frac{1}{2} (\beta - 0)^T (\tau I)^{-1} (\beta - 0) \right\}$$

$$p(\beta) \propto \exp \left\{ -\frac{1}{2} \beta^T (\frac{1}{\tau} I) \beta \right\}$$
后验概率：

$$p(\beta | Y, X) \propto \exp \left\{ -\frac{1}{2\sigma_{\varepsilon}^2} (Y - f(X, \beta))^T (Y - f(X, \beta)) - \frac{1}{2\tau} \beta^T I \beta \right\}$$

$f(X, \beta)$ 是线性的，即 $f(X, \beta) = H\beta$

$$ \frac{1}{\sigma_{\varepsilon}^2} (Y - H\beta)^T (Y - H\beta) + \frac{1}{\tau} \beta^T \beta$$

$$\propto \frac{1}{\sigma_{\varepsilon}^2} (Y^T Y - 2Y^T H\beta + \beta^T H^T H\beta) + \frac{1}{\tau} \beta^T \beta$$


$$\propto {\beta^T \left( \frac{1}{\sigma_{\varepsilon}^2} H^T H + \frac{1}{\tau} I \right) \beta} - {\left( \frac{2}{\sigma_{\varepsilon}^2} Y^T H \right) \beta}+ {\frac{1}{\sigma_{\varepsilon}^2} Y^T Y}$$


这个指数包含$\beta$也是一个二次函数，所以具备高斯函数的形式，在题目条件下，后验概率满足高斯分布。

---

##### 3. 以基展开模型 \( f(x, \beta) = \sum_{j=1}^N \beta_j h_j(x) \); \( h_j(x) \)是一组基函数为例，给出回归系数\( \beta \)后验概率的均值与方差。

---

基展开模型 $f(X, \beta) = \sum_{j=1}^{N} \beta_j h_j(x)$ 是问题2里面的 $f(X, \beta) = H\beta$ 的具体形式，其中 $H$ 是由基函数 $h_j(x_i)$ 构成的矩阵。


问题2已经知道后验分布 $p(\beta | Y, X)$ 也是一个高斯分布 $N(\hat{\mu}, \hat{\Sigma})$。

任何一个均值为 $\hat{\mu}$、协方差为 $\hat{\Sigma}$ 的高斯分布，其概率密度函数：

$$\propto \exp \left\{ -\frac{1}{2} (\beta - \hat{\mu})^T \hat{\Sigma}^{-1} (\beta - \hat{\mu}) \right\}$$

展开这个标准形式，并与实际的后验指数项进行比较，来解 $\hat{\mu}$。


$$\begin{aligned} (\beta - \hat{\mu})^T \hat{\Sigma}^{-1} (\beta - \hat{\mu}) &= \beta^T \hat{\Sigma}^{-1} \beta - \beta^T \hat{\Sigma}^{-1} \hat{\mu} - \hat{\mu}^T \hat{\Sigma}^{-1} \beta + \hat{\mu}^T \hat{\Sigma}^{-1} \hat{\mu} \\ &= \beta^T \hat{\Sigma}^{-1} \beta - 2 (\hat{\Sigma}^{-1} \hat{\mu})^T \beta + \hat{\mu}^T \hat{\Sigma}^{-1} \hat{\mu} \end{aligned}$$


问题2得到的指数项：
$$\propto \beta^T \left( \frac{H^T H}{\sigma_{\varepsilon}^2} + \frac{I}{\tau} \right) \beta - 2 \left( \frac{H^T Y}{\sigma_{\varepsilon}^2} \right)^T \beta + \text{与 $\beta$ 无关的常数项}$$

比较二次项，直接得到后验协方差矩阵的逆：
$$\hat{\Sigma}^{-1} = \frac{H^T H}{\sigma_{\varepsilon}^2} + \frac{I}{\tau}$$
**即后验概率方差：**
$$\hat{\Sigma} = (\frac{H^T H}{\sigma_{\varepsilon}^2} + \frac{I}{\tau})^{-1}$$

比较一次项：

$$- 2 (\hat{\Sigma}^{-1} \hat{\mu}) = - 2 \left( \frac{H^T Y}{\sigma_{\varepsilon}^2} \right)$$

$$\hat{\Sigma}^{-1} \hat{\mu} = \frac{H^T Y}{\sigma_{\varepsilon}^2}$$

**解出后验概率均值：**

$$\hat{\mu} = \left( H^T H + \frac{\sigma_{\varepsilon}^2}{\tau} I \right)^{-1} H^T Y$$

---

#### 五、(模型选择) 
在平方误差损失情况下，线性回归模型的训练误差的乐观性有下列估计
$$op = \frac{2}{N}\sum_{i=1}^{N}Cov(\hat{y}_i, y_i) = 2\frac{d}{N}\sigma_{\varepsilon}^2$$

---

$Y = X\beta + \varepsilon$其中$\varepsilon \sim N(0, \sigma_{\varepsilon}^2 I)$
最小二乘估计
$$\hat{\beta} = (X^T X)^{-1} X^T Y$$
预测值：
$$\hat{Y} = X \hat{\beta} = X (X^T X)^{-1} X^T Y = H Y$$


转换为向量形式：

$$\sum_{i=1}^{N} \text{Cov}(\hat{y}_i, y_i) = \text{Tr}(\text{Cov}(\hat{Y}, Y))$$

$$\text{Cov}(\hat{Y}, Y) = \text{Cov}(H Y, Y)= H \cdot \text{Cov}(Y)$$

由于 $Y = X\beta + \varepsilon$，且 $X\beta$ 是确定的，所以 $Y$ 的方差只来源于 $\varepsilon$：

$$\text{Cov}(Y) = \text{Cov}(\varepsilon) = \sigma_{\varepsilon}^2 I$$

$$\text{Cov}(\hat{Y}, Y) = H (\sigma_{\varepsilon}^2 I) = \sigma_{\varepsilon}^2 H$$

$$\text{Tr}(\text{Cov}(\hat{Y}, Y)) = \text{Tr}(\sigma_{\varepsilon}^2 H)= \sigma_{\varepsilon}^2 \text{Tr}(H)$$

对于这个H矩阵  $\text{Tr}(H) = X(X^T X)^{-1} X^T= X^TX(X^T X)^{-1}$ 

$$\text{Tr}(H) = d$$


$$\sum_{i=1}^{N} \text{Cov}(\hat{y}_i, y_i) = \sigma_{\varepsilon}^2 d$$

代回乐观性的推导公式 $op = \frac{2}{N} \sum_{i=1}^{N} \text{Cov}(\hat{y}_i, y_i)$：

$$op = \frac{2}{N} d \sigma_{\varepsilon}^2$$



