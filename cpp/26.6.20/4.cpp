#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
bool cmp(int a, int b){
    return a > b;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int n, m;
    cin >> n >> m;
    vector<int> a(n+1);
    vector<vector<int>> b(n+1);
    vector<int> v1(n+1);
    vector<int> v2(n+1);
    vector<vector<int>> dp(n+1, vector<int>(3,-1));
    for(int i = 1; i <= n; i++) cin >> a[i];
    for(int i = 1; i <= m; i++){
        int idx, y;
        cin >> idx >> y;
        b[idx].push_back(y);
    }
    for(int i = 1; i <= n; i++){
        if(!b[i].empty()){
            sort(b[i].begin(), b[i].end(), cmp);
            v1[i] = b[i][0];
            if(b[i].size() > 1){
                v2[i] = b[i][1];
            }
        }
    }
    dp[1][0] = a[1];
    dp[1][1] = v1[1];
    dp[1][2] = v2[1];
    for(int i = 2; i <= n; i++){
        dp[i][0] = max({dp[i-1][0]+a[i], dp[i-1][0]+v1[i-1], dp[i-1][0]+v2[i-1],
                        dp[i-1][1]+a[i], dp[i-1][1]+v2[i-1],
                        dp[i-1][2]+a[i], dp[i-1][2]+v1[i-1]});
        dp[i][1] = max({dp[i-1][0], dp[i-1][1], dp[i-1][2]}) + v1[i];
        dp[i][2] = max({dp[i-1][0], dp[i-1][1], dp[i-1][2]}) + v2[i];
    }
    cout << max({dp[n][0], dp[n][1], dp[n][2]}) << "\n";
    return 0;
}