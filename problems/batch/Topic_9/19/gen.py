# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90119)
MAXN, MAXM, MAXW = 200, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, roads):
    m = len(roads)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW for u, v, w in roads)
    tests.append(f"{n} {m}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in roads))


def pair(lo, hi):
    """two different districts from lo..hi"""
    a = ri(lo, hi)
    b = ri(lo, hi - 1)
    return a, b + (b >= a)


def rnd(n, m, wlo, whi):
    return [pair(1, n) + (ri(wlo, whi),) for _ in range(m)]


def bridge(n, m, every, heavy):
    """district n is reached only by dear roads (one every 'every' days), all other roads are cheap"""
    roads = []
    for d in range(m):
        if d % every == every - 1:
            roads.append((n, ri(1, n - 1), heavy - ri(0, 1000)))
        else:
            roads.append(pair(1, n - 1) + (ri(1, 1000),))
    return roads


def halves(n, m, every):
    """two halves joined only by dear roads"""
    h = n // 2
    roads = []
    for d in range(m):
        if d % every == 0:
            roads.append((ri(1, h), ri(h + 1, n), ri(MAXW // 2, MAXW)))
        elif d % 2:
            roads.append(pair(1, h) + (ri(1, 10**6),))
        else:
            roads.append(pair(h + 1, n) + (ri(1, 10**6),))
    return roads


def cluster(n, m, k, every, clo, chi, olo, ohi):
    """most roads join districts 1..k (cost clo..chi), one road every 'every' days touches a district
    outside the cluster and is dearer (cost olo..ohi): the cheap roads pile up but never help"""
    roads = []
    for d in range(m):
        if d % every == every - 1:
            a, b = pair(1, n)
            if a <= k and b <= k:
                a = ri(k + 1, n)
            roads.append((a, b, ri(olo, ohi)))
        else:
            roads.append(pair(1, k) + (ri(clo, chi),))
    return roads


def late(n, m):
    """district n gets its first road on the last day"""
    roads = [pair(1, n - 1) + (ri(1, MAXW),) for _ in range(m - 1)]
    roads.append((ri(1, n - 1), n, ri(1, MAXW)))
    return roads


def falling(n, m):
    """every road is cheaper than all earlier ones"""
    return [pair(1, n) + (MAXW - d * (MAXW // m),) for d in range(m)]


def rising(n, m):
    """every road is dearer than all earlier ones (a spanning path comes first)"""
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    roads = [(lab[i], lab[i + 1], i + 1) for i in range(n - 1)]
    for d in range(n - 1, m):
        roads.append(pair(1, n) + (d + 1,))
    return roads


# samples
add(4, [(1, 2, 5), (2, 3, 4), (3, 4, 3), (1, 3, 1), (2, 4, 2), (1, 4, 6)])
add(3, [(1, 2, 7), (1, 2, 3), (2, 3, 1000000000)])
add(2, [(1, 2, 1000000000), (2, 1, 1000000000), (1, 2, 1)])
add(5, [(1, 2, 4), (3, 4, 4), (4, 5, 4), (2, 3, 9), (2, 5, 9), (1, 4, 4), (3, 5, 1)])
add(4, [(2, 3, 2), (3, 2, 1), (1, 4, 8), (4, 2, 6), (1, 3, 5), (2, 1, 7), (3, 4, 2)])
# hidden: small
add(2, [(1, 2, 1)])
add(2, [(2, 1, MAXW)] * 5)
for n, m, wmax in ((3, 6, 3), (5, 12, 2), (6, 20, 10), (8, 40, 5), (10, 60, MAXW), (20, 300, 50)):
    add(n, rnd(n, m, 1, wmax))
add(12, bridge(12, 200, 7, MAXW))
add(30, falling(30, 500))
add(30, rising(30, 500))
add(50, late(50, 1500))
add(200, rnd(200, 3000, 1, 10**6))
# hidden: maximum size
N, M = MAXN, MAXM
add(N, rnd(N, M, 1, MAXW))
add(N, cluster(N, M, 15, 4, 1, 2, 3, 3))                        # many equal costs
add(N, bridge(N, M, 50, MAXW))                                  # cheap roads never finish the job
add(N, bridge(N, M, 1000, MAXW))
add(N, bridge(N, M, 7, 10**6))
add(N, halves(N, M, 100))
add(N, late(N, M))                                              # -1 until the last day
add(N, late(N, M // 2) + rnd(N, M // 2, 1, MAXW))
add(N, falling(N, M))
add(N, rising(N, M))
add(N, cluster(N, M, 20, 3, MAXW - 5, MAXW - 1, MAXW, MAXW))    # the largest totals
add(N, [pair(1, N) + (MAXW,) for _ in range(M)])                # all costs equal
add(N, bridge(N, M, 3, MAXW))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
