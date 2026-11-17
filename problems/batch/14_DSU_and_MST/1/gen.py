# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(140101)
MAXN, MAXQ = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ev):
    q = len(ev)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert any(e[0] == 2 for e in ev)
    for e in ev:
        if e[0] == 1:
            assert len(e) == 3 and 1 <= e[1] <= n and 1 <= e[2] <= n
        else:
            assert e[0] == 2 and len(e) == 2 and 1 <= e[1] <= n
    tests.append(f"{n} {q}\n" + "".join(" ".join(map(str, e)) + "\n" for e in ev))


def labels(n):
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


def rnd_events(n, q, pq=0.4):
    ev = []
    for _ in range(q):
        if random.random() < pq:
            ev.append((2, ri(1, n)))
        else:
            ev.append((1, ri(1, n), ri(1, n)))
    return ev


def chain(p, mode="new"):
    ev = []
    for k in range(1, len(p)):
        if mode == "new":
            b = p[k - 1]
        else:
            b = p[ri(0, k - 1)]
        ev.append((1, p[k], b))
    return ev


def deep_queries(p, cnt, spread):
    return [(2, p[ri(0, spread - 1)]) for _ in range(cnt)]


add(5, [(1, 2, 1), (1, 4, 3), (2, 1), (1, 3, 1), (2, 2), (1, 5, 5), (2, 5)])
add(6, [(1, 6, 5), (1, 5, 4), (2, 4), (1, 1, 2), (1, 4, 2), (1, 2, 6), (2, 1), (2, 3)])
add(1, [(2, 1), (1, 1, 1), (2, 1)])
add(7, [(1, 3, 7), (2, 7), (1, 1, 2), (1, 7, 2), (2, 1), (2, 2), (1, 4, 5), (1, 4, 6), (2, 5), (1, 3, 5), (2, 6)])
add(4, [(2, 4), (1, 4, 1), (1, 1, 2), (1, 2, 3), (2, 3), (2, 2), (1, 3, 4), (2, 1)])


add(2, [(1, 1, 2), (2, 2), (1, 2, 1), (2, 1), (2, 2)])
add(3, [(1, 2, 1), (1, 3, 1), (2, 1), (2, 2), (2, 3)])
for n, q in ((5, 12), (6, 15), (8, 20), (8, 20), (10, 40)):
    add(n, rnd_events(n, q))
add(50, rnd_events(50, 300, 0.5))
add(1000, rnd_events(1000, 3000))
p = labels(2000)
add(2000, chain(p) + deep_queries(p, 2000, 10) + rnd_events(2000, 500))
add(200_000, [(2, ri(1, 200_000)) for _ in range(1000)])


N = MAXN
p = list(range(1, N // 2 + 1))
add(N, chain(p) + [(2, 1)] * (MAXQ - (len(p) - 1)))
p = labels(N)[:110_000]
add(N, chain(p, "any") + deep_queries(p, MAXQ - 109_999, 50))
p = labels(N)
ev = chain(p[:100_000])
mix = []
for e in ev:
    mix.append(e)
    if random.random() < 0.3:
        mix.append((2, p[ri(0, 99)]))
mix = mix[:130_000]
add(N, mix + deep_queries(p, MAXQ - len(mix), 100))
p = labels(N)
a, b = p[:60_000], p[60_000:120_000]
ev = chain(a) + chain(b) + [(1, b[0], a[-1])]
ev += [(2, a[ri(0, 9)]) if random.random() < 0.5 else (2, b[ri(0, 9)]) for _ in range(MAXQ - len(ev))]
add(N, ev)
p = labels(N)
pairs = [(1, p[2 * i], p[2 * i + 1]) for i in range(50_000)]
ev = pairs + [(1, p[2 * i + 1], p[0]) for i in range(1, 50_000)]
ev += [(2, p[ri(0, 3)]) for _ in range(MAXQ - len(ev))]
add(N, ev)
p = labels(N)
c = chain(p[:100_000])
ev = c + [(1, p[ri(0, 99_999)], p[ri(0, 99_999)]) if random.random() < 0.1 else (2, p[ri(0, 20)])
          for _ in range(MAXQ - len(c))]
add(N, ev)
p = labels(N)
c = chain(p[:90_000], "any")
r = rnd_events(N, 30_000, 0.3)
ev = c + r + deep_queries(p, MAXQ - len(c) - len(r), 30)
add(N, ev)
p = labels(N)
c = chain(p[:100_000])
ev = c + [(2, p[k % 100]) for k in range(MAXQ - len(c) - 1)] + [(2, p[-1])]
add(N, ev)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_300_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
