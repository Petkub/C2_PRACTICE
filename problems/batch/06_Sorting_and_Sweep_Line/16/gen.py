# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(40114)
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


def rnd_rect(lo, hi, minside=1, maxside=None):
    maxside = maxside or (hi - lo)
    x1 = ri(lo, hi - minside)
    x2 = min(hi, x1 + ri(minside, maxside))
    y1 = ri(lo, hi - minside)
    y2 = min(hi, y1 + ri(minside, maxside))
    return (x1, y1, x2, y2)


def grid_touch(k, size):
    return [(i * size, j * size, (i + 1) * size, (j + 1) * size) for i in range(k) for j in range(k)]


add([(0, 0, 4, 4), (2, 2, 6, 6), (4, 4, 8, 8)])
add([(0, 0, 2, 2), (3, 0, 5, 2), (1, 1, 4, 3)])
add([(0, 0, MAXC, MAXC)])
add([(0, 0, 1, 1), (2, 2, 3, 3), (5, 0, 6, 9)])
add([(1, 1, 3, 3), (1, 1, 3, 3), (3, 3, 5, 5), (0, 2, 9, 4), (4, 0, 5, 1)])
add([(0, 4, 10, 6), (4, 0, 6, 10), (6, 6, 9, 9), (0, 0, 3, 3)])

add([(5, 5, 6, 6), (6, 6, 7, 7)])
add(grid_touch(3, 2))
add([rnd_rect(0, 10) for _ in range(8)])
add([rnd_rect(0, 20) for _ in range(30)])
add([rnd_rect(0, 100) for _ in range(150)])
add([rnd_rect(0, MAXC, 1, MAXC // 3) for _ in range(250)])
add([rnd_rect(0, 50, 1, 5) for _ in range(300)])

N = MAXN
add([rnd_rect(0, MAXC) for _ in range(N)])
add([rnd_rect(0, MAXC, 1, MAXC // 4) for _ in range(N)])
add([rnd_rect(0, MAXC, 1, MAXC // 20) for _ in range(N)])
add([(0, 0, MAXC, MAXC)] * N)
s = []
for i in range(N):
    s.append((i * 200_000, i * 200_000, (i + 1) * 200_000, (i + 1) * 200_000))
random.shuffle(s)
add(s)
s = grid_touch(54, 18_000_000)
random.shuffle(s)
add(s)
s = []
for i in range(N):
    a = ri(0, MAXC - 10**6)
    b = ri(10**5, 10**6)
    s.append((0, a, MAXC, a + b) if i % 2 else (a, 0, a + b, MAXC))
add(s)
add([rnd_rect(0, 1000, 1, 300) for _ in range(N)])
s = []
for i in range(N):
    x = ri(0, 999) * 10**6
    y = ri(0, 999) * 10**6
    s.append((x, y, x + 10**6 * ri(1, 3), y + 10**6 * ri(1, 3)))
s = [(a, b, min(c, MAXC), min(d, MAXC)) for (a, b, c, d) in s]
add(s)
s = [(ri(0, MAXC // 2), ri(0, MAXC // 2), ri(MAXC // 2, MAXC), ri(MAXC // 2, MAXC)) for _ in range(N)]
for i in range(0, N, 3):
    s[i] = rnd_rect(0, MAXC // 2 - 1, 1, MAXC // 4)
add(s)
s = [(i * 100_000, 0, i * 100_000 + 2 * 10**8, MAXC - i * 100_000) for i in range(N)]
random.shuffle(s)
add(s)
add([rnd_rect(0, MAXC, MAXC // 3, MAXC) for _ in range(N)])


xl = random.sample(range(0, 10**7), N)
add([(xl[i], y, MAXC - ri(0, 10**7), y + ri(1, 10**6)) for i, y in enumerate(ri(0, MAXC - 10**6) for _ in range(N))])
xl = random.sample(range(0, 10**7), N)
s = [(xl[i], i * 190_000, MAXC - ri(0, 10**7), i * 190_000 + 380_000) for i in range(N)]
random.shuffle(s)
add(s)
xl = random.sample(range(0, 10**7), N)
s = [(xl[i], y, MAXC - ri(0, 10**7), y + ri(1, 3 * 10**6)) for i, y in enumerate(ri(0, MAXC - 3 * 10**6) for _ in range(N))]
for i in range(0, N, 50):
    s[i] = (ri(0, MAXC - 10**6), 0, 0, MAXC)
    s[i] = (s[i][0], 0, s[i][0] + ri(1, 10**6), MAXC)
add(s)

xl = random.sample(range(0, 10**7), N)
add([(xl[i], y, MAXC - ri(0, 10**7), y + ri(1, 2 * 10**7)) for i, y in enumerate(ri(0, MAXC - 2 * 10**7) for _ in range(N))])
xl = random.sample(range(0, 10**7), N)
s = []
for i in range(N):
    if i % 4 == 0:
        y = ri(4 * 10**8, 5 * 10**8)
        s.append((xl[i], y, MAXC - ri(0, 10**7), y + ri(10**8, 2 * 10**8)))
    else:
        y = ri(0, MAXC - 10**5)
        s.append((xl[i], y, MAXC - ri(0, 10**7), y + ri(1, 10**5)))
add(s)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
