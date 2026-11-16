# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160009)
MAXN, MAXA = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


# samples
add([2, 1, 3, 2, 4])
add([1, 2, 2, 3])
add([5])
add([1, 2, 3, 4, 5])
add([3, 1, 4, 1, 5, 9, 2, 6])
# hidden: small
add([4, 4])
add([ri(1, 4) for _ in range(12)])
add([ri(1, 10) for _ in range(300)])
add([ri(1, MAXA) for _ in range(2000)])
add([i // 3 + 1 for i in range(3000)])                 # increasing with plateaus
add([i * 10 + ri(0, 25) for i in range(8000)])          # increasing with noise
# hidden: maximum size
N = MAXN
add([i + 1 for i in range(N)])                          # every pair: about 2 * 10^10
add([MAXA - N + 1 + i for i in range(N)])
add([N - i for i in range(N)])                          # no pair
add([MAXA] * N)                                         # no pair (ties)
add([i * 1000 + ri(0, 1500) + 1 for i in range(N)])     # increasing with noise
add([i // 2 + 1 for i in range(N)])                     # pairs of equal prices
add([ri(1, MAXA) for _ in range(N)])
add([ri(1, 5) for _ in range(N)])
add([(i % 50000) * 10 + 1 for i in range(N)])           # four long ramps
a = [i * 2 + 2 for i in range(N)]                        # a ramp with dips
for k in range(1000, N, 1000):
    a[k] = 1
add(a)
add([i + 1 if i < N // 2 else N - i for i in range(N)])  # mountain
add([i // 3 + ri(1, 3) for i in range(N)])               # rising with small noise and ties

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
