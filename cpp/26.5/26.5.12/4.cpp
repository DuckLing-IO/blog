#include<bits/stdc++.h>
using namespace std;

int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	int n;
	cin >> n;
	vector<int> q(n+1,0);
	for(int i = 1; i <= n; i++){
		int x;
		cin >> x;
		q[i] = x + q[i-1];		
	}

	int t;
	cin >> t;
	while(t--){
		int l, r;
		cin >> l >> r;
		cout << q[r] - q[l-1] << "\n";
	}
	return 0;
}
