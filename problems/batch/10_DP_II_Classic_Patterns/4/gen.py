# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(70707)
MAXN, MAXV = 10000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(v):
    n = len(v)
    assert 1 <= n <= MAXN
    assert all(1 <= x <= MAXV for x in v)
    tests.append(f"{n}\n" + " ".join(map(str, v)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


add([1, 3, 1, 5, 2])
add([3, 5, 1, 4])
add([7])
add([5, 5, 5])
add([4, 1, 6, 2, 9, 3, 1, 8])

add([MAXV])
add([MAXV, 1])
add(rnd(10, 1, 10))
add(rnd(14, 1, 100))
add(rnd(16, 1, MAXV))
add([1, 9, 1, 1, 9, 1, 1, 9, 1, 1, 9, 1, 1, 9, 1, 1])
add([3, 1, 2, 1, 3, 1, 2, 1, 3, 1, 2, 1, 3, 1, 2, 1])

add(rnd(300, 1, 1000))
add(rnd(2000, 1, MAXV))

N = MAXN
add([MAXV] * N)
add(rnd(N, 1, MAXV))
add(rnd(N, 1, 10))
add(rnd(N, MAXV - 1000, MAXV))
add(sorted(rnd(N, 1, MAXV)))
add(sorted(rnd(N, 1, MAXV), reverse=True))
add([MAXV if i % 2 else 1 for i in range(N)])
add([ri(1, 5) if i % 7 else MAXV - ri(0, 5) for i in range(N)])
v = sorted(rnd(N // 2, 1, MAXV))
add(v[::-1] + rnd(N - N // 2, 1, MAXV))
add([abs(N // 2 - i) * 100000 + ri(1, 1000) for i in range(N)])
add(rnd(N - 1, 1, MAXV))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
