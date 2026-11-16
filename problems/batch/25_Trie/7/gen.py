# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(250007)
MAXN, MAXV = 300_000, (1 << 20) - 1
tests = []


def add(L, a):
    n = len(a)
    assert 1 <= L <= n <= MAXN
    assert all(0 <= x <= MAXV for x in a)
    tests.append(f"{n} {L}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


# samples
add(2, [1, 2, 4, 8, 3])
add(4, [5, 5, 5, 5])
add(1, [0])
add(3, [7, 1, 6, 0, 3, 5])
add(6, [9, 12, 3, 10, 6, 1])
# hidden: small
add(1, [6, 3])
add(3, rnd(10, 0, 15))
add(5, rnd(100, 0, 255))
add(1000, rnd(1000, 0, MAXV))
add(37, rnd(3000, 0, MAXV))
add(400, rnd(3000, 0, 7))
add(2, [1 << b for b in range(20)] * 50)                       # long runs would give much more
# hidden: maximum size
N = MAXN
add(N, rnd(N, 0, MAXV))
add(N // 2, rnd(N, 0, MAXV))
add(N // 3, rnd(N, 0, 1023))
a = [0] * N                                                    # mostly zeros: equal prefix values
for _ in range(60):
    a[random.randrange(N)] = random.randint(1, MAXV)
add(N // 2, a)
add(1, rnd(N, 0, MAXV))
add(7, rnd(N, 0, MAXV))
add(N - 1, [MAXV] * N)
a = rnd(N, 0, (1 << 12) - 1)                                    # two far values: only a long segment joins them
a[1000] = (1 << 19)
a[N - 1000] = (1 << 19) | ((1 << 12) - 1)
add(N - 3000, a)
add(N // 4, [random.choice([1 << 19, 1 << 18, 3]) for _ in range(N)])
add(5000, rnd(N, 0, MAXV))
# the answer stays below 2^20 - 1, so stopping at the all-ones bound does not help (review)
add(N, [random.randint(0, MAXV) & ~1 for _ in range(N)])
add(N - 1, [random.choice([1 << 19, 1 << 18, 3]) for _ in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
