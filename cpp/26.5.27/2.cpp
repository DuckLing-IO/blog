#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 15;
ll dp[N][N];
int a[N];

ll dfs(int pos, int last, bool lead, bool limit){
    if(pos == 0) return 1;
    if(!lead && !limit && dp[pos][last] != -1) return dp[pos][last];
    ll ans = 0;
    int up = (limit ? a[pos] : 9);
    for(int i = 0; i <= up; i++){
        if(abs(i - last) < 2) continue;
        if(lead && i == 0) ans += dfs(pos-1, -2, 1, limit && (i == up));
        else ans += dfs(pos-1, i, 0, limit && (i == up));
    }
    if(!lead && !limit) dp[pos][last] = ans;
    return ans;
}

ll solve(int x){
    int len = 0;
    while(x > 0){
        a[++len] = x % 10;
        x /= 10;
    }
    memset(dp,-1,sizeof(dp));
    return dfs(len, -2, 1, 1);
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    ll a,b;
    cin >> a >> b;
    cout << solve(b) - solve(a-1);
    return 0;
}