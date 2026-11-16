# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20201)
MAXN = 200_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(shows, ts):
    n, q = len(shows), len(ts)
    assert 1 <= n <= MAXN and 1 <= q <= MAXN
    assert all(0 <= l <= r <= MAXV for l, r in shows)
    assert all(0 <= t <= MAXV for t in ts)
    tests.append(f"{n} {q}\n" + "".join(f"{l} {r}\n" for l, r in shows) + " ".join(map(str, ts)) + "\n")


def rnd_shows(n, hi, maxlen):
    res = []
    for _ in range(n):
        l = ri(0, hi)
        res.append((l, min(hi, l + ri(0, maxlen))))
    return res


def rnd_ts(q, hi):
    return [ri(0, hi) for _ in range(q)]


def edge_ts(shows, q, hi):
    """queries placed on interval ends and one minute outside them"""
    res = []
    for _ in range(q):
        l, r = shows[ri(0, len(shows) - 1)]
        res.append(max(0, min(hi, random.choice((l, r, l - 1, r + 1)))))
    return res


# samples
add([(1, 5), (3, 8), (6, 6), (10, 12)], [0, 3, 6, 9, 12])
add([(2, 4), (4, 4), (4, 7)], [4, 3, 5, 8])
add([(0, 0)], [0, 1])
add([(0, MAXV), (5, 5), (0, MAXV)], [MAXV, 5])
add([(3, 9), (1, 2), (7, 7), (2, 5), (8, 10)], [2, 7, 8, 11, 6, 5])
add([(1, 10), (2, 9), (3, 8), (4, 7)], [1, 4, 8, 10])
# hidden: small
add([(7, 7)], [6, 7, 8])
add(rnd_shows(10, 20, 5), list(range(0, 22)))
s = rnd_shows(200, 1000, 100)
add(s, edge_ts(s, 300, 1000))
s = rnd_shows(2000, MAXV, MAXV)
add(s, edge_ts(s, 1000, MAXV) + rnd_ts(1000, MAXV))
s = [(ri(0, 50),) * 2 for _ in range(3000)]           # every show lasts one minute
add(s, list(range(0, 52)) * 40)
add([(0, MAXV)] * 1500 + [(MAXV, MAXV)] * 1500, [0, MAXV, MAXV - 1, 1] * 500)
# hidden: maximum size (values up to 10^5 keep the files near 3.5 MB)
N, H = MAXN, 100_000
add(rnd_shows(N, H, H), rnd_ts(N, H))
add(rnd_shows(N, H, 1000), rnd_ts(N, H))
add([(0, H)] * N, rnd_ts(N, H))                        # every show covers every query
s = [(ri(0, 100), ri(H - 100, H)) for _ in range(N)]   # early starts, late ends: early breaks do not help
add(s, [ri(H - 2000, H) for _ in range(N)])
s = [(ri(0, H), ) * 2 for _ in range(N)]
add(s, edge_ts(s, N, H))                               # single-minute shows, queries on and beside them
s = rnd_shows(N, H, 300)
add(s, edge_ts(s, N, H))
s = [(0, ri(0, H)) for _ in range(N)]
add(s, [ri(0, H) for _ in range(N)])
s = [(ri(0, H), H) for _ in range(N)]
add(s, [ri(0, H) for _ in range(N)])
# full range values, smaller N and Q
N2 = 100_000
s = rnd_shows(N2, MAXV, MAXV // 2)
add(s, edge_ts(s, N2 // 2, MAXV) + rnd_ts(N2 // 2, MAXV))
s = [(ri(0, 1000), ri(MAXV - 1000, MAXV)) for _ in range(N2)]
add(s, [ri(MAXV - 5000, MAXV) for _ in range(N2)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
