#include<bits/stdc++.h>
using namespace std;
const int N = 1e7 + 5;
int pr[N/10];
bool st[N];
int cn = 0;
void init(){
    st[0] = st[1] = 1;

    for(int i = 2; i < N; i++){
        if(!st[i]){
            pr[cn++] = i;
        }

        for(int j = 0; j < cn && pr[j] <= (N-1) / i; j++){
            st[pr[j] * i] = 1;
            if(i % pr[j] == 0) break;
        }
    }
}
string s;
int le;
bool dfs(int idx){
    if(idx >= le){
        if(s[le-1] == '0' || s[le-1] == '2' || s[le-1] == '4' || s[le-1] == '5' || s[le-1] == '6' || s[le-1] == '8')
        return 0;
        if(!st[stoi(s)]){
            cout << s << "\n";
            return 1;
        }else return 0;
    }
    if(s[idx] == '*'){
        for(char c = '0'; c <= '9'; c++){
            s[idx] = c;
            if(dfs(idx+1)){
                return 1;
            }
            s[idx] = '*';
        }
        return 0;
    }else{
        return dfs(idx+1);
    }
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    init();
    int t;
    cin >> t;
    while(t--){
        
        cin >> s;
        le = s.size();
        if (!dfs(0)) {
            cout << -1 << "\n";
        }
    }


    return 0;
}