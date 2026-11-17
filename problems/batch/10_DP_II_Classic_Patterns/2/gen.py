# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(10002)
MAXN, MAXM, MAXC = 300, 20, 10**9
tests = []


def add(A, p, q):
    n = len(p)
    m = [len(r) for r in p]
    assert 1 <= n <= MAXN and len(q) == n
    assert all(1 <= m[i] <= MAXM and len(q[i]) == m[i] for i in range(n))
    assert 0 <= A <= sum(m)
    assert all(0 <= c <= MAXC for r in p + q for c in r)
    lines = [f"{n} {A} {sum(m) - A}", " ".join(map(str, m))]
    lines += [" ".join(map(str, r)) for r in p] + [" ".join(map(str, r)) for r in q]
    tests.append("\n".join(lines) + "\n")


def table(m, kind, hi):
    """prices of 1..m bags for one village"""
    if kind == "rand":
        return [random.randint(0, hi) for _ in range(m)]
    if kind == "up":                       # price grows with the number of bags
        return sorted(random.randint(0, hi) for _ in range(m))
    if kind == "bulk":                     # a big package may be cheaper than a small one
        base = sorted(random.randint(hi // 2, hi) for _ in range(m))
        return [base[j] if random.random() < 0.6 else random.randint(0, hi // 3) for j in range(m)]
    if kind == "linear":                   # the same price per bag: many cheapest splits
        c = random.randint(1, 3)
        return [c * (j + 1) for j in range(m)]
    if kind == "same":
        return [hi] * m
    raise ValueError(kind)


def case(n, m_lo, m_hi, kind, hi, A=None):
    m = [random.randint(m_lo, m_hi) for _ in range(n)]
    p = [table(x, kind, hi) for x in m]
    q = [table(x, kind, hi) for x in m]
    if A is None:
        A = random.randint(sum(m) * 9 // 20, sum(m) * 11 // 20)
    add(A, p, q)


# samples
add(4, [[15, 28], [10, 30, 35], [20, 45]], [[10, 20], [12, 20, 40], [5, 30]])
add(3, [[20, 30], [40, 50], [20, 50]], [[10, 60], [20, 50], [20, 40]])
add(0, [[7, 8, 9], [1, 1]], [[4, 6, 10], [3, 3]])
add(2, [[5, 9, 12, 20]], [[6, 7, 30, 31]])
add(5, [[40, 15, 50], [20, 35, 30], [25, 10, 45]], [[30, 30, 60], [10, 50, 20], [5, 40, 35]])
# hidden: small (brute.cpp tries every split)
add(1, [[0]], [[0]])
add(0, [[5, 6]], [[7, 1000000000]])
case(4, 1, 3, "rand", 3)
case(5, 1, 4, "rand", 20)
case(6, 1, 4, "linear", 0)
case(6, 2, 4, "bulk", MAXC)
case(5, 1, 4, "same", MAXC)
case(6, 1, 4, "up", 50, A=1)
case(6, 1, 3, "rand", 2)
# hidden: medium and lopsided
case(300, 20, 20, "rand", MAXC, A=5)
case(300, 1, 20, "up", MAXC, A=0)
case(100, 1, 20, "rand", 3)
# hidden: maximum size
N = MAXN
case(N, 20, 20, "rand", MAXC)
case(N, 20, 20, "rand", 3)
case(N, 20, 20, "up", MAXC)
case(N, 20, 20, "bulk", MAXC)
case(N, 20, 20, "linear", 0)
case(N, 20, 20, "same", MAXC)
case(N, 20, 20, "same", 0)
case(N, 20, 20, "up", 10)
case(N, 18, 20, "rand", MAXC // 1000)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
