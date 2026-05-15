#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int d[200005];
int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	int n,k,q;
	cin >> n >> k >> q;
	while(n--){
		int l,r;
		cin >> l >> r;
		d[l]++; d[r+1]--;
	}
	for(int i = 1; i <= 200005; i++){
		d[i] += d[i-1];
	}
	for(int i = 1; i <= 200005; i++){
		if(d[i] >= k) d[i] = d[i-1] + 1;
		else d[i] = d[i-1];
	}
	while(q--){
		int l,r;
		cin >> l >> r;
		 
		cout << d[r] - d[l-1] << "\n";
	}
	return 0;
}
