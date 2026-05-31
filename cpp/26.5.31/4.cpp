#include<bits/stdc++.h>
using namespace std;
const int N = 1005;
const int max_P = 2*1e4 + 5;
const int mod = 998244353;
vector<pair<int, int>> g[N];
int dp[N][max_P];
int a[N];
int n, m, P;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n >> m >> P;
    for(int i = 1; i <= n; i++){
        cin >> a[i];
        if(a[i] <= P){
            dp[i][a[i]] = 1;
        }
    }

    for(int i = 1; i <= m; i++){
        int u, v, k;
        cin >> u >> v >> k;
        g[u].push_back({v, k});
    }

    for(int w = 1; w <= P; w++){
        for(int u = 1; u <= n; u++){
            if(dp[u][w] == 0) continue;
            for(auto p : g[u]){
                int v = p.first;
                int k = p.second;
                if(w + k <= P){
                    dp[v][w + k] = (dp[v][w+k] + dp[u][w]) % mod;
                }
            }
        }
    }

    for(int i = 1; i <= n; i++){
        int ans = 0;
        for(int w = 1; w <= P; w++){
            ans = (ans + dp[i][w]) % mod;
        }
        cout << ans;
        if(i != n) cout << "\n";
    }

    return 0;
}