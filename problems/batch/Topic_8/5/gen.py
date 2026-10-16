# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(8005)
MAXR = MAXC = 1000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(rows):
    r, c = len(rows), len(rows[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC
    assert all(len(x) == c and all(ch in "0123456789#" for ch in x) for x in rows)
    assert rows[0][0] != "#" and rows[-1][-1] != "#"
    tests.append(f"{r} {c}\n" + "".join(x + "\n" for x in rows))


def digit(lo, hi):
    return chr(48 + ri(lo, hi))


def rnd(r, c, lo, hi, wall=0.0):
    pop = [chr(48 + d) for d in range(lo, hi + 1)] + ["#"]
    wt = [(1 - wall) / (hi - lo + 1)] * (hi - lo + 1) + [wall]
    g = ["".join(random.choices(pop, wt, k=c)) for _ in range(r)]
    g[0] = digit(lo, hi) + g[0][1:]
    g[-1] = g[-1][:-1] + digit(lo, hi)
    return g


def maze(r, c, lo, hi, wallch="#", wlo=0, whi=9):
    """recursive backtracker maze; r and c odd; passages get digits lo..hi, walls get wallch or digits wlo..whi"""
    h, w = r // 2 + 1, c // 2 + 1
    seen = bytearray(h * w)
    passage = bytearray(r * c)
    seen[0] = passage[0] = 1
    stack = [0]
    rand = random.random
    while stack:
        x = stack[-1]
        i, j = divmod(x, w)
        nb = []
        if i + 1 < h and not seen[x + w]:
            nb.append(x + w)
        if i > 0 and not seen[x - w]:
            nb.append(x - w)
        if j + 1 < w and not seen[x + 1]:
            nb.append(x + 1)
        if j > 0 and not seen[x - 1]:
            nb.append(x - 1)
        if not nb:
            stack.pop()
            continue
        y = nb[int(rand() * len(nb))]
        a, b = divmod(y, w)
        seen[y] = 1
        passage[2 * a * c + 2 * b] = 1
        passage[(i + a) * c + (j + b)] = 1
        stack.append(y)
    pd = random.choices([chr(48 + d) for d in range(lo, hi + 1)], k=r * c)
    wd = ["#"] * (r * c) if wallch == "#" else random.choices([chr(48 + d) for d in range(wlo, whi + 1)], k=r * c)
    cells = [pd[k] if passage[k] else wd[k] for k in range(r * c)]
    return ["".join(cells[i * c:(i + 1) * c]) for i in range(r)]


def serpentine(r, c, lo, hi):
    """walls on every other row with one gap at alternating ends"""
    g = []
    for i in range(r):
        if i % 2 == 0:
            g.append("".join(random.choices([chr(48 + d) for d in range(lo, hi + 1)], k=c)))
        else:
            gap = c - 1 if i % 4 == 1 else 0
            g.append("".join(digit(lo, hi) if j == gap else "#" for j in range(c)))
    return g


def diagonal(r, c, lo, hi):
    """staircase corridors along anti-diagonals (i + j) mod 4 in {0, 1}, joined at alternating ends"""
    assert (r + c - 2) % 4 in (0, 1)
    digits = [chr(48 + d) for d in range(lo, hi + 1)]
    g = []
    for i in range(r):
        row = random.choices(digits, k=c)
        for j in range(c):
            if (i + j) % 4 >= 2:
                row[j] = "#"
        g.append(row)
    for s in range(2, r + c - 1):
        if s % 4 < 2:
            continue
        t = s // 4
        i = max(0, s - (c - 1)) if t % 2 == 0 else min(r - 1, s)
        g[i][s - i] = random.choice(digits)
    return ["".join(x) for x in g]


def transpose(g):
    return ["".join(g[i][j] for i in range(len(g))) for j in range(len(g[0]))]


# samples
add(["19111", "19191", "11191"])
add(["5#1", "3#4"])
add(["1111", "###1", "1111", "1###", "1111"])
add(["7"])
add(["000", "000"])
add(["2#315", "41190", "3#2#6", "12843"])
# hidden: small
add(["9" * 20])
add(["3"] * 25)
add(rnd(5, 5, 0, 9, 0.3))
add(rnd(10, 12, 1, 9, 0.25))
add(maze(15, 21, 1, 9))
add(serpentine(17, 9, 0, 9))
add(maze(41, 41, 0, 9, "0", 5, 9))
add(diagonal(30, 28, 1, 9))
add(rnd(60, 60, 1, 9, 0.35))
# hidden: large
R = C = MAXR
add(rnd(R, C, 1, 9))
add(rnd(R, C, 0, 9, 0.35))
add(rnd(R, C, 1, 9, 0.2))
add(maze(999, 999, 1, 9))
add(maze(999, 999, 9, 9))
add(maze(999, 999, 0, 1, "9", 9, 9))            # walls are only expensive, not closed
add(serpentine(999, C, 1, 9))
add(transpose(serpentine(999, C, 0, 9)))
g = maze(999, 999, 1, 9)                       # closed exit
g[-1] = g[-1][:-2] + "#" + g[-1][-1]
g[-2] = g[-2][:-1] + "#"
add(g)
add(["5" * C] * R)                             # everything equal
add(diagonal(R, 999, 1, 9))                    # one long staircase corridor
add(transpose(diagonal(R, 999, 0, 9)))
add(diagonal(998, 1000, 9, 9))
add(maze(999, 999, 0, 9, "0", 3, 9))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
