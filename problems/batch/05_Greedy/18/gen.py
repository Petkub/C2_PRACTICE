# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(51818)
MAXN = 200_000
MAXC = 10**9
MAXB = 10**15
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, b, c):
    n = len(c)
    assert 1 <= k <= n <= MAXN and 1 <= b <= MAXB
    assert all(1 <= x <= MAXC for x in c)
    tests.append(f"{n} {k} {b}\n" + " ".join(map(str, c)) + "\n")


def cheapest(c, k):
    return sum(sorted(c)[:k])


def tight(k, c, slack=0):
    add(k, max(1, cheapest(c, k) + slack), c)


def cheap_end(n, share):
    cut = int(n * (1 - share))
    return [ri(MAXC // 2, MAXC) for _ in range(cut)] + [ri(1, MAXC // 1000) for _ in range(n - cut)]


def waves(n, w):
    return [ri(1, MAXC // 100) if (i // w) % 2 else ri(MAXC // 10, MAXC) for i in range(n)]


def lonely_cheap(n, every):
    return [ri(1, 10) if i % every == every - 1 else ri(MAXC // 2, MAXC) for i in range(n)]


add(2, 7, [8, 5, 6, 4, 7, 1])
add(2, 6, [8, 7, 1, 4, 2, 4])
add(3, 10, [5, 4, 3, 6])
add(3, 10, [3, 3, 4])
add(3, 7, [8, 5, 5, 4, 5, 1, 1])
add(1, 5, [5])

add(1, 4, [5])
add(2, 9, [5, 6, 3, 1])
tight(4, [9, 1, 8, 2, 7, 3, 6, 4, 5, 5, 4, 6, 3, 7, 2, 8], 1)
tight(5, [ri(1, 30) for _ in range(14)], 3)
tight(3, [20, 1, 1, 1, 20, 20, 2, 2, 2, 20, 20, 1], 0)
add(5, 24, [ri(5, 9) for _ in range(12)])

tight(1000, [ri(1, MAXC) for _ in range(2500)], 10**6)
tight(700, cheap_end(3000, 0.4))
tight(1, [ri(1, MAXC) for _ in range(3000)], 0)

c = [ri(1, MAXC) for _ in range(MAXN)]
tight(MAXN // 2, c, 0)
tight(MAXN // 2, c, 10**12)
tight(60_000, cheap_end(MAXN, 0.4))
tight(100_000, cheap_end(MAXN, 0.6), 5 * 10**8)
tight(50_000, waves(MAXN, 1000))
tight(30_000, lonely_cheap(MAXN, 5), 10**9)
tight(39_000, lonely_cheap(MAXN, 5), 0)
tight(150_000, list(range(MAXC, MAXC - MAXN * 4000, -4000)))
add(MAXN, MAXN * MAXC, [MAXC] * MAXN)
tight(MAXN - 5, [ri(MAXC - 10, MAXC) for _ in range(MAXN)], 0)
c = [ri(1, MAXC) for _ in range(MAXN)]
add(80_000, cheapest(c, 80_000) - 1, c)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
