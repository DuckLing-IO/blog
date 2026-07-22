#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 1005;
int d[N][N];
int X[N], Y[N], R[N];
int n;
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n;
    for(int i = 1; i <= n; i++){
        cin >> X[i] >> Y[i] >> R[i];
    }

    for(int idx = 1; idx <= n; idx++){
        int x = X[idx], y = Y[idx], r = R[idx];
        for(int j = max(1, y - r); j <= min(1000, y + r); j++){
            int sd = sqrt(r*r - abs(y - j)*abs(y - j));
            d[max(1, x - sd)][j] ++;
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