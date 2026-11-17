# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(90404)
MAXN, MAXC = 8000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(pts):
    n = len(pts)
    assert 1 <= n <= MAXN
    assert all(0 <= x <= MAXC and 0 <= y <= MAXC for x, y in pts)
    tests.append(f"{n}\n" + "".join(f"{x} {y}\n" for x, y in pts))


def rnd(n, lo=0, hi=MAXC):
    return [(ri(lo, hi), ri(lo, hi)) for _ in range(n)]


def clusters(n, k, spread):
    cs = rnd(k, spread, MAXC - spread)
    pts = []
    for _ in range(n):
        cx, cy = random.choice(cs)
        pts.append((cx + ri(-spread, spread), cy + ri(-spread, spread)))
    return pts


add([(0, 0), (3, 0), (0, 4), (3, 4)])
add([(0, 0), (1, 0), (3, 0)])
add([(7, 7)])
add([(5, 5), (5, 5), (6, 7)])
add([(0, 0), (MAXC, MAXC), (0, MAXC), (MAXC, 0), (MAXC // 2, MAXC // 2)])

add([(0, 0), (MAXC, MAXC)])
add(rnd(8, 0, 20))
add(rnd(50))
add([(0, 0)] * 30)
add(rnd(300, 0, 100))
add(clusters(1000, 5, 1000))
add([(ri(0, MAXC), 0) for _ in range(2000)])

N = MAXN
add(rnd(N))
add(rnd(N))
add(clusters(N, 2, 10))
add(clusters(N, 40, 5000))
add([(ri(0, 1) * MAXC, ri(0, 1) * MAXC) for _ in range(N)])
add([(i * 125, ri(0, MAXC)) for i in range(N)])
add([((i % 90) * 11111, (i // 90) * 11111) for i in range(N)])
add([(i * 125, i * 125) for i in range(N)])
pts = [(0, 0)] * (N // 2) + [(MAXC, MAXC)] * (N - N // 2)
random.shuffle(pts)
add(pts)
add(rnd(N, 0, 50))
pts = []
x, y = 0, 0
for i in range(N):
    x = min(MAXC, max(0, x + ri(-30000, 30000)))
    y = min(MAXC, max(0, y + ri(-30000, 30000)))
    pts.append((x, y))
add(pts)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
