#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 2 * 1e5 + 5;
ll a[2 * N];
ll n, m, k;
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n >> m >> k;
    for(int i = 1; i <= n; i++){
        ll x;
        cin >> x;
        a[i] = a[i+n] = x;
    }
    ll ms = 0;
    int l = 1;
    int ans = -100;
    for(int r = 2; r <= 2*n; r++){
        if(abs(a[r] - a[r-1]) > k) ms++;
        while(ms > m || r-l+1 > n){
            l++;
            if(abs(a[l]-a[l-1]) > k) ms--;
        }
        ans = max(ans, (r-l+1));
    }
    cout << ans;
    return 0;
}