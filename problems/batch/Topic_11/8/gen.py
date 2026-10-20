# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90801)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, st):
    m = len(st)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM
    assert all(t in "SD" and 1 <= a <= n and 1 <= b <= n for (t, a, b) in st)
    tests.append(f"{n} {m}\n" + "".join(f"{t} {a} {b}\n" for (t, a, b) in st))


def truth(n):
    """a hidden true team for everybody"""
    return [0] + [ri(0, 1) for _ in range(n)]


def stmt(team, a, b, lie):
    """a statement about a and b that is true for the hidden teams (or false if lie)"""
    same = (team[a] == team[b]) != lie
    return ("S" if same else "D", a, b)


def rnd(n, m, plie, a_eq_b=0.0):
    team = truth(n)
    res = []
    for _ in range(m):
        a = ri(1, n)
        b = a if random.random() < a_eq_b else ri(1, n)
        res.append(stmt(team, a, b, random.random() < plie))
    return res


def chain_then_ask(n, m, plie, rev=False):
    """a long path of true statements first (one huge group), then statements across it"""
    team = truth(n)
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    res = []
    for i in range(n - 1):
        a, b = perm[i], perm[i + 1]
        res.append(stmt(team, b, a, False) if rev else stmt(team, a, b, False))
    while len(res) < m:
        res.append(stmt(team, ri(1, n), ri(1, n), random.random() < plie))
    return res


def star(n, m, plie, big_first):
    """every new player is attached to the big group: relabelling the big side each time is slow"""
    team = truth(n)
    res = []
    for v in range(2, n + 1):
        u = ri(1, v - 1)
        res.append(stmt(team, u, v, False) if big_first else stmt(team, v, u, False))
    while len(res) < m:
        res.append(stmt(team, ri(1, n), ri(1, n), random.random() < plie))
    return res[:m]


def path_in_order(n, m, plie, up):
    """statements 1-2, 2-3, 3-4, ... (or reversed): a union without sizes builds a long chain"""
    team = truth(n)
    res = []
    for i in range(1, n):
        res.append(stmt(team, i, i + 1, False) if up else stmt(team, i + 1, i, False))
    while len(res) < m:
        res.append(stmt(team, ri(1, n), ri(1, n), random.random() < plie))
    return res[:m]


# samples
add(4, [("S", 1, 2), ("D", 2, 3), ("S", 1, 3), ("D", 3, 4), ("D", 4, 1), ("S", 2, 4)])
add(3, [("D", 1, 2), ("D", 2, 3), ("D", 3, 1), ("S", 3, 1)])
add(1, [("D", 1, 1), ("S", 1, 1)])
add(5, [("D", 1, 2), ("D", 3, 4), ("S", 2, 3), ("D", 1, 4), ("D", 5, 5), ("D", 5, 1)])
add(6, [("S", 6, 5), ("D", 2, 4), ("D", 5, 2), ("S", 4, 6), ("D", 1, 1), ("S", 4, 2)])
# hidden: small
add(1, [("S", 1, 1)])
add(2, [("D", 1, 2), ("D", 2, 1), ("S", 1, 2), ("S", 2, 2), ("D", 2, 2), ("S", 1, 2)])
add(10, rnd(10, 30, 0.3, 0.1))
add(50, rnd(50, 200, 0.1))
add(300, chain_then_ask(300, 1000, 0.5))
add(1000, [("D", ri(1, 1000), ri(1, 1000)) for _ in range(3000)])    # odd cycles appear soon
add(2000, rnd(2000, 4000, 0.02, 0.01))
add(3000, [("S", ri(1, 3000), ri(1, 3000)) for _ in range(5000)])    # everything is believed
# hidden: maximum size
N, M = MAXN, MAXM
add(N, chain_then_ask(N, M, 0.5))
add(N, chain_then_ask(N, M, 0.3, rev=True))
add(N, star(N, M, 0.5, True))
add(N, star(N, M, 0.5, False))
add(N, path_in_order(N, M, 0.5, True))
add(N, path_in_order(N, M, 0.5, False))
add(N, rnd(N, M, 0.0))                                              # all true: all believed
add(N, rnd(N, M, 0.05))
add(N // 2, chain_then_ask(N // 2, M, 0.9))
add(2, [("S" if random.random() < 0.5 else "D", ri(1, 2), ri(1, 2)) for _ in range(M)])
add(N, [("D", ri(1, N), ri(1, N)) for _ in range(M)])
add(1000, rnd(1000, M, 0.5, 0.05))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
