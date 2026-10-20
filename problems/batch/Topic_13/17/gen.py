# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(131703)
MAXT = 10_000
MAXN = 10**18
tests = []


def add(cases):
    assert 1 <= len(cases) <= MAXT
    for n, s, x, p in cases:
        assert 0 <= n <= MAXN
        assert 1 <= len(s) <= 50 and 1 <= len(x) <= 50 and 1 <= len(p) <= 20
        assert all("a" <= ch <= "z" for ch in s + x + p)
    tests.append(f"{len(cases)}\n" + "".join(f"{n} {s} {x} {p}\n" for n, s, x, p in cases))


def word(lo, hi, al):
    return "".join(random.choice(al) for _ in range(random.randint(lo, hi)))


def build(s, x, k):
    for _ in range(k):
        s = s + x + s
        if len(s) > 5000:
            break
    return s


def case(nlo, nhi, slen, xlen, al, sub=0.7):
    """random case; with probability sub the pattern is a piece of S_k for a small k,
    often one that covers a copy of X (so that it crosses the middle)"""
    s = word(1, slen, al)
    x = word(1, xlen, al)
    n = random.randint(nlo, nhi)
    if random.random() < sub:
        t = build(s, x, random.randint(1, 6))
        m = random.randint(1, min(20, len(t)))
        if random.random() < 0.5 and len(t) > len(s) + len(x):
            # around the first copy of X
            c = len(s) + random.randint(0, len(x) - 1)
            i = max(0, min(len(t) - m, c - random.randint(0, m - 1)))
        else:
            i = random.randint(0, len(t) - m)
        p = t[i:i + m]
    else:
        p = word(1, 20, al)
    return (n, s, x, p)


def brute_cost(c):
    n, s, x, p = c
    return (2 ** n) * (len(s) + len(x)) * len(p) if n < 40 else 10**18


def small_file(cnt, nmax, slen, xlen, al, budget=3 * 10**7):
    cases, used = [], 0
    while len(cases) < cnt:
        c = case(0, nmax, slen, xlen, al)
        if used + brute_cost(c) <= budget:
            cases.append(c)
            used += brute_cost(c)
    return cases


# samples
add([(2, "ab", "a", "aba"), (1, "aaa", "aa", "aaaa")])
add([(0, "abc", "x", "abc"), (3, "a", "b", "aba")])
add([(10**18, "ab", "a", "aba"), (10**18, "z", "z", "zzzzzzzzzzzzzzzzzzzz"), (999_999_999_999, "abc", "d", "cda")])
add([(5, "ab", "c", "ca"), (0, "a", "a", "aa"), (7, "cat", "s", "tsc"), (60, "xyz", "x", "yx")])
add([(4, "ba", "ab", "bab"), (6, "a", "aa", "aaaaaaa"), (50, "hello", "o", "oo"), (1, "pq", "rs", "qrsp"),
     (2, "abc", "abc", "cabca"), (3, "a", "b", "babab")])
# hidden: small n (the brute force builds S_n)
add([(n, s, x, p) for n in range(0, 5) for s in ("a", "b", "ab") for x in ("a", "b", "ba")
     for p in ("a", "ab", "aba", "bab", "aaa", "abba", "aabaa", "abaabaaba")])
add(small_file(400, 8, 2, 2, "ab"))
add(small_file(400, 9, 4, 3, "ab"))
add(small_file(400, 10, 1, 1, "ab"))
add(small_file(300, 7, 10, 10, "abc"))
add(small_file(200, 6, 50, 50, "ab"))
add(small_file(300, 12, 3, 5, "a"))
add([case(0, 3, 50, 50, "abcdefghijklmnopqrstuvwxyz") for _ in range(300)])
add([(n, "a", "b", ("ab" * 10)[:m]) for n in range(0, 13) for m in range(1, 21)])
add(small_file(30, 21, 1, 1, "ab", budget=4 * 10**8))
# hidden: large (n up to 10^18)
add([case(0, MAXN, 50, 50, "ab") for _ in range(MAXT)])
add([case(10**17, MAXN, 3, 3, "ab") for _ in range(MAXT)])
add([case(10**9, MAXN, 1, 1, "ab") for _ in range(MAXT)])
add([case(60, MAXN, 10, 5, "abc") for _ in range(MAXT)])
add([case(0, 70, 2, 2, "ab") for _ in range(MAXT)])
add([case(0, MAXN, 50, 50, "abcdefghijklmnopqrstuvwxyz", sub=0.9) for _ in range(MAXT)])
add([(MAXN - random.randint(0, 100), word(1, 50, "a"), word(1, 50, "a"), word(1, 20, "a")) for _ in range(MAXT)])
add([(random.randint(0, MAXN), "a" * 50, "a" * 50, "a" * 20) for _ in range(MAXT)])
add([(MAXN, "z" * 50, "z" * 50, "z" * random.randint(1, 20)) for _ in range(MAXT)])
add([case(MAXN // 2, MAXN, 1, 50, "ab") for _ in range(MAXT)])
add([case(MAXN // 2, MAXN, 50, 1, "ab") for _ in range(MAXT)])
add([case(25, 64, 4, 4, "ab") for _ in range(MAXT)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
