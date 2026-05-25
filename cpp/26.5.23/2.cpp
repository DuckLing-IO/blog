#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

int n,k,p;
ll a[20];
ll ans = LLONG_MIN;
bool op[20];
void f(){
    ll an = 1;
    ll cur = a[1];
    for(int i = 2; i <= n; i++){
        if(op[i] == 1){
            cur += a[i];
        }else{
            an *= cur;
            cur = a[i];
        }
    }
    an *= cur;
    ans = max(ans, an);
}


void dfs(int idx,int cnt){
    if(cnt == p){
        f();
        return;
    }
    if(idx > n){
        if(cnt != p) return;
        f();
        return;
    }

    op[idx] = 1;
    dfs(idx+1,cnt+1);
    op[idx] = 0;
    dfs(idx+1,cnt);
}

int main(){
    cin >> n >> k;
    p = n-1-k;
    for(int i = 1; i <= n; i++) cin >> a[i];

    dfs(2,0);
    cout << ans;


    return 0;
}