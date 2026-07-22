#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const double ex = 1e-9;
struct nn{
    ll x, y;
    int num;
}a[3];
bool cmp(nn a, nn b){
    ll x = a.x * b.y;
    ll y = b.x * a.y;
    return x == y ? a.num < b.num : x > y;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int tt;
    cin >> tt;
    
    while(tt--){
        for(int i = 0; i < 3; i ++) a[i].num = i+1;
        for(int i = 0; i < 3; i++){
            cin >> a[i].x;
        }
        for(int i = 0; i < 3; i ++){
            cin >> a[i].y;
        }

        sort(a, a + 3, cmp);
        cout << a[0].num;
        if(tt) cout << "\n";
        // for(auto& x : a) cout << x.v << " " << x.num << "\n";
    }
    return 0;
}