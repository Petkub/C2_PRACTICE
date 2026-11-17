# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(30620)
MAXNM = 500
tests = []

def add(g):
    n, m = len(g), len(g[0])
    assert 1 <= n <= MAXNM and 1 <= m <= MAXNM
    assert all(len(r) == m and all(v in (0, 1) for v in r) for r in g)
    tests.append(f"{n} {m}\n" + "\n".join("".join(map(str, r)) for r in g) + "\n")

def from_diff(n, m, D):
    g = [[0] * m for _ in range(n)]
    for i in range(n):
        run, up = 0, g[i - 1] if i else [0] * m
        row = g[i]
        Di = D[i]
        for j in range(m):
            run ^= Di[j]
            row[j] = run ^ up[j]
    return g

def stamps(n, m, k, places):
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for a, b in places:
        assert 0 <= a <= n - k and 0 <= b <= m - k
        D[a][b] ^= 1; D[a + k][b] ^= 1; D[a][b + k] ^= 1; D[a + k][b + k] ^= 1
    return from_diff(n, m, D)

def random_blocks(n, m, sizes, cnt):
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for _ in range(cnt):
        k = random.choice(sizes)
        a, b = random.randint(0, n - k), random.randint(0, m - k)
        D[a][b] ^= 1; D[a + k][b] ^= 1; D[a][b + k] ^= 1; D[a + k][b + k] ^= 1
    return from_diff(n, m, D)

def product(f, g):
    return [[x & y for y in g] for x in f]

def segs(length, L, starts):
    f = [0] * length
    for p in starts:
        for t in range(p, p + L):
            f[t] ^= 1
    return f

def pairs1d(length, L, s, cnt):
    starts = []
    for p in random.sample(range(0, min(s, length - L - s + 1)), cnt):
        starts += [p, p + s]
    return segs(length, L, starts)

def stretch(bits, t):
    return [int(c) for c in bits for _ in range(t)]


add(stamps(4, 5, 2, [(0, 0), (1, 1), (2, 2)]))
add([[1, 0], [0, 1]])
add([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
add(stamps(5, 6, 3, [(0, 0), (1, 2), (2, 1)]))
add([[1] * 6, [1] * 6])

add([[0]])
add([[1]])
add(product(stretch("1100101", 1), stretch("1100101", 1)))
f8 = [1, 1, 0, 0, 0, 0, 1, 1]
add(product(f8, f8))
add([[random.randint(0, 1) for _ in range(8)] for _ in range(6)])
add(stamps(12, 15, 4, [(random.randint(0, 8), random.randint(0, 11)) for _ in range(10)]))
add(product(stretch("1100101", 10), stretch("1010011", 10)))
add(random_blocks(60, 80, [24], 300))
add(product(pairs1d(120, 60, 20, 15), pairs1d(100, 60, 20, 8)))
add([[random.randint(0, 1) for _ in range(200)] for _ in range(200)])
add([segs(MAXNM, 7, random.sample(range(MAXNM - 6), 100))])
add(stamps(30, 40, 30, [(0, 3), (0, 7)]))

N = MAXNM
add(random_blocks(N, N, [360], 40000))
add(random_blocks(N, N, [336], 40000))
add(random_blocks(N, N, [324], 40000))
add(random_blocks(N, N, [360], 25000))
add(random_blocks(N, N, [384], 40000))
add(product(pairs1d(N, 300, 100, 50), pairs1d(N, 300, 100, 60)))
add(product(pairs1d(N, 288, 96, 60), pairs1d(N, 288, 96, 70)))
add(product(pairs1d(N, 240, 80, 70), pairs1d(N, 240, 80, 75)))
add(random_blocks(N, 490, [360], 40000))
add(random_blocks(490, N, [336], 40000))
add(product(pairs1d(N, 252, 84, 80), pairs1d(N, 252, 84, 60)))
add(random_blocks(N, N, [360], 32000))

add([[0] * N for _ in range(N)])
corner = [[0] * N for _ in range(N)]
corner[N - 1][N - 1] = 1
add(corner)
patch = [[0] * N for _ in range(N)]
for i in range(N - 3, N):
    for j in range(N - 4, N):
        patch[i][j] = random.randint(0, 1)
patch[N - 1][N - 1] = 1
add(patch)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
