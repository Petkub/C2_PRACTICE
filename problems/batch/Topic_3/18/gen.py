# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20218)
MAXN, MAXA, MAXC, MAXS = 200_000, 10**9, 10**6, 10**17
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(S, items):
    n = len(items)
    assert 1 <= n <= MAXN
    assert 1 <= S <= MAXS
    assert all(1 <= a <= MAXA and 0 <= c <= MAXC for a, c in items)
    tests.append(f"{n} {S}\n" + "".join(f"{a} {c}\n" for a, c in items))


def f(items, k):
    """smallest total for exactly k items"""
    if k == 0:
        return 0
    return sum(sorted(a + c * k for a, c in items)[:k])


def add_k(items, k, where="mid"):
    """choose S so that the answer is exactly k"""
    n = len(items)
    lo = f(items, k)
    hi = f(items, k + 1) - 1 if k < n else MAXS
    hi = min(hi, MAXS)
    lo = max(lo, 1)
    S = {"low": lo, "high": hi, "mid": ri(lo, hi)}[where]
    add(S, items)


def rnd(n, amax=MAXA, cmax=MAXC):
    return [(ri(1, amax), ri(0, cmax)) for _ in range(n)]


# samples
add(20, [(2, 1), (3, 2), (5, 1), (1, 3)])
add(4, [(5, 0), (6, 0), (7, 0)])
add(6, [(1, 0), (2, 0), (3, 0)])
add(22, [(2, 1), (3, 2), (5, 1), (1, 3)])
add(100, [(10, 4), (1, 9), (7, 2), (20, 0), (3, 5)])
add(10**12, [(MAXA, MAXC), (MAXA, MAXC)])
# hidden: small
add(1, [(1, 0)])
add(1, [(1, 1)])
for n, am, cm in ((6, 10, 3), (10, 50, 10), (40, 1000, 30), (300, MAXA, MAXC), (2000, 1000, 1000)):
    items = rnd(n, am, cm)
    add_k(items, ri(1, n))
items = rnd(2000, MAXA, MAXC)
add_k(items, 2000, "low")
items = [(ri(1, 10**6), 0) for _ in range(2000)]
add_k(items, 777, "high")
# hidden: large (answers mostly far from both 0 and N)
N = 150_000                                           # keeps the inputs near 2.5 MB (40 MB in total)
items = rnd(N)
add_k(items, N // 2)
items = rnd(N)
add_k(items, ri(N // 4, 3 * N // 4), "low")
items = rnd(N)
add_k(items, ri(N // 4, 3 * N // 4), "high")
items = [(ri(1, MAXA), ri(0, 10)) for _ in range(N)]
add_k(items, ri(N // 3, N // 2))
items = [(MAXA, MAXC)] * 150_000                      # largest possible totals
add(MAXS, items)
add(f(items, len(items)) - 1, items)
items = [(ri(1, MAXA), 0) for _ in range(N)]          # no fee at all
add_k(items, ri(1000, N - 1000))
x = [ri(1, MAXC) for _ in range(N)]
items = [(MAXA - (v - 1) * 1000, v) for v in x]       # cheap base price comes with a high fee
add_k(items, ri(N // 4, 3 * N // 4))
items = [(ri(MAXA // 2, MAXA), ri(MAXC // 2, MAXC)) if i % 2 else (ri(1, 1000), ri(MAXC // 2, MAXC))
         for i in range(N)]
add_k(items, ri(N // 4, N // 2))
items = rnd(N)
add_k(items, ri(1, 50))                               # small answer
items = rnd(N)
add_k(items, N - ri(1, 50))                           # answer close to N
items = rnd(N)
add(min(a + c for a, c in items) - 1, items)          # nothing affordable
items = [(ri(1, MAXA), ri(0, MAXC // 100)) for _ in range(N)]
add_k(items, ri(N // 3, 2 * N // 3), "high")
items = [(ri(1, 10**6), ri(MAXC - 1000, MAXC)) for _ in range(N)]
add_k(items, ri(N // 4, N // 2), "low")
items = [(5 * 10**8, 2500)] * N                       # every item costs the same
add_k(items, ri(N // 3, 2 * N // 3))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f_:
        f_.write(t)
