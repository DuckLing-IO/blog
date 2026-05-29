#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
double x = 517 / 2091.0, y = 2632 / 10455.0, z = 308 / 2091.0;
const double eps = 1e-9;

bool check(ll a, ll b, ll c){
    ll S = a + b + c;
    double p1 = (2.0 * a * b) / (S * (S-1));
    double p2 = (2.0 * c * b) / (S * (S-1));
    double p3 = (2.0 * a * c) / (S * (S-1));
    return abs(p1 - x) <= eps && abs(p2 - y) <= eps && abs(p3 - z) <= eps;
}

int main(){

    ll a,b,c;
    for(a = 1; a <= 1000; a++)
        for(b = 1; b <= 1000; b++)
            for(c = 1; c <= 1000; c++)
                if(check(a,b,c)){
                    cout << a << "," << b << "," << c;
                    break;
                }


    return 0;
}