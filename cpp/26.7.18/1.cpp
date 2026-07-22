#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
void solve(){
    int n;
    cin >> n;
    vector<int> a(n+1);
    vector<int> b(n+1);
    bool fa = 0, fb = 0, ff = 0;
    int sum = 0;
    for(int i = 1; i <= n; i++){
        cin >> a[i];
        if(a[i] == 1) fa = 1;
    }
    for(int i = 1; i <= n; i++){
        cin >> b[i];
        if(b[i] == 0) fb = 1;
        if(a[i] != b[i]){
            ff = 1;
            sum += a[i];
        }
    }
    if(ff == 0){
        cout << "0\n";
        return;
    }
    if(fa == 0 || fb == 0){
        cout << "-1\n";
        return;
    }
    if(sum % 2 == 1){
        cout << "1\n";
        return;
    }
    if(sum % 2 == 0){
        cout << "2\n";
        return;
    }
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