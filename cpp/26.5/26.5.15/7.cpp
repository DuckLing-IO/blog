#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 105;
int n;
char s[N][N];
bool v[N][N];
vector<pair<int,int>> po;
string sc = "yizhong";
void up(int x,int y){
    for(int i = 1; i <= 6; i++){
        if(y-i < 1) return;
        char c = s[x][y-i];
        if(c != sc[i]) return;
    }
    for(int i = 0; i <= 6; i++) v[x][y-i] = 1;
}

void down(int x,int y){
    for(int i = 1; i <= 6; i++){
        if(y+i > n) return;
        char c = s[x][y+i];
        if(c != sc[i]) return;
    }
    for(int i = 0; i <= 6; i++) v[x][y+i] = 1;
}

void re(int x,int y){
    for(int i = 1; i <= 6; i++){
        if(x+i > n) return;
        char c = s[x+i][y];
        if(c != sc[i]) return;
    }
    for(int i = 0; i <= 6; i++) v[x+i][y] = 1;
}

void le(int x,int y){
    for(int i = 1; i <= 6; i++){
        if(x-i < 1) return;
        char c = s[x-i][y];
        if(c != sc[i]) return;
    }
    for(int i = 0; i <= 6; i++) v[x-i][y] = 1;
}

void u1(int x,int y){
    for(int i = 1; i <= 6; i++){
        if(x-i < 1 || y-i < 1) return;
        char c = s[x-i][y-i];
        if(c != sc[i]) return;
    }
    for(int i = 0; i <= 6; i++) v[x-i][y-i] = 1;
}

void u2(int x,int y){
    for(int i = 1; i <= 6; i++){
        if(x+i > n || y-i < 1) return;
        char c = s[x+i][y-i];
        if(c != sc[i]) return;
    }
    for(int i = 0; i <= 6; i++) v[x+i][y-i] = 1;
}

void d1(int x,int y){
    for(int i = 1; i <= 6; i++){
        if(x-i < 1 || y+i > n) return;
        char c = s[x-i][y+i];
        if(c != sc[i]) return;
    }
    for(int i = 0; i <= 6; i++) v[x-i][y+i] = 1;
}

void d2(int x,int y){
    for(int i = 1; i <= 6; i++){
        if(x+i < 1 || y+i > n) return;
        char c = s[x+i][y+i];
        if(c != sc[i]) return;
    }
    for(int i = 0; i <= 6; i++) v[x+i][y+i] = 1;
}

void f(){
    for(pair<int,int> p : po){
        int x = p.first;
        int y = p.second;
        
        up(x,y); down(x,y);
        le(x,y); re(x,y);
        u1(x,y); u2(x,y);
        d1(x,y); d2(x,y);

    }
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);

    cin >> n;
    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= n; j++){
            char c;
            cin >> c;
            s[i][j] = c;
            if(c == 'y') po.push_back({i,j});
        }
    }

    f();

    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= n; j++){
            if(v[i][j]) cout << s[i][j];
            else cout << "*";
        }
        cout << "\n";
    }

    return 0;
}