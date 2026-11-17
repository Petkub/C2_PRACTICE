# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(150009)
MAXN, MAXA = 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    par = [0, 0]
    half = max(1, n // 2)
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "caterpillar":
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":
            p = i - 1 if i <= half else half
        elif kind == "combs":
            p = 1 if i <= 21 else (i - 20 if random.random() < 0.5 else ri(2, i - 1))
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def mine(n, kind):
    par = shape(n, kind)
    assert all(1 <= par[i] < i for i in range(2, n + 1))
    lab = list(range(2, n + 1))
    random.shuffle(lab)
    lab = [1] + lab
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    return p


def add(n, a, p):
    assert 2 <= n <= MAXN and len(a) == n + 1 and len(p) == n + 1
    kids = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        kids[p[i]].append(i)
    seen, k = [1], 0
    while k < len(seen):
        seen.extend(kids[seen[k]])
        k += 1
    assert len(seen) == n
    assert all(1 <= a[i] <= MAXA for i in range(1, n + 1))
    tests.append(f"{n}\n" + " ".join(map(str, a[1:])) + "\n" + " ".join(map(str, p[2:])) + "\n")


def gold(n, lo=1, hi=MAXA, rich=0.0):
    if rich == 0.0:
        return [0] + [ri(lo, hi) for _ in range(n)]
    return [0] + [ri(hi // 2, hi) if random.random() < rich else ri(lo, lo + 9) for _ in range(n)]


def trunk(n, t):
    p = [0, 0]
    a = [0, ri(1, 10)]
    for i in range(2, n + 1):
        if i <= t + 1:
            p.append(i - 1)
            a.append(ri(10**8, MAXA))
        elif i % 3 == 0:
            p.append(t + 1)
            a.append(ri(1, 10**6))
        elif i % 3 == 1:
            p.append(1)
            a.append(ri(10**7, 10**8))
        else:
            p.append(i - 1 if p[i - 1] == 1 else 1)
            a.append(ri(10**7, 10**8))
    lab = list(range(2, n + 1))
    random.shuffle(lab)
    lab = [1] + lab
    pp, aa = [0] * (n + 1), [0] * (n + 1)
    for i in range(1, n + 1):
        aa[lab[i - 1]] = a[i]
        if i >= 2:
            pp[lab[i - 1]] = lab[p[i] - 1]
    return aa, pp


def case(n, kind, lo=1, hi=MAXA, rich=0.0):
    add(n, gold(n, lo, hi, rich), mine(n, kind))


add(6, [0, 5, 3, 1, 4, 2, 7], [0, 0, 1, 1, 2, 2, 3])
add(7, [0, 1, 1, 1, 3, 9, 4, 2], [0, 0, 1, 2, 3, 3, 3, 2])
add(2, [0, 7, 3], [0, 0, 1])
add(5, [0, 4, 5, 1, 3, 2], [0, 0, 1, 1, 1, 1])
add(10, [0, 2, 8, 1, 6, 3, 5, 4, 9, 2, 1], [0, 0, 6, 10, 1, 6, 1, 5, 4, 10, 4])

case(3, "path")
case(9, "random", 1, 10)
case(14, "binary", 1, 20)
case(15, "star", 1, 5)
case(20, "caterpillar", 1, 100, rich=0.3)
case(30, "deep", 1, 50)
add(40, *trunk(40, 8))
case(2000, "random", rich=0.1)
case(5000, "path")
case(5000, "broom", 1, 1000)
add(4000, *trunk(4000, 300))

N = MAXN
case(N, "random", rich=0.05)
case(N, "random", 1, 10)
case(N, "deep")
case(N, "binary", rich=0.2)
case(N, "caterpillar")
case(N, "caterpillar", MAXA, MAXA)
case(N, "broom", 1, 3)
case(N, "star")
case(N, "combs", rich=0.02)
add(N, *trunk(N, 3000))
add(N, *trunk(N, 20_000))
case(N, "deep", 1, MAXA, rich=0.01)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
