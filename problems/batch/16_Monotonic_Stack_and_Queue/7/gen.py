# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(160105)
MAXN, MAXA = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


add([2, 1, 3])
add([2, 2])
add([MAXA])
add([1, 2, 3, 4])
add([MAXA, MAXA, MAXA])

add([5, 5, 5, 5])
add([ri(1, 3) for _ in range(10)])
add([ri(1, 5) for _ in range(300)])
add([ri(1, MAXA) for _ in range(2000)])
add([ri(1, 2) for _ in range(5000)])
add([(i * 7919) % 101 + 1 for i in range(8000)])

N = MAXN
add([MAXA] * N)
add([i + 1 for i in range(N)])
add([MAXA - i for i in range(N)])
add([ri(1, MAXA) for _ in range(N)])
add([ri(1, 3) for _ in range(N)])
add([ri(MAXA - 10, MAXA) for _ in range(N)])
add([MAXA - abs(N // 2 - i) * 300 for i in range(N)])
add([1 + abs(N // 2 - i) * 300 for i in range(N)])
add([MAXA if i % 2 else 1 for i in range(N)])
add([(i % 1000) * 100000 + 1 for i in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
