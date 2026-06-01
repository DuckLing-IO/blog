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
        ll ma = 0ll;
        ll mi = 0ll;
        for(int i = 1; i <= n; i++){
            ll d = (a[i] ^ k) - a[i];
            ma = max(0ll, ma + d);
            mi = min(0ll, mi + d);
        }
        cout << sum + mi << " " << sum + ma;
        if(i != m) cout << "\n";
    }


    return 0;
}