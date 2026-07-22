#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 100;
void solve(){
    int n;
    cin >> n;
    string s, t;
    cin >> s;
    cin >> t;
    char a, b, c;
    int cnt = 0;
    bool f = 0;
    for(int i = 0; i < n; i++){
        if(s[i] != t[i]){
            cnt++;
            if(cnt == 1){
                a = s[i];
                b = t[i];
            }else if(cnt == 2){
                if(s[i] == a && t[i] == b){
                    f = 1;
                }
            }
        }
    }
    if(f && cnt == 2){
        cout << "YES";
    }else{
        cout << "NO";
    }
    cout << "\n";
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