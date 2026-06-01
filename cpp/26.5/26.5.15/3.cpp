#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int s[1000005];
int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	int n;
	cin >> n;
	vector<int> b(7,-1);
	b[0] = 0;
	ll sum = 0;
	int ma = -100000;
	for(int i = 1; i <= n; i++){
		ll x;
		cin >> x;
		sum += x;
		int mod = sum % 7;
		if(b[mod] != -1){
			ma = max(ma, i - b[mod]);
		}else{
			b[mod] = i;
		}
	}
	cout << ma;
	return 0;
}
