# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7006)
MAXT, MAXSUM = 10_000, 200_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(cases):
    assert 1 <= len(cases) <= MAXT
    assert sum(n for n, _ in cases) <= MAXSUM and sum(len(e) for _, e in cases) <= MAXSUM
    out = [f"{len(cases)}\n"]
    for n, edges in cases:
        assert n >= 1 and all(1 <= a <= n and 1 <= b <= n for a, b in edges)
        out.append(f"{n} {len(edges)}\n")
        out.append("".join(f"{a} {b}\n" for a, b in edges))
    tests.append("".join(out))


def perm(n):
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


def dag(n, m):
    """random edges that all go from a later to an earlier package of a hidden order"""
    p = perm(n)
    res = []
    if n == 1:
        return res
    for _ in range(m):
        i, j = ri(0, n - 1), ri(0, n - 1)
        while i == j:
            j = ri(0, n - 1)
        if i < j:
            i, j = j, i
        res.append((p[i], p[j]))
    return res


def local_dag(n, m):
    """like dag(), but every package needs packages a little earlier in the hidden order (long chains of needs)"""
    p = perm(n)
    res = [(p[i], p[i - 1]) for i in range(1, n)][:m]
    while len(res) < m:
        i = ri(1, n - 1)
        res.append((p[i], p[max(0, i - ri(1, 5))]))
    random.shuffle(res)
    return res


def chain(n, back=False):
    """p[i+1] needs p[i]; with back=True also p[0] needs p[n-1]"""
    p = perm(n)
    res = [(p[i + 1], p[i]) for i in range(n - 1)]
    if back:
        res.append((p[0], p[n - 1]))
    random.shuffle(res)
    return res


def rnd(n, m):
    return [(ri(1, n), ri(1, n)) for _ in range(m)]


def small_mix(count, maxn):
    cases = []
    for k in range(count):
        n = ri(1, maxn)
        kind = k % 4
        if kind == 0:
            cases.append((n, dag(n, ri(0, 2 * n))))
        elif kind == 1:
            cases.append((n, rnd(n, ri(0, 2 * n))))
        elif kind == 2:
            cases.append((n, chain(n, back=random.random() < 0.5)))
        else:
            e = dag(n, ri(0, n))
            if e and random.random() < 0.5:
                a, b = random.choice(e)
                e.append((b, a))                  # reverse one edge: a cycle of length 2 or more
            cases.append((n, e))
    return cases


# samples
add([(2, [(1, 2)]), (3, [(1, 2), (2, 3), (3, 1)])])
add([(4, [(1, 2), (1, 3), (2, 4), (3, 4)])])
add([(1, [(1, 1)])])
add([(1, []), (2, [(1, 2), (2, 1)])])
add([(4, [(1, 2), (2, 3), (3, 4), (4, 2), (1, 4)])])
add([(5, []), (3, [(3, 1), (2, 1), (3, 2), (3, 1)])])
# hidden: small
add(small_mix(300, 4))
add(small_mix(300, 8))
add(small_mix(200, 15))
add(small_mix(50, 60))
add([(2, [(1, 1)]), (2, [(2, 2)]), (3, [(1, 2), (2, 3), (1, 3)]), (3, [(1, 3), (3, 2), (2, 1)])])
add([(8, chain(8)), (8, chain(8, back=True)), (10, dag(10, 30)), (10, dag(10, 30) + [(4, 4)])])
add([(500, dag(500, 2000)), (500, chain(500, back=True))])
add(small_mix(MAXT, 20))                                    # many systems at once
# hidden: large (one system each, unless stated)
N = MAXSUM
add([(N, chain(N))])
add([(N, chain(N, back=True))])                             # one cycle through everything
add([(N, local_dag(N, N))])
add([(N, dag(N, N))])
add([(N, local_dag(N, N - 1) + [(N, N)])])  # a self-requirement on the last package
p = perm(N)
e = [(p[i + 1], p[i]) for i in range(N - 1)]
e.append((p[N - 10], p[N - 5]))                             # a short cycle at the very end of a chain
random.shuffle(e)
add([(N, e)])
layers = N // 2                                             # ladder of diamonds: many paths to the same package
e = []
for k in range(layers - 1):
    for x in (2 * k + 1, 2 * k + 2):
        for y in (2 * k + 3, 2 * k + 4):
            e.append((x, y))
add([(N, e[:MAXSUM])])
add([(N, [(i, N // 2 + ri(1, N // 2)) for i in range(1, N // 2 + 1)] * 2)])   # two layers, many shared needs
add([(N, rnd(N, N))])
add([(N // 2, local_dag(N // 2, N // 2)), (N // 2, chain(N // 2, back=True))])
add([(20, dag(20, 19) + ([(k % 20 + 1, k % 20 + 1)] if k % 7 == 3 else [(1, 2)])) for k in range(MAXT)])
add([(N - 1, local_dag(N - 1, N - 1)), (1, [(1, 1)])])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
