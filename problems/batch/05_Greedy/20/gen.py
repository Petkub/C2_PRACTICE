# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(52006)
MAXN = 100_000
MAXV = 10 ** 9
tests = []
rnd = random.random


def ri(lo, hi):
    return lo + int(rnd() * (hi - lo + 1))


def add(e, s, b):
    n = len(e)
    assert 1 <= n <= MAXN and len(s) == n and len(b) == n
    assert all(c in "HL" for c in s)
    assert all(1 <= v <= MAXV for v in e) and all(1 <= v <= MAXV for v in b)
    tests.append(f"{n}\n{' '.join(map(str, e))}\n{s}\n{' '.join(map(str, b))}\n")


def vals(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def rules(n, ph=0.5):
    return "".join("H" if rnd() < ph else "L" for _ in range(n))


def near(a, d):
    return [min(MAXV, max(1, v + ri(-d, d))) for v in a]


def strong(s, lo, mid, hi):
    return [ri(mid, hi) if ch == "H" else ri(lo, mid) for ch in s]


def copy_of(e, d):
    b = near(e, d)
    random.shuffle(b)
    return b


add([4, 4, 2, 1, 4], "HHLLL", [5, 2, 6, 4, 3])
add([2, 2, 2], "HHL", [2, 2, 2])
add([10, 10, 10, 1, 1, 1], "HHHLLL", [1, 1, 1, 10, 10, 10])
add([7], "H", [3])
add([5, 3, 4, 1, 5], "HHLLH", [6, 3, 3, 1, 4])
add([5, 4, 3, 4, 4, 3, 1, 1], "HLHHHLLL", [2, 6, 6, 4, 1, 4, 1, 5])


add([1], "L", [1])
add([MAXV, 1], "LH", [1, MAXV])
add(vals(7, 1, 3), rules(7), vals(7, 1, 3))
add(vals(8, 1, 4), "HHHHHHHH", vals(8, 1, 4))
add(vals(8, 1, 3), "LLLLLLLL", vals(8, 1, 3))
add(vals(8, 2, 5), rules(8, 0.3), vals(8, 1, 4))


for n, v, ph in ((300, 3, 0.5), (350, 6, 0.7)):
    add(vals(n, 1, v), rules(n, ph), vals(n, 1, v))
for n, v, ph, d in ((400, 20, 0.4, 1), (400, 8, 0.5, 2)):
    s = rules(n, ph)
    e = strong(s, 1, v // 2, v)
    add(e, s, copy_of(e, d))


N = MAXN
add(vals(N, 1, 3), rules(N), vals(N, 1, 3))
add(vals(N, 1, 10), "H" * N, vals(N, 1, 10))
add(vals(N, 1, 100), "L" * N, vals(N, 1, 100))
add(vals(N, 1, 5), "H" * N, vals(N, 1, 5))
add(vals(N, 300, 1000), rules(N, 0.5), vals(N, 1, 700))
add(vals(N, 1, 4), rules(N, 0.25), vals(N, 2, 5))
add(vals(N, 1, 30), "L" * N, vals(N, 1, 30))
for v, ph, d in ((10, 0.5, 1), (50, 0.6, 2), (1000, 0.5, 3), (MAXV, 0.5, 2), (30, 0.8, 1), (200, 0.5, 1)):
    s = rules(N, ph)
    e = strong(s, 1, v // 2, v) if v < MAXV else strong(s, MAXV - 50, MAXV - 25, MAXV)
    add(e, s, copy_of(e, d))
s = "H" * (N // 2) + "L" * (N - N // 2)
e = strong(s, 1, 10, 20)
add(e, s, copy_of(e, 0))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
