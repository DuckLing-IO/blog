#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    ll n;
    cin >> n;
    if(n == 0) return 0;
    ll x = 0;
    ll ans = 0;
    int cnt = 0;
    cin >> x;
    for(int i = 2; i <= n; i++){
        ll y;
        cin >> y;
        y *= pow(2,cnt);
        while(y < x){
            y *= 2;
            cnt++;
        }
        while(y > x){
            if(y / 2 < x) break;
            y /= 2;
            cnt--;
        }
        x = y;
        ans += cnt;
    }
    cout << ans;

    return 0;
}