#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 25;

ll dp[N][N];
int a[N];

ll dfs(int pos, int last, bool lead, bool limit){
    if(pos == 0) return 1;
    if(!lead && !limit && dp[pos][last] != -1) return dp[pos][last];
    int up = limit ? a[pos] : 9;
    bool x = last % 2;
    ll ans = 0;
    for(int i = 0; i <= up; i++){
        bool y = i % 2;
        if(!lead && x == y) continue;
        if(lead && i == 0)  ans += dfs(pos-1, 1, 1, limit && (i == up));
        else ans += dfs(pos-1, i, 0, limit && (i == up));
    }
    if(!lead && !limit) dp[pos][last] = ans;
    return ans;
}

bool check(ll x, ll target){
    int len = 0;
    ll xx = x;
    while(xx > 0){
        a[++len] = xx % 10;
        xx /= 10;
    }
    
    return (dfs(len,1,1,1) - 10) >= target;
}

ll solve(ll x){
    memset(dp,-1,sizeof(dp));
    ll l = 10, r = 4e18;
    int ans = -1;
    while(l <= r){
        ll mid = l + (r - l) / 2;
        if(check(mid, x)){
            ans = mid;
            r = mid-1;
        }else {
            l = mid+1;
        }
    }
    return ans;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    ll n;
    cin >> n;
    cout << solve(n);
    return 0;
}