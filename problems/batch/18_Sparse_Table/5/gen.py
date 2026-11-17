# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180005)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(h, qs):
    n, q = len(h), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXV for v in h)
    assert all(1 <= i <= n and 1 <= x <= MAXV for i, x in qs)
    t = f"{n} {q}\n" + " ".join(map(str, h)) + "\n" + "".join(f"{i} {x}\n" for i, x in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def far_q(h, q, low):
    """trucks start near the beginning and are low: long drives"""
    n = len(h)
    return [(ri(1, max(1, n // 20)), ri(1, low)) for _ in range(q)]


def mixed_q(h, q):
    """the truck height is a bridge height (+0 / +1): ties matter"""
    n = len(h)
    res = []
    for _ in range(q):
        i = ri(1, n)
        res.append((i, min(MAXV, h[ri(0, n - 1)] + ri(0, 1))))
    return res


# samples
add([5, 3, 7, 6, 2, 8], [(1, 3), (3, 6), (2, 4), (6, 1)])
add([10, 10, 10, 10], [(1, 10), (2, 11)])
add([1], [(1, 1), (1, 2)])
add([4, 9, 9, 1, 9, 3, 2], [(1, 4), (2, 9), (2, 10), (5, 3), (5, 1), (7, 2)])
add([MAXV, 1, MAXV, MAXV, MAXV], [(1, MAXV), (3, MAXV), (2, 1), (1, 2), (3, 1)])
# hidden: small
h = [ri(1, 10) for _ in range(10)]
add(h, [(i, x) for i in range(1, 11) for x in range(1, 12)])
h = [ri(1, 100) for _ in range(200)]
add(h, mixed_q(h, 500) + far_q(h, 200, 20))
h = [ri(1, MAXV) for _ in range(2000)]
add(h, mixed_q(h, 3000))
h = [ri(990, 1000) for _ in range(3000)]
add(h, mixed_q(h, 3000) + far_q(h, 1000, 995))
# hidden: maximum size (values kept short so the input stays <= 3 MB)
N = MAXN
h = [ri(500_000, 999_999) for _ in range(N)]
add(h, far_q(h, 110_000, 500_000))                                        # everyone drives to the end
h = [999_999] * N
h[N - 2] = 1
add(h, far_q(h, 110_000, 999_999))                                        # stop just before the last bridge
h = [ri(500_001, 999_999) for _ in range(N)]                               # low bridges every 1 000, lower and
walls = []                                                                  # lower along the road: a truck as
for k in range(N // 1000):                                                  # high as one of them (or 1 higher)
    p = 1000 * k + ri(0, 999)                                               # drives far, the tie decides
    h[p] = 500_000 - 2000 * k - ri(0, 1999)
    walls.append(h[p])
add(h, [(ri(1, 5000), walls[ri(N // 2000, N // 1000 - 1)] + ri(0, 1)) for _ in range(110_000)])
h = [ri(100_000, 999_999) for _ in range(N)]
for _ in range(10):
    h[ri(N - N // 5, N - 1)] = ri(1, 1000)
add(h, far_q(h, 110_000, 99_999))                                           # a few low bridges near the end
h = list(range(999_999, 999_999 - 4 * N, -4))                               # decreasing heights
add(h, [(ri(1, 10), ri(1, 199_999)) for _ in range(110_000)])
h = list(range(5, 4 * N + 5, 4))                                            # increasing heights
qs = []
for _ in range(110_000):
    i = ri(1, 10_000)                                                       # h_i = 4i + 1
    qs.append((i, 4 * i + 2 if ri(0, 9) == 0 else 4 * i + 1 - ri(0, 3) * ri(0, i)))
add(h, qs)
h = [MAXV] * N
add(h, [(ri(1, 50), MAXV) for _ in range(50_000)])                       # equal height: passes all
h = [ri(999_000, 999_999) for _ in range(N)]
add(h, far_q(h, 55_000, 999_000) + mixed_q(h, 55_000))
h = [ri(1, 999_999) for _ in range(N)]
add(h, [(ri(1, N // 10), 1) for _ in range(110_000)])                    # x = 1: always to the end
h = [1 if i % 20_000 == 19_999 else ri(2, 999_999) for i in range(N)]       # low bridge every 20 000
add(h, [(20_000 * ri(0, 2) + ri(1, 50), 2 if ri(0, 3) == 0 else 1) for _ in range(110_000)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
