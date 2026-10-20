# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(70015)
MAXN = 200_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(1 <= x <= n for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def relabel(a):
    """same graph shape with the students renumbered at random"""
    n = len(a)
    p = list(range(1, n + 1))
    random.shuffle(p)
    b = [0] * n
    for i in range(n):
        b[p[i] - 1] = p[a[i] - 1]
    return b


def rnd(n):
    return [ri(1, n) for _ in range(n)]


def broom(tail, cyc):
    """a path of `tail` students leading into a cycle of `cyc` students"""
    n = tail + cyc
    a = [0] * n
    for i in range(1, cyc + 1):
        a[i - 1] = i % cyc + 1
    for i in range(cyc + 1, n + 1):
        a[i - 1] = i - 1
    return a


def deep_forest(n, cyc, back):
    """a cycle of `cyc` students; every other student i sends to one of the `back` students just before it"""
    a = broom(0, cyc) + [0] * (n - cyc)
    for i in range(cyc + 1, n + 1):
        a[i - 1] = ri(max(1, i - back), i - 1)
    return a


def caterpillar(n, spine, cyc):
    """a long path (the spine) into a cycle; everybody else sends to a random spine student"""
    a = broom(spine, cyc) + [0] * (n - spine - cyc)
    for i in range(spine + cyc + 1, n + 1):
        a[i - 1] = ri(1, spine + cyc)
    return a


# samples
add([2, 3, 1, 1, 4])
add([1, 1, 4, 3])
add([1])
add([2, 3, 4, 5, 6, 1])
add([3, 3, 5, 2, 6, 7, 5, 7])
add([2, 1, 2, 3, 4, 10, 6, 6, 9, 8])
# hidden: small
add([2, 1])
add([1, 2, 3, 4, 5, 6, 7])                     # everybody keeps the letter
for n in (5, 9, 12, 20, 50):
    add(rnd(n))
add(relabel(broom(15, 4)))
add(relabel(deep_forest(300, 7, 3)))
add(relabel(caterpillar(2000, 600, 50)))
# hidden: large
N = MAXN
add(broom(N - 1, 1))                           # one long chain ending at a student who keeps the letter
add(relabel(broom(N - 1, 1)))
add(relabel(broom(0, N)))                      # one cycle through everybody
add(relabel(broom(N // 4 * 3, N // 4)))
add(relabel(broom(N - 2, 2)))
y = broom(N // 2, 1)                           # two long chains joining at the end
m = len(y)
y += [1] + [m + j for j in range(1, N - m)]
add(relabel(y))
add(relabel(deep_forest(N, 3, 4)))
add(relabel(deep_forest(N, 1000, 20)))
add(relabel(caterpillar(N, N // 2, 7)))
add(relabel(caterpillar(N, 3000, 50000)))
add(relabel(deep_forest(N, 50000, 2)))
add(broom(N // 2, N // 2))
add(rnd(N))
a = [1] * N                                    # everybody sends to a 2-cycle
a[0], a[1] = 2, 1
add(relabel(a))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
