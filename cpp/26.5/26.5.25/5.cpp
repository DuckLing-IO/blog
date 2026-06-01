#include<bits/stdc++.h>
using namespace std;
const int MOD = 1e9+7;
const int N = 1e5 + 5;
typedef long long ll;
ll dp[N] = {0}, o[N] = {0}, l[N] = {0};
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    dp[1] = 0; dp[2] = 0; o[1] = 1; l[2] = 1; 
    for(int i = 3; i <= N-5; i++){
        o[i] = (o[i-1] + o[i-2]) % MOD;
        l[i] = (l[i-1] + l[i-2]) % MOD;
        dp[i] = (dp[i-1] + dp[i-2] + l[i-2]*o[i-1]) % MOD;
    }
    int T;
    cin >> T;
    while(T--){
        // 0 1 01 101 01101 10101101 0110110101101 101011010110110101101
        int x;
        cin >> x;
        
        
        cout << dp[x] % MOD << "\n";
    }

    return 0;
}