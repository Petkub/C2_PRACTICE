# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(40404)
MAXN, MAXT = 150_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (deterministic, faster than randint)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(T, C, a, shuffle=True):
    a = list(a)
    if shuffle:
        random.shuffle(a)
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= T <= MAXT and 0 <= C <= n
    assert all(1 <= l <= r <= T for l, r in a)
    tests.append(f"{n} {T} {C}\n" + "".join(f"{l} {r}\n" for l, r in a))


def rnd(n, T, maxlen):
    out = []
    for _ in range(n):
        l = ri(1, T)
        out.append((l, min(T, l + ri(0, maxlen - 1))))
    return out


# samples
add(20, 0, [(3, 5), (4, 8), (12, 13)], False)
add(9, 0, [(3, 4), (6, 7)], False)
add(5, 0, [(1, 3), (2, 5)], False)
add(10**9, 2, [(1, 10**9), (5, 6)], False)
add(10, 1, [(1, 6), (2, 3), (5, 7), (9, 10), (9, 9)], False)
add(8, 1, [(1, 4), (4, 6), (6, 8)], False)
# hidden: small
add(1, 0, [(1, 1)])
add(1, 1, [(1, 1)])
add(MAXT, 0, [(1, MAXT - 1)])                           # only the last minute is free
add(MAXT, 0, [(2, MAXT)])                               # only the first minute is free
add(30, 1, rnd(8, 30, 6))
add(100, 2, rnd(40, 100, 10))
add(1000, 0, rnd(200, 1000, 5))
add(10**6, 5, rnd(1000, 10**6, 5000))
add(MAXT, 3, rnd(2000, MAXT, 10**6))
add(50, 4, [(1, 50)] * 4 + [(10, 20)])                   # load 4 everywhere, 5 on 10..20
add(1000, 1, [(i, i + 1) for i in range(1, 999, 2)])     # touching pieces with load 1
# hidden: large (T too big to walk minute by minute, N too big for O(N^2))
N = MAXN
add(MAXT, 0, rnd(N, MAXT, 2000))
add(MAXT, 2, rnd(N, MAXT, 20_000))
add(MAXT, 10, rnd(N, MAXT, 60_000))
add(N * 6000, 0, [(i * 6000 + 1, i * 6000 + 3000 + (i % 3)) for i in range(N)])  # many equal gaps: tie rule
add(MAXT, 1, [(ri(1, 1000), ri(MAXT - 1000, MAXT)) for _ in range(N)])        # load > 1 almost everywhere
add(MAXT, N - 1, [(1, MAXT)] * N)                        # load N everywhere: answer 0
add(MAXT, N // 2, [(i, MAXT - i + 1) for i in range(1, N + 1)])  # nested: the middle is the busiest
x = [ri(1, 100) * 6000 for _ in range(N)]
add(700_000, 3, [(v, v + 5999) for v in x])               # many equal event times
a = rnd(N - 1, MAXT, 30_000) + [(1, MAXT)]
add(MAXT, 1, a)                                          # one job covers everything
add(MAXT, 1, [(2 * i + 1, 2 * i + 2) for i in range(N)], False)    # load 1 up to 2N, then 0
add(200_000_000, 4, rnd(N, 200_000_000, 3000))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
