# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(30111)
MAXN = 200_000
tests = []


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert sorted(a) == list(range(1, n + 1))
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def perm(n):
    a = list(range(1, n + 1))
    random.shuffle(a)
    return a


def merge_runs(runs):
    """interleave the given increasing lists at random, keeping each list in order"""
    idx = [k for k, r in enumerate(runs) for _ in r]
    random.shuffle(idx)
    ptr = [0] * len(runs)
    res = []
    for k in idx:
        res.append(runs[k][ptr[k]])
        ptr[k] += 1
    return res


# samples
add([3, 1, 4, 2, 5])
add([4, 1, 2, 3])
add([1, 2, 3, 4, 5, 6])
add([1])
add([5, 4, 3, 2, 1])
add([2, 6, 3, 7, 1, 4, 8, 5])
# hidden: small (checked by BFS over all piles)
add([2, 1])
add([2, 3, 1])
add([3, 4, 1, 2])
add([1, 5, 2, 6, 3, 7, 4, 8])
add([6, 1, 7, 2, 8, 3, 9, 4, 5])
add([9, 8, 7, 6, 5, 4, 3, 2, 1])
for n in (6, 7, 8, 9, 9):
    add(perm(n))
add(perm(3000))
# hidden: large
N = MAXN
add(list(range(1, N + 1)))                                       # already sorted
add(list(range(N, 0, -1)))
add(list(range(70_001, N + 1)) + list(range(1, 70_001)))         # two blocks swapped
add(merge_runs([list(range(1, 50_001)), list(range(50_001, 160_001)), list(range(160_001, N + 1))]))
add([x for k in range(N // 2) for x in (k + 1, N // 2 + k + 1)])  # 1, N/2+1, 2, N/2+2, ...
a = list(range(1, N + 1))
for _ in range(3):                                               # a few random swaps
    i, j = random.randrange(N), random.randrange(N)
    a[i], a[j] = a[j], a[i]
add(a)
mid = list(range(60_001, 150_001))                               # the best run is in the middle of the values
others = [x for x in range(1, N + 1) if not 60_001 <= x <= 150_000]
random.shuffle(others)
add(merge_runs([mid] + [[x] for x in others]))
add(merge_runs([list(range(1, 90_001)), list(range(90_001, N + 1))]))
add(perm(N))
a = list(range(1, N + 1))
a[0], a[-1] = a[-1], a[0]                                        # N on top, 1 at the bottom
add(a)
a = list(range(2, N + 1)) + [1]
add(a)
add(merge_runs([list(range(k, min(N + 1, k + 66_667))) for k in range(1, N + 1, 66_667)]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
