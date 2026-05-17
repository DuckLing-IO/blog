#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 205;

int n,a,b,v[N];
int ans = 0;
bool vi[N];
int bfs(){
    queue<pair<int,int>> q;
    q.push({a,0});
    vi[a] = 1;
    while(!q.empty()){
        int x = q.front().first;
        int y = q.front().second;
        if(x == b){

            return y;
        }
        q.pop();
        if(x+v[x]<=n&&!vi[x+v[x]]){q.push({x+v[x],y+1}); vi[x+v[x]] = 1;} 
        if(x-v[x]>=1&&!vi[x-v[x]]){q.push({x-v[x],y+1}); vi[x-v[x]] = 1;} 
    }
    return -1;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    cin >> n >> a >> b;
    for(int i = 1; i <= n; i++){
        int x;
        cin >> x;
        v[i] = x;
    }

    cout << bfs();


    return 0;
}