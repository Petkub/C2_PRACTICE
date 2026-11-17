# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(131602)
MAXN = 18
MAXT = 10_000
MAXTOTAL = 300_000
LET = "abcdefghijklmnopqrstuvwxyz"
tests = []


def add(cases):
    assert 1 <= len(cases) <= MAXT
    total = 0
    for n, s in cases:
        assert 0 <= n <= MAXN and len(s) == 1 << n and set(s) <= set(LET)
        total += len(s)
    assert total <= MAXTOTAL
    tests.append(f"{len(cases)}\n" + "".join(f"{n} {s}\n" for n, s in cases))


def rnd(n, letters):
    return "".join(random.choice(letters) for _ in range(1 << n))


def good(n, c=0):
    """a random c-good string of length 2^n (as a list of letters)"""
    if n == 0:
        return [LET[c]]
    half = 1 << (n - 1)
    rest = good(n - 1, c + 1)
    if random.random() < 0.5:
        return [LET[c]] * half + rest
    return rest + [LET[c]] * half


def noisy(n, p, letters=LET[:20]):
    """an a-good string with each letter replaced with probability p"""
    g = good(n)
    for i in range(len(g)):
        if random.random() < p:
            g[i] = random.choice(letters)
    return "".join(g)


def decoy(n, p):
    """a noisy good string whose other halves are filled with many copies of their letter
    (choosing the half that already looks right is not always best)"""
    g = good(n)
    l, r, c = 0, len(g), 0
    while r - l > 1:
        mid = (l + r) // 2
        side_all_c = all(x == LET[c] for x in g[l:mid])
        # put c into about 40-70% of the half that is c-good below this level
        lo, hi = (mid, r) if side_all_c else (l, mid)
        for i in range(lo, hi):
            if random.random() < random.uniform(0.4, 0.7):
                g[i] = LET[c]
        if side_all_c:
            l = mid
        else:
            r = mid
        c += 1
    for i in range(len(g)):
        if random.random() < p:
            g[i] = random.choice(LET[:6])
    return "".join(g)


# samples
add([(3, "abaabbdd"), (2, "bcaa")])
add([(1, "ba"), (0, "z")])
add([(3, "dcbbaaba")])
add([(4, "aaaaaaaabbbbccde"), (4, "bbbbbbbbaaaaaaaa")])
add([(0, "a"), (1, "aa"), (2, "cbaa"), (2, "abcd"), (3, "zzzzzzzz"), (3, "abababab"), (3, "aaaaaaab")])
# hidden: small (the brute force tries every a-good string)
add([(n, rnd(n, "ab")) for n in range(0, 5) for _ in range(40)])
add([(n, rnd(n, "abc")) for n in range(1, 8) for _ in range(30)])
add([(n, rnd(n, "abcdefg")) for n in range(3, 10) for _ in range(10)])
add([(n, noisy(n, 0.2)) for n in range(1, 11) for _ in range(8)])
add([(n, decoy(n, 0.05)) for n in range(2, 12) for _ in range(5)])
add([(n, "".join(good(n))) for n in range(0, 12)])
add([(12, rnd(12, LET)), (12, "a" * 4096), (12, "z" * 4096), (12, noisy(12, 0.5)), (12, decoy(12, 0.1))])
add([(13, decoy(13, 0.02)), (13, noisy(13, 0.1)), (12, rnd(12, "ab"))])
# hidden: large
add([(MAXN, rnd(MAXN, LET))])
add([(MAXN, rnd(MAXN, "ab"))])
add([(MAXN, noisy(MAXN, 0.1))])
add([(MAXN, noisy(MAXN, 0.4))])
add([(MAXN, decoy(MAXN, 0.01))])
add([(MAXN, decoy(MAXN, 0.05))])
add([(MAXN, "".join(good(MAXN)))])
add([(MAXN, "z" * (1 << MAXN))])
add([(MAXN, "a" * (1 << MAXN))])
add([(MAXN, decoy(MAXN, 0.0))] + [(n, decoy(n, 0.03)) for n in range(1, 15)])
add([(MAXN, noisy(MAXN, 0.02))] + [(15, noisy(15, 0.2)) for _ in range(1)])
add([(17, decoy(17, 0.02)), (17, rnd(17, "abcd"))] + [(n, rnd(n, "abc")) for n in range(15)])
add([(MAXN, rnd(MAXN, "abcdefghijklmnopqrs"))])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
