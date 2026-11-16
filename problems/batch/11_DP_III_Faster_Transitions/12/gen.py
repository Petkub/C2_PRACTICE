# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
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
        s0 = ri(2 - ln, L)                  # may stick out on either side, then clipped
        out.append((max(1, s0), min(L, s0 + ln - 1), ri(clo, chi)))
    return out


# samples
add(10, [(1, 4, 3), (3, 7, 4), (5, 10, 5), (1, 10, 15), (8, 10, 2)])
add(8, [(1, 3, 1), (5, 8, 1), (2, 3, 1)])
add(5, [(1, 5, 7)])
add(12, [(1, 6, 10), (7, 12, 10), (1, 12, 25), (4, 9, 3), (1, 3, 4), (10, 12, 4)])
add(6, [(2, 6, 1), (1, 5, 2), (3, 4, 1)])
add(1000000000, [(1, 600000000, 1000000000), (400000001, 1000000000, 1000000000), (1, 999999999, 1000000000), (999999999, 1000000000, 999999999)])
# hidden: small (the brute tries every set of guards)
add(1, [(1, 1, 5), (1, 1, 3)])
add(3, [(1, 1, 1), (3, 3, 1)])
add(20, rguards(12, 20, 1, 6, 1, 20))
add(30, rguards(16, 30, 2, 10, 1, 100))
add(15, rguards(14, 15, 1, 4, 1, 5))
add(50, rguards(10, 50, 5, 30, 1, 10**9))
# hidden: medium
add(10**5, rguards(3000, 10**5, 100, 5000, 1, 10**6))
add(5000, rguards(4000, 5000, 1, 40, 1, 1000))
# hidden: maximum size
N, L = MAXN, MAXL
add(L, rguards(N, L, 1, 10**8, 1, MAXC))
add(L, rguards(N, L, 10**5, 10**6, 1, 10**6))
add(L, rguards(N, L, 1, L, 1, MAXC))
add(N, [(i, min(N, i + 1), 1) for i in range(1, N + 1)])          # chain, every guard needed... nearly
add(N, [(1, i, ri(10**8, MAXC)) for i in range(1, N // 2 + 1)]
    + [(i, N, ri(10**8, MAXC)) for i in range(N // 2 + 1, N + 1)])  # one guard from 1 plus one guard to N
add(N, [(1, i, i) for i in range(1, N // 2 + 1)] + [(i, N, N - i + 1) for i in range(N // 2 + 1, N + 1)])
gs = rguards(N - 1, L, 10**4, 10**7, 1, MAXC)
gs = [(s, e, c) for s, e, c in gs if not (s <= 500_000_000 <= e)] # hour 5*10^8 uncovered
add(L, gs + [(1, 499_999_999, 1)])
add(L, rguards(N, L, 1, 2 * 10**4, 1, 10))                        # short guards: usually -1
step = L // N
add(L, [(i * step + 1, min(L, (i + 2) * step), MAXC - ri(0, 10)) for i in range(N)])  # answer near 10^14
add(L, [(max(1, i * step - ri(0, step)), min(L, (i + 1) * step + ri(0, 3 * step)), ri(1, MAXC))
        for i in range(N)])
add(N, [(max(1, i - ri(0, 50)), min(N, i + ri(0, 50)), ri(1, 1000)) for i in range(1, N + 1)])
# every guard overlaps the middle hour, so all earlier guards are possible predecessors
# (walking back over the guards with e_j >= s_i - 1 is quadratic here)
gs = [(1, ri(1, L // 2), ri(1, MAXC)) for _ in range(10)]
gs += [(ri(2, L // 2), L if random.random() < 0.05 else ri(L // 2, L), ri(1, MAXC)) for _ in range(N - 10)]
add(L, gs)
gs = [(1, ri(L // 4, L // 2), ri(1, MAXC)) for _ in range(10)]
for _ in range(N - 10):
    s, e = ri(2, L // 2), (L if random.random() < 0.02 else ri(L // 2, L))
    gs.append((s, e, (e - s) // 10**4 + ri(1, 1000)))             # wage grows with length
add(L, gs)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
