#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 2 * 1e5 + 3;
int ct[40][N];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int n, q;
    cin >> n >> q;
    for(int i = 1; i <= n; i++){
        int x;
        cin >> x;
        
        for(int j = 1; j <= 35; j++){
            ct[j][i] = ct[j][i-1] + x % 2;
            x >>= 1;
        }
    }
    while(q--){
        int op, l, r;
        ll k;
        cin >> op >> k >> l >> r;
        int kk[40] = {0};
        int idx = 35;
        ll tmp = 1;
        ll ans = 0;
        for(int i = 1; i <= 35; i++){
            kk[i] = k % 2;
            k >>= 1;
        }
        if(op == 0){
            for(int i = 1; i <= idx; i++){
                if(kk[i] == 1){
                    int cnt = ct[i][r] - ct[i][l-1];
                    if(cnt % 2 == 1) kk[i] = 1;
                    else kk[i] = 0;
                }else{
                    kk[i] = 0;
                }
            }
        }else{
            for(int i = 1; i <= idx; i++){
                if(kk[i] == 1){
                    kk[i] = (r - l + 1) % 2;
                }else{
                    int cnt = ct[i][r] - ct[i][l-1];
                    if(cnt % 2 == 1) kk[i] = 1;
                    else kk[i] = 0;
                }
            }
        }
        
        for(int i = 1; i <= idx; i++){
            if(kk[i] == 1){
                ans += tmp;
            }
            tmp *= 2;
        }
        cout << ans;
        if(q) cout << "\n";
    }
    return 0;
}