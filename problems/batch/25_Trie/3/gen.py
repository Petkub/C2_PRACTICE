# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(250003)
MAXN, MAXV = 300_000, (1 << 30) - 1
tests = []


def add(a):
    n = len(a)
    assert 2 <= n <= MAXN
    assert all(0 <= x <= MAXV for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


# samples
add([3, 10, 5, 25, 2])
add([7, 7, 7, 7])
add([0, MAXV])
add([1, 2, 3, 4, 5, 6])
add([8, 8, 1, 9, 0])
# hidden: small
add([5, 5])
add(rnd(10, 0, 15))
add(rnd(100, 0, 7))
add(rnd(1000, 0, MAXV))
add(rnd(3000, 0, 1000))
x = random.randint(0, MAXV)
add([x ^ random.choice([0, 1, 2, 1 << 29]) for _ in range(2000)])
# hidden: maximum size
N = MAXN
add([123456789] * N)                                                   # 0 for every pair
add([MAXV if i % 2 else 0 for i in range(N)])                          # 2.25 * 10^10 pairs reach the maximum
add(rnd(N, 0, MAXV))
add(rnd(N, 0, 255))
add(rnd(N, 1 << 29, MAXV))                                              # the top bit never differs
add([random.choice([0, 1 << 29]) | random.randint(0, 3) for _ in range(N)])
a = rnd(N - 1, 0, (1 << 20) - 1)                                        # one far value
a.insert(random.randrange(N), MAXV)
add(a)
add([random.randint(0, MAXV) & ~(1 << random.randint(0, 29)) | (1 << 3) for _ in range(N)])
add(sorted(rnd(N, 0, MAXV)))
a = []
for i in range(N):                                                      # values come in complement pairs
    x = random.randint(0, 1 << 15)
    a.append(x if i % 3 else MAXV ^ x)
add(a)

# few distinct values with many copies: more than 2^31 pairs reach the maximum
add(rnd(N, 0, 3))                                                       # 0 with 3 and 1 with 2
add(rnd(N, 0, 15))
a = [random.choice([0, 1, MAXV, MAXV - 1]) for _ in range(N)]           # 0 with MAXV and 1 with MAXV - 1
add(a)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
