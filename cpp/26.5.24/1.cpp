#include<bits/stdc++.h>
using namespace std;

int d[10] = {6,2,5,5,4,5,6,3,7,6};

int main(){
    int T;
    cin >> T;
    while(T--){
        int x;
        cin >> x;
        if(x <= 1){
            cout << "-1\n";
            continue;
        }
        int xx = x % 7;
        if(x % 7 == 0){
            int cnt = x/7;
            while(cnt--){
                cout << "8";
            }
            cout << "\n";
        }else if(x % 7 == 1){
            int cnt = (x-8)/7;
            cout << "10";
            while(cnt--){
                cout << "8";
            }
            cout << "\n";
        }else if(xx == 2){
            cout << "1";
            int cnt = (x-2)/7;
            while(cnt--){
                cout << "8";
            }
            cout << "\n";
        }else if(xx == 3){
            if(x == 3) cout << 7 << "\n";
            else if(x == 10) cout << "22\n";
            else{
                cout << 200;
                int cnt = (x-17) / 7;
                while(cnt--){
                    cout << 8;
                }
                cout << "\n";
            }
        }else if(xx == 4){
            if(x == 4) cout << "4\n";
            else {
                cout << 20;
                int cnt = (x - 11) / 7;
                while(cnt--){
                    cout << 8;
                }
                cout << "\n";
            }
        }else if(xx == 5){
            cout << "2";
            int cnt = x/7;
            while(cnt--){
                cout << "8";
            }
            cout << "\n";
        }else if(xx == 6){
            cout << "6";
            int cnt = x/7;
            while(cnt--){
                cout << "8";
            }
            cout << "\n";
        }
    }
    return 0;
}