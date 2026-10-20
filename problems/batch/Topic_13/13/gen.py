# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110013)
MAXN, MAXQ = 500_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(s, ops):
    n, q = len(s), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert set(s) <= set("()")
    for op in ops:
        if op[0] == 1:
            assert len(op) == 2 and 1 <= op[1] <= n
        else:
            assert op[0] == 2 and len(op) == 3 and 1 <= op[1] <= op[2] <= n
    assert any(op[0] == 2 for op in ops)
    t = f"{n} {q}\n{s}\n" + "".join(" ".join(map(str, op)) + "\n" for op in ops)
    assert len(t) <= 3_100_000
    tests.append(t)


def rnd_str(n, p_open=0.5):
    return "".join("(" if random.random() < p_open else ")" for _ in range(n))


def mix(n, q, flip_frac, long_frac=0.9):
    ops = []
    for _ in range(q):
        if random.random() < flip_frac:
            ops.append((1, ri(1, n)))
        elif random.random() < long_frac:
            l = ri(1, max(1, n // 20))
            ops.append((2, l, ri(max(l, n - n // 20), n)))
        else:
            l = ri(1, n)
            ops.append((2, l, ri(l, n)))
    if not any(op[0] == 2 for op in ops):
        ops.append((2, 1, n))
    return ops


# samples
add("(()(", [(2, 1, 4), (1, 4), (2, 1, 4), (1, 2), (2, 1, 4)])
add(")(", [(2, 1, 2), (1, 1), (2, 1, 2), (1, 2), (2, 1, 2)])
add("(", [(2, 1, 1)])
add("())(()))((", [(2, 1, 10), (2, 3, 8), (1, 9), (1, 10), (2, 1, 10)])
add(")()(()(", [(2, 1, 7), (1, 1), (2, 1, 7), (2, 2, 6)])
# hidden: small
add(")", [(2, 1, 1), (1, 1), (2, 1, 1)])
s = rnd_str(10)
add(s, [(2, l, r) for l in range(1, 11) for r in range(l, 11)] + [(1, 3), (2, 1, 10), (1, 7), (2, 2, 9)])
add(rnd_str(100), mix(100, 300, 0.3, 0.3))
add(rnd_str(1000, 0.6), mix(1000, 2000, 0.2, 0.4))
add("(" * 5000 + ")" * 5000, mix(10000, 5000, 0.1, 0.5))
add(rnd_str(30000), mix(30000, 10000, 0.3, 0.4))
add(")" * 3000 + "(" * 3000, mix(6000, 4000, 0.2, 0.5))
# hidden: maximum size
N = MAXN
add(rnd_str(N), mix(N, 150_000, 0.2))
add(rnd_str(N), mix(N, 160_000, 0.5))
add(rnd_str(N, 0.55), mix(N, 150_000, 0.3))
add("(" * N, mix(N, 150_000, 0.3))                                     # flips create the only pairs
add(")" * N, mix(N, 150_000, 0.3))
add("(" * (N // 2) + ")" * (N // 2), mix(N, 150_000, 0.2))            # one deep nest
add("()" * (N // 2), mix(N, 150_000, 0.2))
add(")" * (N // 2) + "(" * (N // 2), mix(N, 150_000, 0.2))            # nothing matches at first
s = "".join("(" * 3 + ")" * 2 if i % 2 else "(" + ")" * 2 for i in range(N // 4))[:N]
add(s, mix(len(s), 150_000, 0.3))
add(rnd_str(N), [(2, 1, N) if j % 2 else (1, ri(1, N)) for j in range(170_000)])
add(rnd_str(N, 0.45), mix(N, 150_000, 0.1, 1.0))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
