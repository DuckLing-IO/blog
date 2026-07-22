#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 1e5+5;
ll n, m;
ll a[N];

bool check(ll x){
    ll cnt = 0;
    for(int i = 1; i <= n; i++){
        ll l = a[i];
        cnt += (a[i] - 1) / x;
    }
    return cnt <= m+1;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n >> m;
    ll la = 0;
    for(int i = 1; i <= n; i++){
        ll no = 0;
        cin >> no;
        a[i] = no - la;
        la = no;
    }
    ll l = 1ll;
    ll r = la;
    ll ans = 0;
    while(l <= r){
        ll mid = (l + r) >> 1;
        if(check(mid)){
            ans = mid;
            r = mid -1;
        }else{
            l = mid + 1;
        }
    }
    cout << ans;
    return 0;
}