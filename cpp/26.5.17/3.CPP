#include<bits/stdc++.h>
using namespace std;

bool a[5][5];
bool b[4][4];
int ans = INT_MAX;

bool check(){
    for(int i = 1; i <= 3; i++)
        for(int j = 1; j <= 3; j++)
            if(a[i][j] == 0) return 0;
    return 1;
}
void f(int x, int y){
    a[x][y] = 1-a[x][y];
}
void f1(int x, int y){
    f(x,y);
    f(x,y-1); f(x,y+1);
    f(x-1,y); f(x+1,y);
}
void dfs(int idx, int s){
    if(idx > 9){
        if(check()){
            ans = min(ans,s);
        }
        return;
    }
    
    int x = (idx - 1) / 3 + 1;
    int y = idx % 3;
    if(y == 0) y = 3;
    // if(b[x][y] == 1){
    //     dfs(idx+1,s);
    // }else{
    //     b[x][y] = 1;
    //     f1(x,y);
    //     dfs(idx+1,s+1);
    //     b[x][y] = 0;
    //     dfs(idx+1,s+1);
    // }
    f1(x,y);
    dfs(idx+1,s+1);
    f1(x,y);
    dfs(idx+1,s);
    return;
}

int main(){
    
    for(int i = 1; i <= 3; i++)
        for(int j = 1; j <= 3; j++)
            cin >> a[i][j];
    dfs(1,0);
    cout << ans;
    return 0;
}