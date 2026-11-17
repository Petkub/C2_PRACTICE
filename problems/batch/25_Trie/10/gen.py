# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(250010)
MAXN, MAXQ, MAXK, BITS = 200_000, 20_000, 300_000, 20
MAXV = (1 << BITS) - 1
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def rnd(n, lo=0, hi=MAXV):
    if lo == 0 and hi == MAXV:
        return [random.getrandbits(BITS) for _ in range(n)]
    return [ri(lo, hi) for _ in range(n)]


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= x <= MAXV for x in a)
    assert all(1 <= l <= r <= n and len(xs) >= 1 for l, r, xs in qs)
    assert all(0 <= x <= MAXV for _, _, xs in qs for x in xs)
    assert sum(len(xs) for _, _, xs in qs) <= MAXK
    t = (f"{n} {q}\n" + " ".join(map(str, a)) + "\n"
         + "".join(f"{l} {r} {len(xs)} " + " ".join(map(str, xs)) + "\n" for l, r, xs in qs))
    assert len(t) <= 5_000_000
    tests.append(t)


def counts(q, k):
    c = [1] * q
    for _ in range(k - q):
        c[int(random.random() * q)] += 1
    return c


def questions(ranges, k, xlo=0, xhi=MAXV):
    return [(l, r, rnd(c, xlo, xhi)) for (l, r), c in zip(ranges, counts(len(ranges), k))]


def rlong(n, q):
    out = []
    for _ in range(q):
        l = ri(1, max(1, n // 10))
        out.append((l, ri(max(l, n - n // 10), n)))
    return out


def rwide(n, q):
    out = []
    for _ in range(q):
        ln = ri(n // 4, n)
        l = ri(1, n - ln + 1)
        out.append((l, l + ln - 1))
    return out


def rany(n, q):
    out = []
    for _ in range(q):
        l = ri(1, n)
        out.append((l, ri(l, n)))
    return out


add([1, 6, 3, 7, 2], [(1, 5, [4, 0]), (2, 4, [1]), (5, 5, [7, 2])])
add([0], [(1, 1, [0, MAXV])])
add([5, 5, 9, 5], [(1, 2, [12]), (2, 4, [12, 5]), (4, 4, [5])])
add([8, 1, 15, 2, 4, 11], [(1, 6, [7, 9]), (2, 5, [7]), (4, 6, [9]), (3, 3, [3])])
add([3, 12, 10, 6, 1, 0, 13], [(2, 7, [5, 2]), (1, 3, [1]), (5, 6, [14, 0, 1])])

add(rnd(10, 0, 15), questions(rany(10, 8), 20, 0, 15))
add(rnd(100, 0, 255), questions(rany(100, 100), 300, 0, 255))
add(rnd(1000), questions(rany(1000, 300), 1000))
add(rnd(3000, 0, 7), questions(rany(3000, 1000), 2000, 0, 7))
add(rnd(5000), questions(rlong(5000, 1000), 3000))
n = 20_000
ranges = []
for _ in range(5000):
    l = ri(1, n - 50)
    ranges.append((l, l + ri(0, 50)))
add(rnd(n), questions(ranges, 20_000))
ranges = []
for _ in range(5000):
    r = ri(19_000, n)
    ranges.append((ri(r - 2000, r), r))
add([MAXV ^ ri(0, 1) for _ in range(17_000)] + rnd(3000, 0, 1023), questions(ranges, 20_000))
n = 50_000
add([MAXV] * n, questions([(1, n)] * 100 + rany(n, 1900), 10_000))
add(rnd(n), questions([(1, n)] * 2000, 20_000))

N, Q, K = MAXN, MAXQ, MAXK
add(rnd(N), questions(rlong(N, Q), K))
add(rnd(N), questions(rwide(N, Q), K))
a = rnd(N, 0, (1 << 18) - 1)
for i in range(0, N, 5000):
    a[i] = ri(1 << 19, MAXV)
add(a, questions(rlong(N, Q), K, 0, (1 << 18) - 1))
add(sorted(rnd(N)), questions(rwide(N, Q), K))
ranges = []
for _ in range(Q):
    l = ri(1, N // 2)
    ranges.append((l, l + ri(N // 3, N // 2 - 1)))
add(sorted(rnd(N), reverse=True), questions(ranges, K))
ranges = []
for _ in range(Q):
    l = ri(N // 2 + 1, N // 2 + 20_000)
    ranges.append((l, ri(max(l, N - 20_000), N)))
add([MAXV ^ ri(0, 1) for _ in range(N // 2)] + rnd(N // 2, 0, (1 << 19) - 1), questions(ranges, K))
a = [ri(0, 1023) if random.random() < 0.5 else ri(1 << 19, MAXV) for _ in range(N)]
add(a, questions(rwide(N, Q), K))
add(rnd(N), questions(rwide(N, 300), K))
a = [(ri(0, 3) << 16) | random.getrandbits(16) for _ in range(N)]
add(a, questions(rwide(N, Q), K))
a = rnd(N)
qs = []
for (l, r), c in zip(rwide(N, Q), counts(Q, K)):
    ends = [p for p in (l - 1, l, r, r + 1) if 1 <= p <= N]
    qs.append((l, r, [MAXV ^ a[ends[int(random.random() * len(ends))] - 1] for _ in range(c)]))
add(a, qs)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
assert sum(len(t) for t in tests) <= 40_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
