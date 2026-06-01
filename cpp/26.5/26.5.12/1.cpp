#include<bits/stdc++.h>
using namespace std;

int f(int base,int exp){
	int res = 1;
	while(exp > 0){
		if(exp % 2 == 1){
			res *= base;
		}
		base *= base;
		exp /= 2;
	}
	return res;
}

int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	int n;
	n = f(2,32);
	cout << n;
	return 0;
}
