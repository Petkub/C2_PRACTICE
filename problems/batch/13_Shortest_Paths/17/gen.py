# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(131818)
MAXN, MAXM, MAXQ, MAXT = 17, 100, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        a[i], a[j] = a[j], a[i]


def add(n, start, programs, queries, mix=True):
    programs = list(programs)
    if mix:
        shuffle(programs)
    m, q = len(programs), len(queries)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and 1 <= q <= MAXQ
    assert len(start) == n and set(start) <= set("01")
    for t, need, eff in programs:
        assert 1 <= t <= MAXT and len(need) == n and len(eff) == n and set(need + eff) <= set("01.")
    for s in queries:
        assert len(s) == n and set(s) <= set("01")
    tests.append(f"{n} {m} {q}\n{start}\n" + "".join(f"{t} {need} {eff}\n" for t, need, eff in programs)
                 + "".join(s + "\n" for s in queries))


def bits(x, n):
    """machine i (1-based) is bit i - 1"""
    return "".join("1" if x >> i & 1 else "0" for i in range(n))


def rnd_pattern(n, p1=0.5):
    return "".join("1" if random.random() < p1 else "0" for _ in range(n))


def rnd_rule(n, p):
    return "".join(random.choice("01") if random.random() < p else "." for _ in range(n))


def rnd_programs(n, m, p_need, p_eff, tlo, thi):
    return [(ri(tlo, thi), rnd_rule(n, p_need), rnd_rule(n, p_eff)) for _ in range(m)]


def counter(n, tlo, thi, perm=None):
    """program i: machine i running and machines before it stopped -> machine i stops, machines before it run
    (a binary counter going down by one); machines are renamed by perm"""
    perm = perm or list(range(n))
    res = []
    for i in range(n):
        need, eff = ["."] * n, ["."] * n
        need[perm[i]], eff[perm[i]] = "1", "0"
        for k in range(i):
            need[perm[k]], eff[perm[k]] = "0", "1"
        res.append((ri(tlo, thi), "".join(need), "".join(eff)))
    return res


def shortcuts(n, k, start, t):
    """expensive programs that jump from the start pattern straight to a random pattern"""
    return [(t, start, rnd_pattern(n)) for _ in range(k)]


def queries(n, q, reach=None):
    return [rnd_pattern(n) if reach is None or random.random() < 0.2 else random.choice(reach) for _ in range(q)]


# samples
add(3, "111", [(4, "1.1", "0.."), (1, "0..", ".0."), (2, "00.", "..0"), (5, "..0", "1..")],
    ["000", "011", "110"], False)
add(2, "10", [(3, "1.", "01"), (7, ".1", ".0")], ["10", "01", "00", "11"], False)
add(4, "0000", [(2, "...0", "...1"), (3, "...1", "..10"), (6, "..1.", "1..."), (1, "1...", ".1.0")],
    ["0001", "1100", "1111"], False)
add(3, "101", [(MAXT, "1..", "0.."), (MAXT, "..1", "..0"), (1, "0.0", "010")], ["000", "010", "111"], False)
add(1, "1", [(9, "1", "0"), (4, "0", "1")], ["0", "1"], False)
# hidden: small (checked against the brute force)
add(5, "11111", counter(5, 1, 3), ["00000", "10101", "11110"])
for n, m, pn, pe, thi, q in ((3, 4, 0.5, 0.5, 10, 8), (4, 6, 0.3, 0.6, 5, 16), (6, 10, 0.4, 0.4, 100, 30),
                             (8, 20, 0.3, 0.3, MAXT, 50), (10, 30, 0.2, 0.3, 1000, 100)):
    add(n, rnd_pattern(n), rnd_programs(n, m, pn, pe, 1, thi), queries(n, q))
add(8, "1" * 8, counter(8, 1, 10) + shortcuts(8, 3, "1" * 8, 3000), [bits(x, 8) for x in range(256)])
add(10, "1" * 10, counter(10, MAXT // 2, MAXT, random.sample(range(10), 10)), queries(10, 200))
add(12, rnd_pattern(12), rnd_programs(12, 40, 0.15, 0.25, 1, 50), queries(12, 1000))
# hidden: maximum size
n, Q = MAXN, MAXQ
add(n, "1" * n, counter(n, MAXT - 1000, MAXT) + rnd_programs(n, 80, 0.5, 0.2, MAXT, MAXT), queries(n, Q))
add(n, "1" * n, counter(n, 1, MAXT, random.sample(range(n), n)) + shortcuts(n, 80, "1" * n, MAXT)
    , queries(n, Q))
add(n, rnd_pattern(n), rnd_programs(n, MAXM, 0.15, 0.2, 1, MAXT), queries(n, Q))
add(n, rnd_pattern(n), rnd_programs(n, MAXM, 0.1, 0.1, 1, 10), queries(n, Q))
add(n, "0" * n, rnd_programs(n, MAXM, 0.3, 0.15, 1, 1000), queries(n, Q))
b = rnd_programs(n, MAXM - n, 0.2, 0.15, 10**6, MAXT)
for i in range(n):                        # cheap one-machine programs that need a long chain of steps
    need, eff = ["."] * n, ["."] * n
    need[i], eff[i] = "0", "1"
    if i:
        need[i - 1] = "1"
    b.append((1, "".join(need), "".join(eff)))
add(n, "0" * n, b, queries(n, Q))
add(n, "1" * n, counter(n, 1, 1) + rnd_programs(n, 80, 0.4, 0.3, 2, 3), queries(n, Q))
add(n, rnd_pattern(n), [(ri(1, MAXT), rnd_rule(n, 0.05), rnd_rule(n, 0.05)) for _ in range(MAXM)], queries(n, Q))
add(n, "1" * n, counter(n, MAXT, MAXT), [bits(x, n) for x in random.sample(range(1 << n), Q)])
add(n, rnd_pattern(n), rnd_programs(n, MAXM, 0.6, 0.5, 1, MAXT), queries(n, Q))
add(16, rnd_pattern(16), rnd_programs(16, MAXM, 0.15, 0.2, 1, MAXT), queries(16, Q))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
