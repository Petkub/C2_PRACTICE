# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(40108)
MAXN, MAXC = 3000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(rs):
    n = len(rs)
    assert 1 <= n <= MAXN
    for (x1, y1, x2, y2) in rs:
        assert 0 <= x1 < x2 <= MAXC and 0 <= y1 < y2 <= MAXC
    tests.append(f"{n}\n" + "".join(f"{a} {b} {c} {d}\n" for (a, b, c, d) in rs))


def rnd_rect(lo, hi, minside=1):
    x1 = ri(lo, hi - minside)
    x2 = ri(x1 + minside, hi)
    y1 = ri(lo, hi - minside)
    y2 = ri(y1 + minside, hi)
    return (x1, y1, x2, y2)


def big_rect():
    """a carpet that spans most of the hall (the worst case for marking cells)"""
    return (ri(0, MAXC // 3), ri(0, MAXC // 3), ri(2 * MAXC // 3, MAXC), ri(2 * MAXC // 3, MAXC))


# samples
add([(0, 0, 4, 3), (2, 1, 6, 5)])
add([(0, 0, 10, 10), (2, 2, 5, 5), (10, 0, 12, 1)])
add([(0, 0, MAXC, MAXC)])
add([(1, 0, 3, 6), (0, 2, 4, 4), (1, 0, 3, 6)])
add([(0, 0, 2, 2), (5, 5, 7, 6), (2, 2, 3, 3), (6, 0, 9, 1)])
# hidden: small
add([(3, 4, 5, 9)])
add([(0, 0, 1, 1), (1, 0, 2, 1), (0, 1, 1, 2), (1, 1, 2, 2)])          # four touching unit squares
add([rnd_rect(0, 10) for _ in range(8)])
add([rnd_rect(0, 20) for _ in range(30)])
add([rnd_rect(0, 100) for _ in range(120)])
add([rnd_rect(0, MAXC) for _ in range(200)])
add([(i, i, 1000 - i, 1000 - i) for i in range(0, 500, 3)])             # nested squares
# hidden: maximum size
add([rnd_rect(0, MAXC) for _ in range(MAXN)])
add([big_rect() for _ in range(MAXN)])
add([big_rect() for _ in range(MAXN)])
add([(0, 0, MAXC, MAXC)] * MAXN)                                         # all identical, area 10^18
h = [(0, ri(0, MAXC - 10**5), MAXC, 0) for _ in range(MAXN // 2)]       # horizontal and vertical strips
h = [(0, y, MAXC, y + ri(1, 10**5)) for (_, y, _, _) in h]
v = [(x, 0, x + ri(1, 10**5), MAXC) for x in (ri(0, MAXC - 10**5) for _ in range(MAXN // 2))]
s = h + v
random.shuffle(s)
add(s)
s = [(ri(0, 5 * 10**8), 0, 0, MAXC) for _ in range(MAXN)]               # wide strips, heavy overlaps
s = [(x, ri(0, 4 * 10**8), x + ri(10**8, 5 * 10**8), 0) for (x, _, _, _) in s]
s = [(a, b, c, b + ri(10**8, 6 * 10**8)) for (a, b, c, _) in s]
add(s)
s = [(i * 150_000, i * 150_000, MAXC - i * 150_000, MAXC - i * 150_000) for i in range(MAXN)]
random.shuffle(s)
add(s)                                                                   # nested: the answer is the outer one
s = []
for i in range(MAXN):                                                    # staircase of overlapping squares
    x = i * 250_000
    s.append((x, x, x + 2 * 10**8, x + 2 * 10**8))
add(s)
add([rnd_rect(0, 1000) for _ in range(MAXN)])                            # many equal coordinates
add([rnd_rect(0, MAXC, 4 * 10**8) for _ in range(MAXN)])
s = [(ri(0, MAXC - 1), ri(0, MAXC - 1)) for _ in range(MAXN)]           # tiny disjoint-ish squares
add([(x, y, x + 1, y + 1) for (x, y) in s])
add([big_rect() for _ in range(MAXN - 1)] + [(0, 0, MAXC, MAXC)])
s = []                                                                   # wide and tall carpets crossing
for i in range(MAXN):
    a, b = ri(0, MAXC // 10), ri(9 * MAXC // 10, MAXC)
    c = ri(0, MAXC // 2)
    d = c + ri(MAXC // 3, MAXC // 2)
    s.append((a, c, b, d) if i % 2 else (c, a, d, b))
add(s)
add([big_rect() for _ in range(MAXN // 2)] + [rnd_rect(0, MAXC) for _ in range(MAXN // 2)])
# more maximum tests where marking every compressed cell is expensive
s = [(i * 100_000 + ri(0, 50_000), i * 120_000 + ri(0, 50_000), 0, 0) for i in range(MAXN)]
s = [(a, b, MAXC - (a // 2) - ri(0, 1000), MAXC - (b // 3) - ri(0, 1000)) for (a, b, _, _) in s]
random.shuffle(s)
add(s)                                                                   # nearly nested, every side distinct
add([rnd_rect(0, MAXC, 6 * 10**8) for _ in range(MAXN)])
s = []                                                                   # crossing bands, all edges distinct
for i in range(MAXN):
    a, b = ri(0, MAXC // 5), ri(4 * MAXC // 5, MAXC)
    c = ri(0, 2 * MAXC // 5)
    d = c + ri(MAXC // 2, 3 * MAXC // 5)
    s.append((a, c, b, d) if i % 2 else (c, a, d, b))
add(s)
add([(ri(0, MAXC // 2), ri(0, MAXC // 2), ri(MAXC // 2 + 1, MAXC), ri(MAXC // 2 + 1, MAXC)) for _ in range(MAXN)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
