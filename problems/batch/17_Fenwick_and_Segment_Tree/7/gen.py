# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110007)
MAXN, MAXQ, MAXA, MAXX = 200_000, 200_000, 10**9, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= v <= MAXA for v in a)
    for op in ops:
        assert 1 <= op[1] <= op[2] <= n
        if op[0] == 1:
            assert len(op) == 4 and 1 <= op[3] <= MAXX
        else:
            assert len(op) == 3 and op[0] == 2
    assert any(op[0] == 2 for op in ops)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n"
                 + "".join(" ".join(map(str, op)) + "\n" for op in ops))


def rng_range(n, kind):
    if kind == "long":
        return ri(1, min(n, 99)), ri(max(1, n - 99), n)
    if kind == "short":
        l = ri(1, n)
        return l, min(n, l + ri(0, 3))
    if kind == "suffix":
        return ri(1, min(n, 99)), n
    l = ri(1, n)
    return l, ri(l, n)


def rnd_ops(n, q, p_add, xmax, kind="any"):
    """p_add = chance of fertilising; kind of ranges: any / long / short / suffix (r = N)"""
    ops = []
    for _ in range(q):
        l, r = rng_range(n, kind)
        if random.random() < p_add:
            ops.append((1, l, r, ri(1, xmax)))
        else:
            ops.append((2, l, r))
    if all(op[0] == 1 for op in ops):
        ops[-1] = (2, 1, n)
    return ops


# samples
add([1, 2, 3, 4, 5], [(2, 1, 5), (1, 2, 4, 10), (2, 1, 3), (1, 1, 5, 1), (2, 4, 5)])
add([MAXA, MAXA - 1], [(1, 1, 2, MAXX), (2, 1, 2), (2, 2, 2)])
add([0], [(2, 1, 1), (1, 1, 1, 7), (1, 1, 1, 7), (2, 1, 1)])
add([4, 0, 4, 0, 4, 0], [(1, 2, 5, 3), (1, 5, 6, 2), (2, 1, 6), (2, 5, 5), (2, 2, 3)])
add([9, 8, 7, 6], [(1, 1, 2, 5), (2, 2, 4), (1, 4, 4, 1), (2, 1, 4)])
# hidden: small
add([MAXA], [(1, 1, 1, MAXX), (2, 1, 1)])
for n, q, xmax in ((5, 10, 3), (10, 30, 10), (50, 100, 1000), (400, 800, MAXX), (3000, 3000, 100), (6000, 6000, MAXX)):
    add([ri(0, 100) for _ in range(n)], rnd_ops(n, q, 0.5, xmax))
add([ri(0, 9) for _ in range(5000)], rnd_ops(5000, 8000, 0.5, 9, "short"))
add([MAXA] * 3000, rnd_ops(3000, 3000, 0.6, MAXX, "suffix"))
# hidden: maximum size (short numbers keep the files small; long ranges make a loop per operation too slow)
N, Q = MAXN, MAXQ
add([ri(0, 9) for _ in range(N)], rnd_ops(N, Q, 0.5, 9, "long"))
add([ri(0, 9) for _ in range(N)], rnd_ops(N, Q, 0.8, 9, "long"))
add([ri(0, 9) for _ in range(N)], rnd_ops(N, Q, 0.2, 99, "long"))
add([ri(0, 9) for _ in range(N)], rnd_ops(N, Q, 0.5, 9, "suffix"))
add([0] * N, [(1, 1, N, 1) if k % 2 == 0 else (2, 1, N) for k in range(Q)])
add([ri(0, 99) for _ in range(N)], rnd_ops(N, 140_000, 0.5, 99))
add([ri(0, 9) for _ in range(N)], rnd_ops(N, 160_000, 0.5, 9, "short"))
# largest values: sums up to about 10^16
add([MAXA] * N, [(1, 1, N, MAXX) if k % 3 else (2, 1, N) for k in range(45_000)])
add([MAXA - ri(0, 9) for _ in range(N)], rnd_ops(N, 50_000, 0.5, MAXX, "long"))
add([ri(0, MAXA) for _ in range(N)], rnd_ops(N, 40_000, 0.5, MAXX))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
