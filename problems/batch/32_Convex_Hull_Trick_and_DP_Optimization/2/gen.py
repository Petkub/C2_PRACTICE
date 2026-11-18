# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(320101)
MAXN, MAXX, MAXA, MAXBC = 500_000, 100, 5, 10_000_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, b, c, x):
    n = len(x)
    assert 1 <= n <= MAXN and -MAXA <= a <= -1 and abs(b) <= MAXBC and abs(c) <= MAXBC
    assert all(0 <= v <= MAXX for v in x)
    tests.append(f"{n}\n{a} {b} {c}\n" + " ".join(map(str, x)) + "\n")


def arr(n, kind):
    rnd = random.random
    if kind == "rand":
        return [int(rnd() * (MAXX + 1)) for _ in range(n)]
    if kind == "zeros":
        return [0 if rnd() < 0.9 else 1 + int(rnd() * MAXX) for _ in range(n)]
    if kind == "allzero":
        return [0] * n
    if kind == "max":
        return [MAXX] * n
    if kind == "small":
        return [int(rnd() * 4) for _ in range(n)]
    if kind == "blocks":
        out = []
        while len(out) < n:
            v = 0 if rnd() < 0.5 else MAXX - int(rnd() * 5)
            out += [v] * (1 + int(rnd() * 50))
        return out[:n]
    raise ValueError(kind)


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_000_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


add(-1, 10, -20, [3, 1, 4, 1, 5])
add(-2, 3, 20, [2, 2, 1])
add(-1, 0, -7, [4, 6])
add(-5, 100, 1, [7])
add(-3, 50, 0, [1, 9, 2, 8, 3, 7])

add(-1, 5, 3, [0])
add(-4, -10_000_000, -10_000_000, [100, 100, 100])
add(-1, 300, -200, arr(40, "zeros"))
add(-2, 1000, 50, arr(200, "small"))
add(-1, 10_000_000, -10_000_000, arr(300, "rand"))
add(-3, 2500, 10_000, arr(2000, "blocks"))
add(-5, 40_000, -1_000_000, arr(5000, "zeros"))
add(-1, 200, 7, arr(20_000, "rand"))
add(-2, 0, 10_000_000, arr(50_000, "allzero"))
add(-1, 10_000_000, 10_000_000, arr(100_000, "small"))

add(-1, 10_000_000, -10_000_000, arr(MAXN, "rand"))
add(-5, -10_000_000, -10_000_000, arr(MAXN, "max"))
add(-1, 2_000_000, -10_000_000, arr(MAXN, "zeros"))
add(-2, 3_000_000, 5_000_000, arr(MAXN, "blocks"))
add(-1, 10_000_000, 10_000_000, arr(MAXN, "max"))
add(-3, 400, 1_000, arr(MAXN, "rand"))
add(-1, 0, 10_000_000, arr(MAXN, "allzero"))
add(-4, 9_999_991, -9_999_973, arr(MAXN, "small"))
write_all()
