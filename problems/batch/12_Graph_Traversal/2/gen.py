# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(12001)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, k, starters, edges):
    m, s = len(edges), len(starters)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and 1 <= s <= n
    assert len(k) == n and all(1 <= x <= n for x in k)
    assert len(set(starters)) == s and all(1 <= p <= n for p in starters)
    seen = set()
    for u, v in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v
        key = (min(u, v), max(u, v))
        assert key not in seen
        seen.add(key)
    tests.append(f"{n} {m} {s}\n" + " ".join(map(str, k)) + "\n" + " ".join(map(str, starters)) + "\n"
                 + "".join(f"{u} {v}\n" for u, v in edges))


def shuffled(n, k, starters, edges):
    p = list(range(1, n + 1))
    random.shuffle(p)
    k2 = [0] * n
    for i in range(n):
        k2[p[i] - 1] = k[i]
    e = [(p[u - 1], p[v - 1]) if random.random() < 0.5 else (p[v - 1], p[u - 1]) for u, v in edges]
    random.shuffle(e)
    st = [p[x - 1] for x in starters]
    random.shuffle(st)
    add(n, k2, st, e)


def rnd_graph(n, m, base=0):
    seen, e = set(), []
    while len(e) < m:
        u, v = ri(1, n), ri(1, n)
        if u == v:
            continue
        key = (min(u, v), max(u, v))
        if key in seen:
            continue
        seen.add(key)
        e.append((u + base, v + base))
    return e


def rnd_k(deg, lo_frac=0.2, hi_frac=0.7):
    return max(1, int(deg * (lo_frac + (hi_frac - lo_frac) * random.random())) + (1 if random.random() < 0.5 else 0))


def degrees(n, edges):
    d = [0] * (n + 1)
    for u, v in edges:
        d[u] += 1
        d[v] += 1
    return d


add(7, [1, 2, 1, 2, 2, 1, 1], [7], [(7, 6), (7, 5), (6, 5), (6, 4), (5, 4), (4, 3), (3, 2), (2, 1)])
add(6, [2, 2, 1, 1, 1, 1], [6], [(6, 5), (5, 4), (4, 3), (2, 5), (2, 3), (1, 2), (1, 6)])
add(1, [1], [1], [])
add(4, [1, 2, 1, 3], [4], [(4, 1), (4, 2), (4, 3)])
add(5, [2, 1, 2, 1, 2], [5, 4], [(5, 3), (4, 3), (3, 2), (2, 1), (4, 1)])


add(2, [1, 1], [1], [])
add(3, [3, 2, 1], [1, 2, 3], [(1, 2), (2, 3)])
add(5, [1, 1, 1, 1, 1], [3], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
add(6, [1, 2, 2, 2, 2, 1], [1], [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6)])
for n, m in [(8, 12), (10, 20), (12, 30), (15, 25), (20, 60), (30, 80)]:
    e = rnd_graph(n, m)
    d = degrees(n, e)
    k = [rnd_k(d[i]) if d[i] else ri(1, 2) for i in range(1, n + 1)]
    shuffled(n, k, random.sample(range(1, n + 1), ri(1, 3)), e)
n, m = 3000, 9000
e = rnd_graph(n, m)
d = degrees(n, e)
shuffled(n, [rnd_k(d[i], 0.1, 0.6) if d[i] else 1 for i in range(1, n + 1)], random.sample(range(1, n + 1), 5), e)


def path_tail(start, length, attach_to, kk=1):
    e = [(attach_to, start + 1)] + [(start + i, start + i + 1) for i in range(1, length)]
    return e, [kk] * length


N, M = MAXN, MAXM

e = [(i, i + 1) for i in range(1, N)]
shuffled(N, [1] * N, [1], e)

n1 = N // 2
e = rnd_graph(n1, M - (N - n1))
d = degrees(n1, e)
k = [rnd_k(d[i], 0.1, 0.5) if d[i] else 1 for i in range(1, n1 + 1)]
starters = random.sample(range(1, n1 + 1), 50)
tail, kt = path_tail(n1, N - n1, starters[0])
shuffled(N, k + kt, starters, e + tail)

e = [(1, 2)] + [(i, i - 1) for i in range(3, N // 2 + 1)] + [(i, i - 2) for i in range(3, N // 2 + 1)]
shuffled(N // 2, [2] * (N // 2), [1, 2], e)

L = N // 4
top = lambda c: c
bot = lambda c: L + c
e = [(top(c), bot(c)) for c in range(1, L + 1)] + [(top(c), top(c + 1)) for c in range(1, L)] \
    + [(bot(c), bot(c + 1)) for c in range(1, L)] + [(top(c), bot(c + 1)) for c in range(1, L)]
shuffled(2 * L, [2] * (2 * L), [top(1), bot(1)], e)

n1 = 60_000
e = rnd_graph(n1, 60_000)
d = degrees(n1, e)
k = [rnd_k(d[i], 0.2, 0.6) if d[i] else 1 for i in range(1, n1 + 1)]
starters = random.sample(range(1, n1 + 1), 30)
cur = n1
for length in [60_000, 30_000, 20_000, 10_000, 5_000, 4_000, 1_000]:
    tail, kt = path_tail(cur, length, ri(1, n1))
    e += tail
    k += kt
    cur += length
tail, kt = path_tail(cur, N - cur, starters[1])
e += tail
k += kt
shuffled(N, k, starters, e)

n6 = N // 2
e = [(i, i + 1) for i in range(1, n6)] + [(i, i + 2) for i in range(1, n6 - 1, 2)]
k = [ri(1, 2) if i % 2 == 1 and i > 2 else 1 for i in range(1, n6 + 1)]
shuffled(n6, k, [1], e)

n1 = 80_000
e = rnd_graph(n1, 75_000)
d = degrees(n1, e)
k = [max(1, d[i] - ri(0, 1)) if d[i] else n1 for i in range(1, n1 + 1)]
starters = random.sample(range(1, n1 + 1), 2000)
tail, kt = path_tail(n1, N - n1, starters[0])
shuffled(N, k + kt, starters, e + tail)

n8 = 80_000
e = [(1, 2)] + [(i, i - 1) for i in range(3, n8 + 1)] + [(i, i - 2) for i in range(3, n8 + 1)]
seen = set((min(u, v), max(u, v)) for u, v in e)
while len(e) < M:
    u = ri(1, n8)
    v = u + ri(3, 2000)
    if v > n8 or (u, v) in seen:
        continue
    seen.add((u, v))
    e.append((u, v))
back = [0] * (n8 + 1)
for u, v in e:
    back[max(u, v)] += 1
k = [max(1, back[i] - (1 if random.random() < 0.3 else 0)) for i in range(1, n8 + 1)]
shuffled(n8, k, [1, 2], e)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
