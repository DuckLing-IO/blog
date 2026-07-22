#include<bits/stdc++.h>
using namespace std;
const int N = 2 * 1e5 + 5;
vector<char> c;
string s1, s2;

int main(){
    int n, m;
    cin >> n >> m;
    cin >> s1 >> s2;
    sort(s2.begin(), s2.end());
    int i = 0, j = 0;
    while(i < n && j < m){
        if(s1[i] <= s2[j]){
            cout << s1[i];
            i++;
        }else{
            cout << s2[j];
            j++;
        }
    }
    if(i < n) for(; i < n; i++) cout << s1[i];
    if(j < m) for(; j < m; j++) cout << s2[j];
}