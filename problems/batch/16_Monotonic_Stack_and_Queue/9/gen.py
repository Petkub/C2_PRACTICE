# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(160009)
MAXN, MAXA = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


add([2, 1, 3, 2, 4])
add([1, 2, 2, 3])
add([5])
add([1, 2, 3, 4, 5])
add([3, 1, 4, 1, 5, 9, 2, 6])

add([4, 4])
add([ri(1, 4) for _ in range(12)])
add([ri(1, 10) for _ in range(300)])
add([ri(1, MAXA) for _ in range(2000)])
add([i // 3 + 1 for i in range(3000)])
add([i * 10 + ri(0, 25) for i in range(8000)])
add([20000 - i for i in range(20000)])
add([MAXA] * 20000)
add([ri(1, MAXA) for _ in range(20000)])
add([ri(1, 5) for _ in range(20000)])

N = MAXN
add([i + 1 for i in range(N)])
add([MAXA - N + 1 + i for i in range(N)])
add([i * 1000 + ri(0, 1500) + 1 for i in range(N)])
add([i // 2 + 1 for i in range(N)])
add([(i % 50000) + (i // 50000) * 25000 + 1 for i in range(N)])
a = [i * 2 + 100 for i in range(N)]
for k in range(1000, N, 1000):
    a[k] -= 50
add(a)
add([i + 1 if i < N // 2 else N - i for i in range(N)])
add([i + ri(1, 3) for i in range(N)])
a, cur = [], 1
for _ in range(N):
    a.append(cur)
    cur = max(1, cur + ri(-3, 10))
add(a)
add([30000 - i if i < 30000 else i - 29999 for i in range(N)])
add([ri(1, MAXA) for _ in range(20000)] + [MAXA - 180000 + i for i in range(180000)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
