#include<bits/stdc++.h>
using namespace std;

typedef long long ll;
const int N = 15;

int t[N],d[N],l[N];
bool v[N];
int n;

bool dfs(int idx, int time){
    if(idx > n) return 1;

    for(int i = 1; i <= n; i++){
        if(v[i] || time > t[i] + d[i]) continue;
        v[i] = 1;
        if(dfs(idx+1,max(time,t[i]) + l[i])){
            v[i] = 0;
            return 1;
        }
        v[i] = 0;
    }
    return 0;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    int T;
    cin >> T;
    while(T--){
        memset(t,0,sizeof(t));
        memset(d,0,sizeof(d));
        memset(l,0,sizeof(l));
        memset(v,0,sizeof(v));
        cin >> n;

        for(int i = 1; i <= n; i++){
            cin >> t[i] >> d[i] >> l[i];
        }
        
        if(dfs(1,0)){
            cout << "YES";
        }else{
            cout << "NO";
        }
        cout << "\n";
    }

    return 0;
}