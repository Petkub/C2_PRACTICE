# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110004)
MAXN, MAXQ, MAXA, MAXX = 200_000, 200_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXA for v in a)
    for op in ops:
        if op[0] == 1:
            assert len(op) == 4 and 1 <= op[1] <= op[2] <= n and 1 <= op[3] <= MAXX
        else:
            assert len(op) == 2 and op[0] == 2 and 1 <= op[1] <= n
    assert any(op[0] == 2 for op in ops)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n"
                 + "".join(" ".join(map(str, op)) + "\n" for op in ops))


def rnd_ops(n, q, p_add, xmax, kind="any", ask_end=False):
    """p_add = chance of a raise; kind of raise ranges: any / long / short; ask_end: questions about the last 1000"""
    ops = []
    for _ in range(q):
        if random.random() < p_add:
            if kind == "long":
                l, r = ri(1, min(n, 99)), ri(max(1, n - 99), n)
            elif kind == "short":
                l = ri(1, n)
                r = min(n, l + ri(0, 3))
            else:
                l = ri(1, n)
                r = ri(l, n)
            ops.append((1, l, r, ri(1, xmax)))
        else:
            ops.append((2, ri(max(1, n - 999), n) if ask_end else ri(1, n)))
    if all(op[0] == 1 for op in ops):
        ops[-1] = (2, n)
    return ops


# samples
add([10, 20, 30, 40, 50], [(1, 2, 4, 5), (2, 3), (1, 1, 3, 10), (2, 3), (2, 5)])
add([1, 1, 1], [(1, 1, 3, MAXX), (1, 2, 3, MAXX), (1, 2, 2, MAXX), (2, 2), (2, 1)])
add([7], [(2, 1), (1, 1, 1, 3), (2, 1)])
add([5, 5, 5, 5, 5, 5], [(1, 1, 6, 1), (1, 3, 4, 2), (2, 1), (2, 3), (2, 5), (1, 5, 6, 4), (2, 6)])
add([3, 1, 4, 1, 5], [(1, 4, 5, 2), (2, 4), (1, 1, 1, 9), (2, 1), (2, 2)])
# hidden: small
add([MAXA], [(1, 1, 1, MAXX), (2, 1)])
for n, q, xmax in ((5, 10, 3), (10, 30, 10), (50, 100, 1000), (400, 800, MAXX), (3000, 3000, 100), (6000, 6000, MAXX)):
    add([ri(1, 100) for _ in range(n)], rnd_ops(n, q, 0.5, xmax))
add([ri(1, 9) for _ in range(5000)], rnd_ops(5000, 8000, 0.5, 9, "short"))
add([MAXA] * 3000, rnd_ops(3000, 3000, 0.7, MAXX, "long"))
# hidden: maximum size (short numbers keep the files small; long raises make a loop per raise too slow,
# questions about the last employees make summing a plain difference array per question too slow)
N, Q = MAXN, MAXQ
add([ri(1, 9) for _ in range(N)], rnd_ops(N, Q, 0.5, 9, "long", ask_end=True))
add([ri(1, 9) for _ in range(N)], rnd_ops(N, Q, 0.8, 9, "long"))
add([ri(1, 9) for _ in range(N)], rnd_ops(N, Q, 0.3, 99, "long", ask_end=True))
add([1] * N, [(1, 1, N, 1) if k % 2 == 0 else (2, ri(N - 999, N)) for k in range(Q)])
add([ri(1, 99) for _ in range(N)], rnd_ops(N, 170_000, 0.5, 99, ask_end=True))
add([ri(1, 9) for _ in range(N)], rnd_ops(N, Q, 0.5, 9, "short"))
# largest values: salaries up to about 2 * 10^14
add([MAXA] * N, [(1, 1, N, MAXX) if k % 3 else (2, ri(1, N)) for k in range(50_000)])
add([MAXA - ri(0, 9) for _ in range(N)], rnd_ops(N, 50_000, 0.7, MAXX, "long"))
add([ri(1, MAXA) for _ in range(N)], rnd_ops(N, 40_000, 0.5, MAXX))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
