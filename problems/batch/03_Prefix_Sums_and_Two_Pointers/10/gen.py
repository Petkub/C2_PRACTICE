# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(10110)
MAXN = 200_000
tests = []


def add(t, c):
    n, k = len(t), len(c)
    assert 1 <= k <= n <= MAXN
    assert all(1 <= x <= k for x in t)
    assert all(1 <= x <= n for x in c)
    tests.append(f"{n} {k}\n" + " ".join(map(str, t)) + "\n" + " ".join(map(str, c)) + "\n")


def rnd(n, k):
    return [random.randint(1, k) for _ in range(n)]


# samples
add([1, 2, 1, 3, 2, 2, 1, 3, 1, 2], [2, 1, 1])
add([1, 1, 2, 1, 1], [1, 2])
add([1, 1, 1], [1])
add([2, 1, 1, 3, 2, 2, 3, 1], [1, 1, 1])
add([3, 1, 2, 1, 3], [2, 1, 2])
add([2, 2, 1, 2, 1, 2, 2], [1, 3])
# hidden (small)
add([1], [1])
add([1, 1, 2], [3, 1])                      # not enough of type 1
add([1, 2, 3, 4], [1, 1, 1, 1])
add([1, 2, 1, 2, 1, 2], [1, 1])             # many ties
add([5, 1, 2, 3, 4], [1, 1, 1, 1, 1])
add(rnd(30, 3), [2, 3, 1])
add(rnd(200, 5), [random.randint(1, 8) for _ in range(5)])
add(rnd(2000, 40), [random.randint(1, 30) for _ in range(40)])
t = rnd(3000, 10)
add(t, [t.count(j) for j in range(1, 11)])   # need every stamp: the whole street (or a trimmed piece)
# large
N = MAXN
t = rnd(N, 2)
add(t, [t.count(1) - 5, 3])                  # almost every stamp of type 1
t = [2] + rnd(N - 2, 1) + [2]
add(t, [1, 2])                               # the only type-2 stamps are at both ends
t = rnd(N, 50)
add(t, [t.count(j) // 2 + 1 for j in range(1, 51)])
t = list(range(1, N + 1))
random.shuffle(t)
add(t, [1] * N)                              # K = N: the whole street
t = rnd(N, 3)
add(t, [t.count(1), 1, 1])
t = rnd(N, 1000)
add(t, [1] * 999 + [N])                      # impossible (type 1000 is too rare)
add([1] * (N - 1) + [2], [N - 1, 1])
t = list(range(1, 100_001)) * 2
random.shuffle(t)
add(t, [1] * 100_000)
t = [1 + (i % 7) for i in range(N)]
add(t, [N // 7 - 3] * 7)
t = rnd(N, 20)
add(t, [random.randint(1, 3) for _ in range(20)])
t = rnd(N, 5)
add(t, [N // 5 - 2000] * 5)
add([1, 2] * (N // 2), [N // 2, N // 2 - 1])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
