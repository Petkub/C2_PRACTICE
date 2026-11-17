# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180011)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXV for v in a)
    assert all(a[i] <= a[i + 1] for i in range(n - 1))
    assert all(1 <= l <= r <= n for l, r in qs)
    t = f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def from_runs(lens, step=3, start=1):
    """codes for the given run lengths: each run's code is larger than the previous one"""
    a, v = [], start
    for k in lens:
        a.extend([v] * k)
        v += ri(1, step)
    return a


def runs_until(n, lo, hi):
    lens, total = [], 0
    while total < n:
        lens.append(ri(lo, hi))
        total += lens[-1]
    lens[-1] -= total - n
    return lens


def rnd_q(n):
    l = ri(1, n)
    return (l, ri(l, n))


def long_q(n):
    l = ri(1, max(1, n // 10))
    return (l, ri(max(l, n - n // 10), n))


def inside_q(lens, starts):
    """both ends inside one run (often strictly inside)"""
    k = ri(0, len(lens) - 1)
    l = ri(starts[k], starts[k] + lens[k] - 1)
    return (l, ri(l, starts[k] + lens[k] - 1))


def queries(n, q, long_frac, lens=None, inside_frac=0.0):
    starts = [1]
    for k in (lens or [])[:-1]:
        starts.append(starts[-1] + k)
    qs = []
    for _ in range(q):
        x = random.random()
        if lens and x < inside_frac:
            qs.append(inside_q(lens, starts))
        elif x < inside_frac + long_frac:
            qs.append(long_q(n))
        else:
            qs.append(rnd_q(n))
    return qs


# samples
add([3, 3, 3, 5, 5, 8, 8, 8, 8, 9, 9, 9], [(1, 12), (2, 7), (4, 11), (7, 12), (6, 9)])
add([10, 20, 30, 40, 50, MAXV], [(1, 6), (2, 4), (6, 6)])
add([1, 1, 2, 4, 4, 4, 6, 6, 7, 7, 7], [(1, 11), (2, 8), (3, 3), (4, 7), (1, 2), (7, 11)])
add([2, 2, 5, 5, 5, 6, 6, 9, 9, 9, 9], [(3, 11), (1, 7), (6, 9), (2, 10), (3, 5)])
add([MAXV], [(1, 1)])
# hidden: small
a = sorted(ri(1, 4) for _ in range(12))
add(a, [(l, r) for l in range(1, 13) for r in range(l, 13)])             # every question
lens = runs_until(300, 1, 6)
add(from_runs(lens), queries(300, 500, 0.3, lens, 0.3))
lens = [4] * 250
add(from_runs(lens, 10), queries(1000, 1000, 0.4, lens, 0.1))           # equal runs: ties everywhere
add([777] * 2000, queries(2000, 2000, 0.3))                              # one code
lens = runs_until(3000, 1, 100)
add(from_runs(lens), queries(3000, 3000, 0.3, lens, 0.3))
add(sorted(random.sample(range(1, MAXV + 1), 3000)), queries(3000, 3000, 0.3))   # all different
# hidden: maximum size (codes kept short so the input stays <= 3 MB)
N, Q = MAXN, 110_000
lens = runs_until(N, 1, 5)
add(from_runs(lens), queries(N, Q, 0.9))
lens = [3] * (N // 3) + [2]
add(from_runs(lens), queries(N, Q, 0.9))                                # ties everywhere
add([7] * N, queries(N, Q, 0.9))                                         # one code
lens = runs_until(N, 500, 1500)
add(from_runs(lens), queries(N, Q, 0.5, lens, 0.3))
lens = runs_until(N, 1, 2)
add(from_runs(lens), queries(N, Q, 0.9))
add(list(range(1, N + 1)), queries(N, Q, 0.9))                           # all different
lens, k = [], 1
while sum(lens) + k <= N:
    lens.append(k)
    k += 1
lens.append(N - sum(lens))
add(from_runs(sorted(lens)), queries(N, Q, 0.7, lens, 0.1))              # longer and longer runs
add(from_runs(sorted(lens, reverse=True)), queries(N, Q, 0.7, sorted(lens, reverse=True), 0.1))
lens = runs_until(N - 40 * 400, 1, 4)
for _ in range(40):
    lens.insert(ri(0, len(lens)), 400)                                   # several equal longest runs
add(from_runs(lens), queries(N, Q, 0.8, lens, 0.05))
lens = runs_until(N // 2, 1, 6) + [N // 2]                               # one huge run at the end
add(from_runs(lens), [(ri(1, N // 2), ri(N // 2 + 1, N)) for _ in range(Q)])
lens = ([7] + [2] * 6) * (N // 19) + [N % 19]                            # many tied runs of 7
add(from_runs(lens), queries(N, Q, 0.8, lens, 0.05))
lens = runs_until(N, 20_000, 60_000)
add(from_runs(lens), queries(N, Q, 0.2, lens, 0.6))                      # mostly inside one long run

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
