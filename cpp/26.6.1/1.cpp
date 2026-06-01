#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll mod = 1000000007;
const int N = 1e5 + 5;
ll fact[N];
ll invFact[N];
int d[N];
ll l, r;
ll q_pow(ll x, ll exp){
    ll res = 1;
    x %= mod;
    while(exp > 0){
        if(exp % 2 == 1) res = (res * x) % mod;
        x = (x * x) % mod;
        exp >>= 1;
    }
    return res;
}

ll ny(ll x){
    return q_pow(x, mod-2);
}

void init(){
    fact[0] = 1;
    invFact[0] = 1;
    for(int i = 1; i <= N-1; i++){
        fact[i] = (fact[i-1] * i) % mod;
    }
    invFact[N-1] = ny(fact[N-1]);
    for(int i = N-2; i >= 1; --i){
        invFact[i] = (invFact[i+1] * (i+1)) % mod;
    }
}

ll C(ll n, ll k){
    if(k < 0 || k > n) return 0;
    ll num = fact[n];
    ll den = (invFact[k] * invFact[n - k]) % mod;
    return (num * den) % mod;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    ll n;
    cin >> n;
    for(int i = 1; i <= n-1; i++){
        int u, v;
        cin >> u >> v;
        d[u] ++;
        d[v] ++;
    }
    cin >> l >> r;
    ll ans = 0;
    init();
    if(l <= 1 && r >= 1){
        ans = (ans + n) % mod;
    }
    if(l <= 2 && r >= 2){
        ans = (ans + n-1) % mod;
    }
    ll st = max(3ll, l); 
    for(int i = 1; i <= n; i++){
        ll dd = d[i];
        ll en = min(r, dd+1);
        for(ll k = st; k <= en; k++){
            ans = (ans + C(dd, k-1)) % mod;
        }
    }
    cout << ans;
    return 0;
}
