# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(44004)
MAXN = 300_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(x):
    n = len(x)
    assert 1 <= n <= MAXN
    assert sorted(x) == list(range(1, n + 1))
    tests.append(f"{n}\n" + " ".join(map(str, x)) + "\n")


def build(n, cycles):
    x = list(range(1, n + 1))
    used = [False] * n
    for cyc in cycles:
        assert sum(cyc) == 0
        for _ in range(200):
            p = ri(0, n - 1)
            seats, cur = [], p
            for t in cyc:
                seats.append(cur)
                cur = (cur + t) % n
            if len(set(seats)) == len(seats) and not any(used[s] for s in seats):
                break
        else:
            continue
        for i, s in enumerate(seats):
            used[s] = True
            x[s] = (s + cyc[i]) % n + 1
    add(x)


def three(a, b):
    return [a, b, -(a + b)]


def rnd_cycles(n, k, right, left):
    res = []
    for _ in range(k):
        if random.random() < 0.5:
            a, b = ri(*right), ri(*right)
            if a + b < n:
                res.append(three(a, b))
        else:
            a, b = ri(*left), ri(*left)
            if a + b < n:
                res.append(three(-a, -b))
    return res


add([2, 7, 1, 3, 4, 5, 6])
add([1, 5, 2, 3, 4])
add([1, 2, 3, 4])
add([1, 6, 7, 5, 4, 2, 3, 8])
add([7, 1, 3, 6, 2, 4, 8, 5, 9])
add([4, 5, 6, 1, 2, 3])

add([1])
add([2, 1])
for n in [10, 25, 40]:
    build(n, rnd_cycles(n, ri(1, 4), (1, n // 3), (1, n // 2)))
p = list(range(1, 1001))
random.shuffle(p)
add(p)
build(5000, rnd_cycles(5000, 30, (1, 400), (1, 2000)))
build(20000, [three(1, 2), [5000, -5000], three(-30, -40)])

N = MAXN
p = list(range(1, N + 1))
random.shuffle(p)
add(p)
add([(i + 123_456) % N + 1 for i in range(N)])
add(list(range(1, N + 1)))
build(N, rnd_cycles(N, 20, (1, 40_000), (1, 120_000)))
build(N, rnd_cycles(N, 200, (1, 100_000), (1, 30_000)))
build(N, [[1, -1], three(-2, -3), [60_000, 70_000, -130_000], [-1000, 1000]])
build(N, [three(10, 20), three(-99_000, -100_000), three(1, 49_000)])
build(N, rnd_cycles(N, 5000, (1, 1000), (1, 140_000)))
build(N, [[i, -i] for i in range(1, 6)] + [three(70_000, 70_001)])
for k, right, left in [(12, (1, 20_000), (1, 90_000)), (8, (1, 90_000), (1, 140_000)),
                       (20, (1, 90_000), (1, 90_000)), (5, (1, 20_000), (1, 30_000)), (12, (1, 20_000), (1, 140_000)),
                       (8, (1, 20_000), (1, 140_000))]:
    build(N, rnd_cycles(N, k, right, left))

build(150_000, [three(2, 3), three(-40_000, -1), [74_000, -74_000]])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
