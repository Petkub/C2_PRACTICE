# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(90401)
MAXN = 100000
MAXQ = 200000
SEG = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
tests = []


def add(c, m, qs):
    assert len(c) == 10 and all(1 <= x <= 10 for x in c)
    assert 1 <= m <= 20
    assert 1 <= len(qs) <= MAXQ and all(1 <= x <= MAXN for x in qs)
    tests.append(" ".join(map(str, c)) + "\n" + f"{m} {len(qs)}\n" + " ".join(map(str, qs)) + "\n")


def rc(lo=1, hi=10):
    return [random.randint(lo, hi) for _ in range(10)]


add(SEG, 3, [6])
add([1, 3, 3, 3, 3, 3, 3, 3, 3, 3], 2, [4])
add(SEG, 1, [6, 7, 10])
add([2, 1, 1, 1, 1, 1, 1, 1, 1, 1], 7, [2, 5, 9])
add([4, 3, 7, 2, 9, 5, 5, 8, 6, 3], 20, [10, 15])
add(SEG, 11, [6, 12, 20, 30])

add(SEG, 3, list(range(1, 13)))
add([10, 1, 1, 1, 1, 1, 1, 1, 1, 1], 5, [1, 9, 10, 11, 25])
add([1] * 10, 1, [1, 2, 3, 10])
add([1] * 10, 20, [1, 2, 3, 4, 5, 6])
add([10] * 10, 13, [9, 10, 20, 100, 300])
add([3, 10, 10, 10, 10, 10, 10, 10, 10, 1], 9, [2, 3, 50, 200])
add(rc(), 17, [random.randint(1, 60) for _ in range(30)])
add(rc(5, 10), 4, [random.randint(1, 400) for _ in range(50)])

add(rc(1, 3), 19, [random.randint(1, 5000) for _ in range(500)])
add(SEG, 12, [random.randint(1, 20000) for _ in range(2000)])

add([1] * 10, 20, [random.randint(1, MAXN) for _ in range(MAXQ)])
add(SEG, 20, [MAXN - random.randint(0, 50) for _ in range(MAXQ)])
add([10, 1, 1, 1, 1, 1, 1, 1, 1, 1], 19, [random.randint(1, MAXN) for _ in range(MAXQ - 20)] + list(range(1, 21)))
add(rc(), 17, [random.randint(1, MAXN) for _ in range(MAXQ)])
add(rc(1, 2), 16, [random.randint(1, 30) if i % 10 == 0 else random.randint(1, MAXN) for i in range(MAXQ)])
add([7, 1, 2, 3, 4, 5, 6, 7, 8, 9], 1, [random.randint(1, MAXN) for _ in range(MAXQ)])
add([9, 2, 2, 2, 2, 2, 2, 2, 2, 2], 18, [MAXN] * (MAXQ // 2) + [8] * (MAXQ // 2))
add(rc(1, 4), 20, [random.randint(1, MAXN) for _ in range(MAXQ)])
add([5, 3, 1, 4, 1, 5, 9, 2, 6, 5], 11, list(range(1, MAXN + 1)) + [random.randint(1, MAXN) for _ in range(MAXQ - MAXN)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
