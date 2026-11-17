# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(40402)
MAXN = 200_000
MAXC = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def need(a, C):
    best = 0
    for j in range(len(a)):
        s = a[j]
        for i in range(j + 1, len(a)):
            s += a[i]
            if s > C:
                best = max(best, -(-(s - C) // (i - j)))
    return best


def from_start(a, C):
    best, s = 0, 0
    for i, x in enumerate(a):
        s += x
        if i and s > C:
            best = max(best, -(-(s - C) // i))
    return best


def add(C, a, sample=False):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= C <= MAXC
    assert all(0 <= x <= C for x in a)
    if sample:
        assert need(a, C) == from_start(a, C)
    tests.append(f"{n} {C}\n" + " ".join(map(str, a)) + "\n")


def calm(n, top):
    return [ri(0, top) for _ in range(n)]


def ramp(n, top):
    return [ri(0, max(1, top * (i + 1) // n)) for i in range(n)]


def bursts(n, C, rate, length):
    res = []
    while len(res) < n:
        k = ri(1, length)
        res += [min(C, ri(rate // 2, rate * 3 // 2)) for _ in range(k)]
        res += [ri(0, rate // 10) for _ in range(ri(1, length))]
    return res[:n]


add(10, [9, 8, 7, 3, 2], sample=True)
add(9, [2, 3, 4], sample=True)
add(10, [10, 9, 6, 8, 1, 0], sample=True)
add(5, [5, 5, 5, 5], sample=True)
add(MAXC, [MAXC, MAXC, MAXC], sample=True)

add(1, [0])
add(7, [7])
add(10, [4, 8, 9, 3, 7])
add(10, [6, 6, 0, 0, 9, 9, 9])
add(20, ramp(30, 20))
add(1000, bursts(300, 1000, 300, 6))
add(MAXC, [ri(0, MAXC) for _ in range(2000)])
add(5000, calm(1500, 50) + ramp(1500, 5000))
add(MAXC, [MAXC] * 3000)
add(123456, [0] * 2999 + [123456])

N = MAXN
add(10**6, calm(N // 2, 1000) + ramp(N // 2, 10**6))
add(MAXC, calm(N // 2, 10**4) + [ri(0, MAXC) for _ in range(N // 2)])
add(5 * 10**8, ramp(N, 5 * 10**8))
add(10**7, calm(N // 3, 100) + bursts(N - N // 3, 10**7, 3 * 10**6, 50))
add(MAXC, calm(N // 2, 10**5) + bursts(N // 2, MAXC, 6 * 10**8, 5))
add(10**8, ramp(N // 2, 10**6) + ramp(N // 2, 10**8))
add(2 * 10**6, calm(N - 1000, 5000) + [2 * 10**6] * 1000)
add(MAXC, [x * 1000 for x in ramp(N, 10**6)])
add(3 * 10**5, calm(N // 2, 10**4) + [ri(10**5, 3 * 10**5) for _ in range(N // 2)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
