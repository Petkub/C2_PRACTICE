# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(11016)
MAXN, MAXH, MAXB = 100_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(poles):
    n = len(poles)
    assert 1 <= n <= MAXN and all(1 <= h <= MAXH and 1 <= b <= MAXB for h, b in poles)
    tests.append(f"{n}\n" + "".join(f"{h} {b}\n" for h, b in poles))


def tricky(n, hlo, hhi, costs):
    return [(ri(hlo, hhi), random.choice(costs)) for _ in range(n)]


add([(7, 1)] * 4)
add([(2, 3), (2, 1), (2, 3), (5, 2)])
add([(1, 20), (4, 10), (3, 2), (2, 20), (2, 50)])
add([(10, 10)])
add([(3, 5), (1, 2), (2, 4), (1, 1)])
add([(5, 2)] * 6)

add([(1, 1), (1, 1)])
add([(MAXH, MAXB)] * 7)
add(tricky(7, 1, 4, [1, 50, 1000]))
add(tricky(7, 1, 3, [1, 1000]))
add(tricky(6, 1, 5, [1, 2, 3]))
add([(1, 50), (4, 1000), (1, 1), (3, 1000), (2, 50)])

add(tricky(2000, 1, 5, [1, 50, 1000, 10**6]))
add(tricky(3000, 1, 3, [1, 1000]))

N = MAXN
add([(MAXH, MAXB)] * N)
add(tricky(N, 1, 4, [1, 50, 1000]))
add(tricky(N, 1, 5, [1, 1, 50, 1000, 10**9]))
add(tricky(N, MAXH - 3, MAXH, [1, MAXB]))
add([(ri(1, MAXH), ri(1, MAXB)) for _ in range(N)])
add([(1 + i % 3, ri(1, MAXB)) for i in range(N)])
add([(1 + (i // 2) % 3, ri(1, 10)) for i in range(N)])
add([(1, 1 if i % 3 == 1 else 10**6) for i in range(N)])
add(tricky(N, 1, 2, [1, 10**9]))
add([(h, 1000 if i % 2 else 1) for i, h in enumerate(ri(1, 6) for _ in range(N))])
add([(1, 50), (1, 1000), (1, 1), (3, 50), (4, 50)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
