# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(40801)
MAXN = 100_000
MAXQ = 100_000
MAXP = 10**9
MAXW = 10**9
MAXB = 10**15
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def needs(T, parts):
    """(level, cost) for every quality level at which every type is available, highest level first"""
    order = sorted(parts, key=lambda x: -x[2])
    best = [None] * (T + 1)
    covered = cost = 0
    res = []
    i = 0
    while i < len(order):
        j = i
        while j < len(order) and order[j][2] == order[i][2]:
            c, p, w = order[j]
            if best[c] is None:
                covered += 1
                cost += p
                best[c] = p
            elif p < best[c]:
                cost -= best[c] - p
                best[c] = p
            j += 1
        if covered == T:
            res.append((order[i][2], cost))
        i = j
    return res


def add(T, parts, budgets):
    n, q = len(parts), len(budgets)
    assert 1 <= T <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= c <= T and 1 <= p <= MAXP and 1 <= w <= MAXW for c, p, w in parts)
    assert len(set(c for c, p, w in parts)) == T
    assert all(1 <= b <= MAXB for b in budgets)
    tests.append(f"{n} {T} {q}\n" + "".join(f"{c} {p} {w}\n" for c, p, w in parts)
                 + " ".join(map(str, budgets)) + "\n")


def rnd_parts(n, T, pmax, wmax, shape="random"):
    """every type gets at least one part; shape: random, monotone (better = dearer), anti (better = cheaper)"""
    types = list(range(1, T + 1)) + [ri(1, T) for _ in range(n - T)]
    parts = [(c, ri(1, pmax), ri(1, wmax)) for c in types]
    if shape != "random":
        by = {}
        for c, p, w in parts:
            by.setdefault(c, ([], []))
            by[c][0].append(p)
            by[c][1].append(w)
        parts = []
        for c in sorted(by):
            ps, ws = sorted(by[c][0]), sorted(by[c][1])
            if shape == "anti":
                ps.reverse()
            parts.extend((c, p, w) for p, w in zip(ps, ws))
    random.shuffle(parts)
    return parts


def budgets(T, parts, q, miss=0.05):
    """budgets exactly on a level's cost, one below it, between levels, too small, or very large"""
    costs = [c for _, c in needs(T, parts)]
    lowest, top, k = costs[-1], costs[0], len(costs) - 1
    shifts = (0, 0, -1, 1)
    res = []
    for _ in range(q):
        r = random.random()
        if r < miss:
            res.append(ri(1, lowest - 1) if lowest > 1 else lowest)
        elif r < miss + 0.03:
            res.append(ri(top, MAXB))
        else:
            s = shifts[int(r * 1000) % 4] if r < 0.9 else ri(-1000, 1000)
            res.append(max(1, costs[ri(0, k)] + s))
    return res


# samples (better parts are never cheaper here, and every total stays small)
S1 = [(1, 30, 5), (2, 20, 4), (3, 10, 6), (1, 50, 8), (2, 45, 9), (3, 25, 7), (3, 40, 10)]
add(3, S1, [100, 59, 60, 105, 140])
add(1, [(1, 5, 3), (1, 9, 7), (1, 1, 1)], [1, 4, 9])
add(2, [(1, 1000, 1000), (2, 1000, 1000)], [2000, 1999])
add(2, [(1, 4, 3), (2, 5, 2), (2, 9, 8), (1, 6, 8), (2, 12, 10)], [8, 9, 13, 14, 15, 1000])
add(3, [(1, 8, 4), (2, 8, 4), (3, 8, 4), (1, 9, 6), (2, 9, 6), (3, 9, 6), (2, 1, 1)], [17, 24, 26, 27])
# hidden: small (checked by brute force)
add(1, [(1, 1, 1)], [1, 2])
add(2, [(1, 5, 9), (1, 1, 2), (2, 7, 3), (2, 2, 8)], list(range(1, 15)))   # the better part is cheaper
p = rnd_parts(40, 5, 50, 30)
add(5, p, budgets(5, p, 60))
p = rnd_parts(300, 20, 10**6, 200, "anti")
add(20, p, budgets(20, p, 300))
p = rnd_parts(800, 40, MAXP, MAXW)                                   # totals beyond 2^31
add(40, p, budgets(40, p, 400))
p = rnd_parts(1000, 1000, MAXP, 50)                                  # one part per type
add(1000, p, budgets(1000, p, 200))
p = rnd_parts(1000, 7, 100, 10)
add(7, p, budgets(7, p, 500))
# hidden: maximum size
N, Q = MAXN, 90_000
for T, pmax, wmax, shape in ((1000, 10**7, 10**6, "random"), (1000, 10**7, 10**6, "anti"),
                             (1, 10**7, 10**6, "random"), (50_000, 10**5, 10**5, "random"),
                             (300, 10**7, 10**6, "monotone"), (2000, 10**7, 20, "random"),
                             (100, MAXP, 10**5, "random"), (20_000, 10**6, 10**6, "anti")):
    p = rnd_parts(N, T, pmax, wmax, shape)
    add(T, p, budgets(T, p, Q))
p = rnd_parts(N, 1000, 10**7, 10**6)
add(1000, p, budgets(1000, p, Q, miss=0.5))                           # many budgets below every robot
p = [(c, 10**7 - w, w) for c, _, w in rnd_parts(N, 500, 1, 10**6)]   # quality and price add up to 10^7
add(500, p, budgets(500, p, Q))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
