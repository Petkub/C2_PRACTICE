# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110003)
MAXN, MAXQ, MAXP = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(p, ops):
    n, q = len(p), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXP for v in p)
    for t, u, v in ops:
        if t == 1:
            assert 1 <= u <= n and 1 <= v <= MAXP
        else:
            assert t == 2 and 1 <= u <= v <= n
    assert any(t == 2 for t, _, _ in ops)
    tests.append(f"{n} {q}\n" + " ".join(map(str, p)) + "\n"
                 + "".join(f"{t} {u} {v}\n" for t, u, v in ops))


def rnd_ops(n, q, p_set, lo, hi, kind="any"):
    """p_set = chance of a price change to a value in [lo, hi]; kind of query ranges: any / long / short"""
    ops = []
    for _ in range(q):
        if random.random() < p_set:
            ops.append((1, ri(1, n), ri(lo, hi)))
        elif kind == "long":
            ops.append((2, ri(1, min(n, 99)), ri(max(1, n - 99), n)))
        elif kind == "short":
            l = ri(1, n)
            ops.append((2, l, min(n, l + ri(0, 5))))
        else:
            l = ri(1, n)
            ops.append((2, l, ri(l, n)))
    if all(t == 1 for t, _, _ in ops):
        ops[-1] = (2, 1, n)
    return ops


# samples
add([5, 3, 8, 3, 6, 2], [(2, 1, 4), (2, 3, 5), (1, 2, 9), (2, 1, 3)])
add([7, 7, 7], [(2, 1, 3), (1, 1, 8), (2, 1, 3), (2, 3, 3)])
add([MAXP], [(1, 1, 1), (2, 1, 1)])
add([1, 2, 3, 4], [(1, 1, 5), (1, 2, 5), (2, 1, 4)])
add([4, 9, 2, 7, 2, 5, 1, 8], [(2, 2, 6), (1, 3, 6), (1, 7, 2), (2, 4, 8)])
# hidden: small
add([5, 5], [(2, 1, 2), (1, 2, 4), (2, 1, 2), (1, 1, 4), (2, 1, 2), (2, 2, 2)])
for n, q, hi in ((6, 12, 3), (10, 30, 2), (40, 80, 10), (300, 600, MAXP), (2000, 3000, 5), (6000, 6000, MAXP)):
    add([ri(1, hi) for _ in range(n)], rnd_ops(n, q, 0.4, 1, hi))
add([ri(1, 4) for _ in range(5000)], rnd_ops(5000, 8000, 0.5, 1, 4, "short"))
add(list(range(3000, 0, -1)), rnd_ops(3000, 3000, 0.2, 1, 3000, "long"))
# hidden: maximum size (short prices keep the files small; long ranges make one pass per query too slow)
N, Q = MAXN, MAXQ
add([ri(1, 9) for _ in range(N)], rnd_ops(N, Q, 0.2, 1, 9, "long"))           # many ties
add([ri(10, 99) for _ in range(N)], rnd_ops(N, Q, 0.1, 1, 99, "long"))
add([ri(2, 99) for _ in range(N)],                                             # one cheap shop moves around near the end
    [(1, N - ri(0, 99), 1) if k % 4 == 0 else (2, ri(1, 99), N) for k in range(Q)])
add([N - i for i in range(N)], rnd_ops(N, 150_000, 0.05, 1, 99, "long"))            # the cheapest shop is the last one
add([ri(1, 99) for _ in range(N)], rnd_ops(N, 160_000, 0.5, 1, 99))
add([7] * N, [(2, ri(1, 99), ri(N - 99, N)) if k % 3 else (1, ri(1, N), 7) for k in range(Q)])
p = [ri(1, 9) for _ in range(N)]
add(p, rnd_ops(N, 150_000, 0.3, 1, 9, "short"))
add([ri(1, MAXP) for _ in range(N)], rnd_ops(N, 70_000, 0.3, 1, MAXP, "long"))
add([MAXP - ri(0, 2) for _ in range(N)], rnd_ops(N, 70_000, 0.3, MAXP - 2, MAXP, "long"))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
