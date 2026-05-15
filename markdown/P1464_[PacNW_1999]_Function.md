# [每日算法]P1464 [PacNW 1999] Function

## 题目描述

对于一个递归函数 $w(a,b,c)$


- 如果 $a \le 0$ 或 $b \le 0$ 或 $c \le 0$ 就返回值 $1$。
- 如果 $a>20$ 或 $b>20$ 或 $c>20$ 就返回 $w(20,20,20)$
- 如果 $a<b$ 并且 $b<c$ 就返回 $w(a,b,c-1)+w(a,b-1,c-1)-w(a,b-1,c)$。
- 其它的情况就返回 $w(a-1,b,c)+w(a-1,b-1,c)+w(a-1,b,c-1)-w(a-1,b-1,c-1)$


这是个简单的递归函数，但实现起来可能会有些问题。当 $a,b,c$ 均为 $15$ 时，调用的次数将非常的多。你要想个办法才行。

注意：例如 $w(30,-1,0)$ 又满足条件 $1$ 又满足条件 $2$，请按照最上面的条件来算，答案为 $1$。

## 输入格式

会有若干行。

并以 $-1,-1,-1$ 结束。

## 输出格式

输出若干行，每一行格式：

`w(a, b, c) = ans`

注意空格。

## 输入输出样例 #1

### 输入 #1

```
1 1 1
2 2 2
-1 -1 -1
```

### 输出 #1

```
w(1, 1, 1) = 2
w(2, 2, 2) = 4
```

## 说明/提示

### 数据规模与约定

保证输入的数在 $[-9223372036854775808,9223372036854775807]$ 之间，并且是整数。

保证不包括 $-1, -1, -1$ 的输入行数 $T$ 满足 $1 \leq T \leq 10 ^ 5$。

---

# 题解

```cpp

#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
ll dp[21][21][21];
ll w(ll a,ll b,ll c){
    if(a <= 0 || b <= 0 || c <= 0) return 1;
    if(a > 20 || b > 20 || c > 20) return w(20,20,20);
    if(dp[a][b][c] != 0) return dp[a][b][c];
    if(a < b && b < c){
        if(dp[a][b][c-1] == 0) dp[a][b][c-1] = w(a,b,c-1);
        if(dp[a][b-1][c-1] == 0) dp[a][b-1][c-1] = w(a,b-1,c-1);
        if(dp[a][b-1][c] == 0) dp[a][b-1][c] = w(a,b-1,c);

        dp[a][b][c] = dp[a][b][c-1] + dp[a][b-1][c-1] - dp[a][b-1][c];
    }else{
        if(dp[a-1][b][c] == 0) dp[a-1][b][c] = w(a-1,b,c);
        if(dp[a-1][b-1][c] == 0) dp[a-1][b-1][c] = w(a-1,b-1,c);
        if(dp[a-1][b][c-1] == 0) dp[a-1][b][c-1] = w(a-1,b,c-1);
        if(dp[a-1][b-1][c-1] == 0) dp[a-1][b-1][c-1] = w(a-1,b-1,c-1);
        
        dp[a][b][c] = dp[a-1][b][c] + dp[a-1][b-1][c] + dp[a-1][b][c-1] - dp[a-1][b-1][c-1];
    }
    return dp[a][b][c];
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    while(1){
        ll a,b,c;
        cin >> a >> b >> c;
        if(a == -1 && b == -1 && c == -1) break;
        int ans = w(a,b,c);
        cout << "w(" << a << ", " << b << ", " << c << ") = " << ans << endl;
    }

    return 0;
}

```
