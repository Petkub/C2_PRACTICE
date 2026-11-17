// Accepted: the rectangle sum is (sum of a over the rows) x (sum of b over the columns), two prefix sums.
#include <bits/stdc++.h>
using namespace std;

int32_t main() {
    cin.tie(0); ios::sync_with_stdio(0);
    int n, m, q;
    cin >> n >> m >> q;
    vector<long long> pa(n + 1, 0), pb(m + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        pa[i] = pa[i - 1] + x;
    }
    for (int j = 1; j <= m; j++) {
        long long x;
        cin >> x;
        pb[j] = pb[j - 1] + x;
    }
    while (q--) {
        int r1, c1, r2, c2;
        cin >> r1 >> c1 >> r2 >> c2;
        cout << (pa[r2] - pa[r1 - 1]) * (pb[c2] - pb[c1 - 1]) << '\n';
    }
    return 0;
}
