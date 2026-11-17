# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(14004)
MAXQ = 100_000
MAXV = 5_000_000
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    assert all(1 <= l <= r <= MAXV for l, r in qs)
    tests.append(f"{len(qs)}\n" + "".join(f"{l} {r}\n" for l, r in qs))


def rq(lo, hi, maxlen=None):
    l = ri(lo, hi)
    r = ri(l, hi if maxlen is None else min(hi, l + maxlen))
    return (l, r)


PERFECT = [6, 28, 496, 8128]

# samples
add([(1, 12), (6, 6), (20, 30)])
add([(1, 1), (945, 945)])
add([(1, 10_000), (496, 8128)])
add([(4_999_000, MAXV), (8128, 8128), (2, 5)])
add([(1, MAXV)])
# hidden: small (the brute force does trial division for every x)
add([(1, 1)])
add([(x, x) for x in range(1, 3001)])
add([rq(1, 2000) for _ in range(300)])
add([(p - ri(0, 3), p + ri(0, 3)) for p in PERFECT for _ in range(50)])
add([rq(MAXV - 3000, MAXV, 50) for _ in range(500)])
add([rq(1, MAXV, 30) for _ in range(800)])
add([(ri(1, MAXV), MAXV) for _ in range(5)] + [(1, ri(1, 30_000)) for _ in range(5)])
# hidden: large
add([(1, MAXV)] * MAXQ)
add([rq(1, MAXV) for _ in range(MAXQ)])
add([(ri(1, 10), MAXV - ri(0, 10)) for _ in range(MAXQ)])
add([(p, p) for p in random.choices(PERFECT, k=MAXQ // 2)] + [rq(1, MAXV) for _ in range(MAXQ // 2)])
add([rq(1, MAXV, 1000) for _ in range(MAXQ)])
add([(x, x) for x in random.sample(range(1, MAXV + 1), MAXQ)])
add([(1, ri(1, MAXV)) for _ in range(MAXQ)])
add([(ri(MAXV // 2, MAXV), MAXV) for _ in range(MAXQ)])
add([(l, l + ri(10 ** 6, MAXV - l)) for l in [ri(1, MAXV - 10 ** 6) for _ in range(MAXQ)]])  # long ranges
add([(MAXV, MAXV)] + [rq(1, MAXV) for _ in range(MAXQ - 1)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
