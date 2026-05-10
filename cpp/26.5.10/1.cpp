#include<bits/stdc++.h>
using namespace std;
const int N = 1e5+5;
int n, W;
int v[N],w[N],m[N],nv[N],nw[N];
int main(){
	cin >> n >> W;
	for(int i = 1; i <= n; i++) cin >> v[i] >> w[i] >> m[i];
	
	int new_n = 0;
	
	for(int i = 1; i <= n; i++){
		for(int j = 1; j <= m[i]; j++){
			m[i] -= j; new_n++;
			nv[new_n] = v[i] * j;
			nw[new_n] = w[i] * j;
		}
		if(m[i]){
			new_n++;
			nv[new_n] = v[i] * m[i];
			nw[new_n] = w[i] * m[i];
		}
	}
	int dp[W+1];
	memset(dp,0,sizeof(dp));
	for(int i = 1; i <= new_n; i++){
		for(int j = W; j >= nw[i]; j--){
			dp[j] = max(dp[j],dp[j-nw[i]]+nv[i]);
		}
	}
	cout <<  dp[W];
	return 0;
} 
