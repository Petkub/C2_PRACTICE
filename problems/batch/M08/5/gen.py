# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4205)
MAXN, MAXS, MAXK = 200000, 10**12, 10**9
tests = []


def add(g, k, s):
    n = len(s)
    assert 2 <= n <= MAXN and 1 <= g <= n - 1 and 1 <= k <= MAXK
    assert all(0 <= x <= MAXS for x in s)
    assert sum(1 for x in s[:-1] if x > s[-1]) >= g
    tests.append(f"{n} {g} {k}\n" + " ".join(map(str, s)) + "\n")


def rnd(n, lo, hi):
    r = random.random
    return [lo + int(r() * (hi - lo + 1)) for _ in range(n)]


def make(n, g, k, others, me):
    s = others[: n - 1]
    random.shuffle(s)
    return g, k, s + [me]


add(2, 2, [9, 5, 7, 3, 1])
add(1, 3, [12, 6, 9, 0])
add(1, 1, [MAXS, MAXS - 10])
add(3, 4, [20, 20, 20, 20, 4, 4])
add(2, 10, [50, 50, 30, 10, 10])

add(1, 1, [1, 0])
add(1, 7, [8, 3, 1])
add(2, 5, [11, 11, 11, 3, 3, 1])
add(3, 4, [30, 25, 25, 25, 25, 9, 2])
add(*make(10, 3, 6, rnd(9, 50, 120), 20))
add(*make(50, 10, 13, rnd(49, 0, 3000), 100))
add(*make(300, 150, 1, rnd(299, 0, 3000), 0))
add(*make(1000, 1, 999999937, rnd(999, 0, MAXS), 0))
add(*make(1000, 400, 123456789, rnd(999, 0, MAXS), 5 * 10**11))
add(*make(2000, 1999, MAXK, [MAXS] * 1999, 0))

N = MAXN
add(*make(N, 1, 1, rnd(N - 1, 0, MAXS), 0))
add(*make(N, N // 2, 1, rnd(N - 1, 0, MAXS), 0))
add(*make(N, N - 1, 3, [MAXS] * (N - 1), 0))
add(*make(N, 1000, 99991, rnd(N - 1, 0, MAXS), 0))
add(*make(N, 70000, 12345, rnd(N - 1, 0, MAXS), 7))
add(*make(N, 1, 30000, [MAXS - i for i in range(N - 1)], 0))
add(*make(N, 5, 7, rnd(N - 1, MAXS - 10**9, MAXS), 10**9))
add(*make(N, 50000, 100003, [random.choice([MAXS, MAXS - 1, 10**11 + 1, 10**11]) for _ in range(N - 1)], 5))
add(*make(N, 100, 99, rnd(N - 5000, MAXS // 2, MAXS) + rnd(5000, 0, 10), 10))
g = 20000
others = [MAXS] * g + rnd(N - 1 - g, 0, MAXS)
add(*make(N, g, 199, others, 1))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
