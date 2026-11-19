# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(44005)
MAXN, MAXK, MAXQ, MAXSUM = 100_000, 20, 100_000, 300_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, clubs, qs):
    n, q = len(clubs), len(qs)
    assert 1 <= n <= MAXN and 1 <= k <= MAXK and 1 <= q <= MAXQ
    assert sum(len(c) for c in clubs) <= MAXSUM
    assert all(len(set(c)) == len(c) for c in clubs if len(c) > 1)
    flat = [x for c in clubs for x in c]
    assert not flat or (min(flat) >= 1 and max(flat) <= k)
    assert all(1 <= s <= n and 1 <= e <= n for s, e in qs)
    num = [str(i) for i in range(MAXK + 1)]
    lines = [" ".join([num[len(c)]] + [num[x] for x in c]) for c in clubs]
    tests.append(f"{n} {k} {q}\n" + "\n".join(lines) + "\n" + "".join(f"{s} {e}\n" for s, e in qs))


def pick(lo, hi, m):
    res = []
    while len(res) < m:
        x = ri(lo, hi)
        if x not in res:
            res.append(x)
    return res


def mixed(clubs, order=True):
    res = [list(c) for c in clubs]
    random.shuffle(res)
    if order:
        for c in res:
            if len(c) > 1:
                random.shuffle(c)
    return res


def queries(n, q, rare=(), same=0.02, far=0.3):
    res = []
    for _ in range(q):
        t = random.random()
        s = ri(1, n)
        if t < same:
            e = s
        elif t < same + far and rare:
            e = rare[ri(0, len(rare) - 1)]
            if random.random() < 0.5:
                s, e = e, s
        else:
            e = ri(1, n)
        res.append((s, e))
    return res


def clubless(clubs):
    return [i + 1 for i, c in enumerate(clubs) if not c]


add(4, [[1], [1, 2], [2, 3], [4], [3]], [(1, 5), (1, 2), (4, 1), (3, 3)])
add(3, [[1], [2, 1], [2], []], [(1, 3), (3, 2), (4, 4), (4, 1)])
add(1, [[1]], [(1, 1)])
add(5, [[2, 3], [1], [5], [3, 4], [4, 5], [2, 1]], [(2, 3), (3, 2), (1, 2), (6, 4), (1, 1)])
add(6, [[2, 1], [2], [3], [4, 5], [6], [5, 6], [4, 3]], [(3, 5), (7, 6), (1, 2), (2, 4), (6, 6)])

add(1, [[1], [], [1]], [(1, 2), (2, 2), (1, 3), (3, 1)])
add(2, [[1], [2]], [(1, 2), (2, 1), (1, 1)])
for n, k, q in [(8, 4, 20), (15, 6, 40), (30, 8, 60), (60, 12, 100), (200, 20, 200), (2000, 20, 2000)]:
    clubs = [random.sample(range(1, k + 1), min(k, random.choice([0, 1, 1, 1, 2, 2, 3]))) for _ in range(n)]
    add(k, clubs, queries(n, q, clubless(clubs), same=0.05))

N, K, Q = MAXN, MAXK, MAXQ
clubs = [[i, i + 1] for i in range(1, K) for _ in range(3)]
clubs += [[ri(1, K)] for _ in range(N - len(clubs) - 2000)] + [[] for _ in range(2000)]
clubs = mixed(clubs)
add(K, clubs, queries(N, Q, clubless(clubs)))
clubs = [[i, i + 1] for i in range(1, K)]
clubs += [[1, 7, 13], [13, 4, 20], [5, 11, 17]]
clubs += [[ri(1, K)] for _ in range(N - len(clubs) - 1000)] + [[] for _ in range(1000)]
clubs = mixed(clubs, order=False)
add(K, clubs, queries(N, Q, clubless(clubs)))
clubs = [pick(1, K, ri(1, 3)) for _ in range(N - 3000)] + [[] for _ in range(3000)]
add(K, mixed(clubs), queries(N, Q, clubless(clubs)))
clubs = [pick(1, 10, ri(1, 2)) for _ in range(N // 2)] + [pick(11, 20, ri(1, 2)) for _ in range(N // 2)]
clubs = mixed(clubs)
add(K, clubs, queries(N, Q, [i + 1 for i, c in enumerate(clubs) if c[0] > 10], far=0.5))
clubs = [[1, i] for i in range(2, K + 1)] + [[ri(2, K)] for _ in range(N - K + 1 - 500)] + [[] for _ in range(500)]
clubs = mixed(clubs)
add(K, clubs, queries(N, Q, clubless(clubs)))
clubs = [list(range(1, K + 1)) for _ in range(5)]
clubs += [[ri(1, K)] for _ in range(N - 5 - 1000)] + [[] for _ in range(1000)]
clubs = mixed(clubs)
add(K, clubs, queries(N, Q, clubless(clubs)))
clubs = [[1] for _ in range(N - 1000)] + [[] for _ in range(1000)]
clubs = mixed(clubs)
add(1, clubs, queries(N, Q, clubless(clubs), far=0.4))
perm = list(range(1, K + 1))
random.shuffle(perm)
clubs = [[perm[i], perm[i + 1]] for i in range(K - 1)]
for _ in range(30):
    i = ri(0, K - 4)
    clubs.append([perm[i], perm[ri(i + 1, i + 2)], perm[i + 3]])
clubs += [[ri(1, K) for _ in range(1)] for _ in range(N - len(clubs) - 1500)] + [[] for _ in range(1500)]
clubs = mixed(clubs, order=False)
add(K, clubs, queries(N, Q, clubless(clubs)))
clubs = [pick(1, K, 3) for _ in range(N)]
add(K, clubs, queries(N, Q, [], same=0.01))
clubs = [[i, i + 1] for i in range(1, K)]
clubs += [[ri(1, 3)] for _ in range((N - K) // 2)] + [[ri(K - 2, K)] for _ in range(N - K + 1 - (N - K) // 2 - 800)]
clubs += [[] for _ in range(800)]
clubs = mixed(clubs)
add(K, clubs, queries(N, Q, clubless(clubs)))

clubs = [pick(1, 12, ri(0, 2)) for _ in range(20_000)]
add(12, mixed(clubs), queries(20_000, 20_000, clubless(clubs)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
