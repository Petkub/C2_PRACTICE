# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(5114)
MAXN, MAXP = 300_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(p):
    n = len(p)
    assert 1 <= n <= MAXN
    assert all(1 <= x <= MAXP for x in p)
    tests.append(f"{n}\n" + " ".join(map(str, p)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def walk(n, step):
    x, out = MAXP // 2, []
    for _ in range(n):
        x = min(MAXP, max(1, x + ri(-step, step)))
        out.append(x)
    return out


add([2, 3, 4, 1, 3])
add([5, 4, 3])
add([7])
add([1, 3, 1, 3])
add([3, 1, 4, 1, 5, 9, 2, 6])
add([1, 10, 1, 1, 10, 1, 10])

add([1, MAXP])
add([MAXP, 1])
add(rnd(10, 1, 10))
add(rnd(14, 1, 100))
add(rnd(16, 1, MAXP))
add([1, 2] * 8)
add([1, MAXP, MAXP, 1, MAXP, 1, MAXP, 1, 1, MAXP, 1, MAXP, MAXP, 1, MAXP, 1, MAXP])
add(list(range(1, 18)))

N = MAXN
add([1, MAXP] * (N // 2))
add([1, 1, MAXP] * (N // 3))
add(rnd(N, 1, MAXP))
add(walk(N, 1000))
add(walk(N, 10**7))
add(list(range(N, 0, -1)))
add(list(range(1, N + 1)))
add([MAXP] * N)
add([ri(1, 3) for _ in range(N)])
add([1, 2, 3] * (N // 3))
add([MAXP - ri(0, 5) if i % 4 in (1, 2) else ri(1, 5) for i in range(N)])
add(rnd(N - 1, 1, MAXP))
add([ri(1, 1000) * (1 if i % 3 else 10**6) for i in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
