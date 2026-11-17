# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(30603)
MAXS, MAXRC = 3000, 3_000_000
tests = []

def add(g):
    R, C = len(g), len(g[0])
    assert 1 <= R <= MAXS and 1 <= C <= MAXS and R * C <= MAXRC
    assert all(len(row) == C and all(ch in "0123456789" for ch in row) for row in g)
    tests.append(f"{R} {C}\n" + "\n".join(g) + "\n")

def cart():
    return str(random.randint(1, 9))

def row_with_empties(C, k, heavy=False):
    """C cells, exactly k empty cells at random places, carts elsewhere."""
    pos = set(random.sample(range(C), k)) if k else set()
    if heavy:
        return "".join("0" if j in pos else random.choice("789") for j in range(C))
    return "".join("0" if j in pos else cart() for j in range(C))

def row_density(C, p):
    return "".join("0" if random.random() < p else cart() for _ in range(C))

def row_graded(C, k):
    """heavy carts on one side of the row, light ones on the other: the nearer empty cell is often the heavier way"""
    pos = set(random.sample(range(C), k))
    flip = random.random() < 0.5
    out = []
    for j in range(C):
        if j in pos:
            out.append("0")
        else:
            heavy = (j < C // 2) != flip
            out.append(random.choice("89") if heavy else "1")
    return "".join(out)

def row_ends(C):
    """empty cells only at one or both ends: walking to the nearest empty cell is long"""
    s = [cart() for _ in range(C)]
    t = random.randint(0, 2)
    if t in (0, 2): s[0] = "0"
    if t in (1, 2): s[-1] = "0"
    return "".join(s)

def answer(g, mode):
    """reference (used only to pick trap grids): mode "ok", "nearer" (wrong side rule) or "wall" (edge = empty)"""
    C = len(g[0])
    tot = [0] * C
    for row in g:
        for j in range(C):
            if row[j] == "0" or tot[j] is None:
                continue
            L = j
            while L >= 0 and row[L] != "0": L -= 1
            Rt = j
            while Rt < C and row[Rt] != "0": Rt += 1
            a = sum(map(int, row[L + 1:j + 1])) if (L >= 0 or mode == "wall") else None
            b = sum(map(int, row[j:Rt])) if (Rt < C or mode == "wall") else None
            if "0" not in row: a = b = None
            if mode == "nearer" and a is not None and b is not None:
                c = a if j - L <= Rt - j else b
            else:
                c = min(x for x in (a, b, 10 ** 9) if x is not None)
            tot[j] = None if c == 10 ** 9 else tot[j] + c
    best = min((t, j + 1) for j, t in enumerate(tot) if t is not None) if any(t is not None for t in tot) else -1
    return best

def trap(R, C, kind):
    while True:
        g = [row_density(C, 0.25) for _ in range(R)]
        ok = answer(g, "ok")
        if ok == -1:
            continue
        if kind in ("nearer", "both") and answer(g, "nearer") == ok:
            continue
        if kind in ("wall", "both") and answer(g, "wall") == ok:
            continue
        return g

# samples
add(["10230", "02104", "31020"])
add(["1203", "1111"])
add(["1102", "2301", "0405"])
add(["101", "010"])
add(["293057", "298300", "700155", "162600"])
# hidden: small and special
add(["0"])
add(["7"])
add(["9" * 10 + "0", "0" + "1" * 10])        # only one side is possible in each row
add(trap(3, 8, "nearer"))                   # the nearer empty cell is on the heavier side
add(trap(4, 7, "wall"))                     # pushing over the edge would be cheaper
add(trap(5, 10, "both"))
add([row_density(12, 0.3) for _ in range(9)])
add([row_with_empties(40, random.randint(1, 3)) for _ in range(30)])
add([row_density(200, 0.05) for _ in range(150)])
add([row_with_empties(300, 2) for _ in range(299)] + ["9" * 300])   # one full row
add([row_with_empties(1, 1) if random.random() < 0.5 else "0" for _ in range(500)])
add([row_with_empties(250, 1, heavy=True) for _ in range(400)])
# hidden: maximum size (few empty cells per row)
add([row_ends(3000) for _ in range(1000)])
add([row_with_empties(3000, 1) for _ in range(1000)])
add([row_graded(3000, random.randint(2, 3)) for _ in range(1000)])
add([row_ends(3000) for _ in range(999)] + ["5" * 3000])          # last row full: -1
add([row_graded(2000, 2) for _ in range(1500)])
add([random.choice(["0" + "9" * 2999, "9" * 2999 + "0"]) for _ in range(1000)])   # carts pushed far, weights 9
add([row_with_empties(2500, 2) for _ in range(1200)])
add([row_ends(2000) for _ in range(1500)])
add([row_with_empties(3000, 1, heavy=True) for _ in range(1000)])
add([row_graded(3000, 1) for _ in range(1000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
