# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(160103)
MAXN, MAXV = 150_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def solve(x, h):
    n = len(x)
    reach, last, st = [0] * n, [0] * n, []
    for i in range(n - 1, -1, -1):
        r, e = x[i] + h[i], i
        while st and x[st[-1]] <= r:
            r = max(r, reach[st[-1]])
            e = last[st[-1]]
            st.pop()
        reach[i], last[i] = r, e
        st.append(i)
    return [last[i] - i + 1 for i in range(len(x))]


def next_only(x, h):
    import bisect
    n = len(x)
    r = [0] * n
    for i in range(n - 1, -1, -1):
        r[i] = x[i] + h[i]
        if i + 1 < n and x[i + 1] <= x[i] + h[i]:
            r[i] = max(r[i], r[i + 1])
    return [bisect.bisect_right(x, r[i]) - i for i in range(n)]


def add(x, h):
    n = len(x)
    assert 1 <= n <= MAXN and len(h) == n
    assert all(1 <= v <= MAXV for v in x) and all(1 <= v <= MAXV for v in h)
    assert all(x[i] < x[i + 1] for i in range(n - 1))
    tests.append(f"{n}\n" + " ".join(map(str, x)) + "\n" + " ".join(map(str, h)) + "\n")
    assert len(tests[-1]) <= 3_100_000


def positions(n, lo, hi, start=1):
    xs, p = [], start
    for _ in range(n):
        xs.append(p)
        p += ri(lo, hi)
    assert xs[-1] <= MAXV
    return xs


def skips(n, start=1):
    x, h, p = [], [], start
    while len(x) < n:
        k = min(ri(2, 6), n - len(x))
        for j in range(k):
            x.append(p)
            if j == 0:
                h.append(ri(3 * k, 4 * k))
            elif j < k - 1:
                h.append(1)
            else:
                h.append(ri(30, 60))
            p += 3
    return x, h


add([1, 3, 4, 7, 9, 12], [2, 4, 3, 3, 2, 1])
add([1, 4, 6], [3, 1, 5])
add([500], [1000000000])
add([2, 5, 6, 8, 13, 14, 20], [1, 3, 3, 6, 2, 9, 4])
add([10, 20, 30, 40, 50], [10, 10, 9, 10, 10])
for k in range(5):
    lines = tests[k].split("\n")
    x, h = list(map(int, lines[1].split())), list(map(int, lines[2].split()))
    assert solve(x, h) == next_only(x, h)

add([1, 2], [1, 1])
add([1, 3, 4, 5], [5, 1, 1, 10])
x = positions(12, 1, 4)
add(x, [ri(1, 6) for _ in x])
x = positions(200, 1, 10)
add(x, [ri(1, 12) for _ in x])
x, h = skips(300)
add(x, h)
x = positions(2000, 1, 100)
add(x, [ri(1, 150) for _ in x])
x = positions(5000, 1, 3)
add(x, [ri(1, 3) for _ in x])
x = positions(10000, 1, 10**5)
add(x, [ri(1, 10**5) for _ in x])
x, h = skips(20000)
add(x, h)

N = MAXN


def chained(n, p_short, ahead, gmin, gmax, breaks=()):
    x = positions(n, gmin, gmax)
    short = [False] * n
    run = 0
    for i in range(1, n - 1):
        if run < ahead - 1 and random.random() < p_short:
            short[i] = True
            run += 1
        else:
            run = 0
    h = []
    for i in range(n):
        if short[i]:
            h.append(max(1, x[i + 1] - x[i] - 1))
        else:
            j = min(n - 1, i + ahead)
            h.append(max(1, x[j] - x[i] + ri(0, gmin - 1)))
    for b in breaks:
        for i in range(max(0, b - ahead - 1), b):
            h[i] = max(1, min(h[i], x[b] - x[i] - 1))
    return x, h


def work(x, h):
    return sum(solve(x, h))


big = []
big.append((list(range(1, N + 1)), [1] * N))
big.append((list(range(MAXV - N, MAXV)), [MAXV - 1] * (N - 1) + [MAXV]))
big.append(skips(N))
big.append(chained(N, 0.3, 2, 1, 10))
big.append(chained(N, 0.45, 2, 3, 3))
big.append(chained(N, 0.3, 2, 2, 20, breaks=(N // 2,)))
big.append(chained(N, 0.5, 6, 1, 50))
big.append(chained(N, 0.2, 3, 1000, 6000))
x, h = chained(N, 0.35, 2, 1, 30)
h[0] = x[-1]
big.append((x, h))
x, h = chained(N, 0.4, 4, 1, 9, breaks=(N // 5,))
big.append((x, h))
for x, h in big:
    assert work(x, h) >= 3 * 10**9, work(x, h)
    add(x, h)
for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
