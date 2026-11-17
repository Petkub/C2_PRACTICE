# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160006)
MAXN, MAXH = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(h):
    n = len(h)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXH for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")


# samples
add([2, 3, 3, 1, 2])
add([2, 1, 2])
add([7])
add([1, 2, 3, 4])
add([3, 1, 3, 1, 3])
# hidden: small (checked by the exhaustive search)
add([5, 5, 5])
add([2, 1, 2, 1, 2, 1, 2, 1])
add([1, 3, 2, 3, 1, 3, 2])
add([ri(1, 4) for _ in range(8)])
add([ri(1, 3) * 10**8 for _ in range(10)])
add([3, 2, 1, 2, 3, 2, 1, 2])
# hidden: medium (checked by the slab recursion)
add([ri(1, 5) for _ in range(2000)])
add([ri(1, MAXH) for _ in range(5000)])
add([i % 50 + 1 for i in range(20000)])
add([MAXH] * 20000)                               # all equal
add([MAXH if i % 2 else MAXH - 1 for i in range(20000)])
h, cur = [], 1                                    # random walk
for _ in range(20000):
    cur = max(1, min(MAXH, cur + ri(-3, 3)))
    h.append(cur)
add(h)


def descent(n, top, step):                        # strictly decreasing from top, steps 1..step
    h, cur = [], top
    for _ in range(n):
        h.append(cur)
        cur -= ri(1, step)
    assert h[-1] >= 1
    return h


# hidden: maximum size (each has a long falling stretch: most columns stand right of many higher ones)
N = MAXN
add([N - i for i in range(N)])                    # staircase down
add([N - abs(N // 2 - i) for i in range(N)])      # mountain
add([(N - i) * 1000 + ri(0, 3000) for i in range(N)])        # noisy ramp down
add([1 + abs(170_000 - i) for i in range(N)])     # long fall, short climb
d = descent(150_000, MAXH, 1000)                  # random prefix, then a fall
add([ri(1, MAXH) for _ in range(50_000)] + d)
d = descent(150_000, MAXH, 1000)                  # the fall's heights seen earlier, closed by a low column
pre = random.sample(d, 49_999) + [1]
add(pre + d)
d = descent(160_000, MAXH, 5)                     # a fall, then small random heights
add(d + [ri(1, 50) for _ in range(40_000)])
h, cur = [], MAXH                                 # a fall with little notches y+2, y, y+3, y+2
while len(h) < N:
    if len(h) % 10 == 6:
        h += [cur + 2, cur, cur + 3, cur + 2]
    else:
        h.append(cur)
    cur -= ri(4, 9)
add(h[:N])
add([(i % 8000) * 20000 + ri(1, 9) for i in range(40_000)] + descent(160_000, MAXH, 1000))  # ramps, then a fall
h, cur = [], 10**6                                # random walk, then a fall
for _ in range(40_000):
    cur = max(1, min(MAXH, cur + ri(-3, 3)))
    h.append(cur)
add(h + descent(160_000, MAXH, 1000))
add([ri(1, 3) for _ in range(40_000)] + descent(160_000, 160_003, 1))  # 1..3, then a fall by 1
add(list(range(50_000, 0, -1)) + list(range(150_001, 0, -1))[:150_000])  # two falls

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
