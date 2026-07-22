#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
ll gcd(ll a, ll b){
    return b == 0 ? a : gcd(b, a%b);
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    ll n, q;
    cin >> n >> q;
    vector<ll> k(n+1), b(n+1);
    vector<int> tp(n);
    vector<pair<ll, ll>> jd(n);
    vector<int> ct(n+1,0);
    vector<int> fidx(n+1, n+1);
    vector<int> fdif(n+1, n+1);
    for(int i = 1; i <= n; i++) cin >> k[i] >> b[i];
    for(int i = 1; i < n; i++){
        ll dx = b[i+1] - b[i];
        ll dy = k[i+1] - k[i];
        if(dy == 0){
            if(dx == 0) tp[i] = 1;
            else tp[i] = 0;
        }else{
            tp[i] = 2;
            ll g = gcd(abs(dx), abs(dy));
            dx /= g;
            dy /= g;
            if(dy < 0){
                dx = -dx;
                dy = -dy;
            }
            jd[i] = {dx, dy};
        }
        ct[i] = ct[i-1] + (tp[i] == 0 ? 1 : 0);
    }
    int tmp = n+1;
    for(int i = n-1; i >= 1; i--){
        if(tp[i] == 2){
            if(tmp == n+1){
                fdif[i] = n+1;
            }else{
                if(jd[i] == jd[tmp]) fdif[i] = fdif[tmp];
                else fdif[i] = tmp;
            }
            tmp = i;
            fidx[i] = i;
        }else{
            fidx[i] = tmp;
        }
    }
    while(q--){
        ll l, r;
        cin >> l >> r;
        int nct = ct[r-1] - ct[l-1];
        if(nct > 0){
            cout << "No\n";
            continue;
        }
        int nn = fidx[l];
        if(nn > r-1){
            cout << "Yes\n";
        }else{
            if(fdif[nn] <= r-1){
                cout << "No\n";
            }else{
                cout << "Yes\n";
            }
        }
    }
    return 0;
}