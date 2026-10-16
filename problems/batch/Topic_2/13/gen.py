# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20213)
MAXN, MAXA, MAXC, MAXB = 200_000, 10**9, 10**9, 10**18
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def add(B, a, c):
    n = len(a)
    assert 1 <= n <= MAXN and len(c) == n
    assert 0 <= B <= MAXB
    assert all(1 <= x <= MAXA for x in a)
    assert all(1 <= x <= MAXC for x in c)
    tests.append(f"{n} {B}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, c)) + "\n")


def cost(m, a, c):
    return sum(ci * (m - ai) for ai, ci in zip(a, c) if ai < m)


# samples
add(10, [3, 5, 4], [2, 1, 3])
add(MAXB, [1, 1], [1, 1])
add(0, [7, 2, 9], [5, 5, 5])
add(MAXB, [MAXA], [MAXC])
add(6, [4, 1, 1, 8], [1, 3, 2, 1])
add(25, [6, 2, 9, 3, 5], [2, 1, 4, 3, 1])
# hidden: small (the brute raises one level at a time, so answers stay small here)
add(0, [5], [3])
add(2, [5], [3])                               # not enough for even one level
add(1000, [1, MAXA], [1, 1])
add(7, [2, 2, 2], [1, 2, 4])                   # exactly 7 coins for one level of all
a, c = rnd(10, 1, 20), rnd(10, 1, 5)
add(cost(25, a, c), a, c)                      # the budget is exactly enough for 25
a, c = rnd(50, 1, 1000), rnd(50, 1, 100)
add(cost(700, a, c) - 1, a, c)                 # one coin short of 700
a, c = rnd(200, 1, 10**5), rnd(200, 1, 10**4)
add(ri(0, 10**10), a, c)
a, c = rnd(1000, 999_000, 10**6), rnd(1000, 1, MAXC)
add(ri(10**12, 10**14), a, c)
# hidden: overflow traps with few characters
add(MAXB, [1, 2], [MAXC, MAXC])
add(MAXB, [MAXA, 1, 7], [MAXC, MAXC - 1, MAXC])
# hidden: maximum size (most answers are far above min a_i)
N = MAXN
H = 150_000                                     # smaller tests keep the total size under 40 MB
add(MAXB, rnd(H, 1, 3 * 10**5), [MAXC] * H)     # c * (m - a) overflows during the search
add(MAXB, rnd(H, 1, 10**5), [MAXC] * H)
add(MAXB, rnd(H, 1, MAXA), rnd(H, 1, 10))
a = list(range(1, N + 1))
random.shuffle(a)
add(MAXB, a, [1] * N)                           # answer about 5 * 10^12
add(MAXB, [MAXA] * H, rnd(H, 1, 100))
add(ri(10**17, MAXB), rnd(N, 1, MAXA), rnd(N, 1, 100))
add(ri(10**16, 10**17), rnd(H, 1, MAXA), rnd(H, 1, 10))
a, c = rnd(N, 1, MAXA), rnd(N, 1, 10)
add(cost(3 * 10**10, a, c), a, c)               # exactly enough for 3 * 10^10
a, c = rnd(N, 1, MAXA), rnd(N, 1, 3)
add(cost(5 * 10**10, a, c) - 1, a, c)           # one coin short of 5 * 10^10
a = [1] + rnd(H - 1, MAXA // 2, MAXA)
c = [1] + rnd(H - 1, 2, 1000)
add(MAXB // 3, a, c)                            # one cheap low character
a = sorted(rnd(N, 1, MAXA))
add(MAXB, a, sorted(rnd(N, 1, 1000), reverse=True))
add(MAXB, rnd(H, 1, MAXA), rnd(H, 1, 50))
add(MAXC - 1, [5] * N, [MAXC] * N)              # cannot afford a single level
add(MAXB, rnd(H, MAXA - 10**6, MAXA), [1] * H)
add(10**17, rnd(N, 1, 10**6), rnd(N, 1, 10))
add(MAXB, sorted(rnd(N, 1, 10**6), reverse=True), rnd(N, 1, 5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
