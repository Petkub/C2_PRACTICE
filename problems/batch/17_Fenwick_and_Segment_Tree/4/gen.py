# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(170103)
MAXN, MAXQ, MAXS = 200_000, 200_000, 10_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(s, ops):
    n, q = len(s), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXS for v in s)
    lines = []
    for t, x, y in ops:
        if t == 1:
            assert 1 <= x <= n and 1 <= y <= MAXS
        else:
            assert t == 2 and 1 <= x <= y <= n
        lines.append(f"{t} {x} {y}")
    tests.append(f"{n} {q}\n" + " ".join(map(str, s)) + "\n" + "\n".join(lines) + "\n")


def any_rng(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_rng(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def ops_of(n, q, upd, value, rng):
    """upd: share of updates; value() -> a new skill; rng() -> (l, r)"""
    return [(1, ri(1, n), value()) if random.random() < upd else (2,) + rng() for _ in range(q)]


# samples
add([1, 3, 2, 6], [(2, 1, 3), (1, 2, 6), (2, 2, 4), (2, 3, 3)])
add([5, 5, 5], [(2, 1, 3), (1, 2, 1), (2, 1, 3)])
add([1, MAXS], [(2, 1, 2), (1, 1, MAXS), (2, 1, 2)])
add([3, 1, 4, 1, 5], [(2, 1, 5), (1, 3, 9), (2, 2, 4), (2, 1, 5)])
add([MAXS] * 3 + [1] * 3, [(2, 1, 6), (2, 3, 4)])
# hidden: small (the brute force checks these)
for n, q, smax, upd in ((1, 5, 10, 0.4), (3, 20, 5, 0.3), (8, 60, 100, 0.3), (30, 300, MAXS, 0.3),
                        (100, 800, 9, 0.4), (300, 1500, MAXS, 0.3), (250, 1500, 2, 0.5)):
    s = [ri(1, smax) for _ in range(n)]
    add(s, ops_of(n, q, upd, lambda: ri(1, smax), lambda: any_rng(n)))
n = 300                                                     # only the two extreme skills
s = [random.choice((1, MAXS)) for _ in range(n)]
add(s, ops_of(n, 1500, 0.3, lambda: random.choice((1, MAXS)), lambda: any_rng(n)))
# hidden: maximum size (inputs kept near 3 MB)
N = MAXN
s = [ri(1, 9) for _ in range(N)]
add(s, ops_of(N, 120_000, 0.3, lambda: ri(1, 9), lambda: long_rng(N, 50)))
s = [random.choice((1, MAXS)) for _ in range(N)]
add(s, ops_of(N, 120_000, 0.2, lambda: random.choice((1, MAXS)), lambda: long_rng(N, 100)))
s = [MAXS] * N                                              # everybody equal: 0 until the updates break it
add(s, ops_of(N, 110_000, 0.05, lambda: random.choice((MAXS, MAXS, 1)), lambda: long_rng(N, 1000)))
s = [ri(1, MAXS) for _ in range(N)]
add(s, ops_of(N, 100_000, 0.3, lambda: ri(1, MAXS), lambda: long_rng(N, 5000)))
s = [ri(1, 99) for _ in range(N)]                           # every question asks the whole row
add(s, [(2, 1, N)] * 120_000)
s = [1] * (N // 2) + [MAXS] * (N // 2)                      # the largest possible answer, close to 10^18
add(s, [(2, 1, N) if k % 4 else (1, ri(1, N // 2), 1) for k in range(110_000)])
n = 160_000
s = [1] * (n // 2) + [MAXS] * (n // 2)
add(s, ops_of(n, 110_000, 0.1, lambda: random.choice((1, MAXS)), lambda: long_rng(n, 3000)))
s = [ri(1, 1000) for _ in range(N)]                         # half of the commands are updates
add(s, ops_of(N, 120_000, 0.5, lambda: ri(1, 1000), lambda: long_rng(N, 200)))
s = [ri(9_000, MAXS) for _ in range(N)]
add(s, ops_of(N, 100_000, 0.2, lambda: ri(1, MAXS), lambda: long_rng(N, 20_000)))
# hidden: many short questions
n = 5000
s = [ri(1, MAXS) for _ in range(n)]
add(s, ops_of(n, MAXQ, 0.3, lambda: ri(1, MAXS), lambda: any_rng(n)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
