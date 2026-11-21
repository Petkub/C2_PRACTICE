# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(490012)
MAXN = 200000
MAXA = 10 ** 9
tests = []


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(1 <= x <= MAXA for x in a)
    tests.append(f"{n}\n{' '.join(map(str, a))}\n")


def value(r, big=False):
    top = (MAXA - r) // 3
    x = 3 * (random.randint(top - 1000, top) if big else random.randint(0, top)) + r
    return x if x >= 1 else 3


def mix(x, y, z, big=False):
    a = [value(0, big) for _ in range(x)] + [value(1, big) for _ in range(y)] + [value(2, big) for _ in range(z)]
    random.shuffle(a)
    return a


add([3, 4, 8, 6, 7])
add([2, 3, 4, 5, 1])
add([3, 9, 6])
add([1000000000, 999999999, 999999998])
add([7])
add([2])

add([5, 5, 2])
add(mix(0, 7, 0))
add(mix(2, 0, 7))
add(mix(1, 9, 2))
add(mix(3, 2, 10))
add(mix(0, 6, 4))
add(mix(4, 5, 7))
add(mix(0, 1, 13))
add([random.randint(1, 30) for _ in range(random.randint(10, 18))])

add(mix(0, 150000, 50000))
add(mix(0, 50000, 150000))
add(mix(0, 200000, 0))
add(mix(0, 0, 200000))
add(mix(100000, 60000, 40000))
add(mix(1, 199999, 0))
add(mix(66666, 66667, 66667))
add(mix(2, 99999, 99999))
add(mix(0, 100001, 99999))
add(mix(0, 133333, 66667))
add(mix(10, 180000, 19990))
add(mix(5, 1, 199994))
add(mix(0, 150000, 50000, big=True))
add(mix(3, 66667, 133330, big=True))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
