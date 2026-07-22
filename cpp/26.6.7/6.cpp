#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int n, m;
string s;
int len;
ll v[100005];
ll d[100005];

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n >> m;
    cin >> s;
    len = s.size();
    ll cn = 0;
    for(int i = 0; i < len; i++){
        if(s[i] == '0'){
            cn ++;
            v[0] += cn;
        }else{
            ll x = 0;
            for(int j = i; j < min(i+6, len); j++){
                x *= 10;
                x += s[j] - '0';
                if(x > 100000) break;
                v[x] += cn+1;
            }
            cn = 0;
        }
    }

    d[0] = v[0];
    for(int i = 1; i <= 100000; i++){
        d[i] = d[i-1] + v[i];
    }
    while(m--){
        int l, r;
        cin >> l >> r;
        if(l == 0) cout << d[r];
        else cout << d[r] - d[l-1];
        if(m != 0) cout << "\n";
    }
    return 0;
}