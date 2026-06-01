#include<bits/stdc++.h>
using namespace std;

typedef long long ll;
const int N = 15;
ll dp[N][N];
int a[N];
ll dfs(int pos, int sum, bool is_lead, bool is_limit, int target){
    if(pos == 0){
        return sum;
    }
    if(!is_lead && !is_limit && dp[pos][sum] != -1){
        return dp[pos][sum];
    }
    int up = is_limit ? a[pos] : 9;
    ll res = 0;
    
    for(int i = 0; i <= up; i++){
        bool next_lead = is_lead && (i==0);
        bool next_limit = is_limit && (i == up);
        int next_sum = sum;
        if(i == target && !next_lead){
            next_sum ++;
        }
        res += dfs(pos-1,next_sum,next_lead,next_limit,target);
    }
    if(!is_lead && !is_limit) dp[pos][sum] = res;
    return res;
}

ll solve(ll x, int target){
    int len = 0;
    while(x > 0){
        a[++len] = x % 10;
        x /= 10;
    }
    memset(dp,-1,sizeof(dp));
    return dfs(len,0,1,1,target);
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    ll a,b;
    cin >> a >> b;
    for(int i = 0; i < 10; i++){
        cout << solve(b,i) - solve(a-1,i);
        if(i != 9) cout << " ";
    }

    return 0;
}