# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(130808)
MAXN, MAXM, MAXC = 100_000, 150_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        a[i], a[j] = a[j], a[i]


def add(n, abc, cost, roads, relabel=True):
    roads = list(roads)
    a, b, c = abc
    if relabel:
        p = list(range(1, n + 1))
        shuffle(p)
        roads = [(p[u - 1], p[v - 1]) for u, v in roads]
        new = [0] * n
        for v in range(1, n + 1):
            new[p[v - 1] - 1] = cost[v - 1]
        cost = new
        a, b, c = p[a - 1], p[b - 1], p[c - 1]
        shuffle(roads)
    m = len(roads)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and len(cost) == n
    assert all(1 <= x <= n for x in (a, b, c))
    assert all(0 <= x <= MAXC for x in cost)
    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v in roads)
    tests.append(f"{n} {m}\n{a} {b} {c}\n" + " ".join(map(str, cost)) + "\n"
                 + "".join(f"{u} {v}\n" for u, v in roads))


def costs(n, lo, hi, zero=0.0):
    return [0 if random.random() < zero else ri(lo, hi) for _ in range(n)]


def rnd_connected(n, m, first=1):
    e = [(first + ri(0, v - 1), first + v) for v in range(1, n)]
    while len(e) < m:
        u, v = ri(first, first + n - 1), ri(first, first + n - 1)
        if u != v:
            e.append((u, v))
    return e


def grid(r, c, m):
    e = []
    for i in range(r):
        for j in range(c):
            v = i * c + j + 1
            if j + 1 < c:
                e.append((v, v + 1))
            if i + 1 < r:
                e.append((v, v + c))
    shuffle(e)
    return e[:m]


def three_arms(n, m, arm_lo, arm_hi, rest_lo, rest_hi, direct):
    """centre 1 with three long arms (L cities each) of cheap cities ending at a, b, c; the other cities are
    expensive and join everything at random; if direct, a cheap route a ... b of 1.5 L cities that misses the
    centre is added: it is the cheapest a-b route, but joining c to it costs more than the three arms"""
    L = n // 5
    cost = [ri(rest_lo, rest_hi) for _ in range(n)]
    cost[0] = ri(arm_lo, arm_hi)
    e = []
    ends = []
    nxt = 2
    for _ in range(3):
        prev = 1
        for _ in range(L):
            e.append((prev, nxt))
            cost[nxt - 1] = ri(arm_lo, arm_hi)
            prev = nxt
            nxt += 1
        ends.append(prev)
    if direct:
        prev = ends[0]
        for _ in range(L + L // 2):
            e.append((prev, nxt))
            cost[nxt - 1] = ri(arm_lo, arm_hi)
            prev = nxt
            nxt += 1
        e.append((prev, ends[1]))
    while nxt <= n:
        e.append((ri(1, nxt - 1), nxt))
        nxt += 1
    while len(e) < m:
        u, v = ri(1, n), ri(1, n)
        if u != v and (cost[u - 1] >= rest_lo or cost[v - 1] >= rest_lo):
            e.append((u, v))
    return ends, cost, e


# samples
add(5, (1, 3, 5), [0, 4, 0, 2, 0], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)], False)
add(6, (2, 4, 6), [3, 0, 1, 0, 5, 0], [(1, 2), (2, 3), (3, 4), (5, 6)], False)
add(3, (2, 2, 2), [1, 7, 2], [(1, 2), (2, 3)], False)
add(6, (1, 6, 4), [2, 1, 3, 0, 6, 2], [(1, 2), (2, 3), (3, 6), (1, 4), (4, 5), (5, 6), (2, 4)], False)
add(4, (1, 2, 3), [0, 0, 0, 0], [(1, 4), (2, 4), (3, 4)], False)
# hidden: small (checked against the brute force)
add(1, (1, 1, 1), [MAXC], [])
add(2, (1, 2, 1), [MAXC, MAXC], [(1, 2)])
for n, m, hi, zero in ((7, 9, 10, 0.3), (12, 20, 100, 0.0), (16, 22, 50, 0.1),
                       (16, 30, MAXC, 0.2)):
    add(n, random.sample(range(1, n + 1), 3), costs(n, 1, hi, zero), rnd_connected(n, m))
for n, m, hi in ((15, 20, 3), (16, 22, 2)):
    ends, cost, e = three_arms(n, m, 0, hi, 20, 40, True)
    add(n, ends, cost, e)
ends, cost, e = three_arms(40, 60, 0, 5, 50, 100, True)
add(40, ends, cost, e)
ends, cost, e = three_arms(200, 280, 0, 10, 100, 1000, True)
add(200, ends, cost, e)
add(300, random.sample(range(1, 301), 3), costs(300, 0, 20, 0.3), grid(15, 20, 500))
# hidden: maximum size
N, M = MAXN, MAXM
ends, cost, e = three_arms(N, M, 0, 3, 10**6, MAXC, True)
add(N, ends, cost, e)
ends, cost, e = three_arms(N, M, 1, 1000, 10**8, MAXC, True)
add(N, ends, cost, e)
ends, cost, e = three_arms(N, M, 0, 10**4, MAXC, MAXC, False)
add(N, ends, cost, e)
ends, cost, e = three_arms(N, M, 0, 50, 10**7, MAXC, True)
add(N, (ends[1], ends[0], ends[2]), cost, e)
add(N, (1, 400, N), costs(N, 1, 100, 0.3), grid(250, 400, M))                   # three corners of a grid
add(N, (1, 400, N - 399), costs(N, 0, MAXC, 0.5), grid(250, 400, M))
add(N, (ri(1, N), ri(1, N), ri(1, N)), costs(N, 1, MAXC, 0.3), rnd_connected(N, M))
add(N, (ri(1, N), ri(1, N), ri(1, N)), costs(N, 1, 10, 0.5), rnd_connected(N, M))
add(N, (1, N, N // 2), costs(N, MAXC, MAXC),                                      # a long line, all at 10^9
    [(v, v + 1) for v in range(1, N)] + [(v, v + 2) for v in range(1, M - N + 2)])
v = ri(1, N)
add(N, (v, v, ri(1, N)), costs(N, 0, MAXC, 0.2), rnd_connected(N, M))
e = rnd_connected(N - 500, M - 600) + rnd_connected(500, 600, N - 499)         # c is cut off
add(N, (1, 2, N), costs(N, 0, 1000, 0.5), e)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
