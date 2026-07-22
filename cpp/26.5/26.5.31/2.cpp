#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 5 * 1e3 + 5;
int n, m;
ll a[N];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n >> m;
    ll sum = 0;
    for(int i = 1; i <= n; i++){
        cin >> a[i];
        sum += a[i];
    }

    for(int i = 1; i <= m; i++){
        ll k;
        cin >> k;
        ll r1 = 0ll;
        ll r2 = 0ll;
        ll a1 = 0ll;
        ll a2 = 0ll;
        for(int i = 1; i <= n; i++){
            ll d = (a[i] ^ k) - a[i];
            r1 += d;
            if(r1 > 0) r1 = 0;
            r2 += d;
            if(r2 < 0) r2 = 0;
            a1 = min(a1, r1);
            a2 = max(a2, r2);
        }
        cout << sum + a1 << " " << sum + a2;
        if(i != m) cout << "\n";
    }


    return 0;
}