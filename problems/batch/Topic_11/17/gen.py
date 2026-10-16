# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(11017)
MAXN, MAXQ = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ops):
    q = len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(c in "UDQ" and 1 <= l <= r <= n for c, l, r in ops)
    assert any(c == "Q" for c, l, r in ops)
    tests.append(f"{n} {q}\n" + "".join(f"{c} {l} {r}\n" for c, l, r in ops))


def rnd_range(n):
    l = ri(1, n)
    return l, ri(l, n)


def wide_range(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack), n)


def mix(n, q, rng, pq=1 / 3, pu=0.5):
    """each operation is a query with probability pq, otherwise U with probability pu, else D"""
    ops = []
    for _ in range(q):
        l, r = rng()
        if random.random() < pq:
            ops.append(("Q", l, r))
        else:
            ops.append(("U" if random.random() < pu else "D", l, r))
    return ops


# samples
add(6, [("U", 2, 4), ("Q", 1, 6), ("D", 3, 6), ("Q", 4, 5), ("Q", 1, 1)])
add(5, [("U", 1, 5), ("D", 1, 5), ("Q", 2, 2), ("Q", 1, 5)])
add(1, [("Q", 1, 1), ("U", 1, 1), ("D", 1, 1), ("Q", 1, 1)])
add(8, [("U", 3, 8), ("Q", 8, 8), ("D", 1, 4), ("Q", 2, 6), ("U", 5, 5), ("Q", 1, 8)])
add(10, [("D", 1, 10), ("U", 6, 10), ("Q", 6, 10), ("Q", 1, 5), ("D", 2, 3), ("Q", 3, 7)])
# hidden: small
add(1, [("U", 1, 1)] * 5 + [("Q", 1, 1)])
add(7, mix(7, 30, lambda: rnd_range(7)))
add(20, mix(20, 60, lambda: rnd_range(20), 0.4))
add(100, mix(100, 300, lambda: rnd_range(100)))
add(3000, mix(3000, 3000, lambda: rnd_range(3000)))
add(3000, mix(3000, 3000, lambda: wide_range(3000, 30), 0.5))
add(2000, [("U" if i % 2 else "D", 1, 2000) for i in range(2000)] + [("Q", 1, 2000), ("Q", 1000, 1000)])
# hidden: maximum size
N, Q = MAXN, MAXQ
add(N, mix(N, Q, lambda: wide_range(N, 50)))
add(N, mix(N, Q, lambda: wide_range(N, N // 4), 0.5, 0.7))
add(N, [("U", 1, N)] * (Q - 10) + [("Q", 1, N)] * 5 + [("Q", ri(1, N), N) for _ in range(5)])  # the largest sums
add(N, [("D", 1, N) if i % 3 else ("U", 1, N) for i in range(Q - 1000)] + [("Q", *wide_range(N, 500)) for _ in range(1000)])
ops = mix(N, 1000, lambda: rnd_range(N), 0.0) + mix(N, Q - 1000, lambda: wide_range(N, 99), 1.0)
add(N, ops)                                                    # few updates, then many long queries
add(N, mix(N, Q * 9 // 10, lambda: rnd_range(N)))
ops = []
for i in range(Q // 2):                                        # U and D on the same range, queries inside it
    l, r = wide_range(N, 1000)
    ops.append(("U", l, r))
    ops.append(("D", l, r) if i % 2 else ("Q", *wide_range(N, 1000)))
add(N, ops)
add(N, mix(N, Q, lambda: (lambda p: (p, p))(ri(1, N)), 0.5))   # single positions only
ops = []
for i in range(Q):                                             # prefixes and suffixes, touching both ends
    k = ri(1, N)
    c = random.choice("UDQ")
    ops.append((c, 1, k) if random.random() < 0.5 else (c, k, N))
add(N, ops)
add(N, mix(N, Q * 9 // 10, lambda: (lambda l: (l, min(N, l + ri(0, 30))))(ri(1, N))))  # short ranges
add(N, mix(N, Q, lambda: wide_range(N, 9), 0.5, 0.0))         # only D, whole line
add(N, mix(N, Q, lambda: wide_range(N, 2000), 0.25, 1.0))     # only U

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
