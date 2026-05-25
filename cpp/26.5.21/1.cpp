#include<bits/stdc++.h>
using namespace std;
int ans;
int v[6][6];

bool check(){
    for(int i = 1; i <= 5; i++){
        int cnt = 0;
        for(int j = 1; j <= 5; j++){
            cnt += v[i][j];
        }
        if(cnt == 5 || cnt == -5) return 0;
    }
    for(int i = 1; i <= 5; i++){
        int cnt = 0;
        for(int j = 1; j <= 5; j++){
            cnt += v[j][i];
        }
        if(cnt == 5 || cnt == -5) return 0;
    }
    if(abs(v[1][1]+v[2][2]+v[3][3]+v[4][4]+v[5][5]) == 5) return 0;
    if(abs(v[1][5]+v[2][4]+v[3][3]+v[4][2]+v[5][1]) == 5) return 0;
    return 1;
}

void dfs(int idx,int cnt){

    if(cnt > 13 || 25 - idx + 1 + cnt < 13) return;

    if(idx > 25){
        if(check()){
            ans++;
        }
        return;
    }

    int x = (idx - 1) / 5 + 1;
    int y = (idx - 1) % 5 + 1;

    v[x][y] = 1;
    dfs(idx+1,cnt+1);
    v[x][y] = -1;
    dfs(idx+1,cnt);
}
int main(){

    dfs(1,0);
    cout << ans;

    return 0;
}