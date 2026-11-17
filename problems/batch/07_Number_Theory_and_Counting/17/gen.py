# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(141701)
MAXN = 200_000
MAXA = 10 ** 6
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(a):
    assert 1 <= len(a) <= MAXN
    for v in a:
        assert 1 <= v <= MAXA
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")


add([2, 4, 6])
add([4, 4, 6])
add([7])
add([1, 1, 1, 1])
add([12, 18, 30, 45, 1000000])

add([MAXA])
add([ri(1, 12) for _ in range(10)])
add([ri(1, 60) for _ in range(16)])
add([6 * ri(1, 50) for _ in range(18)])
add([ri(1, MAXA) for _ in range(300)])
add([720720 // ri(1, 16) for _ in range(2000)])
add([random.choice([2, 3, 5, 7, 11, 13]) * ri(1, 1000) for _ in range(3000)])

add([ri(1, MAXA) for _ in range(MAXN)])
add(random.sample(range(1, MAXA + 1), MAXN))
add(random.sample(range(MAXA - 400_000, MAXA + 1), MAXN))
add([MAXA] * MAXN)
mix = [MAXA] * (MAXN - 3000) + random.sample(range(1, MAXA), 3000)
random.shuffle(mix)
add(mix)
add([ri(1, 33) * 30030 if i % 4 else ri(1, MAXA) for i in range(MAXN)])
add([random.choice([720720, 360360, 554400, 831600, 942480, 997920]) // random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
     for _ in range(MAXN)])
add([2 * ri(1, MAXA // 2) for _ in range(MAXN)])
add([ri(1, MAXA) if i % 2 else 1 for i in range(MAXN)])
add(list(range(MAXA - MAXN + 1, MAXA + 1)))
add([ri(MAXA // 2, MAXA) for _ in range(MAXN)])
add([random.choice([999983, 999979, 2 * 499979, 999961]) if i % 10 else ri(1, MAXA) for i in range(MAXN)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
