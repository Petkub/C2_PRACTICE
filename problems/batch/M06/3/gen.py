# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4603)
MAXN = 300000
tests = []


def add_order(a):
    n = len(a)
    assert 1 <= n <= MAXN and sorted(a) == list(range(1, n + 1))
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def add_places(place):
    a = [0] * len(place)
    for b, k in enumerate(place, 1):
        a[k - 1] = b
    add_order(a)


def reversed_places(n):
    return list(range(n, 0, -1))


def far_swaps(p, k):
    p = p[:]
    for _ in range(k):
        i, j = random.randrange(len(p)), random.randrange(len(p))
        p[i], p[j] = p[j], p[i]
    return p


def near_swaps(p, prob, reach):
    p = p[:]
    for i in range(len(p) - reach):
        if random.random() < prob:
            j = i + random.randint(1, reach)
            p[i], p[j] = p[j], p[i]
    return p


def window_shuffle(p, w):
    p = p[:]
    for i in range(0, len(p), w):
        part = p[i:i + w]
        random.shuffle(part)
        p[i:i + w] = part
    return p


add_order([5, 1, 4, 2, 3])
add_order([4, 3, 1, 5, 2])
add_order([1])
add_order([2, 1, 4, 3])
add_order([7, 6, 1, 5, 2, 3, 4])

add_order([1, 2])
add_order([2, 1])
add_order(list(range(1, 9)))
add_order(random.sample(range(1, 11), 10))
add_places(near_swaps(reversed_places(30), 0.3, 3))
add_places(far_swaps(reversed_places(200), 5))
add_order(random.sample(range(1, 1001), 1000))
add_places(window_shuffle(reversed_places(3000), 4))
add_order(random.sample(range(1, 20001), 20000))
add_order(random.sample(range(1, 100001), 100000))

N = MAXN
add_places(reversed_places(N))
add_places(near_swaps(reversed_places(N), 0.002, 300))
add_places(near_swaps(reversed_places(N), 0.0005, 3000))
add_places(near_swaps(reversed_places(N), 0.05, 2))
add_places(near_swaps(reversed_places(N), 0.3, 5))
add_places(window_shuffle(reversed_places(N), 3))
add_places(window_shuffle(reversed_places(N), 50))
add_places(near_swaps(far_swaps(reversed_places(N), 10), 0.01, 1000))
add_places(near_swaps(reversed_places(N), 0.0001, 30000))
add_places(window_shuffle(list(range(N // 2 + 1, N + 1))[::-1] + list(range(1, N // 2 + 1))[::-1], 7))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
