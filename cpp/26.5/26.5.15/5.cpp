#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
ll dp[21][21][21];
ll w(ll a,ll b,ll c){
    if(a <= 0 || b <= 0 || c <= 0) return 1;
    if(a > 20 || b > 20 || c > 20) return w(20,20,20);
    if(dp[a][b][c] != 0) return dp[a][b][c];
    if(a < b && b < c){
        if(dp[a][b][c-1] == 0) dp[a][b][c-1] = w(a,b,c-1);
        if(dp[a][b-1][c-1] == 0) dp[a][b-1][c-1] = w(a,b-1,c-1);
        if(dp[a][b-1][c] == 0) dp[a][b-1][c] = w(a,b-1,c);

        dp[a][b][c] = dp[a][b][c-1] + dp[a][b-1][c-1] - dp[a][b-1][c];
    }else{
        if(dp[a-1][b][c] == 0) dp[a-1][b][c] = w(a-1,b,c);
        if(dp[a-1][b-1][c] == 0) dp[a-1][b-1][c] = w(a-1,b-1,c);
        if(dp[a-1][b][c-1] == 0) dp[a-1][b][c-1] = w(a-1,b,c-1);
        if(dp[a-1][b-1][c-1] == 0) dp[a-1][b-1][c-1] = w(a-1,b-1,c-1);
        
        dp[a][b][c] = dp[a-1][b][c] + dp[a-1][b-1][c] + dp[a-1][b][c-1] - dp[a-1][b-1][c-1];
    }
    return dp[a][b][c];
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    while(1){
        ll a,b,c;
        cin >> a >> b >> c;
        if(a == -1 && b == -1 && c == -1) break;
        int ans = w(a,b,c);
        cout << "w(" << a << ", " << b << ", " << c << ") = " << ans << endl;
    }

    return 0;
}