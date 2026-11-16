# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160012)
MAXR = MAXC = 1700
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC
    assert all(len(row) == c and all(ch == "#" or "1" <= ch <= "9" for ch in row) for row in g)
    tests.append(f"{r} {c}\n" + "".join(row + "\n" for row in g))


def rand_grid(r, c, alpha):
    """alpha: a string; each cell is a uniformly random character of it (repeat characters for weights)"""
    return ["".join(random.choices(alpha, k=c)) for _ in range(r)]


def put(g, i, j, ch):
    g[i] = g[i][:j] + ch + g[i][j + 1:]


# samples
add(["11#91", "11#29", "11###", "#1111"])
add(["##", "##"])
add(["5"])
add(["123", "456", "789"])
add(["9#1111", "9#1111", "9#####", "999999"])
# hidden: small (the brute force checks every rectangle)
add(["#"])
add(["1#1#1"])
add(rand_grid(8, 9, "#123456789"))
add(rand_grid(20, 25, "#1111111112"))
add(rand_grid(30, 30, "#" + "1" * 30 + "9"))
add(rand_grid(40, 12, "##12345"))
# hidden: medium (no brute)
add(rand_grid(600, 600, "#" + "123456789" * 22))
add(rand_grid(1500, 200, "#" * 3 + "1" * 200 + "9" * 5))
# hidden: maximum size
N = 1700
add(["1" * N] * N)                                                # everything free: 2 250 000
add(["9" * N] * N)
g = ["1" * N] * N                                                 # all 1 but a few 9s, no rock
for _ in range(20):
    put(g, ri(0, N - 1), ri(0, N - 1), "9")
add(g)
g = ["1" * (i + 1) + "#" * (N - 1 - i) for i in range(N)]       # lower-left triangle
for _ in range(300):
    i = ri(0, N - 1)
    j = ri(0, i)
    put(g, i, j, "9")
add(g)
g = ["#" * (N - 1 - i) + "1" * (i + 1) for i in range(N)]       # lower-right triangle
for _ in range(300):
    i = ri(0, N - 1)
    put(g, i, ri(N - 1 - i, N - 1), "9")
add(g)
add(rand_grid(N, N, "#" + "1" * 300 + "9"))                      # few rocks, mostly 1
add(rand_grid(N, N, "#" + "123456789" * 11))                     # 1% rocks
g = [["1"] * N for _ in range(N)]                                 # rocks on the diagonal: heights fall to the left of it
for i in range(N):
    g[i][i] = "#"
for _ in range(20):
    i, j = ri(0, N - 1), ri(0, N - 1)
    if i != j:
        g[i][j] = "9"
add(["".join(row) for row in g])
row_a = "1" * 899 + "#" + "".join(random.choices("9" * 60 + "#", k=600))   # big area of 1s or a richer part
g = [row_a if i % 2 else "1" * 899 + "#" + "".join(random.choices("9" * 60 + "#", k=600)) for i in range(N)]
add(g)
wall_row = "#" * N
cell_row = "".join("#" if j % 100 == 0 else "1" for j in range(N))
g = [wall_row if i % 100 == 0 else cell_row for i in range(N)]
for i in range(301, 400):                                       # one block of 9s among blocks of 1s
    g[i] = g[i][:701] + "9" * 99 + g[i][800:]
add(g)
g = []                                                            # staircase: row i is free in columns 1..i+1 (or i+2)
for i in range(N):
    k = min(N, i + 1 + ri(0, 1))
    g.append("1" * k + "#" * (N - k))
for _ in range(100):
    i = ri(0, N - 1)
    put(g, i, ri(0, i), "9")
g.reverse()                                                       # upper-left staircase
add(g)
g = ["1" * (i + 1) + "#" * (N - 1 - i) for i in range(N)]       # lower-left triangle, few 9s near the corner
for _ in range(15):
    i = ri(N - 200, N - 1)
    put(g, i, ri(0, 150), "9")
add(g)
g = ["1" * N] * N                                                 # few 9s, a few rock columns
for j in (300, 900, 1200):
    for i in range(N):
        if ri(0, 49) == 0:
            put(g, i, j, "#")
for _ in range(10):
    put(g, ri(0, N - 1), ri(0, N - 1), "9")
add(g)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
