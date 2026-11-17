# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(41502)
MAXN = 200_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def best(a, k, restart=True):
    def count(x):
        cnt, cur, open_ = 0, 0, False
        for v in a:
            if restart:
                cur = (cur if open_ and cur > 0 else 0) + v
            else:
                cur = (cur if open_ else 0) + v
            open_ = True
            if cur >= x:
                cnt, open_ = cnt + 1, False
        return cnt

    lo, hi = -MAXV, 2 * 10**14
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if count(mid) >= k:
            lo = mid
        else:
            hi = mid - 1
    return lo


def add(a, k, sample=False):
    n = len(a)
    assert 1 <= k <= n <= MAXN and all(-MAXV <= v <= MAXV for v in a)
    if sample:
        assert best(a, k) == best(a, k, restart=False)
        assert max(abs(v) for v in a) * n < 2**31
    tests.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def bumpy(n, hill, dip):
    a = []
    while len(a) < n:
        a += [ri(1, hill) for _ in range(ri(1, 6))] + [-ri(1, dip) for _ in range(ri(1, 4))]
    return a[:n]


add([4, -2, 5, 3, -1, 6], 2, sample=True)
add([5, 1, -2, 4, 3], 3, sample=True)
add([-MAXV], 1, sample=True)
add([7, 7, 7], 3, sample=True)
add([2, 2, 2, 2, 2, 2], 2, sample=True)
add([6, 6, -1, -1, 3], 2, sample=True)

add([-3, -1, -4, -2], 2)
add([2, -5, 3, 4], 1)
add([-1, 6, -1, 6, -1], 2)
for n in (8, 15, 25, 40, 40, 40):
    a = rnd(n, -10, 10)
    add(a, ri(1, n))
add(rnd(40, -MAXV, MAXV), 5)
add(bumpy(40, 10, 30), 4)
add([MAXV] * 40, 2)

N = MAXN
add(rnd(N, -MAXV, MAXV), 1000)
add(rnd(N, -MAXV, MAXV), 1)
add(rnd(N, -MAXV // 2, MAXV), 20_000)
add(bumpy(N, MAXV, MAXV), 5000)
add(bumpy(N, 10**6, 3 * 10**6), 100)
add([MAXV] * N, 7)
add(rnd(N, -MAXV, -1), N // 2)
add(rnd(N, -100, 100), 3000)
add([MAXV if i % 2 else -MAXV for i in range(N)], 50_000)
add(rnd(N, 1, MAXV), N)
add(bumpy(N, 5 * 10**8, MAXV), 2)
add(rnd(N, -MAXV, MAXV), 200)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
