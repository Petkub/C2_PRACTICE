# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(45004)
MAXN, MAXQ, MAXA, MAXT = 200_000, 200_000, 10**6, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ts):
    n, q = len(a), len(ts)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(-MAXA <= v <= MAXA for v in a)
    assert all(1 <= t <= MAXT for t in ts)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{t}\n" for t in ts))


def mixed_queries(n, q, small, far=0.05):
    ts = []
    for _ in range(q):
        r = random.random()
        if r < small:
            ts.append(ri(1, 3))
        elif r < small + far:
            ts.append(ri(n + 1, MAXT))
        elif r < small + far + 0.15:
            ts.append(ri(max(1, n // 2), n))
        else:
            ts.append(ri(1, n))
    return ts


add([3, -1, 4, -6, 2, 5, -2, 7], [2, 1, 3])
add([-4, 6, -1, -3, 5, -8], [2, 9, 2, 1, 5])
add([-5], [2])
add([10, -20, 30, -40, 50, 60, 70], [1, 2, 3, 7, 8, 1])
add([2, 2, -9, 2, 2, -9, 2, 2, -9, 2], [1, 5, 2, 4])

add([-1], [1, 1, 2])
add([MAXA], [1, MAXT])
add([-3, -1, -2, -5, -4], [1, 2, 3, 4, 5, 6])
for n, q in [(10, 15), (30, 30), (100, 60), (500, 200)]:
    add([ri(-20, 20) for _ in range(n)], mixed_queries(n, q, 0.2, 0.1))
add([ri(-MAXA, MAXA) for _ in range(2000)], mixed_queries(2000, 2000, 0.3))
add([ri(-MAXA // 2, MAXA) for _ in range(20_000)], mixed_queries(20_000, 20_000, 0.3))

N, Q = MAXN, MAXQ
add([ri(-MAXA, MAXA) for _ in range(N)], [1] * Q)
add([ri(-MAXA // 2, MAXA) for _ in range(N)], mixed_queries(N, Q, 0.5))
add([MAXA] * N, mixed_queries(N, Q, 0.5))
add([-ri(1, MAXA) for _ in range(N)], mixed_queries(N, Q, 0.5))
add([ri(-MAXA, MAXA // 3) for _ in range(N)], mixed_queries(N, Q, 0.5, 0.2))
add([MAXA if i % 2 else -MAXA for i in range(N)], mixed_queries(N, Q, 0.5))
add([ri(-MAXA, MAXA // 2) * ri(-1, 1) for _ in range(N)], [ri(1, 2) for _ in range(Q // 2)] + [ri(1, N) for _ in range(Q - Q // 2)])
a = [ri(0, MAXA) for _ in range(N)]
a[N // 2] = -MAXA
add(a, mixed_queries(N, Q, 0.6))
add([ri(-5, 6) for _ in range(N)], mixed_queries(N, Q, 0.5))
add([ri(-MAXA // 3, MAXA) for _ in range(N)], [1 if i % 2 else MAXT for i in range(Q)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
