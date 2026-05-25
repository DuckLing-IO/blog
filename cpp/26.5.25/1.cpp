#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 105;
const int MOD = 1000000007;
int dp[N][N][N];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    int n,m;
    cin >> n >> m;
    dp[0][0][2] = 1;
    for(int i = 0; i <= n; i++){
        for(int j = 0; j <= m; j++){
            if(!i && !j) continue;
            for(int k = 0; k <= m; k++){
                if(k%2 == 0 && i) dp[i][j][k] += dp[i-1][j][k/2];
                if(j) dp[i][j][k] += dp[i][j-1][k+1];
                dp[i][j][k] %= MOD;
            }
        }
    }
    cout << dp[n][m-1][1] % MOD;
    return 0;
}