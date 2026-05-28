#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 1e5+5;
string s;

int solve(int la, int ra, int lb, int rb){
    bool a[26] = {0};
    bool b[26] = {0};
    int res = 0;
    int i = la - 1, j = lb - 1;
    while(i < ra && j < rb){
        if(a[s[i] - 'a']){
            i++;
            continue;
        }
        if(b[s[j] - 'a']){
            j++;
            continue;
        }
        a[s[i] - 'a'] = 1;
        b[s[j] - 'a'] = 1;
        if(s[i] != s[j]) res++;
    }
    if(i < ra){
        while(i < ra){
            if(a[s[i] - 'a']){
            i++;
            continue;
            }
            a[s[i] - 'a'] = 1;
            res++;
        }
    }else if(j < rb){
        while(j < rb){
            if(b[s[j] - 'a']){
            j++;
            continue;
            }
            b[s[j] - 'a'] = 1;
            res++;
        }
    }
    return res;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    getline(cin, s);
    int T;
    cin >> T;
    while(T--){
        int la,lb,ra,rb;
        cin >> la >> ra >> lb >> rb;
        cout << solve(la, ra, lb, rb);
        if(T) cout << "\n";
    }


    return 0;
}