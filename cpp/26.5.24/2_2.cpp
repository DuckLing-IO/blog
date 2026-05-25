#include<bits/stdc++.h>
using namespace std;
const int N = 25;
int n, a[N], b[N][N], dp[N], pr[N];
int main(){
    cin >> n;
    for(int i = 1; i <= n; i++){
        cin >> a[i];
        dp[i] = a[i];
    }
    for(int i = 1; i <= n; i++){
        for(int j = i+1; j <= n; j++){
            cin >> b[i][j];
        }
    }

    int ma = INT_MIN;
    int en = 0;

    for(int i = 1; i <= n; i++){
        for(int j = 1; j < i; j++){
            if(b[j][i] == 1 && dp[i] < dp[j] + a[i]){
                dp[i] = dp[j] + a[i];
                pr[i] = j;
            }
        }
        if(dp[i] > ma){
            ma = dp[i];
            en = i;
        }
    }
    vector<int> q;
    int cur = en;
    while(cur != 0){
        q.push_back(cur);
        cur = pr[cur];
    }
    for(int i = q.size() - 1; i >= 0; i--){
        if(i != q.size() - 1) cout << " ";
        cout << q[i];
    }
    cout << "\n";
    cout << ma;
    return 0;
}