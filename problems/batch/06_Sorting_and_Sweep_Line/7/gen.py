# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(40405)
MAXN, MAXX, MAXB = 100_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(lamps, houses):
    n, q = len(lamps), len(houses)
    assert 1 <= n <= MAXN and 1 <= q <= MAXN
    assert all(1 <= l <= r <= MAXX and 1 <= b <= MAXB for l, r, b in lamps)
    assert all(1 <= p <= MAXX for p in houses)
    tests.append(f"{n} {q}\n" + "".join(f"{l} {r} {b}\n" for l, r, b in lamps)
                 + " ".join(map(str, houses)) + "\n")


def rlamps(n, X, maxlen, B):
    out = []
    for _ in range(n):
        l = ri(1, X)
        out.append((l, min(X, l + ri(0, maxlen)), ri(1, B)))
    return out


def rh(q, X):
    return [ri(1, X) for _ in range(q)]


add([(1, 5, 3), (4, 10, 7), (8, 9, 2)], [2, 4, 9, 11])
add([(5, 5, 4), (1, 4, 9)], [5, 4, 6])
add([(1, MAXX, MAXB)], [MAXX])
add([(2, 6, 5), (3, 4, 5), (6, 8, 1)], [6, 6, 3, 1])
add([(1, 100, 1), (10, 20, 50), (15, 30, 20), (40, 40, 8)], [15, 21, 40, 100, 31])
add([(10, 20, 3)], [1, 9, 21])

add([(1, 1, 1)], [1])
add([(3, 3, 5), (3, 3, 5), (3, 3, 2)], [3, 2, 4])
add(rlamps(6, 20, 5, 10), rh(10, 22))
add(rlamps(40, 100, 20, 30), rh(50, 100))
add(rlamps(300, 1000, 100, 5), rh(300, 1000))
add(rlamps(2000, 10**6, 2000, MAXB), rh(2000, 10**6))
add(rlamps(3000, MAXX, 10**7, MAXB), rh(3000, MAXX))
add([(i, i, i) for i in range(1, 3001)], list(range(3000, 0, -1)))

N = MAXN
X = 10**6
add(rlamps(N, X, 100, 10**4), rh(N, X))
add(rlamps(N, X, 30_000, 10**4), rh(N, X))
add(rlamps(N, X, X, 10**6), rh(N, X))
lamps = [(ri(1, 1000), ri(1001, 2000), ri(100_000, 999_999)) for _ in range(N - 1000)]
lamps += [(1, X, ri(1, 99)) for _ in range(1000)]
add(lamps, [ri(2001, X) for _ in range(N)])
lamps = [(ri(1, 5000), ri(1, 5000) + 5000, ri(1, 10**6)) for _ in range(N)]
add(lamps, [ri(5001, 999_999) for _ in range(N)])
add([(i, X + 1 - i, i) for i in range(1, N + 1)], rh(N, X))
add([(1, X, 7)] * N, rh(N, X))
add([(10 * i + 1, 10 * i + 10, ri(1, 10**6)) for i in range(N)], [10 * i + 10 for i in range(N)])
add([(10 * i + 1, 10 * i + 10, ri(1, 10**6)) for i in range(N)], [10 * i + 1 for i in range(N)])
add(rlamps(N, 100, 30, 10**6), rh(N, 100))
add(rlamps(70_000, MAXX, 10**8, MAXB), rh(70_000, MAXX))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
