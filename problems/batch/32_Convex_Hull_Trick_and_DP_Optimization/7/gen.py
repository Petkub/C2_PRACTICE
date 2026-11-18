# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(320606)
MAXN, MAXX, MAXF, MAXP = 120_000, 1_000_000, 10 ** 9, 1_000_000
tests = []


def add(x, f, p, D):
    n = len(x)
    assert 2 <= n <= MAXN and len(f) == len(p) == len(D) == n - 1
    assert 1 <= x[0] and x[-1] <= MAXX and all(x[i] < x[i + 1] for i in range(n - 1))
    assert all(1 <= v <= MAXF for v in f) and all(1 <= v <= MAXP for v in p) and all(1 <= v <= MAXX for v in D)
    tests.append(f"{n}\n" + "\n".join(" ".join(map(str, a)) for a in (x, f, p, D)) + "\n")


def positions(n, kind):
    rnd = random.random
    if kind == "dense":
        return list(range(1, n + 1))
    s = set()
    while len(s) < n:
        s.add(1 + int(rnd() * MAXX))
    return sorted(s)


def make(n, xk, mode, fk="rand", pmax=MAXP):
    rnd = random.random
    x = positions(n, xk)
    span = x[-1] - x[0]
    f, p, D = [], [], []
    for j in range(n - 1):
        pj = 1 + int(rnd() * pmax)
        fj = 1 + int(rnd() * (MAXF if fk == "rand" else 1000))
        need = x[j + 1] - x[j]
        if mode == "long":
            dj = max(need, MAXX - int(rnd() * span // 20))
        elif mode == "trade":
            dj = max(need, int(span * (pj / pmax) ** 0.5))
        elif mode == "gaps":
            dj = need - 1 if (rnd() < 0.0005 and need > 1) else max(need, int(rnd() * span / 3))
            dj = max(1, dj)
        else:
            raise ValueError(mode)
        f.append(fj)
        p.append(pj)
        D.append(min(MAXX, dj))
    add(x, f, p, D)


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_000_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


add([1, 3, 6, 10], [5, 2, 4], [3, 1, 2], [9, 7, 4])
add([2, 4, 9, 12], [1, 1, 1], [1, 1, 1], [2, 4, 3])
add([1, 1000000], [1000000000], [1000000], [999999])
add([5, 6, 8, 11, 15, 20], [3, 9, 1, 2, 6], [4, 1, 5, 2, 3], [10, 14, 3, 9, 5])
add([1, 2, 3, 4, 5], [10, 1, 1, 1], [1, 9, 9, 9], [4, 1, 1, 1])

make(2, "rand", "long")
make(8, "dense", "trade", "small")
make(40, "rand", "gaps")
make(300, "dense", "trade")
make(2000, "rand", "trade", "small")
make(10_000, "rand", "gaps")
make(30_000, "dense", "long", "small")
make(60_000, "rand", "trade")
make(90_000, "rand", "long", "rand")
make(90_000, "dense", "trade", "rand")

for xk, mode, pmax in [("rand", "long", 1000), ("dense", "long", 1000), ("dense", "long", 30),
                       ("rand", "trade", 1000), ("dense", "trade", 1000), ("rand", "trade", 100),
                       ("dense", "long", 1000), ("rand", "long", 50), ("dense", "trade", 300),
                       ("rand", "long", 1000), ("dense", "trade", 1000)]:
    make(MAXN, xk, mode, "small", pmax)
write_all()
