#include<bits/stdc++.h>
using namespace std;
const int N = 1e9 + 5;
int n;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n;
    int xx = n / 5;
    int ans = 0;
    for(int i = 1; i <= xx; i++){
        if(i & 1){
            ans += 4;
        }else{
            ans += 3;
        }
    }
    cout << ans;
    return 0;
}