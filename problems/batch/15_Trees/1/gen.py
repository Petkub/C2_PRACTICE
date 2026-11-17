# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(100101)
MAXN = 200_000
tests = []


_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(_rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    par = [-1] * n
    h = max(1, n // 2)
    for i in range(1, n):
        if kind == "random":
            par[i] = int(_rnd() * i)
        elif kind == "path":
            par[i] = i - 1
        elif kind == "star":
            par[i] = 0
        elif kind == "deep":
            par[i] = ri(max(0, i - 3), i - 1)
        elif kind == "binary":
            par[i] = (i - 1) // 2
        elif kind == "broom":
            par[i] = i - 1 if i <= h else h
        elif kind == "cater":
            par[i] = i - 1 if i < h else ri(0, h - 1)
        elif kind == "twopaths":
            par[i] = 0 if i <= 2 else i - 2
        else:
            raise ValueError(kind)
    return par


def labels(n, root=None):
    lab = list(range(1, n + 1))
    shuf(lab)
    if root is not None:
        j = lab.index(root)
        lab[0], lab[j] = lab[j], lab[0]
    return lab


def add(p):
    n = len(p)
    assert 1 <= n <= MAXN
    assert sum(1 for x in p if x == 0) == 1
    assert all(0 <= x <= n and x != i + 1 for i, x in enumerate(p))

    ch = [[] for _ in range(n + 1)]
    for i, x in enumerate(p):
        ch[x].append(i + 1)
    seen, st = 0, [p.index(0) + 1]
    while st:
        v = st.pop()
        seen += 1
        st.extend(ch[v])
    assert seen == n
    tests.append(f"{n}\n" + " ".join(map(str, p)) + "\n")


def tree(n, kind, root=None):
    par, lab = shape(n, kind), labels(n, root)
    p = [0] * n
    for i in range(1, n):
        p[lab[i] - 1] = lab[par[i]]
    return p


add([3, 3, 0, 1, 1, 2])
add([2, 3, 4, 5, 0])
add([0])
add([0, 1, 1, 1, 1])
add([6, 0, 2, 6, 3, 2, 5, 4])

add([2, 0])
add([0, 1])
for n, kind in ((7, "random"), (10, "deep"), (12, "binary"), (15, "random"), (30, "cater"), (100, "deep"),
                (1000, "random"), (3000, "twopaths")):
    add(tree(n, kind))
add([i + 2 for i in range(4999)] + [0])

N = MAXN
add([i + 2 for i in range(N - 1)] + [0])
add([0] + [i for i in range(1, N)])
add(tree(N, "path"))
add(tree(N, "deep"))
add(tree(N, "star"))
add(tree(N, "random"))
add(tree(N, "broom"))
add(tree(N, "twopaths"))
add(tree(N, "binary"))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
