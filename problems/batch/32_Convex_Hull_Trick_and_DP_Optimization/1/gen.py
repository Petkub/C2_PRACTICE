# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(320909)
MAXN = MAXM = 100_000
MAXX, MAXB, MAXT = 10 ** 9, 10 ** 9, 1_000_000
tests = []


def add(x, wells):
    n, m = len(x), len(wells)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= v <= MAXX for v in x)
    assert all(1 <= q <= MAXX and 1 <= b <= MAXB and 1 <= t <= MAXT for q, b, t in wells)
    tests.append(f"{n} {m}\n" + " ".join(map(str, x)) + "\n" + "".join(f"{q} {b} {t}\n" for q, b, t in wells))


def rint(a, b):
    return random.randint(a, b)


def make(n, m, kind, X=MAXX, B=100_000, T=100):
    if kind == "left":
        x = [rint(1, X // 2) for _ in range(n)]
        w = [(rint(X // 2 + 1, X), rint(1, B), rint(1, T)) for _ in range(m)]
    elif kind == "right":
        x = [rint(X // 2 + 1, X) for _ in range(n)]
        w = [(rint(1, X // 2), rint(1, B), rint(1, T)) for _ in range(m)]
    else:
        x = [rint(1, X) for _ in range(n)]
        w = [(rint(1, X), rint(1, B), rint(1, T)) for _ in range(m)]
        if kind == "farcheap":
            w = [(q, rint(B // 2, B), rint(T // 2, T)) for q, _, _ in w]
            for i in random.sample(range(m), min(m, 30)):
                w[i] = (w[i][0], rint(1, 10), 1)
        elif kind == "eqt":
            t = rint(1, T)
            w = [(q, b, t) for q, b, _ in w]
        elif kind == "eqb":
            b = rint(1, B)
            w = [(q, b, t) for q, _, t in w]
        elif kind == "sortedx":
            x.sort()
        else:
            assert kind in ("rand", "dense")
    add(x, w)


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


add([1, 5, 8, 11], [(3, 10, 2), (8, 2, 5), (12, 7, 1)])
add([10, 20, 10], [(5, 100, 3), (5, 1, 20)])
add([1], [(10 ** 9, 10 ** 9, 10 ** 6)])
add([17, 21, 33, 23, 30, 21, 17], [(18, 19, 6), (30, 12, 4), (28, 25, 3), (38, 12, 8)])
add([32, 10, 24, 40, 6, 17], [(32, 12, 4), (27, 38, 1), (2, 53, 7), (39, 39, 2), (29, 34, 7)])

add([7], [(7, 5, 3)])
make(10, 10, "rand", 50, 60, 9)
make(200, 200, "farcheap", 10 ** 4, 1000, 50)
make(1000, 1000, "rand", 10 ** 6, 10 ** 6, 1000)
make(3000, 5, "rand", 10 ** 9, 10 ** 9, 10 ** 6)
make(5, 3000, "farcheap")
make(20_000, 20_000, "dense", 3000, 1000, 30)
make(50_000, 50_000, "rand", MAXX, MAXB, MAXT)
make(60_000, 60_000, "farcheap")

for kind, X, B, T in [("rand", MAXX, 100_000, 100), ("farcheap", MAXX, 100_000, 100), ("left", MAXX, 100_000, 100),
                      ("right", MAXX, 100_000, 100), ("dense", 50_000, 1000, 1000), ("eqt", MAXX, 10 ** 6, 100),
                      ("eqb", MAXX, 10 ** 6, 1000), ("sortedx", MAXX, 100_000, 100), ("rand", 10 ** 7, 10 ** 6, MAXT),
                      ("farcheap", 10 ** 8, 10 ** 6, 1000), ("rand", 10 ** 6, 1000, 1000), ("farcheap", MAXX, 10 ** 5, 10)]:
    make(MAXN, MAXM, kind, X, B, T)
write_all()
