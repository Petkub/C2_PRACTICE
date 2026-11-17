# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(20207)
MAXN = 200_000
MAXA = 10**9
MAXK = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ks):
    n, q = len(a), len(ks)
    assert 1 <= n <= MAXN and 1 <= q <= MAXN
    assert 1 <= a[0] and a[-1] <= MAXA
    assert all(a[i] < a[i + 1] for i in range(n - 1))
    assert all(1 <= k <= MAXK for k in ks)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, ks)) + "\n")


def spread(n, hi):
    return sorted(random.sample(range(1, hi + 1), n))


def edge_ks(a, q):
    res = []
    for _ in range(q):
        i = ri(0, len(a) - 1)
        k = a[i] - (i + 1) + ri(0, 1)
        res.append(max(1, min(MAXK, k)))
    return res


add([2, 3, 7], [1, 2, 3, 4, 5])
add([1, 2, 3], [1, MAXK])
add([5], [4, 5, 1])
add([MAXA], [MAXK, MAXK - 1])
add([4, 6, 10, 11, 12], [3, 4, 5, 7, 6, 1])
add([1, 3, 5, 7, 9], [1, 2, 3, 4, 5, 6])

add([1], [1])
add(list(range(1, 51)), list(range(1, 11)))
a = spread(30, 100)
add(a, list(range(1, 80)))
a = spread(500, 5000)
add(a, edge_ks(a, 500) + [ri(1, 6000) for _ in range(500)])
a = spread(3000, MAXA)
add(a, edge_ks(a, 2000) + [ri(1, MAXK) for _ in range(1000)])
a = list(range(MAXA - 1999, MAXA + 1))
add(a, [ri(MAXA - 2100, MAXK) for _ in range(2000)])

N = MAXN
N2 = 150_000
a = list(range(1, N + 1))
add(a, [ri(1, MAXK) for _ in range(N)])
a = list(range(2, 2 * N + 1, 2))
add(a, [ri(N - 1000, MAXK) for _ in range(N)])
a = spread(N, 10**6)
add(a, edge_ks(a, N))
a = spread(N, 10**6)
add(a, [ri(700_000, MAXK) for _ in range(N)])
a = list(range(MAXA - N2 + 1, MAXA + 1))
add(a, [ri(MAXA - N2 - 1000, MAXK) for _ in range(N2)])
a = list(range(1, N // 2 + 1)) + sorted(random.sample(range(N, 2 * 10**6), N // 2))
add(a, [ri(1, MAXK) for _ in range(N)])
a = spread(N, 10**7)
add(a, edge_ks(a, N))
a = spread(N, 10**7)
add(a, [ri(5 * 10**6, 2 * 10**7) for _ in range(N)])
a = spread(N2, MAXA)
add(a, [MAXK] * N2)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
