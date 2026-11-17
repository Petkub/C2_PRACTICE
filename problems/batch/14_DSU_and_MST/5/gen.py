# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(90505)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges):
    m = len(edges)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n for a, b in edges)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in edges))


def flip(a, b):
    return (a, b) if random.random() < 0.5 else (b, a)


def grow(vs, shape="random"):
    res = []
    for i in range(1, len(vs)):
        if shape == "path":
            j = i - 1
        elif shape == "deep":
            j = max(0, i - ri(1, 4))
        else:
            j = ri(0, i - 1)
        res.append(flip(vs[i], vs[j]))
    return res


def labels(n):
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


def rnd_tail(n, k):
    return [(ri(1, n), ri(1, n)) for _ in range(k)]


add(5, [(1, 2), (2, 3), (4, 5), (3, 1), (1, 4)])
add(4, [(1, 2), (3, 4), (2, 3)])
add(3, [(1, 2), (2, 2), (1, 3)])
add(3, [(2, 3), (1, 2), (3, 2)])
add(6, [(1, 2), (3, 4), (5, 6), (2, 3), (4, 5), (6, 1), (1, 3)])

add(1, [(1, 1)])
add(2, [(1, 2)])
add(8, [(1, 2), (3, 4), (5, 6), (7, 8), (2, 3), (6, 7), (4, 5), (8, 1), (1, 5)])
p = labels(20)
add(20, grow(p) + [flip(p[3], p[17])] + rnd_tail(20, 5))
add(100, [(ri(1, 100), ri(1, 100)) for _ in range(100)])
p = labels(500)
add(500, grow(p[:250]) + grow(p[250:]))
p = labels(2000)
add(2000, grow(p, "deep") + [flip(p[0], p[-1])])
p = labels(5000)
e = grow(p)
add(5000, e[:3000] + [flip(p[100], p[100])] + e[3000:])

N, M = MAXN, MAXM
p = labels(N)
add(N, grow(p, "path") + [flip(p[0], p[-1])])
p = labels(N)
add(N, grow(p))
p = labels(N)
e = grow(p, "deep")
add(N, e + [flip(p[ri(0, N - 1)], p[ri(0, N - 1)])])
p = labels(N)
e = grow(p, "path")
add(N, e[:N - 2] + [e[N // 2]] + e[N - 2:])
p = labels(N)
add(N, grow(p) + [(p[N - 1], p[N - 1])])
p = labels(N)
add(N, [flip(p[0], p[k]) for k in range(1, N)] + [flip(p[N // 3], p[N // 2])])
add(N, [(1, k) for k in range(2, N + 1)] + [(N, 2)])
add(N, [(k, 1) for k in range(2, N + 1)] + [(2, N)])
add(N, [(k, k + 1) for k in range(1, N)] + [(N, 1)])
p = labels(N)
half = N // 2
add(N, grow(p[:half], "deep") + grow(p[half:], "deep") + [flip(p[0], p[half])] + [flip(p[1], p[half + 1])])
p = labels(N)
e = grow(p[:100_000]) + grow(p[100_000:])
random.shuffle(e)
add(N, e)
e = []
for _ in range(M):
    a = ri(1, N)
    e.append((a, (a + ri(1, N - 1) - 1) % N + 1))
add(N, e)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
