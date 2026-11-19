# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(47002)
MAXR = MAXC = 1000
tests = []


def add(rows):
    R, C = len(rows), len(rows[0])
    assert 1 <= R <= MAXR and 1 <= C <= MAXC
    assert all(len(r) == C and all(ch == '*' or ch.isdigit() for ch in r) for r in rows)
    assert rows[0][0] != '*' and rows[-1][-1] != '*'
    tests.append(f"{R} {C}\n" + "".join(r + "\n" for r in rows))


def fix_ends(g):
    if g[0][0] == '*':
        g[0][0] = str(random.randint(0, 9))
    if g[-1][-1] == '*':
        g[-1][-1] = str(random.randint(0, 9))
    return ["".join(r) for r in g]


def rnd(R, C, p, lo=0, hi=9):
    return fix_ends([['*' if random.random() < p else str(random.randint(lo, hi)) for _ in range(C)] for _ in range(R)])


def seeded(R, C, p, seed):
    rg = random.Random(seed)
    g = [['*' if rg.random() < p else str(rg.randint(0, 9)) for _ in range(C)] for _ in range(R)]
    if g[0][0] == '*':
        g[0][0] = str(rg.randint(0, 9))
    if g[-1][-1] == '*':
        g[-1][-1] = str(rg.randint(0, 9))
    return ["".join(r) for r in g]


def traps(R, C, p):
    g = [['*' if random.random() < p else str(random.randint(0, 3)) for _ in range(C)] for _ in range(R)]
    for _ in range(R * C // 6):
        r, c = random.randrange(R), random.randrange(C)
        g[r][c] = '9'
        if c + 1 < C and random.random() < 0.5:
            g[r][c + 1] = '*'
        if r + 1 < R and random.random() < 0.5:
            g[r + 1][c] = '*'
    return fix_ends(g)


def stripes(R, C):
    g = [[str(random.randint(0, 2)) for _ in range(C)] for _ in range(R)]
    for r in range(R):
        for c in range(C):
            if (r % 7 == 3 and c % 11 != 0) or (c % 5 == 2 and r % 13 != 0):
                g[r][c] = '*'
            elif r % 7 == 4 or c % 5 == 3:
                g[r][c] = '9' if random.random() < 0.6 else g[r][c]
    return fix_ends(g)


def closed(R, C, p):
    g = [['*' if random.random() < p else str(random.randint(0, 9)) for _ in range(C)] for _ in range(R)]
    for c in range(C):
        g[R - 1][c] = '*'
    for r in range(R):
        g[r][C - 1] = '*'
    g[R - 1][C - 1] = '5'
    return fix_ends(g)


add(["0*71", "69*3", "6*44"])
add(["12*", "3**", "**4"])
add(["7"])
add(["3*2**4"])
add(["6*8*9", "****5", "7**04", "*8883"])

add(["5", "*", "*", "2"])
add(["1*", "*1"])
add(["9*9", "9*9", "*99"])
add(seeded(5, 6, 0.35, 16))
add(seeded(7, 7, 0.4, 3))
add(traps(6, 6, 0.25))
add(seeded(8, 10, 0.35, 7))
add(seeded(8, 10, 0.35, 12))
add(rnd(10, 12, 0.35))
add(closed(6, 7, 0.2))

add(traps(60, 80, 0.3))
add(rnd(200, 150, 0.45))
add(stripes(300, 300))

add(rnd(MAXR, MAXC, 0.3))
add(rnd(MAXR, MAXC, 0.5))
add(traps(MAXR, MAXC, 0.25))
add(traps(MAXR, MAXC, 0.35))
add(stripes(MAXR, MAXC))
add(closed(MAXR, MAXC, 0.1))
add(rnd(MAXR, MAXC, 0.0, 9, 9))
add(rnd(MAXR, MAXC // 2, 0.4))
add(traps(MAXR // 2, MAXC, 0.45))
add(traps(1, MAXC, 0.4))
add(traps(MAXR, 1, 0.4))
add(traps(MAXR, MAXC, 0.6))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
