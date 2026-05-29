#include<bits/stdc++.h>
using namespace std;
const int N = 505;
int gcd(int a, int b){
    return b == 0 ? a : gcd(b, a % b);
}
map<pair<int, int>, int> m;
int xu[N], yu[N], xv[N], yv[N];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int n;
    cin >> n;
    for(int i = 1; i <= n; i++) cin >> xu[i] >> yu[i] >> xv[i] >> yv[i];
    for(int i = 1; i <= n; i++){
        int x1 = xu[i], y1 = yu[i], x2 = xv[i], y2 = yv[i];
        int dx = x2 - x1;
        int dy = y2 - y1;
        int g = gcd(abs(dx), abs(dy));
        int step_x = dx / g;
        int step_y = dy / g;
        int x = x1;
        int y = y1;
        for(int i = 0; i <= g; i++){
            m[{x, y}]++;
            x += step_x;
            y += step_y;
        }
    }
    int ans = 0;
    for(pair<pair<int, int>, int> p : m){
        if(p.second > 1) ans++;
    }
    cout << ans;
    return 0;
}