#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

map<string,ll> m;
int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	int T;
	cin >> T;
	while(T--){
		int op;
		cin >> op;
		if(op == 1){
			string na;
			ll sc;
			cin >> na >> sc;
			m[na] = sc;
			cout << "OK\n";
		}else if(op == 2){
			string na;
			cin >> na;
			if(m.count(na)){
				cout << m[na];
			}else{
				cout << "Not found"; 
			}
			cout << "\n";
		}else if(op == 3){
			string na;
			cin >> na;
			if(m.count(na)){
				m.erase(na);
				cout << "Deleted successfully";
			}else{
				cout << "Not found"; 
			}
			cout << "\n";
		}else if(op == 4){
			cout << m.size();
			cout << "\n";
		}
	}
	
	
	return 0;
}
