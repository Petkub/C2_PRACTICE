# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(16008)
MAXN, MAXA, MAXW = 200_000, 10**9, 1000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a, w):
    n = len(a)
    assert 1 <= n <= MAXN and len(w) == n
    assert all(1 <= x <= MAXA for x in a) and all(1 <= x <= MAXW for x in w)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, w)) + "\n")


def rw(n, lo=1, hi=MAXW):
    return [ri(lo, hi) for _ in range(n)]


def valley(n, lo, hi):
    """a noisy valley: high at both ends, low in the middle"""
    return [max(1, min(MAXA, int(lo + (hi - lo) * abs(2 * i / max(1, n - 1) - 1)) + ri(-(hi - lo) // 20, (hi - lo) // 20)))
            for i in range(n)]


# samples
add([5, 3, 4, 1, 2, 6], [1, 1, 1, 1, 1, 1])
add([4, 2, 6, 3, 1, 5], [2, 1, 3, 1, 2, 1])
add([7], [3])
add([1, 2, 3, 3, 5], [4, 1, 2, 2, 1])
add([6, 1, 4, 2, 4, 1, 5, 3], [1, 2, 3, 1, 1, 2, 2, 1])
# hidden: small
add([3, 3, 3], [5, 1, 2])
add([2, 9, 1], [1, 1000, 1])
add([1, 5, 5, 1], [10, 1, 1, 10])                                  # two lowest sections
add([1, 100, 2, 3, 2, 100], [1, 1, 50, 50, 50, 1])
for n, ah in [(4, 5), (7, 10), (10, 20), (20, 50), (150, 10**9)]:
    add([ri(1, ah) for _ in range(n)], rw(n, 1, 20 if ah < 100 else MAXW))
a = [ri(1, 10**9) for _ in range(300)]
add(a, rw(300))
a = valley(300, 1, 10**6)
a[3] = 1                                                           # a deep narrow pit near the left end
add(a, [1] * 10 + [MAXW] * 290)

# hidden: maximum size
N = MAXN
add([ri(1, MAXA) for _ in range(N)], rw(N))                        # random
add([ri(1, 10**6) if i % 2 else ri(9 * 10**8, MAXA) for i in range(N)], rw(N))   # zigzag: many local minima
a = valley(N, 10**8, 10**9)
a[5] = 1
w = [1] * 20 + rw(N - 20, 500, MAXW)
add(a, w)                                                          # a pit at the end, a wide valley in the middle
add([ri(1, 10) for _ in range(N)], rw(N))                          # many equal heights
a = [min(MAXA, (i * 9973) % 1000 + (i // 1000) * 5_000_000 + 1) for i in range(N)]
add(a[::-1], rw(N))                                                # saw teeth growing to the left
a = sorted(ri(1, MAXA) for _ in range(N // 2))
a = a + sorted((ri(1, MAXA) for _ in range(N - N // 2)), reverse=True)
add(a, [MAXW] * N)                                                 # a mountain: the drain goes to one end
a = valley(N // 2, 1, 5 * 10**8) + valley(N - N // 2, 1, 5 * 10**8)
a[ri(0, 1000)] = 1
add([x + ri(0, 1000) for x in a], rw(N))                           # two valleys with noise
add([MAXA - ri(0, 10**6) for _ in range(N)], [MAXW] * N)           # tall sections, widest everywhere
a = [ri(1, MAXA) for _ in range(N)]
a[0] = a[-1] = 1
add(a, rw(N))                                                      # lowest sections at both ends
add([ri(1, 10**6) for _ in range(N)], [1] * N)                    # narrowest everywhere
h = N // 2
add([MAXA - 4000 * i for i in range(h)] + [MAXA - 4000 * (N - h) + 4000 * i for i in range(1, N - h + 1)], rw(N))
a, cur = [], 5 * 10**8                                             # a random walk: many valleys of all sizes
for _ in range(N):
    cur = max(1, min(MAXA, cur + ri(-3 * 10**6, 3 * 10**6)))
    a.append(cur)
add(a, rw(N))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
