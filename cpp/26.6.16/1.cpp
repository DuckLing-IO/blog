#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 105;
int a[N][N];
int ct[N];
int n;
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n;
    for(int i = 1; i <= n; i++){
        int k;
        cin >> k;
        while(k--){
            int x;
            cin >> x;
            a[x][++ct[x]] = i;
        }
    }
    for(int i = 1; i <= n; i++){
        int ma = ct[i];
        cout << ma;
        for(int j = 1; j <= ma; j++){
            cout << " ";
            cout << a[i][j];
        }
        if(i != n)
        cout << "\n";
    }
    return 0;
}