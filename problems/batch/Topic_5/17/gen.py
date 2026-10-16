# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(10517)
MAXN = 300
MAXP = 1000
tests = []


def add(P, g):
    n, m = len(g), len(g[0])
    assert 1 <= n <= MAXN and 1 <= m <= MAXN and 1 <= P <= MAXP
    assert all(len(r) == m and set(r) <= set(".#~123456789") for r in g)
    assert g[0][0] == "." and g[n - 1][m - 1] == "."
    tests.append(f"{n} {m} {P}\n" + "".join(r + "\n" for r in g))


def rnd(n, m, rock, mud, fruit):
    """random field; rock, mud, fruit are probabilities of each kind of cell"""
    g = []
    for i in range(n):
        row = []
        for j in range(m):
            x = random.random()
            if x < rock:
                row.append("#")
            elif x < rock + mud:
                row.append("~")
            elif x < rock + mud + fruit:
                row.append(str(random.randint(1, 9)))
            else:
                row.append(".")
        g.append(row)
    g[0][0] = g[n - 1][m - 1] = "."
    return ["".join(r) for r in g]


def corridor(n, m, mudp, extra=0):
    """rocks everywhere except one random right/down corridor (plus a few random open cells)"""
    g = [["#"] * m for _ in range(n)]
    r = c = 0
    while True:
        g[r][c] = "~" if random.random() < mudp else random.choice("123456789.")
        if r == n - 1 and c == m - 1:
            break
        if r == n - 1 or (c < m - 1 and random.random() < 0.5):
            c += 1
        else:
            r += 1
    for _ in range(extra):
        g[random.randrange(n)][random.randrange(m)] = random.choice("~9")
    g[0][0] = g[n - 1][m - 1] = "."
    return ["".join(r) for r in g]


# samples
add(2, [".3.1", "2#~.", ".4~."])
add(3, [".~5", "~#~", "5~."])
add(1, [".#9", "9#."])
add(1, [".9..", ".~#9", ".~~.", "9..."])
add(5, ["."])
add(4, [".7~~.", ".#9#.", "8~~3."])
# hidden: small (checked against trying every pair of routes)
add(1, [".", "."])
add(7, [".5~5."])
add(1, rnd(5, 5, 0.15, 0.2, 0.4))
add(10, rnd(6, 7, 0.1, 0.4, 0.4))
add(3, rnd(7, 6, 0.2, 0.2, 0.5))
add(1, rnd(6, 6, 0.0, 0.0, 0.7))
add(MAXP, rnd(7, 7, 0.1, 0.4, 0.3))
add(2, [".9..9..", "~~~~~~.", "9~#####", ".~....."])
add(5, corridor(7, 6, 0.4))
add(1, [".#", "#."])                         # no route
# hidden: large
N = MAXN
add(3, rnd(N, N, 0.1, 0.2, 0.4))
add(1, rnd(N, N, 0.0, 0.0, 0.9))
add(50, rnd(N, N, 0.2, 0.3, 0.3))
add(MAXP, rnd(N, N, 0.05, 0.6, 0.3))          # mud almost everywhere: the score is very negative
add(2, rnd(N, N, 0.3, 0.1, 0.5))
add(7, corridor(N, N, 0.3))                   # one corridor: both pickers pay the same mud twice
add(20, corridor(N, N, 0.5, 3000))
add(1, ["." + "9" * (N - 1)] + ["9" * N for _ in range(N - 2)] + ["9" * (N - 1) + "."])
g = rnd(N, N, 0.0, 0.0, 0.9)                  # a rock wall cuts the field: no route
for i in range(N):
    g[i] = g[i][:N - 1 - i] + "#" + g[i][N - i:]
g[0] = "." + g[0][1:]
add(5, g)
add(4, rnd(N, 120, 0.1, 0.3, 0.4))
add(4, rnd(120, N, 0.1, 0.3, 0.4))
add(9, rnd(N, 1, 0.0, 0.3, 0.5))
add(9, rnd(1, N, 0.0, 0.3, 0.5))
g = [["~"] * N for _ in range(N)]             # two fruit lanes separated by mud
for i in range(N):
    g[i][0] = "9"
    g[N - 1][i] = "9"
    g[0][i] = "9"
    g[i][N - 1] = "9"
g[0][0] = g[N - 1][N - 1] = "."
add(MAXP, ["".join(r) for r in g])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
