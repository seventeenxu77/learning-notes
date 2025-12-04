### 机器学习第六次作业
---
##### 1. 设随机变量服从高斯分布\( z \propto N(\theta, 1) \)，参数\( \theta \)的先验分布为\( \theta \propto N(0, \tau) \)。估计后验概率\( p(\theta \mid z) \)，并讨论其方差与先验方差的大小关系。

---

$$p(z \mid \theta) = N(z \mid \theta, 1) = \frac{1}{\sqrt{2\pi}} \exp\left(-\frac{1}{2}(z - \theta)^2\right)$$

 $$p(\theta) = N(\theta \mid 0, \tau^2) = \frac{1}{\sqrt{2\pi\tau^2}} \exp\left(-\frac{1}{2\tau^2}\theta^2\right)$$

根据贝叶斯定理，由于p(z)在问题里面是归一化系数，所以这里只写了正比的形式。
$$p(\theta \mid z) \propto p(z \mid \theta) p(\theta)$$

$$p(\theta \mid z) \propto \exp\left(-\frac{1}{2}(z - \theta)^2\right) \exp\left(-\frac{1}{2\tau^2}\theta^2\right)$$

$$p(\theta \mid z) \propto \exp\left(-\frac{1}{2} \left[ (z - \theta)^2 + \frac{1}{\tau^2}\theta^2 \right] \right)$$

指数项中的二次项，整理为$\theta$ 的二次形式

$$\begin{aligned}
&= \left(1 + \frac{1}{\tau^2}\right)\theta^2 - 2z\theta + z^2
\end{aligned}$$


假设 $p(\theta \mid z)$ 是高斯分布 $N(\theta \mid \theta_{post}, \sigma_{post}^2)$，则指数项形式是：
$$-\frac{1}{2\sigma_{post}^2} (\theta - \theta_{post})^2 = -\frac{1}{2\sigma_{post}^2} \left( \theta^2 - 2\theta_{post}\theta + \theta_{post}^2 \right)$$

比较系数则：
    $$\sigma_{post}^2 = \frac{\tau^2}{\tau^2 + 1}$$
    $$\theta_{post} = z \cdot \left(\frac{\tau^2}{\tau^2 + 1}\right) = \frac{\tau^2}{\tau^2 + 1} z$$

则后验分布 $p(\theta \mid z)$ 仍然是高斯分布：

$$p(\theta \mid z) = N\left(\theta \mid \frac{\tau^2}{\tau^2 + 1} z, \frac{\tau^2}{\tau^2 + 1}\right)$$



比较 $\sigma_{post}^2$ 和 $\sigma_{prior}^2$：

$$\sigma_{post}^2 - \sigma_{prior}^2 = \frac{\tau^2}{\tau^2 + 1} - \tau^2  = -\frac{\tau^4}{\tau^2 + 1}$$


---
##### 2. 设假设空间\( H \)是有限的，已知对于任意\( h \in H \)，满足一下条件
$$p\left(|\varepsilon(h) - \hat{\varepsilon}(h)| > \varepsilon\right) \leq \delta.$$
请给出以下泛化误差估计式 \( \varepsilon(\hat{h}) - \varepsilon(h^*) \leq 2\varepsilon \) 的置信概率的估计
$$p\left(\varepsilon(\hat{h}) - \varepsilon(h^*) \leq 2\varepsilon\right)$$
记号参见课件 PPT

---


3.  
由于
$$P(|\varepsilon(h) - \hat{\varepsilon}(h)| > \varepsilon) \leq \delta$$
通过并查集，同时考虑到到均匀收敛，以及在训练集上经验误差最小化的假设$\hat{h}$误差一定不会大于最优假设$h^*$的经验误差，所以有：
$$P \left( \exists h \in H \text{ such that } |\varepsilon(h) - \hat{\varepsilon}(h)| > \varepsilon \right) \leq $$

$$\sum_{i=1}^k P(|\varepsilon(h_i) - \hat{\varepsilon}(h_i)| > \varepsilon) \leq k \cdot \delta$$

$$P \left( \forall h \in H, |\varepsilon(h) - \hat{\varepsilon}(h)| \leq \varepsilon \right) \geq 1 - \delta$$


$$\begin{aligned} \varepsilon(\hat{h}) &\leq \hat{\varepsilon}(\hat{h}) + \varepsilon &  \\ &\leq \hat{\varepsilon}(h^*) + \varepsilon & \\ &\leq (\varepsilon(h^*) + \varepsilon) + \varepsilon & \\ &= \varepsilon(h^*) + 2\varepsilon \end{aligned}$$

这个条件是均匀收敛所以和上面的$\delta$是一致的



$$P \left( \varepsilon(\hat{h}) - \varepsilon(h^*) \leq 2\varepsilon \right) = P \left( \forall h \in H, |\varepsilon(h) - \hat{\varepsilon}(h)| \leq \varepsilon \right)$$
所以

$$P \left( \varepsilon(\hat{h}) - \varepsilon(h^*) \leq 2\varepsilon \right) \geq 1 - \delta$$


$P \left( \exists h \in H \text{ such that } |\varepsilon(h) - \hat{\varepsilon}(h)| > \varepsilon \right) \leq |H| \delta$

由于不知道训练集最佳假设的形式，所以在整个假设空间里面并查集，得到一个下界，则 $ \varepsilon(\hat{h}) - \varepsilon(h^*) \leq 2\varepsilon$ 成立的概率估计为：

$$P \left( \varepsilon(\hat{h}) - \varepsilon(h^*) \leq 2\varepsilon \right) \geq 1 - |H| \delta$$

