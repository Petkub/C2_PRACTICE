# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(20203)
MAXQ = 100_000
MAXX = 10**18
KMAX = 1_414_213_561            # the largest k with k(k + 1) / 2 <= 10^18
tests = []


def tri(k):
    return k * (k + 1) // 2


def ri(lo, hi):
    return random.randint(lo, hi)


def add(xs):
    q = len(xs)
    assert 1 <= q <= MAXQ
    assert all(1 <= x <= MAXX for x in xs)
    tests.append(f"{q}\n" + " ".join(map(str, xs)) + "\n")


def near(k):
    """a value next to a triangular number"""
    return min(MAXX, max(1, tri(k) + random.choice((-1, 0, 1))))


assert tri(KMAX) <= MAXX < tri(KMAX + 1)
# samples
add([1, 6, 9, 10])
add([2, 5, 7, 100])
add([3, 4, 15, 14])
add([5050, 5049, 987_654_321])
add([1000, 999_999_999_999, 55, 56, MAXX])
# hidden: small
add(list(range(1, 101)))
add([ri(1, 10**6) for _ in range(1000)])
add([near(ri(1, 2000)) for _ in range(1000)])
add([1] * 50 + [MAXX] * 50)
add([near(ri(KMAX - 1000, KMAX)) for _ in range(500)])
add([ri(1, 2**31) for _ in range(500)] + [tri(65535), tri(65536) - 1, tri(65536), 2**31 - 1, 2**31])
# hidden: maximum size, large x
Q = MAXQ
add([ri(1, MAXX) for _ in range(Q)])
add([ri(MAXX - 10**12, MAXX) for _ in range(Q)])
add([near(ri(KMAX // 2, KMAX)) for _ in range(Q)])       # next to triangular numbers
add([near(ri(KMAX - 10**6, KMAX)) for _ in range(Q)])
add([MAXX] * Q)
add([tri(ri(10**8, KMAX)) - 1 for _ in range(Q)])
add([ri(10**15, 10**17) for _ in range(Q)])
add([ri(1, 10**ri(1, 18)) for _ in range(Q)])

print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
