#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const double esp = 1e-9;
int sum = 9999999;

// void dfs(int n,vector<int> a, vector<int> b,  int stp, int cnt){
//     if(stp >= n-1){
//         sum = min(sum, cnt);
//         return;
//     }
//     if((a[stp] + a[stp+1]) % 2 == b[stp]){
//         dfs(n,a,b,stp+1,cnt);
//     }else{
//         a[stp]++;
//         dfs(n,a,b,stp+1,cnt+1);
//         a[stp]--;
//         a[stp+1]++;
//         dfs(n,a,b,stp+1,cnt+1);
//         a[stp+1]--;
//     }
// }
void solve(){
    int n,m;
    cin >> n >> m;
    vector<int> a(n+1);
    vector<int> b(n+1);
    
    for(int i = 1; i <= n; i++){
        cin >> a[i];
    }
    for(int i = 1; i <= n-1; i++){
        cin >> b[i];
    }
    queue<int> q;
    int binx = 0;
    for(int i = 1; i <= n-1; i++){
        if((a[i] + a[i+1]) % 2 != b[i]){
            binx = i;
            break;
        }
    }
    if(binx == 0){
        cout << 0;
        return;
    }
    q.push(binx);
    q.push(binx+1);
    while(!q.empty()){
        int idx = q.front();
        q.pop();
        
    }
    cout << sum;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int T = 1;
    //cin >> T;
    while(T--){
        solve();
    }
    return 0;
}