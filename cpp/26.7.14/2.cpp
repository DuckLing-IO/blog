#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 100;
int gcd(int a, int b){
    return b == 0 ? a : gcd(b,a%b);
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int T;
    cin >> T;
    while(T--){
        int n, x, y;
        cin >> n >> x >> y;
        vector<int> a(n+1,0);
        for(int i = 1; i <= n; i++) cin >> a[i];
        int z = gcd(x, y);
        bool f = 1;
        for(int i = 1; i <= n; i++){
            if(i == a[i]){
                continue;
            }
            ll gap = abs(i - a[i]);
            if(gap % z != 0){               
                f = 0;
                break;
            }
        }
        if(f) cout << "YES";
        else cout << "NO";
        cout << "\n";
    }
    
    return 0;
}