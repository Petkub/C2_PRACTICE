# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(951277)
MAXL, MAXQ, MAXI, MAXJ = 200_000, 100_000, 100_000, 1000
KEEP = 1100
EXACT = 60                      # terms 1..EXACT are simulated here (prefixes), later terms only grow
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def step(cur, whole, keep=KEEP):
    """the next term's first `keep` digits from the first digits `cur` of a term (whole = cur is the whole term)"""
    out, n, i = [], len(cur), 0
    size = 0
    while i < n and size < keep:
        j = i
        c = cur[i]
        while j < n and cur[j] == c:
            j += 1
        if j == n and not whole:
            break
        piece = str(j - i) + c
        out.append(piece)
        size += len(piece)
        i = j
    nxt = "".join(out)
    nwhole = whole and i == n and len(nxt) <= keep
    return nxt[:keep], nwhole


def lengths(x1, upto):
    """known[t] = a lower bound on |x_t| that is exact when the term is short (t = 1..upto)"""
    known = [0, len(x1)]
    cur, whole = x1, True
    for t in range(2, upto + 1):
        # x_2..x_4 may have long blocks: keep many digits there (a lower bound is all that is needed)
        cur, whole = step(cur, whole, 30_000 if t <= 4 else KEEP)
        assert whole or len(cur) >= MAXJ
        known.append(len(cur) if whole else 10**9)
    return known


def add_raw(x1, qs):
    assert 1 <= len(x1) <= MAXL and all(c in "0123456789" for c in x1)
    assert 1 <= len(qs) <= MAXQ
    known = lengths(x1, min(EXACT, max(i for i, _ in qs)))
    for i, j in qs:
        assert 1 <= i <= MAXI and 1 <= j <= MAXJ
        if x1 == "22":                                     # every term is 22
            assert j <= 2
        elif i < len(known):
            assert j <= known[i]
        else:
            assert x1 != "22" and known[EXACT] >= MAXJ     # terms do not get shorter from x_3 on
    tests.append(x1 + "\n" + str(len(qs)) + "\n" + "".join(f"{i} {j}\n" for i, j in qs))


def add(x1, q, small=0.3, mid=0.2, top=0.05):
    """q random questions: a share with small i (1..12), with i up to EXACT, with i = MAXI, the rest any i"""
    known = lengths(x1, EXACT)
    grows = x1 != "22" and known[EXACT] >= MAXJ
    qs = []
    for _ in range(q):
        r = random.random()
        if r < small:
            i = ri(1, 12)
        elif r < small + mid or not grows:
            i = ri(1, EXACT)
        elif r < small + mid + top:
            i = MAXI
        else:
            i = ri(EXACT + 1, MAXI)
        lim = min(MAXJ, known[i]) if i <= EXACT else MAXJ
        qs.append((i, ri(1, lim)))
    add_raw(x1, qs)


def digits(n, alphabet="0123456789"):
    return "".join(random.choice(alphabet) for _ in range(n))


def blocks(n, lens, alphabet="0123456789"):
    """n digits made of blocks whose lengths come from `lens`, neighbouring blocks with different digits"""
    out, size, last = [], 0, ""
    while size < n:
        c = random.choice([d for d in alphabet if d != last] or alphabet)
        k = min(random.choice(lens), n - size)
        out.append(c * k)
        size += k
        last = c
    return "".join(out)


def long_block(head, run, tail):
    """`head` random digits, one block of `run` equal digits, then `tail` random digits"""
    h = digits(head)
    c = random.choice([d for d in "0123456789" if not h or d != h[-1]])
    t = digits(tail)
    while t and t[0] == c:
        t = random.choice([d for d in "0123456789" if d != c]) + t[1:]
    return h + c * run + t


# samples
add_raw("1", [(4, 2), (5, 4), (6, 1)])
add_raw("3322251", [(2, 3), (3, 5)])
add_raw("22", [(100000, 2)])
add_raw("0", [(2, 1), (3, 3), (4, 1)])
add_raw("9999999", [(3, 2), (50, 1), (1, 7)])
add_raw("12", [(1000, 1000), (99999, 1)])
# hidden: small (few questions)
add("1", 50, 0.3, 0.3)
add("7", 50, 0.3, 0.3)
add("22", 30, 0.5, 0.5)
add(digits(8), 100, 0.3, 0.3)
add(blocks(40, [1, 2, 3, 10, 12]), 200, 0.4, 0.3)
add(long_block(5, 25, 5), 200, 0.4, 0.3)
add(blocks(300, [1, 1, 2, 3]), 300, 0.3, 0.3)
add(long_block(30, 2000, 30), 300, 0.4, 0.3)
add(long_block(3, 20000, 3), 300, 0.4, 0.3)
add(blocks(5000, [1, 2, 3, 10, 11, 12, 300]), 300, 0.4, 0.3)
# hidden: maximum size
Q = MAXQ
add(digits(MAXL), Q)
add(blocks(MAXL, [1, 2, 3], "123"), Q)
add(MAXL * "5", Q)
add(long_block(400, MAXL - 800, 400), Q)
add(long_block(37, 150_000, MAXL - 150_037), Q)
add(blocks(MAXL, [10, 11, 12, 15, 99, 100, 150]), Q)
add(blocks(MAXL, [1, 2, 3, 9, 10, 11, 1000, 5000]), Q)
add(long_block(120, 999, MAXL - 1119), Q)
add(blocks(MAXL, [1, 2, 3, 4, 5, 6, 7, 8, 9]), Q, 0.1, 0.1, 0.4)
add("1" + "2" * (MAXL - 2) + "1", Q)
add(long_block(0, MAXL // 2, MAXL // 2), Q)
add(blocks(MAXL, [100_000]), Q)
# x_2 with long blocks: a block of 111 ones gives 1111, of 111 twos gives 1112, ...
add_raw(("1" * 111 + "2" * 111) * 450, [(4, 1000), (3, 1000), (5, 1000), (2, 1000), (100000, 1000)]
        + [(ri(2, 8), ri(1, MAXJ)) for _ in range(5000)])
add(("1" * 1111 + "2" * 1111) * 90, Q, 0.5, 0.2)
add(("1" * 11111 + "3" * 11111) * 9, Q, 0.5, 0.2)
add("".join(random.choice(["1" * 111, "2" * 111, "1" * 11, "3" * 1111, "2" * 22, "1" * 1]) for _ in range(1500))[:MAXL], Q, 0.5, 0.2)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
