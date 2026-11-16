# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160007)
MAXN, MAXC, MAXP = 200_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(c, p):
    n = len(p)
    assert 1 <= n <= MAXN and 1 <= c <= MAXC and all(1 <= x <= MAXP for x in p)
    tests.append(f"{n} {c}\n" + " ".join(map(str, p)) + "\n")


# samples
add(3, [5, 2, 7, 4, 1, 6])
add(10, [4, 6, 3, 8, 2])
add(1, [7])
add(1, [3, 1, 4, 1])
add(2, [6, 2, 9, 9, 3, 8, 5, 1])
# hidden: small
add(MAXC, [ri(1, 9) for _ in range(10)])
add(3, [ri(1, 9) for _ in range(30)])
add(ri(2, 20), [ri(1, 100) for _ in range(300)])
add(50, [ri(1, MAXP) for _ in range(2000)])
add(7, [3000 - i for i in range(3000)])              # cheaper and cheaper
add(100, [i + 1 for i in range(5000)])               # dearer and dearer
add(1000, [ri(1, 5) for _ in range(20000)])
# hidden: maximum size
N = MAXN
add(N // 2, [ri(1, MAXP) for _ in range(N)])
add(N // 2, [i + 1 for i in range(N)])                # the window minimum is always the oldest station
add(N - 1, [N - i for i in range(N)])                 # every station is the new minimum
add(MAXC, [MAXP] * N)                                 # 2 * 10^14
add(1, [ri(1, MAXP) for _ in range(N)])
add(1000, [ri(1, MAXP) for _ in range(N)])
add(N // 3, [MAXP - (i % 5000) for i in range(N)])    # saw teeth
p = [MAXP] * N                                        # a few cheap stations far apart
for k in range(0, N, 40000):
    p[k] = 1
add(39999, p)
add(N // 4, [MAXP - abs(N // 2 - i) * 1000 for i in range(N)])
add(ri(N // 3, N), [ri(MAXP - 100, MAXP) for _ in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
