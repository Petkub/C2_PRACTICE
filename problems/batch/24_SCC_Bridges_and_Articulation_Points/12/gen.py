# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import gc, os, random

random.seed(2412)
gc.disable()                    # millions of small tuples: no cyclic GC needed, much faster
rnd = random.random
MAXRC, SUMRC, SUMK = 100_000, 200_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(cases):
    """cases: list of (R, C, requests)"""
    assert 1 <= len(cases)
    assert sum(R + C for R, C, q in cases) <= SUMRC and sum(len(q) for R, C, q in cases) <= SUMK
    for R, C, q in cases:
        assert 1 <= R <= MAXRC and 1 <= C <= MAXRC and 1 <= len(q)
        assert all(1 <= a <= R and 1 <= c <= R and 1 <= b <= C and 1 <= d <= C and (a, b) != (c, d)
                   for a, b, c, d in q)
    tests.append(f"{len(cases)}\n" + "".join(f"{R} {C} {len(q)}\n" + "".join(f"{a} {b} {c} {d}\n" for a, b, c, d in q)
                                             for R, C, q in cases))


def point_pair(R, C, straight):
    while True:
        r1, c1, r2, c2 = ri(1, R), ri(1, C), ri(1, R), ri(1, C)
        u = random.random()
        if u < straight:
            r2 = r1
        elif u < 2 * straight:
            c2 = c1
        if (r1, c1) != (r2, c2):
            return r1, c1, r2, c2


def rand_case(R, C, K, straight=0.02):
    return R, C, [point_pair(R, C, straight) for _ in range(K)]


def ok(east, south, q):
    """does request q work with the directions east[r] (row r goes east) and south[c] (column c goes south)?"""
    r1, c1, r2, c2 = q
    row = lambda r: east[r] == (c2 > c1)
    col = lambda c: south[c] == (r2 > r1)
    if r1 == r2:
        return row(r1)
    if c1 == c2:
        return col(c1)
    return (row(r1) and col(c2)) or (col(c1) and row(r2))


def planted_case(R, C, K, straight=0.02, one_route=0.7):
    """random directions, then requests that these directions satisfy (YES); most of them by one route only"""
    east = [random.random() < 0.5 for _ in range(R + 1)]
    south = [random.random() < 0.5 for _ in range(C + 1)]
    q = []
    while len(q) < K:
        r1, c1, r2, c2 = point_pair(R, C, straight)
        if not ok(east, south, (r1, c1, r2, c2)):
            continue
        if r1 != r2 and c1 != c2 and random.random() < one_route:
            a = east[r1] == (c2 > c1) and south[c2] == (r2 > r1)
            b = south[c1] == (r2 > r1) and east[r2] == (c2 > c1)
            if a and b:
                continue
        q.append((r1, c1, r2, c2))
    return R, C, q, east, south


def spoil(case, k):
    """add k requests that the planted directions do not satisfy (the case usually becomes NO)"""
    R, C, q, east, south = case
    q = list(q)
    while k > 0:
        t = point_pair(R, C, 0.0)
        if not ok(east, south, t):
            q.insert(ri(0, len(q)), t)
            k -= 1
    return R, C, q


def chain(R, C, k):
    """2k + 2 requests that no directions satisfy: a staircase of k blocks, block i has east-west streets
    rows[i], rows[i + 1] and north-south streets cols[i], cols[i + 1]; the two diagonal requests of a block force
    a clockwise or anticlockwise loop around it, neighbouring blocks must turn opposite ways, and the two straight
    requests at the ends ask for the wrong parity"""
    rows = sorted(random.sample(range(1, R + 1), k + 1))
    cols = sorted(random.sample(range(1, C + 1), k + 1))
    q = []
    for i in range(k):
        q.append((rows[i], cols[i], rows[i + 1], cols[i + 1]))
        q.append((rows[i + 1], cols[i + 1], rows[i], cols[i]))
    q.append((rows[0], cols[0], rows[0], cols[1]))        # first row goes east: block 0 clockwise
    # block k-1 is clockwise when k is odd, and then its lower row goes west; ask for the opposite
    if k % 2 == 1:
        q.append((rows[k], cols[0], rows[k], cols[k]))    # east
    else:
        q.append((rows[k], cols[k], rows[k], cols[0]))    # west
    return q


def spoil_chain(case, k):
    R, C, q = case[:3]
    q = list(q)
    for t in chain(R, C, k):
        q.insert(ri(0, len(q)), t)
    return R, C, q


def plain(case):
    return case[:3]


def chain_of_turns(k, no=False):
    """a satisfiable case (or NO with no=True) where row 2 + i going east forces column 2 + i south, which forces
    row 3 + i east (through requests ending at (R, 2) and (2, C) whose other streets are fixed), and so on up to
    column k + 2, which must go north: rows 3, 4, ... all have to go west, but each one is found out only at the
    end of a long chain of forced streets"""
    R = C = k + 3
    q = [(1, 2, 1, 1), (2, 1, 1, 1), (2, 1, 2, 2), (2, C, 1, C), (R, 2, R, 1), (1, 2, 2, 2), (2, k + 2, 1, k + 2)]
    q += [(i + 2, i + 2, R, 2) for i in range(1, k + 1)]
    q += [(i + 3, i + 2, 2, C) for i in range(1, k)]
    if no:
        q.append((k + 2, 1, k + 2, 2))                    # the last row of the chain must go east: NO
    random.shuffle(q)
    return R, C, q


# samples
add([(2, 2, [(1, 1, 2, 2), (2, 2, 1, 1)]), (1, 3, [(1, 1, 1, 3), (1, 3, 1, 2)])])
add([(2, 2, [(1, 1, 2, 2), (2, 2, 1, 1), (1, 1, 1, 2), (2, 1, 2, 2)])])
add([(3, 3, [(1, 1, 3, 3), (3, 1, 1, 3), (2, 2, 2, 1)]), (2, 1, [(1, 1, 2, 1)])])
add([(4, 4, [(1, 1, 4, 4), (4, 4, 1, 1), (1, 4, 4, 1), (4, 1, 1, 4)])])
add([(1, 2, [(1, 1, 1, 2), (1, 2, 1, 1)]), (2, 2, [(1, 2, 2, 1)])])
# hidden: many tiny cases (brute force over all directions)
for sizes in ((2, 4), (3, 5), (4, 6)):
    cs = []
    for _ in range(300):
        R, C = ri(1, sizes[0]), ri(1, sizes[1])
        if R * C == 1:
            R = 2
        if random.random() < 0.5:
            cs.append(rand_case(R, C, ri(1, 3 + R + C)))
        else:
            cs.append(plain(planted_case(R, C, ri(1, 3 * (R + C)))))
    add(cs)
cs = []
for _ in range(200):
    R, C = ri(3, 10), ri(3, 10)
    cs.append(spoil(planted_case(R, C, ri(5, 25)), 1) if random.random() < 0.5 else plain(planted_case(R, C, ri(5, 30))))
add(cs)
# hidden: medium
cs = [rand_case(100, 100, k) for k in (30, 40, 50, 60, 70)] + [plain(planted_case(100, 100, 600))] + [spoil(planted_case(100, 100, 500), 1), spoil_chain(planted_case(100, 100, 300), 60)]
add(cs)
cs = [rand_case(1000, 1000, k) for k in range(400, 660, 50)] + [plain(planted_case(1000, 1000, 3000)) for _ in range(3)]
add(cs)
# hidden: maximum size (a file holds several big cases, so answering one word for all of them fails;
# each one has a long chain of forced streets)
K0 = 25_000
add([chain_of_turns(K0), plain(planted_case(37_000, 37_000, 25_000)),
     spoil_chain(planted_case(37_000, 37_000, 14_000), 4999)])
add([spoil_chain(planted_case(37_000, 37_000, 24_990), 4), chain_of_turns(K0, True),
     plain(planted_case(37_000, 37_000, 24_990))])
add([spoil_chain(planted_case(37_000, 37_000, 5000, 0.0, 1.0), 9999), plain(planted_case(37_000, 37_000, 24_990, 0.0, 1.0)),
     chain_of_turns(K0)])
add([rand_case(18_000, 18_000, k) for k in (2500, 3500, 4000, 4500)] + [chain_of_turns(K0)])
add([rand_case(14_000, 21_000, k) for k in (3000, 3800, 4600)] + [plain(planted_case(10_000, 10_000, 26_000)),
                                                                   chain_of_turns(K0, True)])
add([chain_of_turns(K0), plain(planted_case(1000, 73_000, 25_000, 0.1)), plain(planted_case(73_000, 1000, 24_990, 0.1))])
add([spoil_chain(planted_case(1000, 73_000, 24_000, 0.1), 499), chain_of_turns(K0, True),
     plain(planted_case(73_000, 1000, 24_990, 0.1))])
add([plain(planted_case(300, 300, 16_000, 0.0)), spoil_chain(planted_case(300, 300, 16_000, 0.0), 299),
     chain_of_turns(K0), plain(planted_case(74_000, 74_000, 17_000))])
add([rand_case(1, 2, 1), chain_of_turns(K0), rand_case(74_000, 75_000, 49_990)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
