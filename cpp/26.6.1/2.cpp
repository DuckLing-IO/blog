#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll mod = 1000000007;
const int N = 1e5 + 5;

ll fact[N];
ll invFact[N];

ll q_pow(ll x, ll esp){
    ll res = 1;
    x %= mod;
    while(esp > 0){
        if(esp & 1) res = (res * x) % mod;
        x = (x * x) % mod;
        esp >>= 1;
    }
    return res;
}

ll ny(ll x){
    return q_pow(x, mod-2);
}

void init(){
    fact[0] = invFact[0] = 1;
    for(int i = 1; i <= N-1; i++){
        fact[i] = (fact[i-1] * i) % mod;
    }
    invFact[N-1] = ny(fact[N-1]);
    for(int i = N-2; i >= 1; i--){
        invFact[i] = (invFact[i+1] * (i+1)) % mod;
    }
}

ll C(ll n, ll k){
    if(k < 0 || k > n) return 0;
    ll nn = fact[n];
    ll kk = (invFact[k] * invFact[n-k]) % mod;
    return (nn * kk) % mod;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    init();
    
    return 0;
}