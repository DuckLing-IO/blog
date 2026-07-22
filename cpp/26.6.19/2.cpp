#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 1e5 + 5;


int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int T;
    cin >> T;
    while(T--){
        int n;
        cin >> n;
        if(n % 2 != 0) n ++;
        cout << n / 2;
        if(T != 0) cout << "\n";
    }

    return 0;
}