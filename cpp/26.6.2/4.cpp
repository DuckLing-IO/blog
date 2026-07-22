    #include<bits/stdc++.h>
    using namespace std;
    const int N = 100005;
    int a[N];
    int dp[N];
    int n;
    int ans;
    signed main(){
        ios::sync_with_stdio(0);
        cin.tie(0);
        cin >> n;
        
        for(int i = 1; i <= n; i++){
            int x;
            cin >> x;
            int tmp = 1;
            for(int k = 0; k <= 30; k++){
                if((x >> k) & 1){
                    tmp = max(tmp, dp[k] + 1);
                }
            }
            for(int k = 0; k <= 30; k++){
                if((x >> k) & 1){
                    dp[k] = max(dp[k], tmp);
                }
            }
            ans = max(ans, tmp);
        }
        
        cout << ans;


        return 0;
    }