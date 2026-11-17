# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(14005)
MAXQ = 100_000
MAXN = 10 ** 18
P = 10 ** 9 + 7
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    assert all(1 <= n <= MAXN and 0 <= d <= 9 for n, d in qs)
    tests.append(f"{len(qs)}\n" + "".join(f"{n} {d}\n" for n, d in qs))


add([(1, 7), (2, 7), (2, 0)])
add([(1, 0), (3, 0)])
add([(3, 5), (6, 9), (10, 1)])
add([(MAXN, 0), (MAXN, 9), (MAXN - 1, 3)])
add([(19, 0), (20, 4), (P - 1, 5), (P, 0)])

add([(1, d) for d in range(10)])
add([(n, d) for n in range(1, 101) for d in range(10)])
add([(ri(1, 2000), ri(0, 9)) for _ in range(1000)])
add([(ri(10 ** 5, 3 * 10 ** 5), ri(0, 9)) for _ in range(100)])
add([(ri(1, 30), 0) for _ in range(500)] + [(ri(1, 30), ri(1, 9)) for _ in range(500)])
add([(ri(P - 50, P + 50), ri(0, 9)) for _ in range(20)])

add([(ri(1, MAXN), ri(0, 9)) for _ in range(MAXQ)])
add([(MAXN - ri(0, 10 ** 6), ri(0, 9)) for _ in range(MAXQ)])
add([(ri(1, MAXN), 0) for _ in range(MAXQ)])
add([(ri(1, MAXN), 9) for _ in range(MAXQ)])
add([(MAXN, d % 10) for d in range(MAXQ)])
add([((P - 1) * ri(1, 10 ** 8) + ri(0, 2), ri(0, 9)) for _ in range(MAXQ)])
add([(ri(10 ** 9, 10 ** 12), ri(0, 9)) for _ in range(MAXQ)])
add([(ri(1, 10), ri(0, 9)) if i % 2 else (ri(1, MAXN), ri(0, 9)) for i in range(MAXQ)])
add([(2 ** ri(30, 59) - ri(0, 1), ri(0, 9)) for _ in range(MAXQ)])
add([(ri(10 ** 6, 10 ** 7), ri(0, 9)) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
