#include<bits/stdc++.h>
using namespace std;
const int N = 2 * 1e5 + 5;
int n;
int a[N];
int dp[N][2];
int gcd(int a, int b){
    return b == 0 ? a : gcd(b, a%b);
}
bool f(int a, int b){
    return gcd(a,b) != 1;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n;
    for(int i = 1; i <= n; i++) cin >> a[i];
    for(int i = 1; i <- n; i++){
        dp[i][0] = -1;
        dp[i][1] = -1;
    }
    dp[1][1] = 1;
    for(int i = 2; i <= n; i++){
        int la = a[i-1];
        if(dp[i-1][1] == -1) la = a[dp[i-1][0]];
        if(a[i] % la == 0 && f(a[i], la)){
            dp[i][1] = dp[i-1][1] + 1;
            
        }
    }
    return 0;
}