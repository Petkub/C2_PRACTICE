# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(91301)
MAXN, MAXK, MAXL, MAXCH = 100_000, 200_000, 20, 2_000_000
OK = set("abcdefghijklmnopqrstuvwxyz0123456789@.")
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(accs):
    n = len(accs)
    assert 1 <= n <= MAXN and all(len(a) >= 1 for a in accs)
    assert sum(len(a) for a in accs) <= MAXK
    assert sum(len(e) for a in accs for e in a) <= MAXCH
    assert all(1 <= len(e) <= MAXL and set(e) <= OK for a in accs for e in a)
    tests.append(f"{n}\n" + "".join(f"{len(a)} " + " ".join(a) + "\n" for a in accs))


DOMS = ["a.com", "m.th", "x.co", "p.net", "ac.th", "q.org"]
LET = "abcdefghijklmnopqrstuvwxyz0123456789"


def email(i, long=False):
    """a different address for every i"""
    s, x = "", i + 1
    while x:
        s += LET[x % 36]
        x //= 36
    if long:
        return (s + ".abcdefgh")[:13] + "@" + DOMS[0]
    return s + "@" + DOMS[i % len(DOMS)]


def shuffled(accs):
    accs = [list(a) for a in accs]
    for a in accs:
        random.shuffle(a)
    random.shuffle(accs)
    return accs


def from_pool(n, total, pool, long=False):
    """every account takes random addresses from a pool"""
    ks = [1] * n
    for _ in range(total - n):
        ks[ri(0, n - 1)] += 1
    return [[email(ri(0, pool - 1), long) for _ in range(k)] for k in ks]


# samples
add([["ann@a.com", "ann.k@b.org"], ["bob@a.com"], ["ann.k@b.org", "kk@c.net"], ["kk@c.net"]])
add([["a@x"], ["b@x"], ["b@x", "a@x"]])
add([["p@q", "p@q", "r@s"], ["t@u"]])
add([["m1@y.th"], ["m2@y.th"], ["m3@y.th", "m1@y.th"], ["m4@y.th"], ["m2@y.th", "m4@y.th"]])
add([["z@z"], ["c@c", "d@d"], ["e@e"], ["d@d", "e@e"], ["z@z", "f@f"], ["f@f", "g@g"]])
# hidden: small
add([["x"]])
add([["a@b"], ["a@b"]])
add(from_pool(8, 14, 10))
add(from_pool(30, 50, 40))
add(from_pool(200, 400, 300))
add(shuffled([[email(i), email(i + 1)] for i in range(500)]))
add(from_pool(2000, 3000, 2500))
# hidden: maximum size
N, K = MAXN, MAXK
add([[email(0), email(i + 1)] for i in range(N)])               # one address in every account
add([[email(i + 1), email(0)] for i in range(N)])
add([[email(i), email(i + 1)] for i in range(N)])               # a chain 1-2-3-...
add([[email(i), email(i + 1)] for i in range(N)][::-1])
add(shuffled([[email(i), email(i + 1)] for i in range(N)]))
add([[email(i)] * 2 for i in range(N)])                         # nobody shares: N persons
add(from_pool(N, K, N))                                         # one big person and many small ones
add(from_pool(N, K, 3 * N))
add(from_pool(N // 2, K // 2, 200_000, long=True))              # long addresses
accs = []                                                       # 20 persons, accounts interleaved
for i in range(N):
    g = i % 20
    accs.append([email(10**6 + g), email(i)] if random.random() < 0.5 else [email(i), email(10**6 + g)])
add(accs)
add([[email(ri(0, 29))] for _ in range(N)])                     # one address each, from 30 addresses
accs = [[email(5 * (i // 5) + j) for j in range(2)] for i in range(N)]   # groups of five neighbours
add(shuffled(accs))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
