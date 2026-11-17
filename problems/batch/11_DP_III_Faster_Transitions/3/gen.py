# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(11004)
MAXN, MAXG = 500_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(g):
    n = len(g)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXG for x in g)
    tests.append(f"{n}\n" + " ".join(map(str, g)) + "\n")


def rnd(n, k, lo=1):
    return [ri(lo, lo + k - 1) for _ in range(n)]


add([5, 5, 7])
add([4, 4, 4, 4])
add([3, 1, 3, 2, 1])
add([1000000000, 7, 1000000000, 7, 999999999])
add([42])
add([2, 1, 1, 2, 3, 3, 1, 2])

add([1, 2])
add([9, 9])
add(list(range(1, 21)))
add(rnd(18, 2))
add(rnd(20, 3))
add(rnd(19, 5, MAXG - 4))
add([1, 2] * 10)

add(rnd(3000, 3))
add(rnd(5000, 50, 10**8))

N = MAXN
M = 200_000
add(rnd(N, 2))
add(rnd(N, 1000))
add(rnd(N, 30))
add([7] * N)
add(list(range(1, N + 1)))
add([1 + i % 2 for i in range(N)])
add([1 + (i // 3) % 4 for i in range(N)])
add(rnd(M, MAXG))
add(rnd(M, 5, MAXG - 4))
add([MAXG - (i % 3) * 400_000_000 for i in range(M)])
add([1 if random.random() < 0.95 else 2 for _ in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
