# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(44002)
MAXN, MAXA = 200_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(0 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


add([7, 3, 10, 3, 5])
add([4, 9, 4])
add([6])
add([40000, 0, 40000, 0, 39999])
add([12, 30, 21, 16, 26, 12])

add([0, 0])
add([5, 5, 5, 5])
add([0, MAXA])
for n, hi in [(10, 10), (50, 1000), (300, MAXA), (2000, 50), (8000, MAXA), (20000, MAXA)]:
    add([ri(0, hi) for _ in range(n)])

N = MAXN
add([ri(0, MAXA) for _ in range(N)])
add([MAXA if i % 2 else 0 for i in range(N)])
add([MAXA] * (N - 1) + [0])
add([0] * (N - 1) + [MAXA])
add(sorted(ri(0, MAXA) for _ in range(N)))
add(sorted((ri(0, MAXA) for _ in range(N)), reverse=True))
add([MAXA - ri(0, 3) for _ in range(N)])
add([ri(0, 5) * 200_000 for _ in range(N)])
add([MAXA] * N)
add([MAXA - i * 5 for i in range(N)])

add([ri(0, MAXA) for _ in range(60_000)])
add([MAXA if random.random() < 0.1 else ri(0, 10) for _ in range(100_000)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
