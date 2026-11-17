# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(140901)
MAXN = 200_000
MAXA = 10 ** 8
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(a):
    assert 1 <= len(a) <= MAXN
    for x in a:
        assert 1 <= x <= MAXA
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")


def smooth(n, hi=MAXA):
    out = []
    while len(out) < n:
        v = 2 ** ri(10, 26) * 3 ** ri(0, 6) * 5 ** ri(0, 3)
        if v <= hi:
            out.append(v)
    return out


add([6, 4, 2])
add([12, 18, 5, 10])
add([MAXA])
add([MAXA] * 3)
add([36, 24, 60, 7, 14, 28, 56, 1])

add([1])
add([ri(1, 30) for _ in range(50)])
add([ri(1, MAXA) for _ in range(2000)])
add(smooth(2000))
add([720720 * ri(1, 138) for _ in range(1500)])
add([MAXA] * 2999 + [1])

add([MAXA] * MAXN)
add([MAXA] * (MAXN - 1) + [1])
add([1] + [MAXA] * (MAXN - 1))
add([ri(1, MAXA) for _ in range(MAXN)])
add(smooth(MAXN - 1) + [1])
add([2 ** 26] * (MAXN // 2) + smooth(MAXN // 2 - 1) + [3])
add([67_108_864 if i % 1000 else 99_999_989 for i in range(MAXN)])
add([2 ** 26 >> (i * 27 // MAXN) for i in range(MAXN)])
add([ri(1, 10) * 9_999_991 for _ in range(MAXN - 1)] + [ri(1, 9_999_990)])
add([720720 * ri(1, 138) for _ in range(MAXN - 1)] + [1])
add([2 * ri(1, MAXA // 2) for _ in range(MAXN - 1)] + [99_999_989])
add([ri(1, 1000) for _ in range(MAXN)])
add([MAXA - (i % 2) for i in range(MAXN)])
add(sorted(smooth(MAXN)))

add([6 * ri(1, MAXA // 6) for _ in range(MAXN // 2)] + [35 * ri(1, MAXA // 35) for _ in range(MAXN // 2)])
add([2 ** 26] * (MAXN // 2) + [3 ** 16] * (MAXN // 2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
