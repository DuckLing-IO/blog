#include<bits/stdc++.h>
using namespace std;
const int N = 1e5+3;
string s;
int nex[N][26];
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> s;
    int n = s.size();
    int T;
    cin >> T;
    for(int i = 0; i < 26; i++){
        nex[n+1][i] = n+1;
    }

    for(int i = n; i >= 1; i--){
        for(int j = 0; j < 26; j++){
            nex[i][j] = nex[i+1][j];
        }
        nex[i][s[i-1] - 'a'] = i;
    }

    while(T--){
        int la, ra, lb, rb;
        cin >> la >> ra >> lb >> rb;
        vector<int> c1;
        vector<int> c2;
        for(int i = 0; i < 26; i++){
            if(nex[la][i] <= ra) c1.push_back(nex[la][i] - 1);
            if(nex[lb][i] <= rb) c2.push_back(nex[lb][i] - 1);
        }
        sort(c1.begin(), c1.end());
        sort(c2.begin(), c2.end());
        int len1 = c1.size();
        int len2 = c2.size();
        int cnt = abs(len1 - len2);
        int up = min(len1, len2);
        for(int i = 0; i < up; i++){
            if(s[c1[i]] != s[c2[i]]) cnt++;
        }
        cout << cnt;
        if(T) cout << "\n";
    }

    return 0;
}