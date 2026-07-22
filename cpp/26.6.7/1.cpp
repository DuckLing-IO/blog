#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 2 * 1e5 +5;
int n;
string s;
int len;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> n;
    cin >> s;
    len = s.size();
    vector<int> ans;
    int l = 1;
    int r = 0;
    bool le = 1;
    ans.push_back(1);
    bool ab = 1;
    for(int i = 0; i < len; i++){
        if(s[i] == '1'){
            if(le){ 
                //偶数
                r += 2;
                if(r > n){
                    ab = 0;
                    break;
                }
                ans.push_back(r);
                le = 0;
            }else{
                //奇数
                l += 2;
                if(l > n){
                    ab = 0;
                    break;
                }
                ans.push_back(l);
                le = 1;
            }
        }else{
            if(le){
                //奇数
                l += 2;
                if(l > n){
                    ab = 0;
                    break;
                }
                ans.push_back(l);
                le = 1;
            }else{
                //偶数
                r += 2;
                if(r > n){
                    ab = 0;
                    break;
                }
                ans.push_back(r);
                le = 0;
            }
        }
    }
    if(ab == 0){
        ab = 1;
        ans.clear();
        ans.push_back(2);
        le = 0;
        l = -1;
        r = 2;
        for(int i = 0; i < len; i++){
            if(s[i] == '1'){
                if(le){ 
                    //偶数
                    r += 2;
                    if(r > n){
                        ab = 0;
                        break;
                    }
                    ans.push_back(r);
                    le = 0;
                }else{
                    //奇数
                    l += 2;
                    if(l > n){
                        ab = 0;
                        break;
                    }
                    ans.push_back(l);
                    le = 1;
                }
            }else{
                if(le){
                    //奇数
                    l += 2;
                    if(l > n){
                        ab = 0;
                        break;
                    }
                    ans.push_back(l);
                    le = 1;
                }else{
                    //偶数
                    r += 2;
                    if(r > n){
                        ab = 0;
                        break;
                    }
                    ans.push_back(r);
                    le = 0;
                }
            }
        }
    }
    if(ab == 0){
        cout << -1;
    }else{
        for(auto& x : ans){
            cout << x;
            cout << " ";
        }
    }
    return 0;
}