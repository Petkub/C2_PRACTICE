// Accepted, but g++ -Wall warns: an unused variable and a variable that may be used uninitialized.
#include <bits/stdc++.h>
using namespace std;

int32_t main() {
    cin.tie(0); ios::sync_with_stdio(0);
    int unused;
    int maybe;
    int n, q;
    cin >> n >> q;
    vector<long long> p(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long a;
        cin >> a;
        p[i] = p[i - 1] + a;
    }
    if (n > 1000000) maybe = n;
    if (q > 1000000) n = maybe;
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << (l <= r ? p[r] - p[l - 1] : p[n] - p[l - 1] + p[r]) << '\n';
    }
    return 0;
}
