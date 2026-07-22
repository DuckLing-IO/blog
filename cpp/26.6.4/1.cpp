#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 2 * 1e5 + 5;
ll n;
ll h[N];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n;
    for(int i = 1; i <= n; i++) cin >> h[i];
    stack<pair<ll, ll>> st;
    ll sum = 0;
    for(int i = 1; i <= n; i++){
        ll ch = h[i];
        ll cnt = 1;
        while(!st.empty() && st.top().first <= ch){
            pair<ll, ll> p = st.top();
            st.pop();
            cnt += p.second;
            sum -= p.first * p.second;
        }   
        st.push({ch, cnt});
        sum += ch * cnt;
        cout << sum + 1 << (i == n ? "" : " ");
    }
    

    return 0;
}