#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

const int N = 1e6 + 5;

//质数筛
vector<int> pr;
bool is_pr[N];
void p(int n){
    for(int i = 2; i <= n; i++) is_pr[i] = 1;
    for(int i = 2; i <= n; i++){
        if(is_pr[i] == 1) pr.push_back(i);
        for(int j = 0; j < pr.size() && i*pr[j] <= n; j++){
            is_pr[i*pr[j]] = 0;
            if(i % pr[j] == 0) break;
        }
    }
}

//最大公因数
ll gcd(ll a, ll b){
    return b == 0 ? a : gcd(b, a%b);
}

ll lcd(ll a, ll b){
    if(a == 0 || b == 0) return 0;
    return (a / gcd(a, b)) * b;
}


int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);


    return 0;
}