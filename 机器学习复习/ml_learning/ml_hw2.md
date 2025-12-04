### 机器学习第二次作业
#### 1. 请给出多层感知器学习的误差反传算法伪代码描述（不需要推到算法）。
通过前向传播计算输出与误差，再反向传播误差以更新各层权重，最终最小化损失函数，伪代码如下：
```plaintext
初始化：随机初始化各层权重W^l和偏置b^l（小范围随机值）
   对t=1到T：
   a. 对每个样本(x, y)：
      i. 前向传播：
         - 输入层：a^0 = x
         - 对各层l=1到L：
             z^l = W^l · a^(l-1) + b^l
             a^l = σ(z^l)
         - 输出层：y_hat = a^L
      ii. 计算输出层误差：δ^L = ∇_z L(y_hat, y)
      iii. 反向传播误差：
           对l=L-1到1：
               δ^l = ( (W^(l+1))^T · δ^(l+1) ) ⊙ σ’(z^l)  （⊙为元素积）
      iv. 更新参数：
           对各层l=1到L：
               W^l = W^l + η · δ^l · (a^(l-1))^T
               b^l = b^l + η · δ^l
   b. 若训练误差收敛，跳出循环
3. 返回{W^l}, {b^l}
```

#### 2. 在神经网络训练时，如何处理梯度消失？
**我经过整理课件，同时结合相关的研究经历和网上查找部分资料，大致整理出如下的几种方法，可能不太全面和详细，但是是比较容易实现的方法：**
- **ReLU函数**：公式为\(f(x)=\max(0,x)\)。
  - 当输入\(x>0\)时，梯度恒为1，无衰减，可直接传递到前层；
  - 仅当\(x≤0\)时梯度为0，但通过合理初始化可减少该问题。
- **ReLU变体**：如Leaky ReLU（输入\(x<0\)时保留小梯度），进一步降低梯度消失概率，同时避免神经元“死亡”。
- **采用深而窄的网络**：
  - 浅层宽网络需学习复杂映射，易导致梯度分散；
  - 深层窄网络通过分层学习简单特征（低→中→高维），梯度传递路径更清晰，衰减幅度更小，参数量也更少。
- **引入残差连接**：
  - 残差连接将前层输出直接传递到后层，梯度可通过该路径直接回传，跳过中间层衰减，据我所知，Transformer使用了大量的残差连接。
- **合理初始化权重**：
  - 避免初始权重过小（如随机小值），否则前层输入经权重相乘后会逐渐变小，导致后续层激活值趋近于0，梯度随之消失；
- **使用权重动量**：
  - 在梯度下降中加入动量项\(\alpha\)，公式为\(W_{new} = W_{old} + \eta\delta X + \alpha(W_{old} - W_{older})\)；
  - 动量项可累积前几轮的梯度方向，减少梯度波动，即使梯度较小也能持续更新，间接缓解梯度消失导致的“更新停滞”。

#### 3. 请调研神经网络学习的正则化方法（三种以上），并给出相应的参考文献。
正则化是用于解决神经网络过拟合问题，增强模型泛化能力的核心技术，我主要调研了五种正则化方法，

---

##### 1. $L_2$ 正则化

通过惩罚大的权重值，促使模型学习到更小、更分散的权重，从而简化模型，降低对训练数据噪声的敏感度。
在损失函数 $J(\theta)$ 中加入所有权重平方和的惩罚项：$$\text{新的损失} = J(\theta) + \frac{\lambda}{2} \sum_{w \in \mathbf{W}} w^2$$ 
在梯度下降时，权重会以固定的比例衰减（收缩），避免权重过大。 

* **Goodfellow, I., Bengio, Y., & Courville, A. (2016).** *Deep Learning* (Chapter 7: Regularization for Deep Learning). MIT Press.

##### 2. Dropout（随机失活）
在训练过程中，以概率 $p$ 随机暂时性地忽略（失活）网络中的一部分神经元，及其连接。
每次前向传播时，随机将部分神经元的输出设为零。失活的神经元不参与反向传播。
阻止神经元之间形成复杂的**“共适应”**（Co-adaptation）。迫使每个神经元学习更鲁棒的特征，因为它们不能依赖特定的其他神经元。相当于训练了大量稀疏子网络的集成。

**参考文献：**

* **Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014).** **Dropout: A Simple Way to Prevent Neural Networks from Overfitting.** *Journal of Machine Learning Research, 15*(1), 1929-1958.

##### 3. Early Stopping（提前停止）
停止训练的最佳时机，是在模型在验证集上的性能开始恶化（即开始过拟合）时。
训练时监控验证集损失。设置一个“耐心”（Patience）阈值 $N$。一旦验证损失连续 $N$ 个 Epoch 没有下降（或开始上升），则停止训练，并使用验证损失最低时的模型权重。
避免模型对训练数据的过度拟合，是一种高效且几乎没有额外计算成本的“隐式”正则化。

**参考文献：**

* **Prechelt, L. (1998).** *Early stopping—but when?* In *Neural Networks: Tricks of the Trade* (pp. 55-69). Springer.


##### 4. 数据增强（Data Augmentation）

通过人为地对训练样本进行变换，生成新的训练样本，从而有效地扩大训练集规模。
随机裁剪、翻转、旋转、色彩抖动等。**文本：** 随机替换同义词、回译（先译成另一种语言再译回）。
增加了模型学习的数据多样性，使其更关注那些具有不变性（如物体在图像中平移或旋转后仍是同一物体）的特征，显著降低了过拟合风险。 

**参考文献：**

* **Simard, P. Y., Steinkraus, D., & Platt, J. C. (2002).** *Best practices for convolutional neural networks applied to visual document analysis.* In *Seventh International Conference on Document Analysis and Recognition*. (关于图像数据增强的早期实践。)

##### 5. 批量归一化（Batch Normalization, BN）

稳定每层网络的输入分布，并引入一个正则项。
在激活函数之前，对 mini-batch 的输入进行归一化（使其均值为 0，方差为 1），并引入可学习的缩放 ($\gamma$) 和平移 ($\beta$) 参数。
    解决了内部协变量偏移问题，允许使用更高的学习率。BN 在每个 mini-batch 上计算统计量时引入了**随机噪声**（每个 mini-batch 的均值和方差略有不同）。这种噪声具有轻微的正则化效果，类似于 Dropout，可以略微减少对 Dropout 的需求。

**参考文献：**

* **Ioffe, S., & Szegedy, C. (2015).** **Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift.** *Proceedings of the 32nd International Conference on Machine Learning, 37*, 448-456.*

