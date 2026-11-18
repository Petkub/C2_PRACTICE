# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(320303)
MAXN, MAXS, MAXF, MAXW = 120_000, 1_000_000, 1_000_000, 10 ** 9
tests = []


def add(f0, s, f, w):
    n = len(s)
    assert 2 <= n <= MAXN and len(f) == n - 1 and len(w) == n - 1
    assert 1 <= f0 <= MAXF and all(1 <= v <= MAXS for v in s)
    assert all(1 <= v <= MAXF for v in f) and all(1 <= v <= MAXW for v in w)
    tests.append(f"{n} {f0}\n" + " ".join(map(str, s)) + "\n" + " ".join(map(str, f)) + "\n"
                 + " ".join(map(str, w)) + "\n")


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def make(n, fk, sk="rand", wk="rand", f0=None):
    rnd = random.random
    if sk == "rand":
        s = [1 + int(rnd() * MAXS) for _ in range(n)]
    elif sk == "small":
        s = [1 + int(rnd() * 100) for _ in range(n)]
    else:
        s = [MAXS] * n
    if fk == "rand":
        f = [1 + int(rnd() * MAXF) for _ in range(n - 1)]
    elif fk == "wave":
        f = [1 + int((MAXF - 1) * (0.5 + 0.5 * ((i * 37 % 1000) / 1000.0) * (1 if (i // 500) % 2 else -1))) for i in range(n - 1)]
    elif fk == "inc":
        f = sorted(1 + int(rnd() * MAXF) for _ in range(n - 1))
    elif fk == "dec":
        f = sorted((1 + int(rnd() * MAXF) for _ in range(n - 1)), reverse=True)
    else:
        f = [MAXF // 2 + int(rnd() * 1000) for _ in range(n - 1)]
    if wk == "rand":
        w = [1 + int(rnd() * MAXW) for _ in range(n - 1)]
    elif wk == "cheap":
        w = [1 + int(rnd() * 1000) for _ in range(n - 1)]
    else:
        w = [MAXW - int(rnd() * 1000) for _ in range(n - 1)]
    add(f0 if f0 is not None else MAXF, s, f, w)


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_100_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


add(5, [2, 3, 4, 1], [2, 4, 1], [3, 1, 10])
add(3, [1, 1, 1], [1, 2], [5, 1])
add(1, [7, 7], [1], [1])
add(9, [3, 1, 4, 1, 5], [6, 8, 2, 7], [2, 1, 4, 3])
add(10, [5, 2, 6, 3, 2, 4], [7, 9, 3, 2, 8], [4, 1, 6, 30, 2])

make(2, "rand", "small", "cheap", 3)
make(8, "wave", "small", "cheap", 50)
make(30, "rand", "small", "cheap")
make(200, "near", "rand", "cheap")
make(1000, "wave", "rand", "big")
make(5000, "inc", "rand", "cheap")
make(20_000, "rand", "small", "big")
make(50_000, "dec", "rand", "rand")

make(MAXN, "rand", "rand", "rand")
make(MAXN, "rand", "rand", "cheap")
make(MAXN, "wave", "rand", "cheap")
make(MAXN, "wave", "max", "big")
make(MAXN, "near", "rand", "cheap")
make(MAXN, "inc", "rand", "rand")
make(MAXN, "dec", "max", "cheap")
make(MAXN, "rand", "small", "big")
make(MAXN, "near", "max", "big")
make(MAXN, "rand", "max", "cheap", 1)
write_all()
