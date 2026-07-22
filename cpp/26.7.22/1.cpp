#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 100;
void solve(){
    int n;
    cin >> n;
    if(n < 3){
        cout << "No\n";
        return;
    }
    vector<int> a(n+1);
    for(int i = 1; i <= n; i++) cin >> a[i];
    queue<int> v;
    int ct = 0;
    for(int i = 1; i <= n-2; i++){
        if(a[i] > 1) ct--;
        else ct++;
        if(ct >= 0) v.push(i);
    }
    if(v.empty()){
        cout << "No\n";
        return;
    }
    while(!v.empty()){
        int idx = v.front() + 1;
        v.pop();
        int cnt = 0;
        for(int i = idx; i <= n-1; i++){
            if(a[i] > 2) cnt--;
            else cnt++;
            if(cnt >= 0){
                cout << "Yes\n";
                return;
            }
        }
    }
    cout << "No\n";
    return;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int T;
    cin >> T;
    while(T--){
        solve();
    }
    return 0;
}