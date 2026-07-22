        #include<bits/stdc++.h>
        using namespace std;
        const int N = 1e9 + 5;
        int n, q;

        int main(){
            ios::sync_with_stdio(0);
            cin.tie(0);
            //1 2 3 4
            //0 1 1 1
            //1 2 1 0
            // -------
            cin >> n;
            cin >> q;
            vector<int> a(n+1);
            vector<int> d(n+1);
            for(int i = 1; i <= n; i++) cin >> a[i];
            for(int i = 1; i <= n; i++) d[i] = (((a[i] - a[i-1]) % 5) + 5) % 5;
            int ans = 0;
            for(int i = 2; i <= n; i++) ans += d[i];
            while(q--){
                int l, r;
                cin >> l >> r;
                
                if(l > 1){
                    ans -= d[l];
                    d[l] = (d[l] + 1) % 5;
                    ans += d[l];
                }
                if(r < n){
                    ans -= d[r+1];
                    d[r+1] = (((d[r+1] - 1) % 5) + 5) % 5;
                    ans += d[r+1];
                }
                cout << ans;
                if(q != 0) cout << "\n";
            }
            return 0;
        }