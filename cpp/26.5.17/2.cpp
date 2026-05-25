#include<bits/stdc++.h>
using namespace std;

typedef long long ll;
const int N = 10;
int n,a[N+5];

bool check(){
    int ans = 0;
    int i = 1;
    while(i <= n){
        int tmp = i;
        int j = i+1;
        while(j <= n && a[j] == 1){
            tmp = tmp*10 + j;
            j++;
        }
        if(a[i] == 2) ans += tmp;
        if(a[i] == 3) ans -= tmp;
        i = j; 
    }
    return ans == 0;
}

void dfs(int idx){
    if(idx > n){
        if(check()){
            cout << 1;
            for(int i = 2; i <= n; i++){
                if(a[i] == 1) cout << " ";
                if(a[i] == 2) cout << "+";
                if(a[i] == 3) cout << "-";
                cout << i;  
            }
            cout << "\n";     
        }
        return;
    }

    for(int i = 1; i <= 3; i++){
            a[idx] = i;
            dfs(idx+1);
    }
    return;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    cin >> n;
    a[1] = 2;

    dfs(2);
   


    return 0;
}