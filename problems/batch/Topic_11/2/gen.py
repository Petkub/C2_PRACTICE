# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90202)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges):
    m = len(edges)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in edges))


def rnd_edge(lo, hi):
    a = ri(lo, hi)
    b = ri(lo, hi - 1)
    return (a, b + (b >= a))


def flip(e):
    return e if random.random() < 0.5 else (e[1], e[0])


def path_edges(vs):
    return [flip((vs[i - 1], vs[i])) for i in range(1, len(vs))]


def labels(n):
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


# samples
add(5, [(1, 2), (3, 4), (2, 1), (4, 5), (1, 5)])
add(6, [(1, 2), (3, 4), (5, 6), (2, 3)])
add(2, [(2, 1), (1, 2)])
add(7, [(7, 6), (5, 4), (6, 5), (1, 3), (3, 2), (2, 1)])
add(4, [(1, 4), (2, 3), (3, 1), (4, 2), (2, 1)])
# hidden: small
add(3, [(1, 2), (2, 3), (3, 1)])
add(10, [rnd_edge(1, 10) for _ in range(12)])
add(40, [rnd_edge(1, 40) for _ in range(60)])
add(300, [rnd_edge(1, 300) for _ in range(250)])
p = labels(1000)
add(1000, path_edges(p[:500]) + path_edges(p[500:]) + [(p[0], p[999])])
add(2000, [rnd_edge(1, 2000) for _ in range(3000)])
# hidden: maximum size
N, M = MAXN, MAXM
add(N, [rnd_edge(1, N) for _ in range(M)])
add(N, [rnd_edge(1, N) for _ in range(M // 2)] + [rnd_edge(1, 5000) for _ in range(M // 2)])
p = labels(N)
add(N, path_edges(p))                                           # one long path, built in order
add(N, [(1, k) for k in range(2, N + 1)])                       # a star from the centre
add(N, [(k, 1) for k in range(2, N + 1)])
add(N, [(k, k + 1) for k in range(1, N)])
p = labels(N)
add(N, [flip((p[0], p[k])) for k in range(1, N)])               # a star from a random centre, mixed order
p = labels(N)
e = [flip((p[i], p[i + 1])) for i in range(0, N, 2)]             # pairs, then pairs of pairs, ...
size = 2
while size < N:
    e += [flip((p[i], p[i + size])) for i in range(0, N - size, 2 * size)]
    size *= 2
add(N, e[:M])
p = labels(N)
half = N // 2
e = path_edges(p[:half]) + path_edges(p[half:])
random.shuffle(e)
add(N, e[:M - 1] + [(p[0], p[-1])])                             # two halves merge only at the end
add(N, [rnd_edge(1, 3) for _ in range(M)])                       # only three people take part
add(N, [rnd_edge(1, 400) for _ in range(M)])
e = [(2 * k - 1, 2 * k) for k in range(1, N // 2 + 1)]           # many groups of the same size
random.shuffle(e)
add(N, e + [rnd_edge(1, N) for _ in range(M - len(e))])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
