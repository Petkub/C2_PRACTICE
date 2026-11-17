# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(30606)
MAXT, MAXN = 10 ** 6, 100_000
tests = []

def add(T, D, once, routine):
    assert 1 <= D <= T <= MAXT
    assert 0 <= len(once) <= MAXN and 0 <= len(routine) <= MAXN
    assert all(0 <= s < e <= T for s, e in once)
    assert all(0 <= u < v <= D for u, v in routine)
    lines = [f"{T} {D} {len(once)} {len(routine)}"]
    lines += [f"{s} {e}" for s, e in once] + [f"{u} {v}" for u, v in routine]
    tests.append("\n".join(lines) + "\n")

def once_jobs(T, n, maxlen):
    out = []
    for _ in range(n):
        L = random.randint(1, min(maxlen, T))
        s = random.randint(0, T - L)
        out.append((s, s + L))
    return out

def routine_jobs(D, m, lo=0, hi=None, maxlen=None):
    hi = D if hi is None else hi
    maxlen = hi - lo if maxlen is None else maxlen
    out = []
    for _ in range(m):
        L = random.randint(1, min(maxlen, hi - lo))
        u = random.randint(lo, hi - L)
        out.append((u, u + L))
    return out


add(21, 7, [(3, 9), (12, 16)], [(0, 2), (5, 6)])
add(12, 4, [], [(0, 3), (2, 4)])
add(10, 10, [(0, 4), (4, 8), (2, 6)], [])
add(5, 1, [(1, 3)], [(0, 1)])
add(17, 5, [(0, 6), (9, 13), (14, 15)], [(1, 2), (3, 5)])

add(1, 1, [(0, 1)], [])
add(1, 1, [(0, 1)], [(0, 1)])
add(23, 6, [(20, 23)], [(1, 4), (2, 3)])
add(30, 7, [(0, 30), (5, 12)], [(4, 6)])
add(40, 40, once_jobs(40, 6, 15), routine_jobs(40, 5))
add(50, 8, once_jobs(50, 8, 10), routine_jobs(8, 4))
add(97, 10, once_jobs(97, 12, 30), routine_jobs(10, 6, maxlen=3))
add(300, 1, once_jobs(300, 20, 50), [])
add(2000, 37, once_jobs(2000, 60, 200), routine_jobs(37, 20, maxlen=6))
add(3000, 701, once_jobs(3000, 100, 500), routine_jobs(701, 30, maxlen=40))

add(MAXT, 999_983, once_jobs(MAXT, 40_000, 3000), routine_jobs(999_983, 20_000, maxlen=200))
add(MAXT - 1, 333_334, once_jobs(MAXT - 1, 40_000, 50), routine_jobs(333_334, 40_000, maxlen=20))

add(MAXT, 1, once_jobs(MAXT, MAXN, 100), [(0, 1)] * MAXN)
add(MAXT, 10, once_jobs(MAXT, MAXN, 30), routine_jobs(10, MAXN, 0, 1))
add(MAXT, 20, once_jobs(MAXT, MAXN, 8), routine_jobs(20, MAXN, 3, 9, maxlen=2))
add(MAXT, 7, once_jobs(MAXT, MAXN, 4), routine_jobs(7, MAXN, 2, 4))
add(MAXT - 3, 16, once_jobs(MAXT - 3, MAXN, 3), routine_jobs(16, MAXN, 5, 11))
add(MAXT, 25, once_jobs(MAXT, MAXN, 6), [(24, 25)] * (MAXN // 2) + routine_jobs(25, MAXN // 2, 0, 4))
add(MAXT - 7, 12, once_jobs(MAXT - 7, MAXN, 10), [(u, u + 1) for u in (0, 11)] * (MAXN // 2))
add(MAXT, 3, once_jobs(MAXT, MAXN, 2), [(1, 2)] * MAXN)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
