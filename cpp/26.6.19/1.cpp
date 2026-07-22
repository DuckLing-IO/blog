#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 1e5 + 5;
int d[13] = {0,31,28,31,30,31,30,31,31,30,31,30,31};
int a, b, c;
struct dat{
    int y, m, d;
};
dat fk[2027][13][32];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int T;
    int ma = -100;
    dat mad = {-1, -1, -1};
    for(int i = 2026; i >= 1; i --){
        int mj = (i == 2026 ? 1 : 12);
        for(int j = mj; j >= 1; j --){
            int mk = (i == 2026 ? 9 : d[j]);
            for(int k = mk; k >= 1; k --){
                int v = 10000*i + 100*j + k;
                int ans = 0;
                while(v > 0){
                    ans ^= (v % 10);
                    v /= 10;
                }
                if(ans > ma){
                    ma = ans;
                    mad = {i, j, k};
                }
                fk[i][j][k] = mad;
            }
        }
    }
    
    cin >> T;
    while(T--){
        
        cin >> a >> b >> c;
        dat aa = fk[a][b][c];
        cout << aa.y << " " << aa.m << " " << aa.d;
        if(T != 0) cout << "\n";
    }

    return 0;
}