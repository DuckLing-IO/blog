#include<bits/stdc++.h>
using namespace std;
const int N = 1005;
int a[N];
struct node{
    int x, y, k;
}v[3005];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int n, m, p;
    cin >> n >> m >> p;
    for(int i = 1; i <= n; i++) cin >> a[i];
    for(int i = 1; i <= m; i++) cin >> v[i].x >> v[i].y >> v[i].k;
    for(int i = 1; i <= n; i++){
        if(p >= a[i]) cout << 1 << "\n";
        else cout << 0 <<
    }
    return 0;
}