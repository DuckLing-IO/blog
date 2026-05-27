#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    ll n;
    cin >> n;
    ll x;
    cin >> x;
    ll ans = 0;
    ll cnt = 0;
    for(int i = 2; i <= n; i++){
        ll y;
        cin >> y;
        if(x > y){
            ll c = y;
            while(x > c){
                c *= 2;
                cnt ++;
            }
        }else if(x < y){
            ll c = x;
            while(y > c * 2){
                c *= 2;
                cnt --;
                cnt = max(ll(0),cnt);
            }
        }
        ans += cnt;
        x = y;
    }
    cout << ans;
    return 0;
}