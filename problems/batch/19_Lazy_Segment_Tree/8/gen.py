# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(19008)
MAXN, MAXQ = 500_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(s, ops):
    n, q = len(s), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and set(s) <= set("01")
    assert any(op[0] == 'L' for op in ops)
    for op in ops:
        assert op[0] in "TL" and len(op) == 3 and 1 <= op[1] <= op[2] <= n
    tests.append(f"{n} {q}\n{s}\n" + "\n".join(f"{c} {l} {r}" for c, l, r in ops) + "\n")


def coin(n, p):
    return "".join("1" if random.random() < p else "0" for _ in range(n))


def blocks(n, mean_on, mean_off, long_every=0, long_len=0):
    """alternating runs with random lengths around the means; every long_every-th lit run is long_len long"""
    out, on, k = [], random.random() < 0.5, 0
    total = 0
    while total < n:
        if on:
            k += 1
            m = long_len if long_every and k % long_every == 0 else ri(1, 2 * mean_on - 1)
        else:
            m = ri(1, 2 * mean_off - 1)
        m = min(m, n - total)
        out.append(("1" if on else "0") * m)
        total += m
        on = not on
    return "".join(out)


def any_rng(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_rng(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def short_rng(n, d):
    l = ri(1, n)
    return l, min(n, l + ri(0, d))


def ops_of(n, q, pt, upd, ask):
    ops = [('T',) + upd() if random.random() < pt else ('L',) + ask() for _ in range(q)]
    if not any(op[0] == 'L' for op in ops):
        ops[-1] = ('L',) + ask()
    return ops


# samples
add("1101110010", [('L', 1, 10), ('T', 3, 5), ('L', 1, 10), ('L', 2, 6), ('T', 4, 8), ('L', 1, 10), ('L', 6, 6)])
add("00000", [('L', 1, 5), ('T', 1, 5), ('L', 2, 4), ('T', 3, 3), ('L', 1, 5)])
add("1", [('L', 1, 1), ('T', 1, 1), ('L', 1, 1)])
add("011011100111", [('T', 1, 12), ('L', 1, 12), ('T', 5, 9), ('L', 3, 10), ('L', 1, 12), ('T', 2, 2), ('L', 1, 4)])
add("1" * 8 + "0" * 8 + "1" * 8 + "0" * 8, [('T', 9, 16), ('L', 1, 32), ('T', 5, 27), ('L', 1, 32), ('L', 17, 24)])
# hidden: small (the brute force checks these)
for n, q, d in ((1, 10, 1), (5, 40, 2), (12, 100, 5), (60, 500, 20), (500, 3000, 100), (3000, 4000, 700)):
    s = coin(n, 0.5) if n < 500 else blocks(n, 6, 3)
    add(s, ops_of(n, q, 0.45, lambda: short_rng(n, d) if random.random() < 0.6 else any_rng(n), lambda: any_rng(n)))
n = 3000
add("0" * n, ops_of(n, 4000, 0.5, lambda: short_rng(n, 40), lambda: any_rng(n)))      # all off at first
add("1" * 2000, ops_of(2000, 4000, 0.3, lambda: short_rng(2000, 3), lambda: any_rng(2000)))   # all on, few holes
# hidden: maximum size
N, Q = MAXN, MAXQ
add(coin(N, 0.5), ops_of(N, Q, 0.5, lambda: any_rng(N), lambda: long_rng(N, 1000)))
add(blocks(N, 3, 2), ops_of(N, Q, 0.5, lambda: long_rng(N, 1000), lambda: long_rng(N, 1000)))
add(blocks(N, 4, 2, 997, 3000), ops_of(N, Q, 0.4, lambda: any_rng(N), lambda: any_rng(N)))
add(blocks(N, 2, 4), ops_of(N, Q, 0.5, lambda: short_rng(N, 2000), lambda: long_rng(N, 50)))
add(coin(N, 0.8), ops_of(N, Q, 0.5, lambda: (1, N), lambda: long_rng(N, 10)))       # the whole string at once
add(blocks(N, 5, 1, 50, 200), ops_of(N, Q, 0.3, lambda: short_rng(N, 30), lambda: any_rng(N)))
add(coin(N, 0.6), ops_of(N, Q, 0.6, lambda: long_rng(N, N // 2),
                         lambda: short_rng(N, 3) if random.random() < 0.5 else long_rng(N, 1000)))
add(blocks(N, 3, 3), ops_of(N, Q, 0.5, lambda: any_rng(N), lambda: short_rng(N, 100_000)))
add(coin(N, 0.95), ops_of(N, Q, 0.5, lambda: short_rng(N, 1), lambda: long_rng(N, 100)))   # long lit runs, single toggles
add(blocks(N, 8, 2, 101, 5000), ops_of(N, Q, 0.45, lambda: long_rng(N, 150_000), lambda: any_rng(N)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
