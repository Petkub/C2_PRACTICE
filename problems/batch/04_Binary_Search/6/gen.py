# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(40602)
MAXN = 200_000
MAXH = 10**12
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def answer(climbs, classic=False):
    """small tests only: the smallest strength that reaches the top (classic: the largest climb, or one more)"""
    top = max(climbs)

    def ok(k):
        for c in climbs:
            if c > k:
                return False
            if 2 * c > k:
                k -= 1
        return True

    if classic:
        return top if ok(top) else top + 1
    k = top
    while not ok(k):
        k += 1
    return k


def add(climbs, sample=False):
    n = len(climbs)
    assert 1 <= n <= MAXN and all(c >= 1 for c in climbs)
    hs, h = [], 0
    for c in climbs:
        h += c
        hs.append(h)
    assert hs[-1] <= MAXH
    if sample:  # the samples do not separate the correct method from the classic shortcut
        assert answer(climbs) == answer(climbs, classic=True)
    tests.append(f"{n}\n" + " ".join(map(str, hs)) + "\n")


def near(n, G, spread):
    """climbs just below G: almost every climb tires the climber"""
    return [G - ri(0, spread) for _ in range(n)]


# samples
add([2, 3, 1, 4], sample=True)
add([1, 1, 1, 7], sample=True)
add([MAXH], sample=True)
add([5, 2, 5, 3, 1], sample=True)
add([10, 4, 6, 9, 3, 8], sample=True)
add([7, 7], sample=True)
# hidden: small (checked by brute force)
add([3, 3, 3])                                  # 5, two more than the largest climb
add([ri(1, 20) for _ in range(30)])
add(near(200, 1000, 10))
add([ri(1, 100) for _ in range(2000)])
add(near(3000, 10_000, 3000))
add([1] * 1000)
add([ri(400, 500) for _ in range(300)] + [900])
add(near(1000, 2000, 0))
# hidden: maximum size (the answer is far above the largest climb)
N = MAXN
add(near(N, 4_000_000, 0))
add(near(N, 4_000_000, 1_000_000))
add(near(N, 3_000_000, 50))
add(near(N, 1_000_000, 400_000))
add([ri(2_000_000, 4_000_000) if random.random() < 0.9 else ri(1, 1000) for _ in range(N)])
add(near(N // 2, 2_000_000, 100) + near(N // 2, 4_000_000, 100))
add(near(N // 2, 4_000_000, 100) + near(N // 2, 2_000_000, 100))
add(sorted(ri(1_000_000, 4_000_000) for _ in range(N)))
add(near(N, 4_500_000, 200_000))
add(near(N - 1, 3_000_000, 1_000) + [4_999_000])
add([MAXH // N] * N)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
