# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(70019)
MAXN = MAXM = 200_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    """random order of the list a, in place (faster than random.shuffle for long lists)"""
    keys = [random.random() for _ in a]
    a[:] = [a[i] for i in sorted(range(len(a)), key=keys.__getitem__)]


def add(n, facts):
    m = len(facts)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    A, B = [a for a, _ in facts], [b for _, b in facts]
    assert m == 0 or (min(A) >= 1 and max(A) <= n and min(B) >= 1 and max(B) <= n)
    assert all(map(int.__ne__, A, B))
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in facts))


def forward(p, cnt, near, ban=-1):
    """`cnt` random facts that agree with the order p (pairs at most `near` places apart when near > 0),
    never the chain fact p[ban] before p[ban + 1]"""
    n = len(p)
    rnd = random.random
    res = []
    while len(res) < cnt:
        I = [int(rnd() * (n - 1)) for _ in range(cnt - len(res))]
        if near:
            J = [i + 1 + int(rnd() * min(near, n - 1 - i)) for i in I]
        else:
            J = [i + 1 + int(rnd() * (n - 1 - i)) for i in I]
        res += [(p[i], p[j]) for i, j in zip(I, J) if not (i == ban and j == i + 1)]
    return res


def chain(p, skip=None):
    """the facts p[i] before p[i+1] (without the one at index skip)"""
    return [(p[i], p[i + 1]) for i in range(len(p) - 1) if i != skip]


def unique_at(n, m, at, near=0, tail_bad=False):
    """exactly one order is known first after fact number `at` (the last chain fact goes there)"""
    assert n - 1 <= at <= m
    p = list(range(1, n + 1))
    shuffle(p)
    last = ri(0, n - 2)
    ch = chain(p, last)
    before = ch + forward(p, at - 1 - len(ch), near, last)
    shuffle(before)
    after = forward(p, m - at, near)
    if tail_bad and after:
        i = ri(0, n - 2)
        j = ri(i + 1, n - 1)
        after[ri(0, len(after) - 1)] = (p[j], p[i])   # a contradiction later on does not matter
    return n, before + [(p[last], p[last + 1])] + after


def impossible_at(n, m, at, cycle_len, near=0):
    """the chain misses one fact (so several orders stay possible) and fact `at` closes a cycle"""
    assert n - 1 <= at <= m
    p = list(range(1, n + 1))
    shuffle(p)
    # a stretch p[i..j] that is reversed at fact `at`; the missing chain fact lies outside it
    i = ri(0, n - 1 - cycle_len)
    j = i + cycle_len
    miss = random.choice([x for x in (ri(0, i - 1) if i > 0 else -1, ri(j, n - 2) if j <= n - 2 else -1) if x >= 0])
    ch = chain(p, miss)
    before = ch + forward(p, at - 1 - len(ch), near, miss)
    shuffle(before)
    after = forward(p, m - at, near, miss)
    return n, before + [(p[j], p[i])] + after


def ambiguous(n, m, near=0):
    p = list(range(1, n + 1))
    shuffle(p)
    miss = ri(0, n - 2)
    facts = chain(p, miss) + forward(p, m - (n - 2), near, miss)
    shuffle(facts)
    return n, facts


# samples
add(4, [(3, 1), (4, 2), (1, 4), (2, 3), (3, 2)])
add(4, [(1, 2), (2, 3), (3, 1), (4, 1)])
add(3, [(1, 2), (1, 3)])
add(1, [])
add(5, [(2, 5), (4, 1), (2, 5), (5, 4), (3, 2), (1, 3), (3, 4)])
add(6, [(6, 1), (2, 3), (1, 2), (5, 1), (3, 4), (4, 1), (5, 6)])
# hidden: small (every order is tried)
add(2, [(2, 1)])
add(3, [(2, 3), (2, 3), (1, 2), (3, 1)])
add(3, [(1, 2), (2, 1), (1, 3), (3, 2)])
add(5, [])
add(*unique_at(6, 12, 9, tail_bad=True))
add(*unique_at(8, 20, 7))
add(*impossible_at(7, 15, 10, 3))
add(*impossible_at(8, 25, 18, 2))
add(*ambiguous(8, 30))
add(*unique_at(300, 2000, 1500, near=3))
add(*impossible_at(500, 3000, 2500, 120))
# hidden: large
N, M = MAXN, MAXM
add(*unique_at(N // 2, M, M))                      # known only with the very last fact
add(*unique_at(N // 2, M, M // 2 + 7, near=5, tail_bad=True))
add(*unique_at(N // 2, M, N // 2 + 1, near=50))    # known as early as possible
add(*unique_at(N * 3 // 4, M, N * 3 // 4 - 1))     # the chain comes first
add(*unique_at(N // 4, M, M * 3 // 4))
add(*impossible_at(N // 2, M, M * 2 // 3, N // 2 - 2))
add(*impossible_at(N // 2, M, M // 2, 1, near=10))
add(*impossible_at(N // 4, M, M * 2 // 5, 1000))
add(*ambiguous(N // 2, M))
add(*ambiguous(N, M, near=3))
add(*impossible_at(N // 4, M, M // 3, 2, near=3))
p = list(range(1, N // 2 + 1))                     # the chain in order, then the same contradiction many times
add(N // 2, [(p[i], p[i + 1]) for i in range(N // 2 - 1)] + [(p[-1], p[0])] * (M - N // 2 + 1))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
