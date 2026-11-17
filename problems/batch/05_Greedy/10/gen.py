# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(30315)
MAXN = 200_000
MAXT = 10**9
MAXR = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(T, lamps):
    n = len(lamps)
    assert 1 <= n <= MAXN
    assert 1 <= T <= MAXT
    lines = [f"{n} {T}\n"]
    for p, r in lamps:
        assert 0 <= p <= T and 1 <= r <= MAXR
        lines.append(f"{p} {r}\n")
    tests.append("".join(lines))


def lamp_for(lo, hi, T):
    p = (lo + hi + 1) // 2
    p = min(max(p, 0), T)
    r = max(p - lo, hi - p, 1)
    return (p, min(r, MAXR))


def chain(T, k, overlap):
    cuts = sorted(random.sample(range(1, T), k - 1)) if k > 1 else []
    pts = [0] + cuts + [T]
    res = []
    rnd = random.random
    a = 0
    for b in pts[1:]:
        lo = a - int(rnd() * (overlap + 1)) if overlap else a
        if lo < 0:
            lo = 0
        p = (lo + b + 1) // 2
        res.append((p, p - lo if p - lo >= b - p else b - p))
        a = b
    return res


def noise(T, m, rmax):
    return [(ri(0, T), ri(1, rmax)) for _ in range(m)]


def shuffled(a):
    a = a[:]
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]
    return a


add(10, [(2, 2), (5, 2), (6, 1), (9, 2)])
add(6, [(1, 2), (5, 1)])
add(5, [(1, 1), (3, 5), (4, 1)])
add(8, [(3, 2), (5, 3), (8, 1)])
add(12, [(1, 1), (3, 1), (6, 3), (10, 2), (5, 5)])
add(8, [(1, 1), (4, 2), (7, 1), (6, 1)])

add(1, [(0, 1)])
add(10, [(5, 4)])
add(10, [(10, 10), (0, 3)])
add(20, [(2, 2), (6, 2), (11, 2), (15, 2), (19, 2)])
add(30, shuffled(chain(30, 10, 0)))
lamps = chain(300, 40, 5) + noise(300, 40, 6)
add(300, shuffled(lamps))
lamps = chain(10**6, 1000, 300) + noise(10**6, 1000, 2000)
add(10**6, shuffled(lamps))
lamps = chain(10**6, 2000, 0)
lamps[1000] = (lamps[1000][0], lamps[1000][1] - 1) if lamps[1000][1] > 1 else lamps[1000]
add(10**6, shuffled(lamps))
lamps = chain(5000, 2500, 0)
add(5000, shuffled(lamps))

N = MAXN
step = MAXT // N // 2
add(MAXT, shuffled([(step * (2 * k + 1), step) for k in range(N)]))
lamps = [(step * (2 * k + 1), step) for k in range(N)]
lamps[N - 7] = (lamps[N - 7][0], step - 1)
add(MAXT, shuffled(lamps))
add(MAXT, shuffled(chain(MAXT, N, 0)))
add(MAXT, shuffled(chain(MAXT, N // 2, 3000) + noise(MAXT, N // 2, 2000)))
add(MAXT, shuffled(chain(MAXT, 150_000, 10_000) + noise(MAXT, 50_000, 20_000)))
lamps = chain(MAXT, 120_000, 0) + [(ri(MAXT // 2, MAXT), ri(1, 2_000_000)) for _ in range(80_000)]
add(MAXT, shuffled(lamps))
lamps = chain(MAXT, 199_999, 0)
lamps.append(lamp_for(0, MAXT, MAXT))
add(MAXT, shuffled(lamps))
lamps = chain(MAXT - 3, N - 1, 2000)
add(MAXT, shuffled(lamps + [(MAXT - 4, 1)]))
lamps = chain(MAXT, N, 0)
p, r = lamps[N // 2]
lamps[N // 2] = (p + 1, r) if p < MAXT else (p - 1, r)
add(MAXT, shuffled(lamps))
add(MAXT, sorted(chain(MAXT, N, 4000), key=lambda x: -x[0]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
