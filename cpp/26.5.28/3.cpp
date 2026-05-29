#include<bits/stdc++.h>
using namespace std;

string s = "kfdhtshmrw4nxg#f44ehlbn33ccto#mwfn2waebry#3qd1ubwyhcyuavuajb#vyecsycuzsmwp31ipzah#catatja3kaqbcss2th";

int ans = 0;
int si = s.size();
bool check(string ss){
    int si = ss.size();
    if(si < 8 || si > 16) return false;
    bool f1 = 0, f2 = 0;
    for(int i = 0; i < si; i++){
        if(f1 && f2) break;
        char c = ss[i];
        if(c >= '0' && c <= '9') f1 = 1;
        if((c < '0' || c > '9') && (c < 'a' || c > 'z') && (c < 'A' || c > 'Z')) f2 = 1;
    }
    return f1 && f2;
}


int main(){
    
    for(int len = 8; len <= 16; len++){
        for(int i = 0; i + len - 1 < si; i++){
            string ss = s.substr(i, len);
            if(check(ss)) ans++;
        }
    }

    cout << ans;

    return 0;
}