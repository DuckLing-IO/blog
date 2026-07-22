#include<bits/stdc++.h>
using namespace std;
const int N = 1e4 + 5;

// 并查集部分
int f[1005];

int ff(int x){
    return x == f[x] ? x : f[x] = ff(f[x]);
}

bool mag(int x, int y){
    int rx = ff(x);
    int ry = ff(y);
    if(rx == ry) return false;

    f[rx] = ry;
    return true;
}

//生成树部分
struct e{
    int u, v, w;
} edges[N];

bool cmp(e a, e b){
    return a.w < b.w;
}

int n, m, k;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0); 

    cin >> n >> m >> k;
    
    for(int i = 1; i <= n; i++) f[i] = i;

    for(int i = 1; i <= m; i++){
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
    }

    int ma = n - k;

    if(ma < 0){
        cout << "No Answer";
        return 0;
    } 

    if(n == k){
        cout << 0;
        return 0;
    }

    sort(edges + 1, edges + 1 + m, cmp);

    int ans = 0;
    int cnt = 0;

    for(auto& edge : edges){
        int u = edge.u;
        int v = edge.v;
        int w = edge.w;

        if(ff(u) == ff(v)) continue;
        mag(u, v);
        ans += w;
        cnt ++;
        if(cnt == ma) break;
    }

    if(cnt != ma) cout << "No Answer";
    else cout << ans;

    return 0;
}