#### 第八次课后作业
---
1. 构建参数n=143的RSA公钥密码系统：
--如果公钥e=7,私钥d=?
--对消息m=10加密，密文是什么？
--考虑对ASCII码的文档加密,你会如何规定相应的消息预处理,使得针对整数的RSA加密适合对字符串的加密？

---

>1.
$$143 = 11 \times 13$$

$$\phi(n) = (p-1)(q-1) = (11-1)(13-1) = 10 \times 12 = 120$$


$$\begin{array}{l}
120 = 17 \cdot 7 + 1 \\
1 = 120 - 17 \cdot 7
\end{array}$$

则 $1 = 7 \cdot (-17) + 120 \cdot 1$， $d$ 的一个解是 $-17$。

换成正整数：
$$d = -17 + 120 = 103$$

则 $d = 103$



>2.
$$C = 10^7 \pmod{143}$$

计算出密文为10

>3.
按照字符流的手段，首先将所有字符按照8位ASCII码转换，随后每7位编码为一个大整数，使用RSA加密，最后将加密后的整数分组传出给接收者，接收者反向解密，然后拼接所有ASCELL码，反向转换为字符的形式即可。


---

2*. 在RSA体制中,证明$M^{ed} \equiv M \mod n$


---




M和n有可能互素，有可能不是，有两种情况。

1. 情况一：$\gcd(M, n) = 1$

$$\begin{aligned}
M^{ed} &= M^{k \cdot \phi(n) + 1} \\
&= M^{k \cdot \phi(n)} \cdot M^1 \\
&= (M^{\phi(n)})^k \cdot M \end{aligned}$$

$M^{\phi(n)} \equiv 1 \pmod{n}$。代入上式：

$$M^{ed} \equiv (1)^k \cdot M \equiv M \pmod{n}$$


---

情况二：$\gcd(M, n) \neq 1$

只需假设p|M，另一个情况q整除类似处理。

如果 $p \mid M$，则 $M \equiv 0 \pmod{p}$。则分别证明：
$$M^{ed} \equiv M \pmod{p} \quad \text{和} \quad M^{ed} \equiv M \pmod{q}$$

模p部分：

因为 $p \mid M$，所以 $M \equiv 0 \pmod{p}$。

$$M^{ed} \equiv 0^{ed} \equiv 0 \pmod{p}$$

则 $$M^{ed} \equiv M \pmod{p}$$

模q部分：

因为 $p \mid M$ 且 $p \neq q$，所以 $q$ 不整除 $M$，即 $\gcd(M, q) = 1$。

就是和第一种情况相似处理可以证明。

根据中国剩余定理则

$$\begin{cases} M^{ed} \equiv M \pmod{p} \\ M^{ed} \equiv M \pmod{q} \end{cases}$$

且 $\gcd(p, q) = 1$ 这两个同余关系可以合并为一个关于 $n=pq$ 的同余关系：

$$M^{ed} \equiv M \pmod{n}$$

---