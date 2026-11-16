# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1103)
MAXN, MAXM = 1_000_000, 200_000
tests = []

def add(n, k, jobs):
    m = len(jobs)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and 1 <= k <= MAXM
    assert all(1 <= l <= r <= n for l, r in jobs)
    lines = [f"{n} {m} {k}"] + [f"{l} {r}" for l, r in jobs]
    tests.append("\n".join(lines) + "\n")

def rand_jobs(n, m, mode):
    jobs = []
    for _ in range(m):
        if mode == "long":
            l = random.randint(1, max(1, n // 10))
            r = random.randint(min(n, n - n // 10), n)
        elif mode == "short":
            l = random.randint(1, n)
            r = min(n, l + random.randint(0, 20))
        else:
            l, r = sorted((random.randint(1, n), random.randint(1, n)))
        jobs.append((l, r))
    return jobs

def layers(n, jobs):
    d = [0] * (n + 2)
    for l, r in jobs:
        d[l] += 1
        d[r + 1] -= 1
    out, cur = [], 0
    for i in range(1, n + 1):
        cur += d[i]
        out.append(cur)
    return out

def median_k(n, jobs):       # a K that splits the cells into two non-trivial groups
    ls = sorted(layers(n, jobs))
    return max(1, ls[len(ls) // 2])

# samples
add(10, 2, [(1, 5), (3, 8), (5, 10)])
add(5, 3, [(1, 5), (2, 4)])
add(1, 1, [(1, 1)])
add(8, 1, [(2, 3), (6, 6)])
add(6, 4, [(1, 6), (2, 6), (1, 5), (3, 4), (6, 6)])
# hidden: small
add(1, 3, [(1, 1)] * 3)
add(7, 1, [(7, 7)])
add(7, 2, [(1, 1), (7, 7), (1, 7)])
for n, m in [(20, 10), (100, 60), (1000, 500), (5000, 3000), (20000, 15000)]:
    jobs = rand_jobs(n, m, "any")
    add(n, median_k(n, jobs), jobs)
jobs = rand_jobs(30000, 20000, "long")
add(30000, 20000, jobs)
# hidden: maximum size
for mode in ["long", "any", "long"]:
    jobs = rand_jobs(MAXN, MAXM, mode)
    add(MAXN, median_k(MAXN, jobs), jobs)
add(MAXN, MAXM, [(1, MAXN)] * MAXM)                          # every cell has exactly M layers
add(MAXN, MAXM, [(1, MAXN)] * (MAXM - 1) + [(2, MAXN)])      # cell 1 misses one layer
jobs = [(random.randint(1, 1000), random.randint(MAXN - 1000, MAXN)) for _ in range(MAXM)]
add(MAXN, MAXM - 7, jobs)
add(MAXN, 1, rand_jobs(MAXN, MAXM, "short"))
jobs = rand_jobs(MAXN, MAXM, "long")
add(MAXN, MAXM, jobs[:-1] + [(MAXN, MAXN)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
