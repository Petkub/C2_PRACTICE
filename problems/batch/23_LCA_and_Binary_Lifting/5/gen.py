import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


random.seed(230105)
MAXN, MAXQ, MAXW = 200_000, 100_000, 10**9


def add(W, w, qs):
    n = len(w)
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ and W <= MAXW
    assert all(1 <= x <= W for x in w)
    assert all(1 <= l <= r <= n for l, r in qs)
    tests.append(f"{n} {W} {len(qs)}\n" + " ".join(map(str, w)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs))


def make(n, q, W, wlo, whi, qmode="long"):
    """weights in [wlo, whi] (<= W); qmode long: wide ranges, mix: any ranges"""
    rnd = random.random
    span = whi - wlo + 1
    w = [wlo + int(rnd() * span) for _ in range(n)]
    qs = []
    for _ in range(q):
        if qmode == "long":
            l = 1 + int(rnd() * (n // 10))
            r = n - int(rnd() * (n // 10))
        else:
            l, r = 1 + int(rnd() * n), 1 + int(rnd() * n)
            if l > r:
                l, r = r, l
        qs.append((l, r))
    add(W, w, qs)


# samples
add(10, [4, 3, 5, 2, 6, 1, 7, 3], [(1, 8), (3, 5), (6, 6), (2, 7)])
add(5, [3, 3, 3], [(1, 3)])
add(1, [1], [(1, 1)])
add(10**9, [10**9, 10**9, 1, 10**9 - 1, 5], [(1, 5), (2, 4), (3, 5), (1, 1)])
add(7, [2, 5, 2, 2, 3, 4, 1, 6, 7], [(1, 9), (2, 6), (4, 8), (5, 5), (3, 7)])
# hidden: small and medium
add(3, [1, 2, 3, 1, 1, 1, 2], [(l, r) for l in range(1, 8) for r in range(l, 8)])
make(10, 50, 10, 1, 10, "mix")
make(50, 200, 100, 30, 70, "mix")
make(200, 300, 1000, 1, 1000, "mix")
make(2000, 2000, 10**9, 4 * 10**8, 10**9)
make(3000, 3000, 20, 1, 3, "mix")
# hidden: maximum size (most trucks carry one or two crates; sums beyond int)
make(MAXN, 80_000, 10**9, 5 * 10**8, 10**9)
make(MAXN, 80_000, 10**9, 10**9, 10**9)
make(MAXN, MAXQ, 2 * 10**6, 6 * 10**5, 10**6)
make(MAXN, MAXQ, 10**6, 1, 10**6)
make(MAXN, MAXQ, 3, 1, 3)
make(MAXN, MAXQ, 10**6, 10**6, 10**6, "mix")
make(MAXN, MAXQ, 1000, 1, 100)
make(MAXN, 80_000, 10**9, 1, 10**9, "mix")
make(MAXN, MAXQ, 2 * 10**6, 9 * 10**5, 1100000)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_400_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
