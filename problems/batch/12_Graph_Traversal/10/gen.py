# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(12011)
MAXL, MAXM, MAXQ = 16, 200, 80000
tests = []


def add(L, btns, qs):
    assert 1 <= L <= MAXL and 1 <= len(btns) <= MAXM and 1 <= len(qs) <= MAXQ
    for b in btns:
        assert 1 <= len(b) <= L and len(set(b)) == len(b) and all(1 <= x <= L for x in b)
    for a, b in qs:
        assert len(a) == L and len(b) == L and set(a + b) <= set("01")
    lines = [f"{L} {len(btns)} {len(qs)}"]
    lines += [" ".join(map(str, [len(b)] + b)) for b in btns]
    lines += [f"{a} {b}" for a, b in qs]
    tests.append("\n".join(lines) + "\n")


def pat(L, x):
    """pattern of mask x: character t is lamp t + 1"""
    return format(x, f"0{L}b")[::-1]


def rand_btn(L, lo, hi):
    k = random.randint(lo, min(hi, L))
    return sorted(random.sample(range(1, L + 1), k))


def span(L, btns):
    s = {0}
    for b in btns:
        mk = sum(1 << (x - 1) for x in b)
        if mk not in s:                                  # s is a subspace: adding mk doubles it
            s |= {v ^ mk for v in s}
    return sorted(s)


def queries(L, btns, q, p_same=0.02, p_reach=0.5):
    """random pairs; with probability p_reach the pair differs by a reachable mask (so the answer is not -1)"""
    sp = span(L, btns)
    full = 1 << L
    pats = [pat(L, x) for x in range(full)]
    rr = random.random
    out = []
    for _ in range(q):
        a = random.getrandbits(L)
        r = rr()
        if r < p_same:
            b = a
        elif r < p_same + p_reach:
            b = a ^ sp[int(rr() * len(sp))]
        else:
            b = int(rr() * full)
        out.append((pats[a], pats[b]))
    return out


# samples
add(3, [[1, 2], [2, 3], [3]], [("000", "001"), ("110", "011"), ("101", "000")])
add(4, [[1, 2], [3, 4]], [("0000", "1111"), ("1100", "0011"), ("0000", "1000"), ("1111", "0000")])
add(1, [[1]], [("0", "1"), ("0", "0"), ("1", "0")])
add(5, [[1, 2, 3], [3, 4], [5], [1, 2, 3]],
    [("00000", "11011"), ("11100", "00111"), ("10000", "01000"), ("00000", "00000")])
add(8, [[1, 2], [2, 3, 4], [5, 8], [6, 7, 8], [1, 5], [3, 6]],
    [("11001001", "01110111"), ("10001000", "01010100"), ("10111110", "00000000")])
# hidden: small (the brute force tries every subset of buttons)
add(1, [[1], [1]], [("1", "1"), ("1", "0"), ("0", "1")])
add(2, [[1, 2]], [(a, b) for a in ("00", "01", "10", "11") for b in ("00", "01", "10", "11")])
for L, m in ((4, 6), (5, 8), (6, 10), (7, 12), (8, 12)):
    bt = [rand_btn(L, 1, 3) for _ in range(m)]
    add(L, bt, queries(L, bt, 40, 0.1))
bt = [[i, i + 1] for i in range(1, 12)] + [[12]]
add(12, bt, queries(12, bt, 50, 0.05))
# hidden: medium
bt = [rand_btn(10, 1, 4) for _ in range(30)]
add(10, bt, queries(10, bt, 1000))
bt = [rand_btn(14, 2, 2) for _ in range(20)]
add(14, bt, queries(14, bt, 5000))
bt = [rand_btn(16, 1, 16)]                                           # a single button
add(16, bt, queries(16, bt, 3000, 0.05, 0.3))
# hidden: large
L, M, Q = MAXL, MAXM, MAXQ
bt = [rand_btn(L, 1, L) for _ in range(M)]
add(L, bt, queries(L, bt, Q))
bt = [[i] for i in range(1, L + 1)]                                  # one lamp per button
add(L, bt, queries(L, bt, Q))
bt = [[i, i + 1] for i in range(1, L)]                               # neighbouring pairs: half of all patterns
add(L, bt, queries(L, bt, Q))
bt = [[i, i + 1] for i in range(1, L)] + [[L]]                       # long answers (up to L presses)
add(L, bt, queries(L, bt, Q))
base = [rand_btn(L, 3, 8) for _ in range(9)]                         # a small span: many -1
bt = []
while len(bt) < M:
    mk = 0
    for b in random.sample(base, random.randint(1, 4)):
        mk ^= sum(1 << (x - 1) for x in b)
    if mk:
        bt.append([t + 1 for t in range(L) if mk >> t & 1])
add(L, bt, queries(L, bt, Q, 0.02, 0.4))
bt = [rand_btn(L, 10, L) for _ in range(M)]                          # heavy buttons
add(L, bt, queries(L, bt, Q))
bt = [rand_btn(L, 1, 2) for _ in range(M)]                           # many copies of light buttons
add(L, bt, queries(L, bt, Q))
bt = [sorted({1 + (i % L), 1 + ((i + 5) % L)}) for i in range(M)]    # 16 distinct buttons, each 12 or 13 times
add(L, bt, queries(L, bt, Q))
bt = [rand_btn(L, 1, L) for _ in range(M)]                          # 16 = 8 + 8 lamps: two halves
bt = [[x for x in b if x <= 8] or [1] for b in bt[:100]] + [[x for x in b if x > 8] or [L] for b in bt[100:]]
add(L, bt, queries(L, bt, Q))
bt = [list(range(1, i + 1)) for i in range(1, L + 1)]                # prefixes
add(L, bt, queries(L, bt, Q))
bt = [rand_btn(L, 2, 5) for _ in range(40)]
add(L, bt, queries(L, bt, Q, 0.01, 0.8))
bt = [rand_btn(15, 1, 15) for _ in range(M)]
add(15, bt, queries(15, bt, Q))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
