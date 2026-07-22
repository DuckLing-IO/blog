#include <iostream>
#include <vector>

using namespace std;

// 使用 long long 防止乘法过程中的数值溢出
typedef long long ll;

const int MOD = 998244353;
const int N = 341799;

// w[0] = 21 (辅音的数量), w[1] = 5 (元音的数量)
const int w[2] = {21, 5}; 

// dp[i][j][k] 
// i: 当前链的长度
// j: 链表头的状态 (0为辅音, 1为元音)
// k: 链表尾(当前第i个圆)的状态 (0为辅音, 1为元音)
ll dp[N + 5][2][2];

int main() {
    // 优化输入输出流速度
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    // 1. 初始化 DP 数组：长度为 1 的链
    for (int i = 0; i <= 1; ++i) {
        dp[1][i][i] = w[i];
    }

    // 2. 线性 DP 预处理长链
    for (int i = 2; i <= N; ++i) {
        for (int head = 0; head <= 1; ++head) {         // 枚举链表头的状态
            for (int curr = 0; curr <= 1; ++curr) {     // 枚举当前第 i 个圆的状态
                for (int prev = 0; prev <= 1; ++prev) { // 枚举前一个圆(i-1)的状态
                    
                    // 相邻的两个圆不能都是元音 (状态 1)
                    if (!(prev == 1 && curr == 1)) {
                        dp[i][head][curr] = (dp[i][head][curr] + dp[i - 1][head][prev] * w[curr]) % MOD;
                    }
                }
            }
        }
    }

    ll total_result = 0;

    // 3. 枚举第二列(a, b)和第四列(c, d)这 4 个“桥梁”位置的状态
    // 0 代表填辅音，1 代表填元音
    for (int a = 0; a <= 1; ++a) {
        for (int b = 0; b <= 1; ++b) {
            for (int c = 0; c <= 1; ++c) {
                for (int d = 0; d <= 1; ++d) {
                    
                    ll w1_ways = 0; // 第一列的合法方案数
                    ll w2_ways = 0; // 第三列的合法方案数
                    ll w3_ways = 0; // 第五列的合法方案数

                    // 枚举第一、三、五列长链的 头(head) 和 尾(tail) 状态
                    for (int head = 0; head <= 1; ++head) {
                        for (int tail = 0; tail <= 1; ++tail) {
                            
                            ll current_chain_ways = dp[N][head][tail];

                            // 判断是否与相邻的“桥梁”发生元音冲突
                            // 第一列只和 a, b 相邻
                            bool valid_col1 = !(head == 1 && a == 1) && !(tail == 1 && b == 1);
                            // 第五列只和 c, d 相邻
                            bool valid_col5 = !(head == 1 && c == 1) && !(tail == 1 && d == 1);

                            // 如果第一列合法，累加方案数
                            if (valid_col1) {
                                w1_ways = (w1_ways + current_chain_ways) % MOD;
                            }
                            
                            // 第三列被夹在中间，必须同时和左右两边都不冲突
                            if (valid_col1 && valid_col5) {
                                w2_ways = (w2_ways + current_chain_ways) % MOD;
                            }
                            
                            // 如果第五列合法，累加方案数
                            if (valid_col5) {
                                w3_ways = (w3_ways + current_chain_ways) % MOD;
                            }
                        }
                    }

                    // 4. 根据乘法原理合并当前桥梁状态下的总方案数
                    // 总方案 = 列1 * 列3 * 列5 * a的选择数 * b的选择数 * c的选择数 * d的选择数
                    ll current_combo = 1;
                    current_combo = (current_combo * w1_ways) % MOD;
                    current_combo = (current_combo * w2_ways) % MOD;
                    current_combo = (current_combo * w3_ways) % MOD;
                    current_combo = (current_combo * w[a]) % MOD;
                    current_combo = (current_combo * w[b]) % MOD;
                    current_combo = (current_combo * w[c]) % MOD;
                    current_combo = (current_combo * w[d]) % MOD;

                    total_result = (total_result + current_combo) % MOD;
                }
            }
        }
    }

    cout << total_result << "\n";
    return 0;
}