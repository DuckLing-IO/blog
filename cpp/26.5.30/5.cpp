#include<bits/stdc++.h>
using namespace std;
const int N = 1e5;
typedef long long ll;
ll n, m;
const int mod = 998244353;
void solve(){
    cin >> n >> m;
    ll ans = 1;
    vector<int> f(n+1, 0);
    for(int i = 1; i <= n; i++){
        int a;
        cin >> a;
        ll c = m - f[a];
        if(c < 0) c = 0;
        ans = (ans * c) % mod;
        f[a] ++;
        cout << ans << (i == n ? "" : " ");
    }
}


int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int T;
    cin >> T;
    while(T--){
        solve();
        if(T != 0) cout << "\n";
    }
    return 0;
}