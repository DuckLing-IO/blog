#include<bits/stdc++.h>
using namespace std;

int a[7] = {0,1,2,3,5,10,20};
int b[7];
bool dp[1001];

int main(){
	dp[0] = 1;
	int cnt = 0;
	vector<int> q;
	for(int i = 1; i <= 6; i++){
		int x;
		cin >> x;
		for(int j = 1; j <= x; j++){
			x -= j;
			q.push_back(j*a[i]);
		}
		if(x){
			q.push_back(x*a[i]);
		} 
	}
	int nc = q.size();
	for(int i = 0; i < nc; i++){
		for(int j = 1000; j >= 0; j--){
			if(dp[j-q[i]]){
				dp[j] = 1;
				cnt++;
			}
		}
	}
	cout << "Total=" << cnt;
	
	return 0;
}
