#include<bits/stdc++.h>
using namespace std;
int a[11] = {0, 5, 5, 10, 10, 15, 15, 20, 20, 25, 25};
bool b[151];
bool v[11];
int cnt;
void dfs(int pos, int res){
    if(pos > 10){
        if(b[res] == 0){
            cnt ++;
            b[res] = 1;
        }
        return;
    }
    for(int i = 1; i <= 10; i++){
        if(v[i]) continue;
        v[i] = 1;
        dfs(pos+1, res + a[i]);
        dfs(pos+1, res);
        v[i] = 0;
    }
}




int main(){
    dfs(1, 0);
    cout << cnt;
    return 0;
}