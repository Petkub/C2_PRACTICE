// Runtime Error with a message on stderr: vector::at() throws std::out_of_range.
#include <bits/stdc++.h>
using namespace std;

int32_t main() {
    cin.tie(0); ios::sync_with_stdio(0);
    int n, q;
    cin >> n >> q;
    vector<long long> v(1);
    cout << v.at(n) << '\n';                 // n >= 1: out of range
    return 0;
}
