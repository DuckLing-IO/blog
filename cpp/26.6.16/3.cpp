#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll N = 1e9 + 5;

ll n;
ll d;
ll ans;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n >> d;
    map<ll, ll> diff;
    for(int i = 1; i <= n; i++){
        ll s, t;
        cin >> s >> t;
        ll l = s;
        ll r = t - d;
        if(l <= r){
            diff[l] ++;
            diff[r+1] --;
        }
    }
    ll lat = -1;
    ll num = 0ll;
    ll ans = 0ll;
    for(auto&[x, change] : diff){
        if(lat != -1){
            ll len = x - lat;
            ll c = num * (num-1) / 2;
            ans += len * c;
        }
        lat = x;
        num += change;
    }
    cout << ans;
    return 0;
}