#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 3 * 1e5 + 5;
vector<pair<int, int>> a;
int n;
bool cmp(pair<int, int> a, pair<int, int> b){
    return a.first == b.first ? a.second > b.second : a.first < b.first;
}
int mi = N + 1;
int ans;
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n;
    for(int i = 1; i <= n; i++){
        int x, y;
        cin >> x >> y;
        a.push_back({x, y});
    }
    sort(a.begin(), a.end(), cmp);
    for(auto& p : a){
        int y = p.second;
        if(y <= mi){
            ans++;
            mi = y;
        }
    }
    cout << ans;
    return 0;
}