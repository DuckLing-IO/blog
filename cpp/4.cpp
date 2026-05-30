#include<bits/stdc++.h>
using namespace std;
const int N = 1005;
typedef long long ll;
bool g[N][N];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int n;
    cin >> n;
    for(int i = 1; i <= n; i++){
        int x, y, r;
        cin >> x >> y >> r;
        ll rr = 1ll * r * r;
        int x1 = max(1, x - r);
        int x2 = min(1000, x + r);
        int y1 = min(1000, y + r);
        int y2 = max(1, y - r);

        for(int i = x1; i <= x2; i++){
            for(int j = y2; j <= y1; j++){
                if((i-x)*(i-x) + (j-y)*(j-y) <= rr) g[i][j] = 1-g[i][j];
            }
        }

    }
    int q;
    cin >> q;
    while(q--){
        int x, y;
        cin >> x >> y;
        if(g[x][y] == 1) cout << "Yes";
        else cout << "No";
        if(q != 0) cout << "\n";
    }
    return 0;
}