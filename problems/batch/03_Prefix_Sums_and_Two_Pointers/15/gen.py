# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(31503)
MAXN = 100_000
MAXC = 10 ** 9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(pts):
    n = len(pts)
    assert 2 <= n <= MAXN
    assert all(0 <= a <= MAXC and 0 <= b <= MAXC for a, b in pts)
    assert len(set(pts)) == n
    tests.append(f"{n}\n" + " ".join(str(a) for a, b in pts) + "\n" + " ".join(str(b) for a, b in pts) + "\n")


def shuffled(pts):
    pts = sorted(set(pts))
    random.shuffle(pts)
    return pts


def fill(n, make):
    seen = set()
    out = []
    while len(out) < n:
        p = make()
        if p not in seen:
            seen.add(p)
            out.append(p)
    return shuffled(out)


def box(x1, x2, y1, y2):
    return lambda: (ri(x1, x2), ri(y1, y2))


def mix(parts):
    def make():
        r = random.random()
        for w, f in parts:
            if r < w:
                return f()
            r -= w
        return parts[-1][1]()
    return make


add([(8, 4), (2, 5), (7, 1), (5, 2), (6, 8)])
add([(5, 2), (2, 5), (1, 1), (3, 4)])
add([(12, 3), (5, 12), (4, 4), (3, 9), (2, 8), (8, 6), (7, 7)])
add([(300_000_000, 100_000_000), (100_000_000, 600_000_000), (MAXC, 700_000_000), (0, 0)])
add([(3, 1), (3, 9)])


add([(0, 0), (MAXC, MAXC)])
add(shuffled([(3, i * 2 + ri(0, 1)) for i in range(14)]))
add(fill(14, mix([(0.5, box(0, 5, 0, 5)), (1.0, box(6, 11, 6, 11))])))
add(fill(14, mix([(0.5, box(0, 5, 7, 12)), (1.0, box(6, 11, 0, 6))])))
add(shuffled([(ri(0, 10 ** 6) * 7 + i, 500) for i in range(15)]))
add(shuffled([(i, i) for i in range(1, 14)]))
add(fill(16, box(0, 2, 0, 20)))
add(shuffled([(i, 20 - i) for i in range(1, 14)]))
add(fill(13, mix([(0.5, lambda: (7, ri(0, 30))), (1.0, lambda: (ri(0, 30), 7))])))


add(fill(3000, box(0, 2000, 0, 2000)))
add(fill(4000, mix([(0.5, box(0, 10 ** 6, 2 * 10 ** 6, 3 * 10 ** 6)), (1.0, box(2 * 10 ** 6, 3 * 10 ** 6, 0, 10 ** 6))])))
add(shuffled([(123_456, i * 3 + ri(0, 2)) for i in range(5000)]))


N = MAXN
H = MAXC // 2
add(fill(N, box(0, MAXC, 0, MAXC)))
add(fill(N, mix([(0.6, box(0, H - 1, 0, H - 1)), (1.0, box(H, MAXC, H, MAXC))])))
add(fill(N, mix([(0.45, box(0, H - 1, H, MAXC)), (1.0, box(H, MAXC, 0, H - 1))])))
add(shuffled([(i * 10_000, i * 10_000) for i in range(N - 1)]))
add(shuffled([(i * 10_000, MAXC - i * 10_000) for i in range(N - 1)]))
add(shuffled([(i * 10_000 + ri(0, 9_000), 777_777_777) for i in range(N)]))
add(shuffled([(MAXC, i * 10_000 + ri(0, 9_999)) for i in range(N)]))
add(fill(N, lambda: (ri(0, 9) * (MAXC // 9), ri(0, MAXC))))
add(fill(N, box(0, 49_999, 0, 49_999)))
add(fill(N, mix([(0.7, box(0, 6 * 10 ** 8, 4 * 10 ** 8, MAXC)), (1.0, box(6 * 10 ** 8 + 1, MAXC, 0, 4 * 10 ** 8 - 1))])))
add(fill(N, mix([(0.5, lambda: (H, ri(0, MAXC))), (1.0, lambda: (ri(0, MAXC), H))])))
add(shuffled([(x, 0) for x in random.sample(range(MAXC + 1), N)]))
add(fill(N, mix([(0.5, lambda: (0, ri(1, MAXC))), (1.0, lambda: (ri(1, MAXC), 0))])))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
