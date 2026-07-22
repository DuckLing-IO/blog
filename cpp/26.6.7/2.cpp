#include<bits/stdc++.h>
using namespace std;
int main(){
    string s;
    cin >> s;
    int cnt = 0;
    if(s[0] != s[1] && s[0] != s[2] && s[0] != s[3]){
        cnt ++;
    }
    if(s[1] != s[0] && s[1] != s[2] && s[1] != s[3]){
        cnt ++;
    }
    if(s[2] != s[0] && s[2] != s[1] && s[2] != s[3]){
        cnt ++;
    }
    if(s[3] != s[0] && s[3] != s[1] && s[3] != s[2]){
        cnt ++;
    }
    cout << cnt;
}