#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 1005;
char a[N][N];
int n,m;

ll f(int i, int x, int y, int z){
    ll total = 0;
    for(int j = 1; j <= m; j++){
        int cnt = 0;
        if(j > 1 && a[i][j] == a[i][j-1]) cnt++;
        if(j < m && a[i][j] == a[i][j+1]) cnt++;
        int cu = (a[i][j] - '0')^y;
        if(i > 1){
            int la = (a[i-1][j] - '0') ^ x;
            
            if(la == cu) cnt++;
        }
        if(i < n){
            int la = (a[i+1][j] - '0') ^ z;
            if(la == cu) cnt++;
        }

        total += cnt*cnt;
    }
    return total;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    cin >> n >> m;
    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= m; j++){
            cin >> a[i][j];
        }
    }

    ll dp[2][2] = {0};
    
    for(int i = 1; i <= n-1; i++){
        ll ndp[2][2] = {0};
        for(int x = 0; x < 2; x++){
            for(int y = 0; y < 2; y++){
                for(int z = 0; z < 2; z++){
                    ll cost = f(i,x,y,z);
                    if(ndp[y][z] < dp[x][y] + cost){
                        ndp[y][z] = dp[x][y] + cost;
                    }
                }
            }
        }
        for(int xx = 0; xx < 2; xx++){
            for(int yy = 0; yy < 2; yy++){
                dp[xx][yy] = ndp[xx][yy];
            }
        }
    }
    ll ans = -200;
    for(int x = 0; x < 2; x++){
        for(int y = 0; y < 2; y++){
            ll cost = f(n,x,y,0);
            if(ans < dp[x][y] + cost) ans = dp[x][y] + cost;
        }
    }
    cout << ans;
    return 0;
}