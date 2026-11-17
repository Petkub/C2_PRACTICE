# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(141301)
MAXM = 10 ** 6
MAXQ = 100_000
MAXN = 10 ** 18
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(m, a1, a2, ns):
    assert 2 <= m <= MAXM and 0 <= a1 < m and 0 <= a2 < m
    assert 1 <= len(ns) <= MAXQ and all(1 <= n <= MAXN for n in ns)
    tests.append(f"{m} {a1} {a2}\n{len(ns)}\n" + " ".join(map(str, ns)) + "\n")


def mixed(q, period_hint=None):
    ns = []
    for i in range(q):
        c = i % 4
        if c == 0:
            ns.append(ri(1, MAXN))
        elif c == 1:
            ns.append(ri(MAXN - 10 ** 6, MAXN))
        elif c == 2:
            ns.append(ri(1, 10 ** 7))
        else:
            ns.append(ri(1, MAXN // period_hint - 1) * period_hint + ri(0, 2) if period_hint else ri(1, 10 ** 15))
    random.shuffle(ns)
    return ns


# samples
add(10, 1, 1, [1, 2, 3, 7, 10, 61])
add(7, 3, 0, [1, 9, 16, 17, 18, MAXN])
add(2, 0, 0, [5, MAXN])
add(MAXM, MAXM - 1, MAXM - 1, [3, 4, 123_456_789_012, MAXN])
add(13, 5, 8, [1, 2, 3, 4, 5, 6, 7])
# hidden: small values of n, or small m (checked by the brute force)
add(2, 1, 0, list(range(1, 21)) + [MAXN, MAXN - 1, MAXN - 2])
add(ri(2, 50), 0, 1, [ri(1, 1000) for _ in range(2000)])
add(97, 13, 61, [ri(1, MAXN) for _ in range(5000)])
add(1000, 0, 500, [ri(1, MAXN) for _ in range(5000)])
add(781_250, 1, 2, [ri(1, MAXN) for _ in range(300)] + [1, 2, 4_687_500, 4_687_501, 4_687_502, 9_375_001])
add(999_953, 0, 1, [ri(1, MAXN) for _ in range(300)] + [1_999_908, 1_999_909, 1_999_910])
add(999_999, ri(0, 999_998), ri(0, 999_998), [ri(1, MAXN) for _ in range(300)])
# hidden: large
add(781_250, 123, 4567, mixed(MAXQ, 4_687_500))
add(781_250, ri(0, 781_249), ri(0, 781_249), [ri(1, MAXN) for _ in range(MAXQ)])
add(781_250, 0, 390_625, mixed(MAXQ))
add(MAXM, 3, 77, mixed(MAXQ, 1_500_000))
add(MAXM, 0, 0, mixed(MAXQ))
add(999_953, 0, 1, mixed(MAXQ, 1_999_908))
add(999_763, ri(1, 999_762), ri(1, 999_762), [ri(MAXN // 2, MAXN) for _ in range(MAXQ)])
add(999_961, 1, 1, mixed(MAXQ, 999_960))
add(999_998, 1, 3, [MAXN - i for i in range(MAXQ)])
add(ri(900_000, MAXM), ri(0, 899_999), ri(0, 899_999), mixed(MAXQ))
add(781_250, 781_249, 781_249, [ri(1, MAXN) for _ in range(MAXQ)])
add(2, 1, 1, mixed(MAXQ))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
