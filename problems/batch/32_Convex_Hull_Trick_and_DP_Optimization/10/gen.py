# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(321011)
MAXN, MAXX, MAXH, MAXP = 100_000, 10 ** 9, 10 ** 9, 10 ** 9
tests = []


def add(x, h, p):
    n = len(x)
    assert 1 <= n <= MAXN and len(h) == n and len(p) == n
    assert all(1 <= v <= MAXX for v in x) and all(x[i] < x[i + 1] for i in range(n - 1))
    assert all(1 <= v <= MAXH for v in h) and all(h[0] < v for v in h[1:])
    assert all(0 <= v <= MAXP for v in p)
    tests.append(f"{n}\n" + " ".join(map(str, x)) + "\n" + " ".join(map(str, h)) + "\n"
                 + " ".join(map(str, p)) + "\n")


def rint(a, b):
    return random.randint(a, b)


def positions(n, kind):
    if kind == "dense":
        x, cur = [], rint(1, 1000)
        for _ in range(n):
            x.append(cur)
            cur += rint(1, 3)
        return x
    if kind == "wide" or kind == "ends":
        x = sorted(random.sample(range(2, MAXX), n))
        if kind == "ends":
            x[0], x[-1] = 1, MAXX
        return x
    if kind == "clusters":
        x, cur = [], rint(1, 1000)
        step = MAXX // (n // 50 + 2)
        for i in range(n):
            if i % 50 == 0 and i:
                cur += rint(step // 2, step)
            x.append(cur)
            cur += rint(1, 5)
        return x
    raise ValueError(kind)


def heights(n, kind, H=MAXH):
    if kind == "rand":
        h = [rint(2, H) for _ in range(n)]
    elif kind == "few":
        k = rint(3, 7)
        h = [rint(2, k) for _ in range(n)]
    elif kind == "steps":
        h, cur = [], 2
        while len(h) < n:
            h += [cur] * rint(1, 40)
            cur += rint(-3, 6)
            cur = max(cur, 2)
        h = h[:n]
    elif kind == "inc":
        h = sorted(random.sample(range(2, H + 1), n))
        for _ in range(n // 20):
            i = rint(1, n - 1)
            h[i] = max(2, h[i] - rint(0, H // 50))
    elif kind == "dec":
        h = sorted(random.sample(range(2, H + 1), n), reverse=True)
    elif kind == "vee":
        half = n // 2
        h = sorted(random.sample(range(2, H // 2), half), reverse=True) + sorted(random.sample(range(2, H // 2), n - half))
    elif kind == "zigzag":
        h = [rint(2, H // 3) if i % 2 else rint(H // 3, H) for i in range(n)]
    elif kind == "waves":
        h, base = [], 1
        while len(h) < n:
            run = rint(5, 300)
            top = base + rint(run + 1, run + 1000)
            for t in range(run):
                h.append(top - 1 - t)
            base = top
        h = h[:n]
        assert max(h) <= H
    else:
        raise ValueError(kind)
    h[0] = 1
    return h


def bonuses(n, kind):
    if kind == "zero":
        return [0] * n
    if kind == "small":
        return [rint(0, 100) for _ in range(n)]
    if kind == "max":
        return [MAXP] * n
    return [rint(0, MAXP) for _ in range(n)]


def make(n, xk, hk, pk):
    add(positions(n, xk), heights(n, hk), bonuses(n, pk))


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


add([1, 3, 4, 7, 9], [1, 2, 4, 3, 5], [0, 3, 12, 9, 8])
add([1, 2, 6, 7], [1, 5, 2, 3], [0, 4, 1, 20])
add([7], [5], [3])
add([6, 7, 8, 12, 13, 15], [1, 6, 8, 3, 7, 8], [0, 16, 26, 2, 22, 15])
add([1, 500000000, 1000000000], [1, 3, 2], [0, 1000000000, 0])

add([5, 6, 8], [1, 9, 4], [0, 0, 0])
make(8, "wide", "few", "rand")
make(30, "dense", "rand", "small")
make(200, "wide", "vee", "rand")
make(1000, "dense", "waves", "small")
make(2000, "clusters", "steps", "rand")
make(3000, "dense", "zigzag", "rand")
make(5000, "wide", "dec", "rand")

n = MAXN
add(positions(n, "ends"), [1] + [MAXH] * (n - 2) + [2], [0] * n)

for xk, hk, pk in [("dense", "rand", "rand"), ("dense", "rand", "small"), ("dense", "few", "rand"),
                   ("clusters", "steps", "rand"), ("wide", "inc", "max"), ("ends", "inc", "rand"),
                   ("dense", "vee", "rand"), ("clusters", "vee", "max"), ("dense", "waves", "rand"),
                   ("wide", "waves", "zero"), ("clusters", "zigzag", "rand"), ("wide", "rand", "max"),
                   ("dense", "steps", "max")]:
    make(MAXN, xk, hk, pk)
write_all()
