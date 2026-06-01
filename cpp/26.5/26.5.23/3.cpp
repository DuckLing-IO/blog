#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 20;
int n,k;
ll a[N], dp[N][N][N];
int main(){
    cin >> n >> k;
    for(int i = 1; i <= n; i++){
        cin >> a[i];
    }
    memset(dp,-1,sizeof(dp));
    for(int i = 1; i <= n; i++){
        dp[i][i][0] = a[i];
    }
    for(int len = 2; len <= n; len++){
        for(int i = 1; i+len-1 <= n; i++){
            int j = i+len-1;
            for(int m = 0; m <= k; m++){
                if(m > j-i) continue;
                ll  ma = -1;
                for(int cut = i; cut < j; cut++){
                    //情况1
                    for(int m1 = 0; m1 <= m; m1++){
                        int m2 = m - m1;
                        if(dp[i][cut][m1] != -1 && dp[cut+1][j][m2] != -1){
                            ma = max(ma, dp[i][cut][m1] + dp[cut+1][j][m2]);
                        }
                    }
                    //情况2
                    for(int m1 = 0; m1 < m; m1++){
                        int m2 = m - m1 - 1;
                        if(dp[i][cut][m1] != -1 && dp[cut+1][j][m2] != -1){
                            ma = max(ma, dp[i][cut][m1] * dp[cut+1][j][m2]);
                        }
                    }
                }   
                dp[i][j][m] = ma;
            }
        }
    }

    cout << dp[1][n][k];
    return 0;
}