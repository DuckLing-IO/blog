#include<bits/stdc++.h>
using namespace std;
const int N = 2 * 1e5 + 5;
int n, m;
struct edge{
    int u, v, w;
} es[N];

int f[N];
void init(){
    for(int i = 1; i <= n; i++) f[i] = i;
}
int ff(int x){
    return x == f[x] ? x : f[x] = ff(f[x]);
}
bool mag(int x, int y){
    int rx = ff(x);
    int ry = ff(y);
    if(rx == ry) return false;
    else{
        f[rx] = ry;
        return true;
    }
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int T;
    cin >> T;
    while(T--){
        string s;
        getline(cin, s);
        cin >> n >> m;
        for(int i = 1; i <= m; i++){
            cin >> es[i].u >> es[i].v >> es[i].w;
        }
        
        int ans = 0;
        for(int bit = 29; bit >= 0; bit--){
            init();
            int temp = ans | ((1 << bit) - 1);
            int cnt = n;
            for(int i = 1; i <= m; i++){
                if((es[i].w | temp) == temp){
                    if(mag(es[i].u, es[i].v)){
                        cnt --;
                    }
                }
            }
            if(cnt != 1){
                ans |= (1ll << bit);
            }
        }
        cout << ans << "\n";
    }

    return 0;
}