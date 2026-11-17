# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(30232)
MAXN, MAXQ = 500_000, 150_000
tests = []


def add(s, qs):
    n, q = len(s), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and set(s) <= set("OX")
    assert all(1 <= l <= r <= n for l, r in qs)
    tests.append(f"{n} {q}\n{s}\n" + "\n".join(f"{l} {r}" for l, r in qs) + "\n")


def song(n, p_miss):
    return "".join("X" if random.random() < p_miss else "O" for _ in range(n))


def runs(n, lo, hi):

    out = []
    while len(out) < n:
        out.extend("O" * random.randint(lo, hi))
        out.append("X")
    return "".join(out[:n])


def queries(n, q, mode):
    out = []
    for _ in range(q):
        if mode == "long":
            l = random.randint(1, max(1, n // 20))
            r = random.randint(n - n // 20, n)
        elif mode == "short":
            l = random.randint(1, n)
            r = min(n, l + random.randint(0, 50))
        else:
            l, r = sorted((random.randint(1, n), random.randint(1, n)))
        out.append((min(l, r), max(l, r)))
    return out


add("OOXOOO", [(1, 6), (4, 6), (1, 2)])
add("OOOOXOOXO", [(1, 9), (6, 9), (5, 7), (8, 8)])
add("X", [(1, 1)])
add("XOOOOOOOOO", [(1, 10), (2, 5), (1, 1)])
add("OXOOXXOOOX", [(1, 10), (2, 8), (5, 9), (3, 4)])

add("O", [(1, 1)])
add(song(20, 0.3), queries(20, 60, "any"))
add(song(50, 0.1), queries(50, 200, "any"))
add(runs(300, 5, 40), queries(300, 300, "any"))
add("O" * 2000, queries(2000, 1000, "any"))
add(song(5000, 0.5), queries(5000, 3000, "any"))
add("O" * 70_000, [(1, 70_000), (2, 70_000), (35_000, 70_000)])

add("O" * MAXN, queries(MAXN, MAXQ, "long"))
add(runs(MAXN, 1000, 100_000), queries(MAXN, MAXQ, "long"))
add(song(MAXN, 0.0001), queries(MAXN, MAXQ, "long"))
add(runs(MAXN, 1, 30), queries(MAXN, MAXQ, "long"))
add(song(MAXN, 0.01), queries(MAXN, MAXQ, "long"))
add("X" + "O" * (MAXN - 2) + "X", queries(MAXN, MAXQ, "long"))
add(runs(MAXN, 10_000, 200_000), [(random.randint(1, 100), MAXN) for _ in range(MAXQ)])
add(song(MAXN, 0.3), queries(MAXN, MAXQ, "long"))
add("O" * (MAXN // 2) + "X" + "O" * (MAXN - MAXN // 2 - 1), queries(MAXN, MAXQ, "long"))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
