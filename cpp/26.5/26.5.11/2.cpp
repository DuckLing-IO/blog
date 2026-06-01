#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll MOD = 1e9+7;
bool fl[MOD];
ll ans;
map<ll,int> yz;
vector<pair<ll,int>> q;
ll fast(ll base,ll exp){
	ll res = 1;
	base %= MOD;
	while(exp > 0){
		if(exp % 2 == 1){
			res = (res * base) % MOD;
		}
		base = (base * base) % MOD;
		exp /= 2;
	}
	return res;
}
void f(ll x){
	for(ll i = 2; i * i <= x; i++){
		while(x % i == 0){
			yz[i]++;
			x /= i;
		}
	}
}

void bfs(int idx, ll nc){
	if(idx >= q.size()){
		ans += fast(nc,nc);
		return;
	}
	int nn = q[idx].first;
	int cc = q[idx].second;
	for(int i = 0; i <= cc; i++){
		bfs(idx+1,)
	}
}

int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	ll a,b;
	cin >> a >> b;
	f(a); f(b);
	for(pair p : yz){
		q.push_back(p);
	}
	
	dfs(0,1);
	
	
	cout << ans;
	
	return 0;
}
