# Test generator of this problem (the judge runs it to rebuild the big tests).
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


add(2, [1, 2, 4, 8, 3])
add(4, [5, 5, 5, 5])
add(1, [0])
add(3, [7, 1, 6, 0, 3, 5])
add(6, [9, 12, 3, 10, 6, 1])

add(1, [6, 3])
add(3, rnd(10, 0, 15))
add(5, rnd(100, 0, 255))
add(1000, rnd(1000, 0, MAXV))
add(37, rnd(3000, 0, MAXV))
add(400, rnd(3000, 0, 7))
add(2, [1 << b for b in range(20)] * 50)
add(1, rnd(3000, 0, MAXV))
add(7, rnd(3000, 0, MAXV))
a = rnd(2000, 0, (1 << 19) - 1)
a[0] |= 1 << 19
add(50, a)

N = MAXN
add(N, rnd(N, 0, MAXV))
add(N // 2, rnd(N, 0, MAXV))
add(N // 3, rnd(N, 0, 1023))
a = [0] * N
for _ in range(60):
    a[random.randrange(N)] = random.randint(1, MAXV)
add(N // 2, a)
add(N - 1, [MAXV] * N)
a = rnd(N, 0, (1 << 12) - 1)
a[1000] = (1 << 19)
a[N - 1000] = (1 << 19) | ((1 << 12) - 1)
add(N - 3000, a)
add(N // 4, [random.choice([1 << 19, 1 << 18, 3]) for _ in range(N)])
add(150_000, rnd(N, 0, MAXV))

add(N, [random.randint(0, MAXV) & ~1 for _ in range(N)])
add(N - 1, [random.choice([1 << 19, 1 << 18, 3]) for _ in range(N)])

for L, hi in [(N, (1 << 19) - 1), (N // 3, (1 << 19) - 1), (200_000, 1023), (N - 1, (1 << 19) - 1)]:
    a = rnd(N, 0, hi)
    a[0] = (1 << 19) | random.randint(0, (1 << 19) - 1)
    add(L, a)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
