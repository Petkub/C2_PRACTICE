# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(511004)
MAXN = 150000
MAXV = 10 ** 9
MAXW = 10 ** 6
tests = []


def add(a, w):
    n = len(a)
    assert 1 <= n <= MAXN and len(w) == n and len(set(a)) == n
    assert all(1 <= x <= MAXV for x in a) and all(1 <= x <= MAXW for x in w)
    tests.append(f"{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, w))}\n")


def prices(n):
    return sorted(random.sample(range(1, MAXV + 1), n))


def from_ranks(r, n):
    p = prices(n)
    return [p[x] for x in r]


def pieces(n, k):

    cuts = sorted(random.sample(range(1, n), k - 1)) if k > 1 else []
    parts, prev = [], 0
    for c in cuts + [n]:
        parts.append(list(range(prev, c)))
        prev = c
    random.shuffle(parts)
    return [x for p in parts for x in p]


def near_sorted(n, swaps):
    r = list(range(n))
    for _ in range(swaps):
        i, j = random.randrange(n), random.randrange(n)
        r[i], r[j] = r[j], r[i]
    return r


def weights_by_value(r, hi):

    w = [0] * len(r)
    for i, x in sorted(enumerate(r), key=lambda t: t[1]):
        w[i] = random.randint(1, hi)
    return w


def spliced(n, k, at_end=False):

    small = list(range(k))
    random.shuffle(small)
    big = list(range(k, n))
    if at_end:
        r = big + small
    else:
        slots = sorted(random.sample(range(n), k))
        r, si, bi = [], 0, 0
        for i in range(n):
            if si < k and slots[si] == i:
                r.append(small[si])
                si += 1
            else:
                r.append(big[bi])
                bi += 1
    w = [random.randint(MAXW // 2, MAXW) if x < k else random.randint(1, 3) for x in r]
    return r, w


def rw(n, lo=1, hi=MAXW):
    return [random.randint(lo, hi) for _ in range(n)]


add([40, 70, 10, 50, 20, 60], [3, 2, 4, 1, 2, 5])
add([8, 6, 7, 5], [1, 4, 4, 2])
add([123], [7])
add([5, 4, 3, 2, 1], [3, 1, 4, 1, 9])
add([27, 3, 91, 15, 42, 64, 8, 77], [5, 9, 2, 6, 5, 3, 5, 8])

add([1, 2], [5, 5])
add([2, 1], [1, 3])
add(from_ranks(random.sample(range(7), 7), 7), rw(7, 1, 10))
add(from_ranks(near_sorted(8, 2), 8), rw(8, 1, 20))
add(from_ranks(pieces(8, 3), 8), rw(8, 1, 9))
add(from_ranks(pieces(30, 5), 30), rw(30, 1, 100))
add(from_ranks(near_sorted(40, 3), 40), rw(40))
r, w = spliced(60, 6)
add(from_ranks(r, 60), w)

r = pieces(3000, 12)
add(from_ranks(r, 3000), weights_by_value(r, 10))
add(from_ranks(random.sample(range(5000), 5000), 5000), rw(5000))

add(from_ranks(list(range(MAXN)), MAXN), rw(MAXN))
add(from_ranks(pieces(MAXN, 2), MAXN), rw(MAXN))
add(from_ranks(pieces(MAXN, 3), MAXN), [MAXW] * MAXN)
r, w = spliced(MAXN, 2000)
add(from_ranks(r, MAXN), w)
r, w = spliced(MAXN, 100)
add(from_ranks(r, MAXN), w)
r, w = spliced(MAXN, 20000, True)
add(from_ranks(r, MAXN), w)
r = list(range(MAXN))
r[0], r[-1] = r[-1], r[0]
add(from_ranks(r, MAXN), rw(MAXN))
r = [0] * MAXN
r[0::2] = range(MAXN // 2)
r[1::2] = range(MAXN // 2, MAXN)
add(from_ranks(r, MAXN), rw(MAXN))
add(from_ranks(list(range(MAXN)), MAXN), [MAXW] * MAXN)
r, w = spliced(MAXN, 5000)
add(from_ranks(r, MAXN), w)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
