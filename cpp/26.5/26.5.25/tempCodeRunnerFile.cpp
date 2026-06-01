#include<bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int a,b,c;
    cin >> a >> b >> c;
    if(!c){
        if(!a && b) for(int i = 1; i <= b; i++) cout << "Q";
        else if(a && !b) for(int i = 1; i <= a; i++) cout << "L";
        else cout << -1;
        return 0;
    }
    int l = c/2 + 1, q = (c+1) / 2;
    if(a >= l && b >= q){
        for(int i = 1; i <= a-l; i++) cout << "L";
        for(int i = 1; i <= l+q-1; i++){
            if(i % 2 == 1) cout << "L";
            else cout << "Q";
        }
        if(l+q % 2 == 0){
            cout << "Q";
            for(int i = 1; i <= b-q; i++) cout << "Q";
        }else{
            for(int i = 1; i <= b-q; i++) cout << "Q";
            cout << "L";
        }
    }else{
        swap(l,q);
        if(a < l || b < q){
            cout << "-1";
            return 0;
        }
        for (int i = 1; i <= l + q; i++) {
            if (i & 1)
                cout << "Q";
            else
                cout << "L";
        }
        for (int i = 1; i <= b - q; i++) cout << "Q";

    }

    return 0;
}