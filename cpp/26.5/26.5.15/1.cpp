#include<bits/stdc++.h>
using namespace std;
typedef unsigned long long ll;
ll s[1005][1005];
int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	int T;
	cin >> T;
	while(T--){
		int n, m, q;
		cin >> n >> m >> q;
		for(int i = 1; i <= n; i++){
			for(int j = 1; j <= m; j++){
				ll x;
				cin >> x;
				s[i][j] = x - s[i-1][j-1] + s[i-1][j] + s[i][j-1];
			}
		}
		ll ans = 0;
		while(q--){
			int u,v,x,y;
			cin >> u >> v >> x >> y;
			ans = ans ^ (s[x][y] + s[u-1][v-1] - s[x][v-1] - s[u-1][y]);
		}
		cout << ans << "\n";
	}
	return 0;
}
