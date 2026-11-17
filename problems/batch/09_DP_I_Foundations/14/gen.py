# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(91402)
MAXN = 3000
MAXK = 200000
tests = []


def add(n, holes):
    holes = list(holes)
    assert 1 <= n <= MAXN
    assert 0 <= len(holes) <= min(n * n, MAXK)
    assert len(set(holes)) == len(holes)
    assert all(1 <= i <= n and 1 <= j <= 2 * i - 1 for i, j in holes)
    tests.append(f"{n} {len(holes)}\n" + "".join(f"{i} {j}\n" for i, j in holes))


def rnd(n, k, kind=None):
    s = set()
    while len(s) < k:
        i = random.randint(1, n)
        j = random.randint(1, 2 * i - 1)
        if kind is not None and j % 2 != kind:
            continue
        s.add((i, j))
    s = sorted(s)
    random.shuffle(s)
    return s


add(3, [(3, 3)])
add(4, [])
add(1, [(1, 1)])
add(5, [(3, 1), (3, 2), (4, 7), (4, 6)])
add(6, [(2, 1), (2, 2), (2, 3), (6, 1), (5, 9), (6, 11), (6, 10)])
add(7, [(4, 3), (4, 4), (4, 5), (7, 13)])

add(1, [])
add(2, [(2, 2)])
add(5, [(4, 4)])
add(9, rnd(9, 8, 0))
add(12, rnd(12, 20))
add(20, rnd(20, 40))
add(30, rnd(30, 15, 0))
add(25, [(i, j) for i in range(1, 26) for j in range(1, 2 * i) if (i + j) % 7 == 0])

add(300, rnd(300, 300))
add(1000, rnd(1000, 20000))

N = MAXN
add(N, [])
add(N, [(1, 1)])
add(N, rnd(N, 30))
add(N, rnd(N, 100, 0))
add(N, rnd(N, 60, 1))
add(N, [(1500, j) for j in range(1, 3000)] + rnd(N, 20))
add(N, [(i, 1) for i in range(7, N + 1, 7)])
add(N, [(i, i) for i in range(1, N + 1)] + [(i, i + 1) for i in range(2, N)])
add(N, rnd(N, 40, 0) + [(i, j) for i in range(2800, 2900) for j in range(1, 2 * i, 2)][:MAXK - 40])
add(N, [(i, 2 * i - 1) for i in range(100, N + 1, 100)] + [(i, i) for i in range(1000, 1100)])
add(N - 1, rnd(N - 1, 10))
add(N, [(N, j) for j in range(2, 2 * N, 2)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
