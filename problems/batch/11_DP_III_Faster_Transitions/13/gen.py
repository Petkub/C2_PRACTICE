# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(11013)
MAXN, MAXA, MAXC = 200_000, 100_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(D, a, c):
    n = len(a)
    assert 2 <= n <= MAXN and len(c) == n - 1 and 0 <= D <= MAXA
    assert all(0 <= x <= MAXA for x in a) and all(1 <= x <= MAXC for x in c)
    tests.append(f"{n} {D}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, c)) + "\n")


def walk(n, step, lo=0, hi=MAXA):
    """slowly changing shades"""
    x, out = ri(lo, hi), []
    for _ in range(n):
        x = min(hi, max(lo, x + ri(-step, step)))
        out.append(x)
    return out


def rc(n, lo=1, hi=MAXC):
    return [ri(lo, hi) for _ in range(n)]


# samples
add(4, [3, 8, 5, 1, 2, 9], [4, 2, 7, 1, 3])
add(0, [5, 5, 6, 6], [10, 1, 10])
add(10, [7, 1, 4], [5, 5])
add(2, [1, 2, 3, 4, 5, 6, 7], [3, 9, 2, 8, 1, 7])
add(1, [10, 0, 10, 0, 10], [100000, 1, 100000, 1])
add(3, [4, 6, 2, 5, 3, 7, 1, 4], [6, 2, 9, 3, 5, 1, 8])
# hidden: small
add(0, [1, 1], [7])
add(0, [1, 2], [7])
add(5, [ri(0, 10) for _ in range(12)], rc(11, 1, 9))
add(3, [ri(0, 8) for _ in range(15)], rc(14, 1, 20))
add(50, walk(20, 30, 0, 200), rc(19, 1, 100))
add(MAXA, [ri(0, MAXA) for _ in range(18)], rc(17))
# hidden: medium
add(2000, walk(3000, 300), rc(2999))
add(50, walk(4000, 10, 0, 1000), rc(3999, 1, 10))
# hidden: maximum size (long good pieces: slowly changing shades, wide D)
N = MAXN
add(0, [77] * N, rc(N - 1))                       # one piece: 0
add(MAXA, [ri(0, MAXA) for _ in range(N)], rc(N - 1))
add(20_000, walk(N, 100), rc(N - 1))
add(5_000, walk(N, 20), rc(N - 1, 1, 100))
add(1_000, walk(N, 3), rc(N - 1))
add(99_995, [ri(0, MAXA) for _ in range(N)], rc(N - 1))
add(30_000, [(i * 3) % 60_001 for i in range(N)], rc(N - 1))
add(MAXA - 1, [0 if i % 1000 == 0 else ri(1, MAXA - 1) for i in range(N - 1)] + [MAXA], rc(N - 1))
add(10, walk(N, 1, 0, 50), [MAXC] * (N - 1))
add(50_000, [i // 2 for i in range(N)], rc(N - 1, 1, 1000))     # increasing shades
add(1, [i % 3 for i in range(N)], rc(N - 1))      # pieces of length <= 2
add(8_000, walk(N, 40), [1] * (N - 1))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
