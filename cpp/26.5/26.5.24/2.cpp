#include<bits/stdc++.h>
using namespace std;
const int N = 25;
int a[N];
int b[N][N],v[N],ans[N],cnt,path[N];
int n;
int ma = INT_MIN;

int check(int x){
    for(int i = x + 1; i <= n; i++){
        if(b[x][i] && !v[i]) return i;
    }
    return -1;
}

void dfs(int no,int st,int num){
    int x = check(no);
    if(x == -1){
        if(num > ma){
            ma = num;
            cnt = st;
            for(int i = 1; i <= st; i++) ans[i] = path[i];
        }
        return;
    }
    for(int i = x; i <= n; i++){
        if(b[no][i] && !v[i]){
            v[i] = 1;
            path[st+1] = i;
            dfs(i,st+1,num+a[i]);
            path[st+1] = 0;
            v[i] = 0;
        }
    }
}

int main(){
    cin >> n;
    for(int i = 1; i <= n; i++) cin >> a[i];

    for(int i = 1; i <= n; i++){
        for(int j = i+1; j <= n; j++){
            cin >> b[i][j];
        }
    }

    for(int i = 1; i <= n; i++){
        path[1] = i;
        v[i] = 1;
        dfs(i,1,a[i]);
        v[i] = 0;
    }
    
    
    for(int i = 1; i <= cnt; i++){
        if(i != 1) cout << " ";
        cout << ans[i];
    }
    cout << "\n";
    cout << ma;
    return 0;
}