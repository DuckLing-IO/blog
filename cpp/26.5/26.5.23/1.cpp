#include<bits/stdc++.h>
using namespace std;
const int N = 205;
int n;
int dp1[N][N], dp2[N][N], a[N], sum[N];

void f1(){
    for(int len = 2; len <= n; len++){
        for(int i = 1, j = i+len-1; j <= 2*n; i++,j++){
            dp1[i][j] = INT_MAX;
            dp2[i][j] = INT_MIN;
            for(int k = i; k < j; k++){
                dp1[i][j] = min(dp1[i][j], dp1[i][k] + dp1[k+1][j] + sum[j]-sum[i-1]);
                dp2[i][j] = max(dp2[i][j], dp2[i][k] + dp2[k+1][j] + sum[j]-sum[i-1]);
            }
        }
    }
}

int main(){
    cin >> n;
    for(int i = 1; i <= n; i++){
        int x;
        cin >> x;
        a[i] = x;
        a[n+i] = x;
    }

    for(int i = 1; i <= 2*n; i++){
        sum[i] = sum[i-1] + a[i];
    }
    
    f1();

    int ans1 = INT_MAX;
    int ans2 = INT_MIN;
    for(int i = 1; i <= n; i++){
        ans1 = min(ans1, dp1[i][i+n-1]);
        ans2 = max(ans2, dp2[i][i+n-1]);
    }
    cout << ans1 << "\n" << ans2;
}