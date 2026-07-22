#include <bits/stdc++.h>
using namespace std;

using ll = long long;

void solve() {
    int n, m, k;
    cin >> n >> m >> k;

    int total = n * m;
    int ma = (total + 1) / 2;

    if (k > ma) {
        cout << "No\n";
        return;
    }

    if (n >= 2 && m >= 2 && k == 0) {
        cout << "No\n";
        return;
    }

    vector<string> grid(n, string(m, '0'));

    // 只有一行或一列，不存在 2×2
    if (n == 1 || m == 1) {
        for (int pos = 0; pos < total && k > 0; pos += 2) {
            int x = pos / m;
            int y = pos % m;
            grid[x][y] = '1';
            k--;
        }

        cout << "Yes\n";

        for (const auto &row : grid) {
            cout << row << '\n';
        }

        return;
    }

    int rowCount = n / 2;
    int colCount = m / 2;
    int mi = rowCount * colCount;

    // 基础构造，共有 mi 个孤立连通块
    for (int i = 1; i < n; i += 2) {
        for (int j = 1; j < m; j += 2) {
            grid[i][j] = '1';
        }
    }

    if (k >= mi) {
        // 增加孤立的 1，每增加一个，连通块数量加 1
        int need = k - mi;

        for (int i = 0; i < n && need > 0; i += 2) {
            for (int j = 0; j < m && need > 0; j += 2) {
                grid[i][j] = '1';
                need--;
            }
        }
    } else {
        // 每次操作恰好合并两个连通块
        int need = mi - k;

        // 先横向连接第一排连通块
        for (int j = 3; j < m && need > 0; j += 2) {
            grid[0][j - 2] = '1';
            grid[0][j - 1] = '1';
            grid[0][j] = '1';
            need--;
        }

        // 再把下面各排的连通块逐个连接上来
        for (int i = 3; i < n && need > 0; i += 2) {
            for (int j = 1; j < m && need > 0; j += 2) {
                grid[i - 1][j] = '1';
                need--;
            }
        }
    }

    cout << "Yes\n";

    for (const auto &row : grid) {
        cout << row << '\n';
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();

    return 0;
}