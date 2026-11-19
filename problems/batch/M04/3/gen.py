# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(44003)
MAXN, MAXD, MAXV = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(p, ab):
    n, d = len(p), len(ab)
    assert 1 <= n <= MAXN and 1 <= d <= MAXD
    assert all(0 <= x <= MAXV for x in p)
    assert all(0 <= a <= MAXV and 0 <= b <= MAXV for a, b in ab)
    tests.append(f"{n} {d}\n" + " ".join(map(str, p)) + "\n" + "".join(f"{a} {b}\n" for a, b in ab))


def with_money(a, t, m, rest_hi=0, jitter=True):
    d = len(a)
    b = [0] * d
    if t is None:
        cap, m = m, max(0, m - 1)
        for k in range(d):
            b[k] = m // d + (1 if k < m % d else 0) - (ri(0, 1) if m >= 2 * d else 0)
        assert sum(b) < max(1, cap)
        return list(zip(a, b))
    assert m <= MAXV * t
    if m > 0:
        w = [ri(50, 150) if jitter else 100 for _ in range(t)]
        tw = sum(w)
        for k in range(t):
            b[k] = m * w[k] // tw
        b[t - 1] += m - sum(b[:t])
        if b[t - 1] == 0 or max(b[:t]) > MAXV:
            b[:t] = [m // t] * t
            b[t - 1] += m - sum(b[:t])
        if b[t - 1] == 0:
            b[t - 1], b[0] = 1, b[0] - 1 if b[0] else 0
            b[t - 1] = m - sum(b[:t - 1])
        assert sum(b[:t - 1]) < m <= sum(b[:t]) and max(b[:t]) <= MAXV
    for k in range(t, d):
        b[k] = ri(0, rest_hi)
    return list(zip(a, b))


add([6, 2], [(9, 3), (1, 4), (5, 2)])
add([5, 5], [(5, 1), (5, 1), (5, 1)])
add([4], [(0, 0)])
add([10, 1, 8, 3], [(2, 5), (7, 0), (9, 3), (4, 1), (6, 2)])
add([300000000, 400000000, 500000000], [(600000000, 200000000), (100000000, 500000000), (0, 100000000)])

add([0], [(0, 0)])
add([3, 3], [(3, 0), (3, 2), (0, 1)])
for n, d, hi, m in [(3, 5, 9, 10), (4, 4, 100, 48), (8, 12, 50, 125), (30, 40, 10**9, 6705662821),
                    (200, 300, 1000, 89234), (2000, 2000, 10**9, 587055080967)]:
    p = [ri(0, hi) for _ in range(n)]
    a = [ri(0, hi) for _ in range(d)]
    add(p, with_money(a, ri(1, d) if random.random() < 0.8 else None, m, hi))

N, D = MAXN, MAXD
p = [ri(0, MAXV) for _ in range(N)]
a = [ri(0, MAXV) for _ in range(D)]
add(p, with_money(a, D - ri(0, 100), 24911685926473, MAXV))
p = [MAXV] * N
a = [MAXV] * D
add(p, with_money(a, D, MAXV * D, 0, jitter=False))
p = [ri(0, MAXV) for _ in range(N)]
a = [ri(0, MAXV) for _ in range(D)]
add(p, with_money(a, None, 25096874541320))
p = [ri(0, 1000) for _ in range(N)]
a = [MAXV - ri(0, 1000) for _ in range(D)]
add(p, with_money(a, D - ri(0, 1000), 49993248, MAXV))
p = [MAXV - ri(0, 1000) for _ in range(N)]
a = [ri(0, 1000) for _ in range(D)]
add(p, with_money(a, D - ri(0, 1000), 494049337131, MAXV))
p = sorted(ri(0, MAXV) for _ in range(N))
a = sorted(ri(0, MAXV) for _ in range(D))
p.reverse()
add(p, with_money(a, D - ri(1000, 5000), 25067839344938, 10))
p = [ri(0, MAXV) for _ in range(N)]
a = sorted((ri(0, MAXV) for _ in range(D)), reverse=True)
add(p, with_money(a, D - ri(0, 10), 25038086248048, MAXV))
p = [ri(0, 10) for _ in range(N)]
a = [ri(0, 10) for _ in range(D)]
add(p, with_money(a, D - 1, 226582, 5))
p = [ri(0, MAXV) for _ in range(N)]
a = [ri(0, MAXV) for _ in range(D)]
m = 24918117445171
b = [m // D] * D
b[0] += m - sum(b) - 1
add(p, list(zip(a, b)))
p = [ri(0, MAXV) for _ in range(1000)]
a = [ri(0, MAXV) for _ in range(D)]
add(p, with_money(a, D - ri(0, 1000), 5050883104, MAXV))

p = [ri(0, MAXV) for _ in range(20_000)]
a = [ri(0, MAXV) for _ in range(20_000)]
add(p, with_money(a, ri(1, 20_000), 5917973903915, MAXV))
p = [ri(0, 10**6) for _ in range(5000)]
a = [ri(0, 10**6) for _ in range(30_000)]
add(p, with_money(a, ri(1, 30_000), 1437779906, 10**6))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
