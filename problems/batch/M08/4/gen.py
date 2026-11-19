# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random
from itertools import accumulate

random.seed(4204)
MAXN, MAXH = 200000, 10**9
tests = []


def add(h):
    n = len(h)
    assert 1 <= n <= MAXN and len(set(h)) == n and 1 <= min(h) and max(h) <= MAXH
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")


def heights(order):
    n = len(order)
    gap, rnd = MAXH // n, random.random
    vals = list(accumulate(1 + int(rnd() * gap) for _ in range(n)))
    return [vals[r] for r in order]


def perm(n):
    keys = [random.random() for _ in range(n)]
    return sorted(range(n), key=keys.__getitem__)


def mountain(n, noise):
    share = random.random()
    left, right = [], []
    for v in range(n - 1):
        (left if random.random() < share else right).append(v)
    p = left + [n - 1] + right[::-1]
    for _ in range(noise):
        i = random.randrange(n - 1)
        p[i], p[i + 1] = p[i + 1], p[i]
    return p


def spikes(n, step):
    p, low, high = [], 0, n - (n + step - 1) // step
    for i in range(n):
        if i % step == 0:
            p.append(high)
            high += 1
        else:
            p.append(low)
            low += 1
    return p


add([3, 1, 4, 2])
add([2, 1, 3])
add([7])
add([10, 40, 20, 60, 50, 30])
add([5, 8, 2, 1, 9, 3, 7, 4])

add([1, 2])
add([2, 1])
for n in (5, 9, 12, 15, 18, 20):
    add(heights(perm(n)))
add(heights(mountain(16, 3)))
add(heights(list(range(20))))
add(heights(list(range(19, -1, -1))))

N = MAXN
add(list(range(1, N + 1)))
add([MAXH - i for i in range(N)])
add(heights(perm(N)))
add(heights(mountain(N, 0)))
add(heights(mountain(N, N // 10)))
add(heights(spikes(N, 1000)))
add(heights(spikes(N, 3)[::-1]))
p = list(range(N))
p = p[0::2] + p[1::2][::-1]
add(heights(p))
add(heights([N - 1] + perm(N - 1)))
add(heights(perm(N - 1) + [N - 1]))

half = []
for b in range(N // 2000):
    blk = list(range(1000 * b, 1000 * (b + 1)))
    random.shuffle(blk)
    half += blk
add(heights([2 * x for x in half] + [2 * x + 1 for x in half[::-1]]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
