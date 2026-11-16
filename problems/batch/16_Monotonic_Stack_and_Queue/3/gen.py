# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160003)
MAXN, MAXW, MAXH = 150_000, 10_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(w, h):
    n = len(w)
    assert 1 <= n <= MAXN and len(h) == n
    assert all(1 <= x <= MAXW for x in w) and all(1 <= x <= MAXH for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, w)) + "\n" + " ".join(map(str, h)) + "\n")
    assert len(tests[-1]) <= 3_100_000


# samples
add([2, 1, 3, 1, 2], [3, 5, 4, 2, 6])
add([1, 10, 1], [10, 1, 10])
add([MAXW], [MAXH])
add([1, 2, 3, 4], [1, 2, 3, 4])
add([3, 1, 4, 1, 5, 9], [2, 7, 1, 8, 2, 8])
# hidden: small
add([1, 1], [5, 5])
add([ri(1, 5) for _ in range(10)], [ri(1, 10) for _ in range(10)])
add([ri(1, 100) for _ in range(300)], [ri(1, 1000) for _ in range(300)])
add([ri(1, MAXW) for _ in range(2000)], [ri(1, MAXH) for _ in range(2000)])
add([1] * 3000, [ri(1, 3) for _ in range(3000)])
n = 5000                                       # one very wide low section
add([MAXW if i == 2500 else 1 for i in range(n)], [1 if i == 2500 else ri(2, 50) for i in range(n)])
add([ri(1, 10) for _ in range(10000)], [ri(10**8, MAXH) for _ in range(10000)])
# hidden: maximum size
N = MAXN
add([MAXW] * N, [MAXH] * N)                                     # 1.5 * 10^18
add([ri(1, MAXW) for _ in range(N)], [MAXH - i for i in range(N)])        # decreasing staircase
add([ri(1, MAXW) for _ in range(N)], [N - i for i in range(N)])
add([ri(1, MAXW) for _ in range(N)], [i + 1 for i in range(N)])          # increasing
add([ri(1, MAXW) for _ in range(N)], [ri(1, MAXH) for _ in range(N)])
add([1] * N, [ri(MAXH - 5, MAXH) for _ in range(N)])
add([ri(1, MAXW) for _ in range(N)], [MAXH - abs(N // 2 - i) * 1000 for i in range(N)])   # mountain
w = [1] * N                                                       # narrow tall sections vs wide low ones
h = [MAXH if i % 2 else ri(1, 1000) for i in range(N)]
for i in range(0, N, 2):
    w[i] = MAXW
add(w, h)
add([ri(1, MAXW) for _ in range(N)], [ri(1, 2) for _ in range(N)])
add([ri(1, MAXW) for _ in range(N)], [(N - i) * 6000 for i in range(N)])       # steep decreasing staircase
add([ri(1, MAXW) for _ in range(N)], [(N - i) * (N - i) // 30 + 1 for i in range(N)])   # convex decreasing

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
