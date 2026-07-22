#include<bits/stdc++.h>
using namespace std;

int main(){
    int x = 2;
    vector<bool> b1;
    while(x > 0){
        b1.push_back(x & 1);
        x >>= 1;
    }
    for(int i = b1.size()-1; i >= 0; i--){
        cout << b1[i] << " ";
    }
    int y = 2;
    y |= 0;
    cout << y;
    return 0;
}