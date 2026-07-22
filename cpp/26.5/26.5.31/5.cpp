#include<bits/stdc++.h>
using namespace std;

typedef long long ll;
const int N = 0;
vector<int> q;
void pr(__int128_t a){
    if(a == 0){
        cout << 0;
        return;
    }
    if(a < 0){
        cout << "-";
        a = 0-a;
    }
    string s = "";
    while(a > 0){
        s += (char)('0' + (a % 10));
        a /= 10;
    }
    for(int i = s.size() - 1; i >= 0; --i){
        cout << s[i];
    }
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int n, p;
    ll k;
    cin >> n >> k >> p;
    vector<__int128_t> d(n+1, 0);
    for(int i = 1; i <= n; i++){
        ll val;
        cin >> val;
        d[i] = val - k;
    }

    for(int i = 1; i <= p+1; i++){
        for(int j = n; j >= 2; --j){
            d[j] = d[j] - d[j-1];
        }
    }
    __int128_t ans = 0;
    for(int i = 1; i <= n; i++){
        if(d[i] > 0) ans += d[i];
        else ans -= d[i];
    }
    pr(ans);
    return 0;
}