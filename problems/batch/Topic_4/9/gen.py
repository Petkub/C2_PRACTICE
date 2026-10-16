# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(40109)
MAXN, MAXC = 200_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(segs):
    n = len(segs)
    assert 1 <= n <= MAXN
    assert all(0 <= l < r <= MAXC for (l, r) in segs)
    tests.append(f"{n}\n" + "".join(f"{l} {r}\n" for (l, r) in segs))


def rnd_seg(lo, hi, minlen=1):
    l = ri(lo, hi - minlen)
    return (l, ri(l + minlen, hi))


# samples
add([(0, 10), (2, 5), (4, 8)])
add([(3, 6), (1, 7), (7, 9)])
add([(0, MAXC)])
add([(5, 9), (5, 9), (5, 9)])
add([(10, 20), (0, 4), (12, 13), (2, 15), (30, 31)])
add([(1, 9), (2, 8), (3, 7), (4, 6)])
# hidden: small
add([(0, 1)])
add([(0, 5), (5, 10), (0, 10), (3, 4)])
add([rnd_seg(0, 10) for _ in range(8)])
add([rnd_seg(0, 30) for _ in range(40)])
add([rnd_seg(0, 1000) for _ in range(500)])
add([rnd_seg(0, MAXC) for _ in range(3000)])
add([rnd_seg(0, 10**4) for _ in range(10000)])
add([rnd_seg(0, 100) for _ in range(5000)])
# hidden: maximum size (most paints span a large part of the wall: painting piece by piece is too slow)
N, H = MAXN, MAXN // 2


def wide(k):
    return [(ri(0, MAXC // 4), ri(3 * MAXC // 4, MAXC)) for _ in range(k)]


add([rnd_seg(0, MAXC) for _ in range(N)])
s = wide(N)
add(s)
s.sort(key=lambda t: t[1] - t[0])                                         # short first: long ones bury them
add(s)
s.sort(key=lambda t: t[0] - t[1])                                         # long first: nested windows stay visible
add(s)
add([(i * 2, MAXC - i * 2) for i in range(N)])                            # nested, outer first
add([(MAXC // 2 - 10**5 - i * 2, MAXC // 2 + 10**5 + i * 2) for i in range(N)])   # nested, inner first
add(wide(N - 1) + [(0, MAXC)])                                            # the last paint covers everything
s = wide(N)
for i in range(0, N, 1000):                                               # a few short paints on top
    s[i] = rnd_seg(0, MAXC, 1)
add(s)
s = wide(H) + [rnd_seg(0, MAXC) for _ in range(H)]
random.shuffle(s)
add(s)
add([(0, MAXC)] * H)                                                      # only the last one is visible
add([(i * 6, i * 6 + 1000) for i in range(H)])                            # overlapping staircase
add([(MAXC - i * 6 - 1000, MAXC - i * 6) for i in range(H)])              # staircase the other way
add([rnd_seg(0, 2000) for _ in range(H)])                                 # many equal endpoints
add([(x, x + ri(1, 10)) for x in (ri(0, MAXC - 10) for _ in range(H))])   # tiny paints

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
