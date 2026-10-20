# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(120801)
MAXR, MAXC = 14, 200000
tests = []
TO_HT = str.maketrans("01", "TH")


def add(rows):
    r, c = len(rows), len(rows[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC
    assert all(len(x) == c and set(x) <= set("HT") for x in rows)
    tests.append(f"{r} {c}\n" + "".join(x + "\n" for x in rows))


def rnd_rows(r, c):
    """every coin independently H or T"""
    return [format(random.getrandbits(c), "0%db" % c)[-c:].translate(TO_HT) for _ in range(r)]


def from_masks(r, masks):
    """column j is masks[j] (bit i = row i shows H)"""
    return ["".join("H" if m >> i & 1 else "T" for m in masks) for i in range(r)]


def biased_rows(r, c, p):
    return ["".join("H" if random.random() < p else "T" for _ in range(c)) for _ in range(r)]


def balanced_masks(r, c):
    """every column has r // 2 heads: flipping a column alone never helps"""
    out = []
    for _ in range(c):
        bits = random.sample(range(r), r // 2)
        out.append(sum(1 << b for b in bits))
    return out


def hidden_pattern(r, c, noise):
    """a hidden good pattern: each column is a random flip of one fixed column, plus noise"""
    base = random.getrandbits(r)
    full = (1 << r) - 1
    out = []
    for _ in range(c):
        m = base if random.random() < 0.5 else base ^ full
        for i in range(r):
            if random.random() < noise:
                m ^= 1 << i
        out.append(m)
    return out


# samples
add(["HTTH",
     "TTHT",
     "HHTH"])
add(["HT",
     "TT"])
add(["TTHTT"])
add(["T", "H", "T", "T"])
add(["HHHHHH", "HHHHHH"])
add(["THTHH",
     "HTHTT",
     "THHHT",
     "HTTHH"])
# hidden: small (the brute force tries every set of rows and columns)
add(["T"])
add(["H"])
add(rnd_rows(4, 6))
add(rnd_rows(5, 9))
add(rnd_rows(7, 13))
add(rnd_rows(10, 10))
add(from_masks(8, balanced_masks(8, 12)))
add(rnd_rows(14, 300))
add(from_masks(12, hidden_pattern(12, 2000, 0.15)))
# hidden: large
add(rnd_rows(MAXR, MAXC))
add(["T" * MAXC] * MAXR)
add(from_masks(MAXR, [random.randrange(1 << MAXR) for _ in range(MAXC)]))
add(from_masks(MAXR, hidden_pattern(MAXR, MAXC, 0.1)))
add(from_masks(MAXR, hidden_pattern(MAXR, MAXC, 0.3)))
add(from_masks(MAXR, balanced_masks(MAXR, MAXC)))
add(from_masks(MAXR, [m % (1 << MAXR) for m in range(MAXC)]))        # every column pattern, about 12 times each
add(biased_rows(MAXR, MAXC, 0.3))
add(["HT" * (MAXC // 2) if i % 2 == 0 else "TH" * (MAXC // 2) for i in range(MAXR)])   # chessboard
add(from_masks(MAXR, hidden_pattern(MAXR, MAXC, 0.2)))
add(rnd_rows(MAXR, MAXC))
add(from_masks(MAXR, [random.randrange(1 << MAXR) for _ in range(MAXC)]))
add(rnd_rows(1, MAXC))
add(rnd_rows(MAXR, 1))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
