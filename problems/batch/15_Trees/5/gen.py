# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100505)
MAXN, MAXF = 200_000, 10**6
tests = []


_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    rnd = _rnd
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))                                 # = ri(0, i)
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    """par[i] for i = 1..n-1 is a node in 0..i-1; node 0 is the root"""
    par = [-1] * n
    h = max(1, n // 2)
    for i in range(1, n):
        if kind == "random":
            par[i] = int(_rnd() * i)                            # = ri(0, i - 1)
        elif kind == "path":
            par[i] = i - 1
        elif kind == "star":
            par[i] = 0
        elif kind == "deep":                    # depth about n / 2, a few short side branches
            par[i] = ri(max(0, i - 3), i - 1)
        elif kind == "binary":
            par[i] = (i - 1) // 2
        elif kind == "broom":                   # a path of n / 2 nodes, then a star at its end
            par[i] = i - 1 if i <= h else h
        elif kind == "cater":                   # a path of n / 2 nodes with leaves hanging anywhere on it
            par[i] = i - 1 if i < h else ri(0, h - 1)
        elif kind == "twopaths":                # two long chains below the root
            par[i] = 0 if i <= 2 else i - 2
        else:
            raise ValueError(kind)
    return par


def labels(n, root=None):
    """a random numbering 1..n of the nodes 0..n-1; node 0 gets the number root if given"""
    lab = list(range(1, n + 1))
    shuf(lab)
    if root is not None:
        j = lab.index(root)
        lab[0], lab[j] = lab[j], lab[0]
    return lab


def add(f, b, is_tree=False):
    """b = [b_2, ..., b_N]; is_tree: check_shape() already showed that everybody reaches the president"""
    n = len(f)
    assert 2 <= n <= MAXN and len(b) == n - 1
    assert all(1 <= x <= MAXF for x in f)
    assert all(1 <= x <= n and x != i + 2 for i, x in enumerate(b))
    if not is_tree:
        ch = [[] for _ in range(n + 1)]                         # everybody reaches the president
        for i, x in enumerate(b):
            ch[x].append(i + 2)
        seen, st = 0, [1]
        while st:
            seen += 1
            st.extend(ch[st.pop()])
        assert seen == n
    tests.append(f"{n}\n" + " ".join(map(str, f)) + "\n" + " ".join(map(str, b)) + "\n")


def check_shape(par, lab):
    """every node hangs below an earlier node and node 0 (the root) is person 1: a tree rooted at person 1"""
    n = len(par)
    assert all(0 <= par[i] < i for i in range(1, n)) and sorted(lab) == list(range(1, n + 1)) and lab[0] == 1


def tree(n, kind, ffun):
    par, lab = shape(n, kind), labels(n, 1)
    check_shape(par, lab)
    b = [0] * (n + 1)
    for i in range(1, n):
        b[lab[i]] = lab[par[i]]
    add([ffun() for _ in range(n)], b[2:], True)


def tied(n, kind):
    """a boss is worth exactly the total of his direct staff, so many invitations tie"""
    par, lab = shape(n, kind), labels(n, 1)
    check_shape(par, lab)
    f = [0] * n
    ch = [[] for _ in range(n)]
    for i in range(1, n):
        ch[par[i]].append(i)
    for v in range(n - 1, -1, -1):
        s = sum(f[c] for c in ch[v])
        f[v] = s if 1 <= s <= MAXF and ri(0, 3) else ri(1, 3)
    b = [0] * (n + 1)
    for i in range(1, n):
        b[lab[i]] = lab[par[i]]
    ff = [0] * n
    for i in range(n):
        ff[lab[i] - 1] = f[i]
    add(ff, b[2:], True)


# samples
add([5, 4, 3, 2, 1, 6], [4, 1, 1, 4, 3])
add([5, 2, 3], [1, 1])
add([1, 1], [1])
add([2, 1, 3, 1, 2, 2, 1, 3], [5, 1, 6, 1, 1, 6, 4])
add([MAXF] * 5, [1, 2, 3, 4])
# hidden: small (every set is tried)
add([1, 2], [1])
add([1, 2, 1], [1, 2])
add([1, 1, 2, 1, 3, 1], [1, 2, 3, 4, 5])
for n, kind in ((7, "random"), (10, "path"), (12, "binary"), (15, "star"), (16, "cater"), (18, "random"),
                (20, "deep"), (20, "random")):
    tree(n, kind, lambda: ri(1, 3))
for n, kind in ((14, "random"), (17, "binary"), (20, "broom")):
    tied(n, kind)
tree(19, "random", lambda: ri(1, MAXF))
# hidden: maximum size
N = MAXN
tree(N, "path", lambda: MAXF)
tree(N, "random", lambda: ri(1, MAXF))
tree(N, "random", lambda: ri(1, 2))
tree(N, "deep", lambda: ri(1, 3))
tree(N, "star", lambda: ri(1, 10))
tree(N, "binary", lambda: ri(1, MAXF))
tied(N, "random")
tied(N, "binary")
tree(N, "broom", lambda: ri(1, 5))
tree(N, "twopaths", lambda: ri(1, MAXF))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
