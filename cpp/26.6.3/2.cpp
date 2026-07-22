#include<bits/stdc++.h>
using namespace std;
const int N = 1e5 + 5;
string s;
int dp[N][26];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> s;  
    for(int i = 0; i < 26; i++){
        dp[s.size() - 1][i] = s.size();
    }
    dp[s.size() - 1][s[s.size() - 1] - 'a'] = s.size() - 1;
    for(int i = s.size() - 2; i >= 0; i--){
        for(int j = 0; j < 26; j++){
            dp[i][j] = dp[i+1][j];
        }
        dp[i][s[i] - 'a'] = i;
    }

    int T;
    cin >> T;
    while(T--){
        int l1, r1, l2, r2;
        cin >> l1 >> r1 >> l2 >> r2;
        vector<int> s1;
        vector<int> s2;
        for(int i = 0; i < 26; i++){
            if(dp[l1-1][i] <= r1-1){
                s1.push_back(dp[l1-1][i]);
            }
            if(dp[l2-1][i] <= r2-1){
                s2.push_back(dp[l2-1][i]);
            }
        }
        sort(s1.begin(), s1.end());
        sort(s2.begin(), s2.end());
        int ma = min(s1.size(), s2.size());
        int ans = 0;
        for(int i = 0; i < ma; i++){
            if(s[s1[i]] != s[s2[i]]) ans ++;
        }
        int a = s1.size();
        int b = s2.size();
        ans += abs(a - b);
        cout << ans << "\n";
    }
    
    return 0;
}