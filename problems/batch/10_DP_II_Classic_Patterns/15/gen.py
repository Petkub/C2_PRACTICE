# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(10015)
MAXN, MAXV = 200000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    assert 1 <= len(a) <= MAXN and 1 <= min(a) and max(a) <= MAXV
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo=1, hi=MAXV):
    return [ri(lo, hi) for _ in range(n)]


def trap(n, k):
    """k groups; group g holds a falling run of values around 10*g: many longest subsequences,
    the usual rebuild (the last tail found) rarely gives the smallest"""
    out = []
    per = n // k
    for g in range(k):
        base = 1000 * (g + 1)
        out += sorted((base + ri(0, 999) for _ in range(per)), reverse=True)
    return out + [1] * (n - len(out))


def noisy_up(n, step, noise):
    return [max(1, min(MAXV, 1 + i * step + ri(-noise, noise))) for i in range(n)]


# samples
add([5, 1, 6, 2, 7, 3])
add([4, 9, 2, 9, 5, 7])
add([10, 9, 8])
add([3, 3, 3, 4, 4])
add([8, 2, 9, 4, 6, 1, 7, 3, 5, 10])
# hidden: small (brute.cpp tries every subsequence when n <= 18)
add([1])
add([2, 1])
add(rnd(10, 1, 5))
add(rnd(15, 1, 8))
add(rnd(18, 1, 30))
add(trap(18, 3))
add(rnd(300, 1, 50))
add(trap(3000, 30))
# hidden: maximum size
N = MAXN
add(rnd(N))
add(rnd(N, 1, 1000))
add(trap(N, 400))
add(trap(N, 5000))
add(noisy_up(N, 3, 1000))
add(list(range(1, N + 1)))
add(list(range(N, 0, -1)))
add([MAXV] * N)
add([(i * 7919) % 200003 + 1 for i in range(N)])
add([ri(1, 100) + (i // 1000) * 100 for i in range(N)])
add([MAXV - ri(0, 10) - (i % 2) * 1000 for i in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
