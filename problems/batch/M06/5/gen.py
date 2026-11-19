# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4604)
MAXN, MAXA = 300000, 10**9
tests = []


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def shuffled(a):
    a = a[:]
    random.shuffle(a)
    return a


def blocks(n, k, inside, between, expo=False):
    a, base = [], 1
    for g in range(k):
        size = n // k + (1 if g < n % k else 0)
        part = []
        for _ in range(size):
            part.append(base)
            base += int(random.expovariate(1 / inside)) if expo else random.randint(0, inside)
        random.shuffle(part)
        a += part
        base += between + random.randint(0, between)
    return a


def near_sorted(n, swaps, reach, hi):
    a = sorted(rnd(n, 1, hi))
    for _ in range(swaps):
        i = random.randrange(n - 1)
        j = min(n - 1, i + random.randint(1, reach))
        a[i], a[j] = a[j], a[i]
    return a


add([7, 3, 3, 12, 13])
add([6, 26, 17, 26, 27])
add([2, 5, 5, 9])
add([12, 10, 12, 17, 28, 32])
add([MAXA, 1])

add([5])
add([4, 4, 4])
add([3, 1, 2])
add([5, 1, 2, 3, 4])
add([10, 20, 30, 1, 2, 3])
add(shuffled(rnd(8, 1, 20)))
add(blocks(40, 4, 3, 50))
add(near_sorted(60, 5, 3, 1000))
add(shuffled(rnd(300, 1, 50)))
add(blocks(1500, 10, 1000, 100000))
add(shuffled(rnd(2000, 1, MAXA)))

N = MAXN
add(shuffled(rnd(N, 1, MAXA)))
add(sorted(rnd(N, 1, MAXA), reverse=True))
a = sorted(rnd(N, 1, MAXA))
add([a[-1]] + a[:-1])
add(blocks(N, 50, 2800, 10**6, True))
add(blocks(N, 300, 2400, 500000, True))
a = sorted(rnd(N, 1, MAXA))
add(a[1:] + [a[0]])
a = sorted(rnd(N, 1, MAXA))
add(a[N // 2:] + a[:N // 2])
add(blocks(N, 2, 2500, MAXA // 10, True))
a = near_sorted(N, 30000, 50, MAXA)
add([max(a)] + a[:-1] if max(a) == a[-1] else a)
add(shuffled(rnd(N - 1, 1, MAXA)) + [MAXA])
add(blocks(N, 1000, 2700, 100000, True))
add(near_sorted(N, 5000, 100000, MAXA))

add(shuffled(rnd(100000, 1, 1000)))
add(near_sorted(100000, 500, 20, 10**6))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
