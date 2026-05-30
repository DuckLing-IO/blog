#include<bits/stdc++.h>
using namespace std;
int x, y, z;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> x >> y >> z;

    if(x == 0 && y == 0 && z == 0) cout << 1;
    else if(z == 0){
        if(x == 0) cout << y;
        else
        cout << y+1;
    }
    else if(z >= x){
        if(x == 0 || x == 1){
            cout << 1+(z-1+y+x)*2;
        }else{
            cout << 1 + (x-1) * 3 + (z-x) * 2 + y * 2 + 2;
        }
    }else {
        int en = x - (z-1);

        cout << 1 + (z-1) * 3 + y * 2 + 2 + ((en-1) >= 1 ? 1 : 0);
    }
    
    return 0;
}