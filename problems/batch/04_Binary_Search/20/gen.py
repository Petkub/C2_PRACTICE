# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(42001)
MAXL = 300_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def answer(n, k, p, mode="good"):
    a = sorted(p)
    if mode == "drop":
        a = a[len(a) - 2 * n * k:]
    spare = len(a) - 2 * n * k

    def ok(d):
        c, i = 0, 0
        while i + 1 < len(a) and c < n:
            if a[i + 1] - a[i] <= d and (mode == "nocap" or i <= 2 * k * c + spare):
                c, i = c + 1, i + 2
            else:
                i += 1
        return c >= n

    return min(g for g in set(a[i + 1] - a[i] for i in range(len(a) - 1)) if ok(g))


def add(cases, sample=False):
    assert 1 <= len(cases) and sum(len(p) for n, k, p in cases) <= MAXL
    for n, k, p in cases:
        assert n >= 1 and k >= 1 and 2 * n * k <= len(p)
        assert all(1 <= v <= MAXV for v in p)
        if sample:
            assert answer(n, k, p) == answer(n, k, p, "nocap") == answer(n, k, p, "drop")
    tests.append(f"{len(cases)}\n" + "".join(f"{n} {k} {len(p)}\n" + " ".join(map(str, p)) + "\n"
                                             for n, k, p in cases))


def tiny(vmax):
    while True:
        n, k = ri(1, 3), ri(1, 3)
        if 2 * n * k <= 8:
            break
    L = ri(2 * n * k, min(10, 2 * n * k + 3))
    return (n, k, [ri(1, vmax) for _ in range(L)])


def rnd_case(L, n, k, vmax=MAXV):
    return (n, k, [ri(1, vmax) for _ in range(L)])


def top_dense(L, n, k):
    low = 2 * n * k - n
    vals = sorted(random.sample(range(1, MAXV // 2), low))
    base = MAXV // 2 + 1
    dense = [base + ri(0, 10 * (L - low)) for _ in range(L - low)]
    p = vals + dense
    random.shuffle(p)
    return (n, k, p)


def bottom_pairs(L, n, k, G):
    p, x = [], 1
    for _ in range(n):
        g = ri(1, G)
        p += [x, x + g]
        x += g + G + ri(1, G)
    junk = L - 2 * n * k
    step = (MAXV - x) // (junk + 2 * n * (k - 1) + 1)
    assert step > G
    for _ in range(junk + 2 * n * (k - 1)):
        x += step - ri(0, step - G - 1)
        p.append(x)
    random.shuffle(p)
    return (n, k, p)


def adv(L, k, m, dense):
    n = (L - 2 * m) // (2 * k)
    L = 2 * n * k + 2 * m
    p, x = [], 1
    for _ in range(m):
        g = ri(1, 20)
        p += [x, x + g]
        x += g + ri(100, 1000)
    top = MAXV - 20 * dense
    p += [ri(top, MAXV) for _ in range(dense)]
    p += [ri(x, top - 1) for _ in range(L - 2 * m - dense)]
    random.shuffle(p)
    return (n, k, p)


def forced_mid(k, m, x, L=MAXL, n=None):
    if n is None:
        n = (L - 2 * m) // (2 * k)
    M = 2 * (n - m) + x
    F = 2 * n * k - M
    p, v = [], 1
    for _ in range(m):
        g = ri(1, 20)
        p += [v, v + g]
        v += g + ri(100, 1000)
    mid_top = 9 * 10**8
    p += [ri(v, mid_top) for _ in range(M)]
    p += [ri(mid_top + 1, mid_top + 20 * F) for _ in range(F)]
    random.shuffle(p)
    return (n, k, p)


def sparse_dense(k, S, m, L=MAXL):
    n = (L - 2 * m) // (2 * k)
    p, v = [], 1
    for _ in range(m):
        g = ri(1, 20)
        p += [v, v + g]
        v += g + ri(100, 1000)
    rest = 2 * n * k - S
    mid_top = MAXV - 20 * rest - 1
    p += [ri(v, mid_top) for _ in range(S)]
    p += [ri(mid_top + 1, MAXV) for _ in range(rest)]
    random.shuffle(p)
    return (n, k, p)


add([(2, 2, [8, 3, 9, 4, 12, 5, 10, 7, 4])], sample=True)
add([(1, 3, [8, 1, 12, 6, 9, 5, 10]), (2, 1, [10, 20, 13, 22])], sample=True)
add([(1, 1, [MAXV, 1])], sample=True)
add([(3, 1, [7, 7, 7, 7, 7, 7, 7])], sample=True)
add([(1, 2, [13, 26, 1, 20, 8, 33, 4, 19]), (2, 2, [4, 6, 8, 10, 12, 14, 16, 18, 20])], sample=True)

add([tiny(4) for _ in range(3000)])
add([tiny(30) for _ in range(3000)])
add([tiny(MAXV) for _ in range(3000)])
add([sparse_dense(2, 300, 0, 2000) for _ in range(40)] + [forced_mid(1, 50, 0, 2000) for _ in range(40)])

add([rnd_case(ri(2, 300), 1, 1) for _ in range(300)])
add([top_dense(600, 50, 6) for _ in range(50)] + [bottom_pairs(600, 40, 3, 1000) for _ in range(50)])
add([(n, k, [ri(1, 20) for _ in range(2 * n * k + ri(0, 50))])
     for n, k in ((ri(1, 30), ri(1, 5)) for _ in range(400))])
add([(1, 1, [ri(1, MAXV), ri(1, MAXV)]) for _ in range(5000)] + [(2, 1, [7] * 4), (1, 50_000, [MAXV] * 100_000)])

L = MAXL
add([sparse_dense(2, 80_000, 0)])
add([sparse_dense(2, 90_000, 0)])
add([sparse_dense(3, 75_000, 0)])
add([sparse_dense(3, 80_000, 0)])
add([sparse_dense(2, 75_000, 0)])
add([forced_mid(1, 1000, 0)])
add([forced_mid(1, 5000, 2)])
add([adv(L, 1, 200, 1000)])
add([adv(L, 1, 3000, 20_000)])
add([adv(L, 1, 1000, 5000)])
add([rnd_case(L, L // 2 - 10, 1)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
