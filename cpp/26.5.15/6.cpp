#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

const int N = 15;

int n;
int s[N],k[N];
int ans = INT_MAX;

void dfs(int i,int a,int b){
    if(i > n){
        if(a == 1 && b == 0) return;
        ans = min(ans,abs(a-b));
        return;
    }

    dfs(i+1,a*s[i],b+k[i]);
    dfs(i+1,a,b);
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    cin >> n;
    for(int i = 1; i <= n; i++){
        int x,y;
        cin >> x >> y;
        s[i] = x; k[i] = y;
    }
    dfs(1,1,0);
    cout << ans;
    return 0;
}