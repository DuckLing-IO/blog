#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
ll gcd(ll a, ll b){
    return b == 0 ? a : gcd(b, a%b);
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int n, q;
    cin >> n >> q;
    vector<ll> k(n+1);
    vector<ll> b(n+1);
    vector<int> tp(n);
    vector<pair<ll,ll>> jd(n);
    vector<int> cnt(n);
    vector<int> fir(n+1,n+1);
    vector<int> dif(n+1,n+1);
    for(int i = 1; i <= n; i++){
        cin >> k[i] >> b[i];
    }
    for(int i = 1; i < n; i++){
        ll dx = b[i] - b[i+1];
        ll dy = k[i] - k[i+1];
        if(dy == 0){
            if(dx == 0){
                tp[i] = 1;
            }else{
                tp[i] = 0;
            }
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
        cnt[i] = cnt[i-1] + (tp[i] == 0);
    }
    int nxt = n+1;
    for(int i = n; i >= 1; i--){
        if(tp[i] == 2){
            if(nxt == n+1){
                dif[i] = n+1;
            }else{
                if(jd[i] == jd[nxt]){
                    dif[i] = dif[nxt];
                }else{
                    dif[i] = nxt;
                }
            }
            nxt = i;
            fir[i] = i;
        }else{
            fir[i] = nxt;
        }
    }
    while(q--){
        ll l, r;
        cin >> l >> r;
        int ct = cnt[r-1] - cnt[l-1];
        if(ct > 0){
            cout << "No\n";
            continue;
        }
        int idx = fir[l];
        if(idx >= r-1){
            cout << "Yes\n";
        }else{
            if(dif[idx] <= r-1){
                cout << "No\n";
            }else{
                cout << "Yes\n";
            }
        }
    }
    return 0;
}