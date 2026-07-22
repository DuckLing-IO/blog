#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    ll n, k;
    cin >> n >> k;
    if(n == 1){
        ll x;
        cin >> x;
        if(k == 0) cout << 1;
        else cout << 0;
        return 0;
    }
    vector<int> a(n);
    for(int i = 0; i < n; i++){
        cin >> a[i];
    }
    sort(a.begin(), a.end());
    bool f = a[1] - a[0] == 1;
    int l, r;
    l = f ? a[0] : a[1];
    r = f ? a[0]+k : a[1]+k;
    ll cnt = 0;
    int len = a.size();
    for(int i = 1-f; i < len; i++){
        if(a[i] <= r) r = a[i] + k;
        else{
            cnt += (r-l+1);
            l = a[i];
            r = a[i] + k;
        }
    }
    cnt += (r-l+1);
    if(!f) cnt ++;
    cout << cnt - k;
    return 0;
}