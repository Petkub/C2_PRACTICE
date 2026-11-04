# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(80303)
MAXN = MAXM = 200000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, segs):
    m = len(segs)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM
    us, vs = [u for u, _ in segs], [v for _, v in segs]
    assert min(us) >= 1 and min(vs) >= 1 and max(us) <= n and max(vs) <= n
    assert all(map(int.__ne__, us, vs))
    tests.append(f"{n} {m}\n" + "\n".join(map("%d %d".__mod__, segs)) + "\n")


def walk(verts, m, closed=False):
    """segments of a random walk of m steps over the list verts (consecutive points differ)"""
    k = len(verts)
    rnd = random.random
    i = int(rnd() * k)
    first = verts[i]
    segs = []
    for _ in range(m - 1 if closed else m):
        j = (i + 1 + int(rnd() * (k - 1))) % k          # any index but i
        segs.append((verts[i], verts[j]))
        i = j
    if closed:
        cur = verts[i]
        if cur != first:
            segs.append((cur, first))
        else:                   # cannot close with one step: go back over the last segment instead
            segs.append(segs[-1][::-1])
    return segs


def degrees(n, segs):
    d = [0] * (n + 1)
    for u, v in segs:
        d[u] += 1
        d[v] += 1
    return d


def shuffle(a):
    """Fisher-Yates with random.random() (faster than random.shuffle, still deterministic)"""
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def mix(segs):
    """shuffle the order and the direction of every segment"""
    rnd = random.random
    a = list(segs)
    for i in range(len(a) - 1, -1, -1):
        r = rnd() * (i + 1)
        j = int(r)
        e = a[j]
        a[j] = a[i]
        a[i] = e if r - j < 0.5 else e[::-1]          # the fraction of r decides the direction
    return a


def relabel(n, segs):
    p = list(range(1, n + 1))
    shuffle(p)
    return [(p[u - 1], p[v - 1]) for u, v in segs]


# samples
add(5, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3)])
add(4, [(1, 2), (1, 3), (2, 3), (3, 4)])
add(4, [(1, 2), (1, 3), (1, 4)])
add(6, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)])
add(4, [(2, 3), (3, 2), (3, 4)])
add(3, [(3, 2)])
# hidden: small and medium
add(7, mix([(2, 3), (3, 4), (4, 5), (1, 6), (6, 7), (7, 1)]))                 # a path, and a triangle with point 1 apart
add(4, mix([(1, 2), (2, 1), (2, 3), (3, 4), (4, 2)]))                         # repeated segments, a loop through 2
add(7, mix(walk(list(range(2, 8)), 9)))
add(9, mix([(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3), (5, 6), (6, 7), (7, 5), (7, 8), (8, 9), (9, 7)]))   # chain of triangles
add(6, mix([(1, 2), (1, 3), (3, 4), (4, 1), (4, 5), (5, 6), (6, 4)]))
add(6, mix([(1, 2), (2, 3), (4, 5), (5, 6), (6, 4)]))
s = walk(list(range(1, 41)), 120, closed=True) + [(41, 42), (42, 41)]   # a far away pair of segments
add(50, mix(s))
p = random.sample(range(1, 301), 300)                    # an open walk and a closed walk with no common point
add(300, mix(walk(p[:150], 180) + walk(p[150:], 120, closed=True)))
add(30, mix(relabel(30, walk(list(range(1, 31)), 50000, closed=True))))
s = walk(list(range(1, 101)), 250)                       # four odd points
d = degrees(100, s)
odd = [v for v in range(1, 101) if d[v] % 2]
u = next(v for v in range(1, 101) if v not in odd)
w = next(v for v in range(1, 101) if v not in odd and v != u)
add(100, mix(s + [(u, w)]))
add(12, mix([(5, 9), (9, 5), (2, 7), (7, 11), (11, 2), (1, 4), (4, 12), (12, 6), (6, 1), (3, 8)]))   # 4 pieces
# hidden: largest
N = MAXN
add(N, mix(walk(list(range(1, N + 1)), MAXM)))
add(N, [(i, i + 1) for i in range(1, N)])                 # path 1 - 2 - ... - N in order
s = walk(list(range(1, 1001)), MAXM - 5000, closed=True)  # a closed walk, and a path apart
add(N, mix(s + [(i, i + 1) for i in range(1001, 6001)]))
add(N, mix(relabel(N, walk(list(range(1, 1001)), MAXM, closed=True))))
add(2, [(1, 2)] * MAXM)                                   # many segments on one pair
add(N, mix([(2 * k + a, 2 * k + b) for k in range(MAXM // 3) for a, b in ((1, 2), (2, 3), (3, 1))]))   # chain of triangles
s = walk(list(range(2, N + 1)), MAXM, closed=True)        # point 1 has no segment
add(N, mix(s))
tri = []                                                  # triangles through point 1
for k in range(MAXM // 3):
    tri += [(1, 2 * k + 2), (2 * k + 2, 2 * k + 3), (2 * k + 3, 1)]
add(N, mix(tri))
cyc = []                                                  # two overlapping cycles of N / 2 points each
for _ in range(2):
    p = random.sample(range(1, N + 1), N // 2)
    cyc += [(p[i], p[(i + 1) % len(p)]) for i in range(len(p))]
add(N, mix(cyc))
add(N, mix(relabel(N, walk(list(range(1, 31)), MAXM - 1))))   # many repeated segments
s = walk(list(range(1, N - 2)), MAXM - 3)                 # two odd points, a triangle far away
add(N, mix(s + [(N - 2, N - 1), (N - 1, N), (N, N - 2)]))
h = N // 2                                                # two closed walks far apart
add(N, mix(walk(list(range(1, h + 1)), MAXM // 2, closed=True) + walk(list(range(h + 1, N + 1)), MAXM // 2, closed=True)))
add(N, mix(walk(list(range(4, N + 1)), MAXM - 3, closed=True) + [(1, 2), (2, 3), (3, 1)]))   # a closed walk, triangle 1 2 3 apart

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
