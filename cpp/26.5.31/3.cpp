#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 1005;
int d[N][N];
int x1[N], y1[N], r1[N];
int n;
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n;
    for(int i = 1; i <= n; i++){
        cin >> x1[i] >> y1[i] >> r1[i];
    }

    for(int idx = 1; idx <= n; idx++){
        int x = x1[idx], y = y1[idx], r = r1[idx];
        for(int j = max(1, y - r); j <= min(1000, y + r); y++){
            int sd = sqrt(r*r - abs(y - j)*abs(y - j));
            d[max(0, x - sd)][j] ++;
            d[min(1000, x + sd) + 1][j] --;
        }
    }

    for(int i = 1; i <= 1000; i++){
        for(int j = 1; j <= 1000; j++){
            d[i][j] += d[i-1][j];
        }
    }
    int q;
    cin >> q;
    while(q--){
        int x, y;
        cin >> x >> y;
        if(d[x][y] & 1) cout << "Yes";
        else cout << "No";
        if(q) cout << "\n";
    }

    return 0;
}