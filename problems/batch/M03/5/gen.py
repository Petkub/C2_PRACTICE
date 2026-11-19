# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(43005)
MAXN, MAXV = 5000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, c, s):
    n = len(c)
    assert 1 <= k <= n <= MAXN and len(s) == n
    assert all(0 <= x <= MAXV for x in c) and all(0 <= x <= MAXV for x in s)
    tests.append(f"{n} {k}\n" + " ".join(map(str, c)) + "\n" + " ".join(map(str, s)) + "\n")


def blocks(n, gap_lo, gap_hi, clo=MAXV // 2):
    c, i = [], 0
    while len(c) < n:
        g = ri(gap_lo, gap_hi)
        c += [ri(clo, MAXV) for _ in range(g)] + [0]
    c = c[:n]
    s = [ri(MAXV // 3, MAXV) for _ in range(n)]
    return c, s


def rnd(n, clo, chi, slo, shi, zero=0.0):
    c = [0 if random.random() < zero else ri(clo, chi) for _ in range(n)]
    s = [ri(slo, shi) for _ in range(n)]
    return c, s


add(2, [1, 5, 5, 4, 0, 4, 4], [12, 1, 7, 1, 17, 27, 4])
add(4, [3, 1, 4, 1], [5, 9, 2, 6])
add(5, [1, 4, 0, 4, 2, 4], [26, 21, 5, 3, 18, 18])
add(3, [40000, 1, 40000, 2, 30000], [900000, 1000000, 5, 1000000, 999999])
add(3, [2, 0, 4, 5, 0, 4, 0], [19, 6, 15, 21, 17, 13, 24])


add(1, [MAXV], [MAXV])
add(1, [MAXV, MAXV], [5, 7])
add(2, [MAXV, 1, MAXV], [MAXV, MAXV, MAXV])
for n, k, chi, shi, z in [(8, 3, 10, 50, 0.2), (16, 8, MAXV, MAXV, 0.4), (200, 120, MAXV, MAXV, 0.3)]:
    c, s = rnd(n, 0, chi, 0, shi, z)
    add(k, c, s)

for n, k, lo, hi in [(14, 6, 4, 6), (20, 9, 5, 8), (150, 77, 20, 50)]:
    c, s = blocks(n, lo, hi)
    add(k, c, s)


c, s = rnd(MAXN, 0, MAXV, 0, MAXV, 0.3)
add(3, c, s)
c, s = blocks(MAXN, 300, 900)
add(40, c, s)


N = MAXN
c, s = rnd(N, 0, MAXV, 0, MAXV)
add(N, c, s)
c, s = rnd(N, 0, MAXV, 0, MAXV, 0.5)
add(N // 2, c, s)
c, s = rnd(N, 0, 1000, 0, MAXV)
add(N // 2, c, s)
c, s = rnd(N, MAXV, MAXV, MAXV, MAXV)
add(N, c, s)
c, s = rnd(N, MAXV - 1000, MAXV, 0, MAXV)
add(N - 1, c, s)
c, s = rnd(N, 30000, 70000, 0, MAXV, 0.2)
add(N // 3, c, s)
for k, lo, hi in [(N // 4 + 17, 300, 900), (N // 2 + 1, 200, 700), (2 * N // 3 - 3, 400, 1200), (N - 20, 250, 600),
                  (100, 300, 900), (N // 3 + 5, 1, 3000)]:
    c, s = blocks(N, lo, hi)
    add(k, c, s)
c, s = rnd(N, 0, 1500, MAXV // 2, MAXV)
add(3 * N // 4, c, s)
c = [ri(0, 30) if i < N // 2 else ri(MAXV // 2, MAXV) for i in range(N)]
s = [ri(0, MAXV) for _ in range(N)]
add(N // 2 + 300, c, s)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
