#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 1005;
int n, q;
struct node{
    int x, y, r;
}a[N];


bool f(int xx, int yy){
    int cnt = 0;
    for(int i = 1; i <= n; i++){
        double d = sqrt((xx - a[i].x)*(xx - a[i].x) + (yy - a[i].y)*(yy - a[i].y));
        if(d <= a[i].r) cnt++;
    }
    return cnt % 2 == 1;
}

int main(){
    cin >> n;
    for(int i = 1; i <= n; i++) cin >> a[i].x >> a[i].y >> a[i].r;
    cin >> q;
    while(q--){
        int x, y;
        cin >> x >> y;
        if(f(x,y)) cout << "Yes";
        else cout << "No";
        if(q != 0) cout << "\n";
    }
    return 0;
}