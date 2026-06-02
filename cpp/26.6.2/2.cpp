#include<bits/stdc++.h>
using namespace std;
const int N = 2 * 1e5 + 5;
int n, m;
struct e{
    int u, v, w;
} edges[N];

bool cmp(e a, e b){
    return a.w < b.w;
}
int f[5005];
void init(){
    for(int i = 1; i <= n; i++){
        f[i] = i;
    }
}

int ff(int x){
    if(f[x] == x) return x;
    return f[x] = ff(f[x]);
}

bool mag(int x, int y){
    int rx = ff(x);
    int ry = ff(y);
    if(rx == ry) return false;
    f[rx] = ry;
    return true;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n >> m;
    for(int i = 1; i <= m; i++){
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
    }

    sort(edges+1, edges+1+m, cmp);
    init();
    int ans = 0;
    int cnt = 0;

    for(auto edge : edges){
        int u = edge.u;
        int v = edge.v;
        int w = edge.w;
        if(ff(u) == ff(v)) continue;
        else{
            mag(u, v);
            ans += w;
            cnt ++;
        }
    }

    if(cnt != n - 1) cout << "orz";
    else{
        cout << ans;
    }

    return 0;
}