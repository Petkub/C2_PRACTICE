# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(150131)
MAXN, MAXA = 200_000, 10**6
SMOOTH = [720720, 360360, 240240, 166320, 110880, 55440, 27720, 5040, 2520, 720, 360, 120, 60, 12, 6, 2, 1]
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    """par[i] (< i) for the people 2..n of a family of the given shape, before relabelling"""
    par = [0, 0]
    half = max(1, n // 2)
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":                        # depth about n / 2, many short side branches
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "caterpillar":                 # a chain of n / 2 people, the others hang from it
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":                       # a long chain ending in many children
            p = i - 1 if i <= half else half
        elif kind == "twopaths":                    # two long chains from person 1
            p = 1 if i <= 3 else i - 2
        elif kind == "forks":                       # a long chain, every 50th person starts a branch of 40
            p = i - 1 if i % 50 else max(1, i - 41)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def family(n, kind):
    par = shape(n, kind)
    assert all(1 <= par[i] < i for i in range(2, n + 1))
    lab = list(range(2, n + 1))
    random.shuffle(lab)
    lab = [1] + lab
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    return p, lab, par


def add(n, a, p):
    assert 2 <= n <= MAXN and len(a) == n + 1 and len(p) == n + 1
    kids = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        kids[p[i]].append(i)
    seen, k = [1], 0                      # everybody descends from person 1
    while k < len(seen):
        seen.extend(kids[seen[k]])
        k += 1
    assert len(seen) == n
    assert all(1 <= a[i] <= MAXA for i in range(1, n + 1))
    tests.append(f"{n}\n" + " ".join(map(str, a[1:])) + "\n" + " ".join(map(str, p[2:])) + "\n")


def numbers(n, mode, lab=None, par=None):
    if mode == "ones":
        return [0] + [1] * n
    if mode == "small":
        return [0] + [ri(1, 12) for _ in range(n)]
    if mode == "smooth":                  # many divisors each
        return [0] + [SMOOTH[int(random.random() * len(SMOOTH))] for _ in range(n)]
    if mode == "random":
        return [0] + [ri(1, MAXA) for _ in range(n)]
    if mode == "grow":                    # going down, each number is a multiple of the one above (until too big)
        val = [0] * (n + 1)
        val[1] = ri(1, 3)
        for i in range(2, n + 1):
            up = val[par[i]]
            m = ri(1, 3)
            val[i] = up * m if up * m <= MAXA else ri(1, 6)
        a = [0] * (n + 1)
        for i in range(1, n + 1):
            a[lab[i - 1]] = val[i]
        return a
    raise ValueError(mode)


def case(n, kind, mode):
    p, lab, par = family(n, kind)
    add(n, numbers(n, mode, lab, par), p)


# samples
add(7, [0, 2, 4, 3, 4, 8, 9, 6], [0, 0, 1, 1, 2, 2, 3, 6])
add(4, [0, 1, 1, 1, 1], [0, 0, 1, 2, 3])
add(2, [0, 3, 5], [0, 0, 1])
add(4, [0, 1, 2, 3, 5], [0, 0, 1, 1, 1])
add(9, [0, 30, 18, 30, 3, 12, 5, 10, 9, 6], [0, 0, 9, 4, 5, 1, 9, 9, 3, 8])
# hidden: small and medium (the brute force checks these)
case(3, "path", "small")
case(10, "random", "small")
case(30, "binary", "smooth")
case(60, "star", "small")
case(200, "caterpillar", "grow")
case(1000, "random", "smooth")
case(3000, "deep", "small")
case(5000, "broom", "random")
# hidden: maximum size (deep families)
N = MAXN
case(N, "path", "ones")                   # every pair: N (N - 1) / 2
case(N, "path", "grow")
case(N, "deep", "small")
case(N, "deep", "smooth")
case(N, "caterpillar", "small")
case(N, "caterpillar", "grow")
case(N, "broom", "small")
case(N, "broom", "ones")
case(N, "twopaths", "smooth")
case(N, "forks", "small")
case(N, "forks", "random")
case(N, "deep", "grow")
case(N, "path", "smooth")

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
