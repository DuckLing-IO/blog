#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll N = 2 * 1e5 + 5;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    ll T;
    cin >> T;
    vector<ll> ans;
    while(T--){
        ll cost[2] = {0ll};
        ll x, y;
        
        ll an = 0ll;
        cin >> cost[0] >> cost[1] >> x >> y;
        x = abs(x);
        y = abs(y);
        ll la = min(cost[0], cost[1]);
        if(x == y){
            an = la * (x+y);
        }else{
            if(x < y){
                swap(x, y);
                swap(cost[0], cost[1]);
            }
            
            an += la * (y+y);
            ll lax = x - y;
            an += (lax/2) * min(cost[0]+cost[1], 4*la);
            if(lax % 2 == 1){
                an += min(cost[0], 3*la);
            }
        }
        ans.push_back(an);
    }
    for(auto& c : ans){
        cout << c;
        cout << "\n";
    }
    return 0;
}