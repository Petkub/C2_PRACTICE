# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(60019)
MAXN = 200000
MAXA = 10 ** 9
MAXC = 10 ** 4
tests = []


def add(k, A, B, a):
    n = len(a)
    assert 1 <= k <= n <= MAXN and 1 <= A <= MAXC and 1 <= B <= MAXC
    assert all(0 <= x <= MAXA for x in a)
    tests.append(f"{n} {k} {A} {B}\n{' '.join(map(str, a))}\n")


def ra(n, lo=0, hi=MAXA):
    return [random.randint(lo, hi) for _ in range(n)]


def midk(n):
    return random.randint(n // 4, 3 * n // 4)


add(3, 2, 3, [4, 1, 6, 2, 2])
add(5, 5, 6, [0, 10, 3, 7, 7, 2])
add(2, 4, 4, [5, 5, 0, 9])
add(4, 7, 7, [3, 3, 3, 3])
add(1, 9, 2, [8, 0, 1000000000])

add(1, 1, 1, [0])
add(3, 1, 10, ra(12, 0, 20))
add(4, 10, 1, ra(15, 0, 20))
add(5, 3, 7, ra(20, 0, 5))
add(7, 2, 9, ra(60, 0, 100))
add(6, 8, 3, ra(200, 0, MAXA))
add(10, 1, MAXC, ra(300, 0, 1000))
add(9, MAXC, 1, [random.choice([0, 7, 7, 7, MAXA]) for _ in range(300)])
add(300, 4, 9, ra(300))

add(midk(MAXN), 3, 7, ra(MAXN))
add(MAXN // 2, 1, MAXC, ra(MAXN))
add(MAXN // 2, MAXC, 1, ra(MAXN))
add(midk(MAXN), MAXC, MAXC - 1, [MAXA * (i % 2) for i in range(MAXN)])
add(midk(MAXN), 1, 2, sorted(ra(MAXN)))
add(midk(MAXN), 5, 2, sorted(ra(MAXN), reverse=True))
add(midk(MAXN), 6, 13, [random.choice([0, 1, 2, MAXA]) for _ in range(MAXN)])
add(midk(MAXN), 9999, 7, ra(MAXN, 0, 50))
add(MAXN // 3, 2, 3, [MAXA - random.randint(0, 3) for _ in range(MAXN)])
add(midk(MAXN), 17, 4, [(i * 7919) % 1000003 * 997 for i in range(MAXN)])
add(midk(MAXN), 1, 3, [MAXA if random.random() < 0.3 else 0 for _ in range(MAXN)])
add(3 * MAXN // 4, MAXC, 2, [random.randint(0, MAXA) if (i // 1000) % 2 else random.randint(0, 10) for i in range(MAXN)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
