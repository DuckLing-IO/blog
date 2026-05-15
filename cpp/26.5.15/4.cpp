#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

// 组合数返回值
ll f(ll x){
	return (x * (x-1)) / 2; 
}
int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	
	int n,k;
	cin >> n >> k;
	ll sum = 0;
	ll d[100005] = {0};
	d[0] = 1;
	ll ma = -100;
	for(int i = 1; i <= n; i++){
		ll x;
		cin >> x;
		sum += x;
		ll mod = sum % k;
		ma = max(ma,mod);
		d[mod]++;
	} 
	ll ans = 0;
	for(int i = 0; i <= ma; i++){
		if(d[i] > 1)
		ans += f(d[i]);
	}
	cout << ans;
	return 0;
}
