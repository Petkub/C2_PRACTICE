# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7009)
MAXK, MAXF, MAXQ = 6, 100_000, 100_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def code(k, x):
    return str(x).zfill(k)


def add(k, s, banned, queries):
    f, q = len(banned), len(queries)
    assert 1 <= k <= MAXK and 1 <= f <= MAXF and 1 <= q <= MAXQ
    assert len(set(banned)) == f and s not in banned
    assert all(len(c) == k and c.isdigit() for c in [s] + banned + queries)
    tests.append(f"{k} {f} {q}\n{s}\n" + " ".join(banned) + "\n" + " ".join(queries) + "\n")


def rand_banned(k, f, s):
    total = 10 ** k
    if f > total // 2:
        pool = [x for x in range(total) if code(k, x) != s]
        random.shuffle(pool)
        return [code(k, x) for x in pool[:f]]
    got = set()
    while len(got) < f:
        x = ri(0, total - 1)
        if code(k, x) != s:
            got.add(x)
    res = sorted(got)
    random.shuffle(res)
    return [code(k, x) for x in res]


def rand_queries(k, q, banned_share=None):
    return [code(k, ri(0, 10 ** k - 1)) for _ in range(q)]


# samples
add(3, "000", ["555"], ["111", "190", "000"])
add(1, "0", ["1", "9"], ["5", "1", "0"])
add(2, "55", ["45", "65", "54", "56", "66"], ["57", "66"])
add(4, "1234", ["1233", "1235", "2345"], ["1243", "0000", "9999"])
add(5, "00000", ["11000", "99999", "01110"], ["55555", "13579"])
add(2, "09", ["08", "00", "19", "99", "10", "98"], ["09", "00", "77"])
# hidden: small and medium (every answer checked by brute force)
add(1, "7", ["0"], [code(1, x) for x in range(10)])
add(1, "3", ["5"], [code(1, x) for x in range(10)])
add(2, "00", rand_banned(2, 30, "00"), [code(2, x) for x in range(100)])
add(2, "38", rand_banned(2, 60, "38"), [code(2, x) for x in range(100)])
add(3, "500", ["499"], rand_queries(3, 200))
add(3, "123", rand_banned(3, 400, "123"), rand_queries(3, 500))
add(3, "999", rand_banned(3, 700, "999"), rand_queries(3, 500))
add(4, "0000", rand_banned(4, 3000, "0000"), rand_queries(4, 3000))
add(4, "4826", rand_banned(4, 5500, "4826"), rand_queries(4, 3000))
wall = [code(4, x) for x in range(10 ** 4) if code(4, x)[1] == "5" and x % 97 != 0]
add(4, "3333", wall, rand_queries(4, 3000))
add(5, "12345", rand_banned(5, 20000, "12345"), rand_queries(5, 10000))
# hidden: large
add(6, "000000", ["999999"], rand_queries(6, MAXQ))
add(6, "135792", rand_banned(6, MAXF, "135792"), rand_queries(6, MAXQ))
add(6, "000000", [code(6, x) for x in range(1, MAXF + 1)], rand_queries(6, MAXQ))   # 000001..100000 banned
wall = [code(6, x) for x in range(5 * 10 ** 5, 6 * 10 ** 5)]                         # leftmost wheel never shows 5
random.shuffle(wall)
add(6, "300000", wall, rand_queries(6, MAXQ))
wall = [code(6, x) for x in range(10 ** 6) if code(6, x)[2:4] == "55"][:MAXF]        # wheels 3 and 4 never both 5
add(6, "414141", wall, rand_queries(6, MAXQ))
ball = []                                                                            # a shell around the start
for x in range(10 ** 6):
    c = code(6, x)
    if sum(min(int(a), 10 - int(a)) for a in c) == 3:
        ball.append(c)
s = "000000"
ball = [c for c in ball if c != s][:MAXF]
add(6, s, ball, rand_queries(6, MAXQ))
add(5, "00000", rand_banned(5, 50000, "00000"), rand_queries(5, MAXQ))               # many unreachable codes
add(5, "55555", rand_banned(5, 30000, "55555"), rand_queries(5, MAXQ))
add(5, "24680", rand_banned(5, 60000, "24680"), [code(5, x) for x in range(MAXQ)])
add(6, "999999", rand_banned(6, MAXF, "999999"), [code(6, ri(0, 10 ** 6 - 1)) for _ in range(MAXQ)])
add(6, "505050", rand_banned(6, 1, "505050"), ["050505"] * MAXQ)
add(6, "000000", [code(6, x) for x in range(10 ** 5, 2 * 10 ** 5)],                  # leftmost wheel never shows 1
    rand_queries(6, MAXQ))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
