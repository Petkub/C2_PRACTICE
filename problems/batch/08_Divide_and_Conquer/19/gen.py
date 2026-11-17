# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(131804)
MAXN = 18
MAXQ = 200_000
MAXV = 10**6
tests = []


def add(n, a, qs):
    assert 0 <= n <= MAXN and len(a) == 1 << n
    assert all(1 <= v <= MAXV for v in a)
    assert 1 <= len(qs) <= MAXQ and all(0 <= q <= n for q in qs)
    tests.append(f"{n}\n{' '.join(map(str, a))}\n{len(qs)}\n{' '.join(map(str, qs))}\n")


def rnd(n, hi):
    return [random.randint(1, hi) for _ in range(1 << n)]


def perm(n):
    a = list(range(1, (1 << n) + 1))
    random.shuffle(a)
    return a


def queries(n, cnt, lo=0):
    return [random.randint(lo, n) for _ in range(cnt)]


# samples
add(3, [5, 1, 4, 2, 2, 8, 3, 6], [2, 1, 3, 0])
add(2, [2, 2, 1, 2], [2, 1])
add(0, [42], [0, 0])
add(3, [1, 2, 3, 4, 5, 6, 7, 8], [3, 3, 1, 2])
add(4, [9, 4, 7, 4, 1, 3, 3, 8, 6, 2, 5, 7, 10, 1, 4, 6], [1, 4, 2, 3, 0, 4])
# hidden: small (the brute force reverses and counts every pair)
add(1, [3, 5], [1, 0, 1, 1])
add(2, [1, 1, 1, 1], [2, 1, 0])
add(3, rnd(3, 3), queries(3, 50))
add(4, perm(4), queries(4, 100))
add(5, rnd(5, 4), queries(5, 200))
add(6, rnd(6, 1000), queries(6, 200))
add(8, rnd(8, 3), queries(8, 300))
add(8, perm(8), queries(8, 300, 6))
add(10, rnd(10, 50), queries(10, 100))
add(10, sorted(rnd(10, MAXV)), queries(10, 100))
# hidden: large
N = MAXN
add(N, rnd(N, MAXV), queries(N, MAXQ))
add(N, perm(N), queries(N, MAXQ))
add(N, rnd(N, 2), queries(N, MAXQ))                       # many equal values
add(N, rnd(N, 20), queries(N, MAXQ))
add(N, [7] * (1 << N), queries(N, MAXQ))                  # all equal: always 0
add(N, list(range(1, (1 << N) + 1)), [N] * MAXQ)           # sorted / reversed, maximum answer
add(N, list(range(1 << N, 0, -1)), queries(N, MAXQ, N - 3))
add(N, rnd(N, MAXV), [random.choice([0, 1]) for _ in range(MAXQ)])
add(N, rnd(N, 1000), [N - 1 if i % 2 else N for i in range(MAXQ)])
add(N, [MAXV - (i % 3) for i in range(1 << N)], queries(N, MAXQ))
add(N, sorted(rnd(N, 5000)), queries(N, MAXQ))
add(17, rnd(17, MAXV), queries(17, MAXQ))
add(N, [1 + (i >> 9) for i in range(1 << N)], queries(N, MAXQ))   # sorted runs of equal values

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
