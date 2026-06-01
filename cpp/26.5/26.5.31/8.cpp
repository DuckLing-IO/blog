#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

ll f(ll x){
    ll res = 0;
    if(x == 0) return 0ll;
    while(x > 0){
        res = (res << 1) | (x & 1);
        x >>= 1;
    }
    return res;
}
int n, m;
ll dp[1005][1005][2];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n >> m;
    vector<ll> a(n+1);
    vector<ll> d(n+1);
    ll sum = 0;
    for(int i = 1; i <= n; i++){
        ll x;
        cin >> x;
        a[i] = x;
        d[i] = f(x) - x;
        sum += x;
    }
    for(int i = 0; i <= n; i++){
        for(int j = 0; j <= m; j++){
            dp[i][j][0] = LLONG_MIN;
            dp[i][j][1] = LLONG_MIN;
        }
    }
    for(int i = 0; i <= n; i++){
        dp[i][0][0] = 0;
    }
    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= m; j++){
            dp[i][j][0] = max(dp[i-1][j][0], dp[i-1][j][1]);
            
            dp[i][j][1] = max(dp[i-1][j][1], max(dp[i-1][j-1][0], dp[i-1][j-1][1]));
            if(dp[i][j][1] != LLONG_MIN)
            dp[i][j][1] += d[i];
        }
    }

    ll ans = LLONG_MIN;
    for(int j = 0; j <= m; j++){
        ans = max(ans, max(dp[n][j][1], dp[n][j][0]));
    }
    cout << sum + ans;
    return 0;
}