#include<bits/stdc++.h>
using namespace std;
set<int> q;
int f(int x, int y, int len){
	int a = abs(x-len);
	int b = abs(y-len);
	if(b <= a){
		return y;
	}else{
		return x;
	}
}
int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	int T;
	cin >> T;
	while(T--){
		int op;
		cin >> op;
		int len;
		cin >>len;
		if(op == 1){
			if(q.count(len)){
				cout << "Already Exist\n";
			}else{
				q.insert(len);
			}
		}else if(op == 2){
			if(q.empty()){
				cout << "Empty\n";
				continue;
			}
			auto it = q.lower_bound(len);
			if(it == q.begin()){
				cout << *it;
				q.erase(it);
			}else if(it == q.end()){
				cout << * --it;
				q.erase(it);
			}else if(*it == len){
				cout << *it;
				q.erase(it);
			}else{
				int a = *it;
				int b = *--it;
				int x = f(a,b,len);
				cout << x;
				q.erase(x);
			}
			cout << "\n";
		}
	}
	return 0;
}
