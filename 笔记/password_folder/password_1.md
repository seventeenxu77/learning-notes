#### 第一次课后作业
#### 1（a)
$$
\pi^{-1} = \begin{pmatrix}
1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 \\
2 & 4 & 6 & 1 & 8 & 3 & 5 & 7
\end{pmatrix}
$$
即答案为24618357
#### 1（b)
按照8个为一组进行解密：
第一组：G E N T L E M E
第二组：N D O N O T R E
第三组：A D E A C H O T
第四组：H E R S M A I L
即为：GENTLEMEN DONOT READ EACH OTHERS MAIL

#### 2（a)

------------假设 $\pi^2 = \mathrm{id}$，证明 $\forall i,\ \pi(i) = j \implies \pi(j) = i$

设 $\pi(i) = j$，其中 $i, j \in \{1,\dots,m\}$。  
对等式两边应用 $\pi$：
\[
\pi(j) = \pi(\pi(i)) = \pi^2(i)
\]
由于 $\pi^2 = \mathrm{id}$，有 $\pi^2(i) = i$，因此：
\[
\pi(j) = i
\]

------------假设 $\forall i,\ \pi(i) = j \implies \pi(j) = i$，证明 $\pi^2 = \mathrm{id}$

需证对任意 $i \in \{1,\dots,m\}$，有 $\pi^2(i) = i$。  

令 $j = \pi(i)$，由假设条件（取该 $i$ 对应的 $j$）可知：
\[
\pi(j) = i
\]
但 $j = \pi(i)$，代入得：
\[
\pi(\pi(i)) = i
\]
即 $\pi^2(i) = i$ 对任意 $i$ 成立，所以 $\pi^2 = \mathrm{id}$。

##### 即证明了充分必要条件

#### 2（a)

对合置换是满足 \(\pi^2 = \text{id}\) 的置换，即每个轮换的长度只能是 1（不动点）或 2（对换）。

递推公式：
\[
I(m) = I(m-1) + (m-1) \cdot I(m-2), \quad I(0)=1, \ I(1)=1
\]


- \(I(2) = I(1) + 1 \cdot I(0) = 1 + 1 \cdot 1 = 2\)
- \(I(3) = I(2) + 2 \cdot I(1) = 2 + 2 \cdot 1 = 4\)
- \(I(4) = I(3) + 3 \cdot I(2) = 4 + 3 \cdot 2 = 10\)
- \(I(5) = I(4) + 4 \cdot I(3) = 10 + 4 \cdot 4 = 26\)
- \(I(6) = I(5) + 5 \cdot I(4) = 26 + 5 \cdot 10 = 76\)


1. **\(m=2\)**  
   对合置换个数：2  
   例子：\(\pi = (1)(2)\)（恒等置换）或 \(\pi = (1\ 2)\)  
   取 \(\pi = \begin{pmatrix}1 & 2 \\ 2 & 1\end{pmatrix}\)，即 \(\pi(1)=2, \pi(2)=1\)

2. **\(m=3\)**  
   对合置换个数：4  
   例子：\(\pi = (1)(2)(3)\)（恒等）或 \((1\ 2)(3)\) 等  
   取 \(\pi = \begin{pmatrix}1 & 2 & 3 \\ 2 & 1 & 3\end{pmatrix}\)，即 \(\pi(1)=2, \pi(2)=1, \pi(3)=3\)

3. **\(m=4\)**  
   对合置换个数：10  
   例子：取 \(\pi = \begin{pmatrix}1 & 2 & 3 & 4 \\ 2 & 1 & 4 & 3\end{pmatrix}\)，即两个对换 \((1\ 2)(3\ 4)\)

4. **\(m=5\)**  
   对合置换个数：26  
   例子：取 \(\pi = \begin{pmatrix}1 & 2 & 3 & 4 & 5 \\ 2 & 1 & 4 & 3 & 5\end{pmatrix}\)，即 \((1\ 2)(3\ 4)(5)\)

5. **\(m=6\)**  
   对合置换个数：76  
   例子：取 \(\pi = \begin{pmatrix}1 & 2 & 3 & 4 & 5 & 6 \\ 2 & 1 & 4 & 3 & 6 & 5\end{pmatrix}\)，即 \((1\ 2)(3\ 4)(5\ 6)\)

#### 3

明文：`breathtaking` → 数字序列：  
  `[1, 17, 4, 0, 19, 7, 19, 0, 10, 8, 13, 6]`
密文：`RUPOTENTOIFV` → 数字序列：  
  `[17, 20, 15, 14, 19, 4, 13, 19, 14, 8, 5, 21]`
共12个字母，可能维度为2,3,4,6,12(这里不考虑4，6，12，因为无法求逆)，只考虑2,3



##### 假设m=2：
明文矩阵 \(P\)（列向量）：
\[
P = \begin{pmatrix}1 & 4 \\ 17 & 0\end{pmatrix}
\]
密文矩阵 \(C\)：
\[
C = \begin{pmatrix}17 & 15 \\ 20 & 14\end{pmatrix}
\]

\[
\det(P) = 1\cdot0 - 4\cdot17 = -68 \equiv 10 \pmod{26}
\]
gcd(10,26)=2 ≠1 → \(P\) 在模26下不可逆，无法求解唯一 \(K\)。

舍弃m=2。



##### 假设m=3：

\[
P = \begin{pmatrix}
1 & 0 & 19 \\
17 & 19 & 0 \\
4 & 7 & 10
\end{pmatrix}, \quad
C = \begin{pmatrix}
17 & 14 & 13 \\
20 & 19 & 19 \\
15 & 4 & 14
\end{pmatrix}
\]

\[
\det(P) = 1007 \equiv 19 \pmod{26}
\]
gcd(19,26)=1 → 可逆。  
逆元：\(19^{-1} \equiv 11 \pmod{26}\)


余子式矩阵转置后乘11模26：
\[
P^{-1} \equiv \begin{pmatrix}
10 & 7 & 7 \\
2 & 2 & 17 \\
5 & 1 & 1
\end{pmatrix} \pmod{26}
\]

 \(K = C P^{-1} \mod 26\)
\[
K \equiv \begin{pmatrix}
3 & 4 & 6 \\
21 & 15 & 14 \\
20 & 23 & 5
\end{pmatrix} \pmod{26}
\]

- 分组1：\(K \cdot (1,17,4)^T \equiv (17,20,15)^T\) 
- 分组2：\(K \cdot (0,19,7)^T \equiv (14,19,4)^T\) 
- 分组3：\(K \cdot (19,0,10)^T \equiv (13,19,14)^T\) 
- 分组4：\(K \cdot (8,13,6)^T \equiv (8,5,21)^T\) 

全部匹配，说明m=3是维度。

K：
\[
\boxed{\begin{pmatrix}
3 & 4 & 6 \\
21 & 15 & 14 \\
20 & 23 & 5
\end{pmatrix}}
\]
