# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110012)
MAXN, MAXQ, MAXV = 300_000, 300_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(c, gs):
    n, q = len(c), len(gs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= v <= MAXV for v in c)
    assert all(1 <= p <= n and 1 <= g <= MAXV for (p, g) in gs)
    t = f"{n} {q}\n" + " ".join(map(str, c)) + "\n" + "".join(f"{p} {g}\n" for (p, g) in gs)
    assert len(t) <= 3_100_000
    tests.append(t)


# samples
add([3, 1, 4, 1, 5], [(1, 2), (1, 2), (2, 1), (4, 5), (1, 3)])
add([10, 1, 1], [(2, 5), (1, 10), (1, 1), (3, 1)])
add([MAXV], [(1, MAXV), (1, 1)])
add([0, 2, 6, 3, 2, 4], [(1, 3), (3, 4), (5, 3), (2, 2)])
add([4, 4, 4, 4], [(1, 4), (2, 3), (1, 2), (3, 5)])
# hidden: small
add([0], [(1, 1)])
add([ri(0, 5) for _ in range(10)], [(ri(1, 10), ri(1, 6)) for _ in range(30)])
add([ri(0, 50) for _ in range(100)], [(ri(1, 30), ri(1, 40)) for _ in range(300)])
add([ri(0, MAXV) for _ in range(1000)], [(ri(1, 1000), ri(1, MAXV)) for _ in range(2000)])
c = [ri(0, 3) for _ in range(5000)] + [10**6] * 3
add(c, [(ri(1, 50), ri(4, 9)) for _ in range(8000)])
c = [ri(0, 20) for _ in range(20000)]
add(c, [(ri(1, 20000), ri(1, 25)) for _ in range(20000)])
# hidden: maximum size
N = MAXN
c = [ri(0, 3) for _ in range(N - 10)] + [MAXV] * 10                  # everybody walks to the end
add(c, [(ri(1, 99), ri(4, 9)) for _ in range(N)])
c = [ri(0, 3) if random.random() < 0.9999 else ri(5, 9) for _ in range(N - 10)] + [MAXV] * 10
add(c, [(ri(1, 99), ri(4, 9)) for _ in range(N)])                     # a few middle hotels help
c = [1] * (N - 1) + [MAXV]                                            # nobody is full, nobody fits
add(c, [(ri(1, 99), 2) if j % 10 else (ri(1, N), 1) for j in range(N)])
c = [ri(0, 3) for _ in range(N)]                                      # mostly no room at all
c[-1] = MAXV
add(c, [(ri(1, 99), ri(4, 9)) if j % 2 else (ri(1, 99), 10**4) for j in range(N)])
c = [i // 100 for i in range(N)]                                      # bigger hotels further on
add(c, [(ri(1, 99), ri(1, 2999)) for _ in range(180_000)])
c = [ri(1, 1000) for _ in range(N)]
add(c, [(ri(1, N), ri(1, 1000)) for _ in range(150_000)])             # random
c = [9] * N
add(c, [(1, 9) for _ in range(N)])                                    # hotels fill one by one, exact fits
c = [ri(0, 3) for _ in range(N - 1000)] + [ri(0, 99) for _ in range(1000)]
add(c, [(ri(1, 99), ri(4, 99)) for _ in range(N)])                    # the far end slowly runs out
c = [ri(5, 9) if i % 2 else ri(0, 2) for i in range(N)]
add(c, [(ri(1, 9), ri(3, 9)) for _ in range(N)])                      # first fits move right over time
c = [ri(1, MAXV) for _ in range(120_000)]
add(c, [(ri(1, 99), ri(MAXV // 2, MAXV)) for _ in range(120_000)])    # big numbers
c = [ri(0, 3) for _ in range(N - 1)] + [MAXV]
add(c, [(ri(1, 99), 4) for _ in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
