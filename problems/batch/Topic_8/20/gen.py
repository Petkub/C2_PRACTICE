# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(70020)
MAXR = MAXC = 500
MAXK = 50_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(rows, guards):
    """rows: the grid; guards: lists of 0-based cells (i, j)"""
    if isinstance(rows[0], list):
        rows = ["".join(x) for x in rows]
    r, c, k = len(rows), len(rows[0]), len(guards)
    assert 1 <= r <= MAXR and 1 <= c <= MAXC and 0 <= k <= MAXK
    assert all(len(x) == c and set(x) <= set(".#ST") for x in rows)
    text = "".join(rows)
    assert text.count("S") == 1 and text.count("T") == 1
    s = divmod(text.index("S"), c)
    for rt in guards:
        assert 1 <= len(rt) <= 4 and rt[0] != s    # nobody stands on S at minute 0
        a, b = rt[-1]                              # the cell one minute before (cyclically)
        for (i, j) in rt:
            assert 0 <= i < r and 0 <= j < c and rows[i][j] != "#" and abs(a - i) + abs(b - j) <= 1
            a, b = i, j
    lines = [f"{r} {c} {k}"] + rows
    lines += [f"{len(rt)} " + " ".join(f"{i + 1} {j + 1}" for i, j in rt) for rt in guards]
    tests.append("\n".join(lines) + "\n")


def blank(r, c):
    return [["."] * c for _ in range(r)]


def rnd(r, c, p):
    return [random.choices(".#", [1 - p, p], k=c) for _ in range(r)]


def is_open(g, i, j):
    return 0 <= i < len(g) and 0 <= j < len(g[0]) and g[i][j] != "#"


def nbrs(g, i, j):
    return [(i + a, j + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if is_open(g, i + a, j + b)]


def make_route(g, a, p):
    """a patrol of period p starting near cell a: waits, back-and-forth walks or a 2x2 loop"""
    nb = nbrs(g, *a)
    if p == 1 or not nb:
        rt = [a] * p
    else:
        b = random.choice(nb)
        if p == 2:
            rt = [a, b]
        elif p == 3:
            rt = random.choice(([a, a, b], [a, b, b]))
        else:
            nb2 = [x for x in nbrs(g, *b) if x != a]
            di, dj = b[0] - a[0], b[1] - a[1]
            side = random.choice((1, -1))
            c1 = (b[0] + dj * side, b[1] + di * side)     # the 2x2 square on one side of a-b
            c2 = (a[0] + dj * side, a[1] + di * side)
            if random.random() < 0.4 and is_open(g, *c1) and is_open(g, *c2):
                rt = [a, b, c1, c2]
            elif nb2 and random.random() < 0.7:
                rt = [a, b, random.choice(nb2), b]
            else:
                rt = [a, a, b, b]
    x = ri(0, p - 1)
    return rt[x:] + rt[:x]


def guards_random(g, k, periods, s, keep_free=()):
    """k random patrols on open cells (never on S at minute 0, never touching the cells in keep_free)"""
    opens = [(i, j) for i in range(len(g)) for j in range(len(g[0])) if g[i][j] != "#"]
    free = set(keep_free)
    res = []
    while len(res) < k:
        a = opens[ri(0, len(opens) - 1)]
        rt = make_route(g, a, random.choice(periods))
        if rt[0] == s or any(x in free for x in rt):
            continue
        res.append(rt)
    return res


# samples
add(["S.#..",
     ".....",
     "..#.T"], [[(1, 1), (1, 2), (1, 3), (1, 2)]])
add(["S...T"], [[(0, 2), (0, 3)]])
add(["S.T"], [[(0, 2)]])
add(["S#.",
     "...",
     ".#T"], [[(1, 0), (1, 0), (1, 1)], [(1, 2), (2, 2)]])
add(["S..",
     ".#.",
     "..T"], [[(0, 1), (0, 2), (1, 2), (0, 2)], [(2, 0), (1, 0)]])
add(["....",
     "S..T"], [[(1, 2), (1, 2), (1, 1)], [(0, 1), (0, 2), (0, 3), (0, 2)]])



def maze(r, c, braid):
    """a random maze (passages on even cells), then `braid` of the inner walls knocked down to make loops"""
    g = [["#"] * c for _ in range(r)]
    g[0][0] = "."
    stack = [(0, 0)]
    while stack:
        i, j = stack[-1]
        nb = [(i + di, j + dj, di, dj) for di, dj in ((2, 0), (-2, 0), (0, 2), (0, -2))
              if 0 <= i + di < r and 0 <= j + dj < c and g[i + di][j + dj] == "#"]
        if not nb:
            stack.pop()
            continue
        ni, nj, di, dj = nb[ri(0, len(nb) - 1)]
        g[i + di // 2][j + dj // 2] = "."
        g[ni][nj] = "."
        stack.append((ni, nj))
    for i in range(r):
        for j in range(c):
            if g[i][j] == "#" and (i % 2) != (j % 2) and random.random() < braid:
                g[i][j] = "."
    return g


def setup(g, s, t, k, periods, keep_free=()):
    g[s[0]][s[1]] = "S"
    g[t[0]][t[1]] = "T"
    return g, guards_random(g, k, periods, s, set(keep_free) | {s})


def serpentine(r, c):
    """corridors on the even rows joined at alternating ends: one long path from (0, 0)"""
    g = [["."] * c for _ in range(r)]
    for k, i in enumerate(range(1, r, 2)):
        g[i] = ["#"] * c
        g[i][c - 1 if k % 2 == 0 else 0] = "."
    return g


def guards_spaced(g, k, periods, s, t):
    """patrols that never come within 2 cells (in both directions) of another patrol, S or T"""
    opens = [(i, j) for i in range(len(g)) for j in range(len(g[0])) if g[i][j] != "#"]
    near = set()
    for (i, j) in (s, t):
        near |= {(i + a, j + b) for a in range(-2, 3) for b in range(-2, 3)}
    res = []
    for _ in range(20 * k):
        if len(res) == k:
            break
        rt = make_route(g, opens[ri(0, len(opens) - 1)], random.choice(periods))
        if any(x in near for x in rt):
            continue
        res.append(rt)
        for (i, j) in rt:
            near |= {(i + a, j + b) for a in range(-2, 3) for b in range(-2, 3)}
    return res


def dense_small(seed):
    """a small grid crowded with guards (these seeds need waiting and the full 12-minute cycle)"""
    random.seed(seed)
    r, c = ri(3, 8), ri(3, 8)
    g = rnd(r, c, random.choice((0.0, 0.15, 0.3)))
    k = ri(2, r * c // 2)
    add(*setup(g, (0, 0), (r - 1, c - 1), k, random.choice(((3, 4), (2, 3), (1, 3, 4)))))


def crowded(seed, n, p, periods):
    """MAXK guards on an n x n grid, close to the density where the way gets cut"""
    random.seed(seed)
    g = rnd(n, n, p)
    add(*setup(g, (0, 0), (n - 1, n - 1), MAXK, periods))


# hidden: small
add(["ST"], [])
add(["S", "T"], [[(1, 0)]])                                 # a guard stands on T for ever
add(["S.", ".T"], [[(0, 1), (1, 1)], [(1, 0), (1, 0), (0, 0)]])
for (r, c, k, p) in ((4, 5, 4, 0.1), (5, 5, 6, 0.2), (6, 6, 10, 0.15), (7, 7, 14, 0.2)):
    g = rnd(r, c, p)
    add(*setup(g, (0, 0), (r - 1, c - 1), k, (1, 2, 3, 4)))
g = maze(9, 9, 0.2)
add(*setup(g, (0, 0), (8, 8), 6, (3, 4)))
for seed in (1007, 1144, 1417):
    dense_small(seed)
random.seed(70021)
g = rnd(40, 40, 0.2)
add(*setup(g, (0, 0), (39, 39), 300, (2, 3, 4)))
# hidden: large
R = C = MAXR
g = blank(R, C)
add(*setup(g, (0, 0), (R - 1, C - 1), MAXK, (1, 2, 3, 4)))
for seed in (1, 2):                                         # long mazes
    random.seed(seed)
    g = maze(R - 1, C - 1, 0.0)
    add(*setup(g, (0, 0), (R - 2, C - 2), 150 + 100 * seed, (3, 4)))
random.seed(70022)
g = serpentine(R - 1, C)                                    # one path of about 125 000 cells
add(*setup(g, (0, 0), (R - 2, 0), 300, (3, 4)))
g = serpentine(R - 1, C)
g[0][0], g[R - 2][0] = "S", "T"
add(g, guards_spaced(g, 3000, (2, 3, 4), (0, 0), (R - 2, 0)))
g = serpentine(R - 1, C)                                    # the same, but the cell next to T is always watched
g[0][0], g[R - 2][0] = "S", "T"
gs = guards_spaced(g, 2000, (2, 3, 4), (0, 0), (R - 2, 0))
add(g, gs + [[(R - 2, 1)]])
g = blank(R, C)                                             # T is watched on every side: no way in
t = (R // 2, C // 2)
ring = [(t[0] + a, t[1] + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
g, gs = setup(g, (0, 0), t, 20000, (2, 3, 4), ring + [t])
add(g, gs + [[x] for x in ring])
crowded(1, 220, 0.0, (3, 4))
crowded(2, 230, 0.0, (3, 4))
crowded(1, 300, 0.15, (1, 3, 4))
crowded(1, 500, 0.3, (3, 4))
crowded(5, 450, 0.32, (2, 3, 4))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
