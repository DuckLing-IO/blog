#include<bits/stdc++.h>
using namespace std;
int dp[10],ma;
int main(){
    
    int n;
    cin >> n;
    for(int i = 1; i <= n; i++){
        string s;
        cin >> s;
        int len = s.size();

        dp[s[len-1] - '0'] = max(dp[s[len-1] - '0'], dp[s[0] - '0'] + 1);
        
    }

    for(int i = 0; i < 10; i++) ma = max(ma,dp[i]);
    cout << n-ma;

    return 0;
}