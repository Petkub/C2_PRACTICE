# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(11012)
MAXN, MAXL, MAXC = 100_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(L, gs):
    n = len(gs)
    assert 1 <= n <= MAXN and 1 <= L <= MAXL
    assert all(1 <= s <= e <= L and 1 <= c <= MAXC for s, e, c in gs)
    tests.append(f"{n} {L}\n" + "".join(f"{s} {e} {c}\n" for s, e, c in gs))


def rguards(n, L, lenlo, lenhi, clo, chi):
    out = []
    for _ in range(n):
        ln = min(L, ri(lenlo, lenhi))
        s0 = ri(2 - ln, L)
        out.append((max(1, s0), min(L, s0 + ln - 1), ri(clo, chi)))
    return out


add(10, [(1, 4, 3), (3, 7, 4), (5, 10, 5), (1, 10, 15), (8, 10, 2)])
add(8, [(1, 3, 1), (5, 8, 1), (2, 3, 1)])
add(5, [(1, 5, 7)])
add(12, [(1, 6, 10), (7, 12, 10), (1, 12, 25), (4, 9, 3), (1, 3, 4), (10, 12, 4)])
add(6, [(2, 6, 1), (1, 5, 2), (3, 4, 1)])
add(1000000000, [(1, 600000000, 1000000000), (400000001, 1000000000, 1000000000), (1, 999999999, 1000000000), (999999999, 1000000000, 999999999)])

add(1, [(1, 1, 5), (1, 1, 3)])
add(3, [(1, 1, 1), (3, 3, 1)])
add(20, rguards(12, 20, 1, 6, 1, 20))
add(30, rguards(16, 30, 2, 10, 1, 100))
add(15, rguards(14, 15, 1, 4, 1, 5))
add(50, rguards(10, 50, 5, 30, 1, 10**9))

add(10**5, rguards(3000, 10**5, 100, 5000, 1, 10**6))
add(5000, rguards(4000, 5000, 1, 40, 1, 1000))
add(10**9, [(1, 300_000_000, MAXC), (300_000_001, 600_000_000, MAXC), (600_000_001, 10**9, MAXC)])
M = 20_000
add(M, [(i, min(M, i + 1), MAXC) for i in range(1, M + 1)])
add(10**9, rguards(M, 10**9, 1, 10**5, 1, 10))


N, L = MAXN, MAXL


def longs(k, L, smin, smax, emin, emax, clo, chi):
    return [(ri(smin, smax), ri(emin, emax), ri(clo, chi)) for _ in range(k)]


add(L, rguards(N // 10, L, 1, 10**8, 1, MAXC) + longs(N - N // 10, L, 2, 3 * L // 10, 7 * L // 10, L - 1, 1, MAXC))
add(L, rguards(N // 10, L, 10**5, 10**6, 1, 10**6)
    + longs(N - N // 10, L, 2, 45 * L // 100, 55 * L // 100, L - 1, 5 * 10**8, MAXC))
add(L, [(1, ri(1, L // 2), ri(1, MAXC)) for _ in range(50)] + [(ri(L // 2, L), L, ri(1, MAXC)) for _ in range(50)]
    + longs(N - 100, L, 2, L // 2, L // 2, L - 1, 1, MAXC))
h = 9 * L // 10
add(L, [(1, ri(3 * L // 10, L // 2), ri(1, MAXC)) for _ in range(1000)]
    + [(ri(h + 1, L), L, ri(1, MAXC)) for _ in range(1000)]
    + longs(N - 2000, L, 2, 4 * L // 10, 6 * L // 10, h - 1, 1, MAXC))
add(L, [(1, ri(2 * L // 10, 3 * L // 10), ri(8 * 10**8, MAXC)) for _ in range(5000)]
    + [(ri(7 * L // 10, 75 * L // 100), L, ri(8 * 10**8, MAXC)) for _ in range(5000)]
    + longs(N - 10000, L, L // 20, 3 * L // 10, 7 * L // 10, 95 * L // 100, 8 * 10**8, MAXC))
K = N // 10
step = L // K
add(L, [(i * step + 1, min(L, (i + 2) * step), MAXC - ri(0, 10)) for i in range(K)]
    + longs(N - K, L, 3 * L // 10, 4 * L // 10, 6 * L // 10, 7 * L // 10, MAXC - 10, MAXC))
add(L, rguards(N // 10, L, 1, 2 * 10**4, 1, 10) + [(1, ri(L // 3, L // 2), ri(1, 10)) for _ in range(50)]
    + [(ri(L // 2, 2 * L // 3), L, ri(1, 10)) for _ in range(50)] + longs(N - N // 10 - 100, L, 2, L // 3, 2 * L // 3, L - 1, 1, 10))
add(N, [(ri(1, 10), ri(N // 3, N // 2), ri(1, 1000)) for _ in range(100)]
    + longs(N - 100, N, 2, N // 3, 2 * N // 3, N, 1, 1000))
add(N, [(1, ri(1, N // 2), ri(1, MAXC)) for _ in range(5000)] + [(ri(2, N // 2), N, ri(1, MAXC)) for _ in range(N - 5000)])
add(L, [(1, 1, ri(8 * 10**8, MAXC)) for _ in range(10)] + [(L, L, ri(8 * 10**8, MAXC)) for _ in range(10)]
    + [(2, L - 1, ri(8 * 10**8, MAXC)) for _ in range(N - 20)])
add(L, [(1, ri(3 * L // 10, L // 2), ri(9 * 10**8, MAXC)) for _ in range(3000)]
    + [(ri(L // 2, 7 * L // 10), L, ri(9 * 10**8, MAXC)) for _ in range(3000)]
    + longs(N - 6000, L, 3 * L // 10 + 2, L // 2, L // 2, 7 * L // 10, 9 * 10**8, MAXC))


gs = [(1, ri(1, L // 2), ri(1, MAXC)) for _ in range(10)]
gs += [(ri(2, L // 2), L if random.random() < 0.05 else ri(L // 2, L), ri(1, MAXC)) for _ in range(N - 10)]
add(L, gs)
gs = [(1, ri(L // 4, L // 2), ri(1, MAXC)) for _ in range(10)]
for _ in range(N - 10):
    s, e = ri(2, L // 2), (L if random.random() < 0.02 else ri(L // 2, L))
    gs.append((s, e, (e - s) // 10**4 + ri(1, 1000)))
add(L, gs)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
