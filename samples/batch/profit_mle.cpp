// Memory Limit Exceeded: correct answer, but first fills a 400 MB array (the limit is 256 MB).
#include <bits/stdc++.h>
using namespace std;

int32_t main() {
    cin.tie(0); ios::sync_with_stdio(0);
    vector<int> waste(100000000, 1);         // 400 MB, every page touched
    int n, q;
    cin >> n >> q;
    vector<long long> p(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long a;
        cin >> a;
        p[i] = p[i - 1] + a;
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << (l <= r ? p[r] - p[l - 1] : p[n] - p[l - 1] + p[r]) + waste[l] - 1 << '\n';
    }
    return 0;
}
