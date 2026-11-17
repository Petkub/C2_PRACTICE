# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(11501)
MAXN = 1500
MAXS = 10**8
DIG = "0123456789"
tests = []


def add(s, g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= MAXN and 1 <= c <= MAXN
    assert 0 <= s <= MAXS
    assert all(len(row) == c and all(ch in DIG for ch in row) for row in g)
    tests.append(f"{r} {c} {s}\n" + "\n".join(g) + "\n")


def rnd(r, c, digits=DIG):
    return ["".join(random.choices(digits, k=c)) for _ in range(r)]


def const(r, c, d):
    return [d * c] * r


def plant(g, r, c, k, d):
    for i in range(r, r + k):
        g[i] = g[i][:c] + d * k + g[i][c + k:]


add(13, ["31415", "92653", "58979", "32384"])
add(0, ["123", "456"])
add(4, ["9119", "1111", "9119"])
add(5, ["000", "000", "000", "000"])
add(7, ["7"])
add(20, ["5555", "5555", "5555"])

add(0, ["0"])
add(8, ["9"])
add(0, rnd(1, 30, "0123"))
g = rnd(12, 9, "01")
add(6, g)
g = const(8, 8, "9")
plant(g, 5, 0, 3, "1")
plant(g, 0, 5, 3, "1")
plant(g, 4, 4, 3, "1")
add(9, g)
add(35, rnd(40, 50))
add(400, rnd(60, 45, "0123"))
add(25, rnd(100, 100, "0000000009"))
add(0, rnd(150, 120, "0000000000001"))

add(0, const(MAXN, MAXN, "0"))
add(8, const(MAXN, MAXN, "9"))
add(9 * MAXN * MAXN, const(MAXN, MAXN, "9"))
add(9 * 1000 * 1000 - 1, const(MAXN, MAXN, "9"))
add(MAXS, rnd(MAXN, MAXN))
add(900_000, rnd(MAXN, MAXN))
add(200_000, rnd(MAXN, MAXN, "01"))
add(3, rnd(MAXN, MAXN, "0000000123456789"))
g = const(MAXN, MAXN, "9")
plant(g, 1100, 10, 100, "1")
plant(g, 799, 1090, 100, "1")
plant(g, 799, 300, 100, "1")
plant(g, 799, 299, 1, "8")
add(10_000, g)
add(300_000, rnd(MAXN, MAXN, "0001"))
add(50, rnd(MAXN, MAXN, "0000000001"))
g = rnd(MAXN - 1, MAXN, "0123456789")
add(5_000, g)
add(0, rnd(MAXN, MAXN, "0" + "123456789" * 2))
g = const(MAXN, MAXN, "0")
for i in range(MAXN):
    g[i] = g[i][:i] + "1" + g[i][i + 1:]
add(0, g)
add(10, ["".join(random.choices(DIG, k=MAXN))])
add(10, ["".join(random.choices(DIG, k=1)) for _ in range(MAXN)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
