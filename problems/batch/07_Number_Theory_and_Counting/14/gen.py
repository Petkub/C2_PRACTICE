# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(141001)
MAXN = 300_000
MAXA = 10 ** 7
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(a):
    assert 1 <= len(a) <= MAXN
    for x in a:
        assert 1 <= x <= MAXA
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")


SMALLP = [p for p in range(2, 3200) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
LO = MAXA - 200_000
mark = bytearray([1]) * (MAXA - LO + 1)
for p in SMALLP:
    for m in range((LO + p - 1) // p * p, MAXA + 1, p):
        mark[m - LO] = 0
BIGP = [LO + i for i in range(len(mark)) if mark[i]]


SMOOTH = [1]
for p in (2, 3, 5, 7, 11, 13):
    SMOOTH = [v * p ** e for v in SMOOTH for e in range(24) if v * p ** e <= MAXA]
SMOOTH.sort()


def smooth():
    return random.choice(SMOOTH)


def mostly(n, base, share):
    return [base * ri(1, MAXA // base) if random.random() < share else ri(1, MAXA) for _ in range(n)]


def spread(n, p, share):
    maxe = 1
    while p ** (maxe + 1) <= MAXA:
        maxe += 1
    out = []
    while len(out) < n:
        if random.random() < share:
            pe = p ** ri(1, maxe)
            v = pe * ri(1, MAXA // pe)
            while v % (p * pe) == 0:
                v //= p
        else:
            v = ri(1, MAXA)
            while v % p == 0:
                v //= p
        out.append(v)
    return out


MID = [p for p in SMALLP if 2000 <= p <= 3162]


add([12, 18])
add([5, 6, 30])
add([MAXA])
add([1, 2, 4, 8, 16])
add([9_699_690, 1, 720, 1024, 7_999_993, 360, 9_699_690])

add([1])
add([1] * 50)
add([ri(1, 50) for _ in range(40)])
add([ri(1, MAXA) for _ in range(300)])
add([smooth() for _ in range(300)])
add(mostly(300, 2 ** 10 * 3 ** 4, 0.6))
add([2 ** ri(0, 23) for _ in range(301)])
add([6] * 120 + [1] * 80 + [2 ** 23] * 50 + [3 ** 14] * 51)

add([random.choice(BIGP) for _ in range(MAXN)])
add([ri(1, MAXA) for _ in range(MAXN)])
add([smooth() for _ in range(MAXN)])
add(mostly(MAXN, 2 ** 8 * 3 ** 3 * 5, 0.55))
add(mostly(MAXN, 2 ** 15 * 7, 0.51))
add([2 ** 23] * MAXN)
add([2 ** ri(0, 23) for _ in range(MAXN)])
add([9_699_690 if i % 2 else random.choice(BIGP) for i in range(MAXN)])
add([1] * (MAXN // 2) + [9_699_690] * (MAXN // 2))
add([random.choice([2 ** 23, 3 ** 14, 5 ** 10, 7 ** 8, 1]) if i % 4 == 0 else random.choice(BIGP) for i in range(MAXN)])
add([MAXA - ri(0, 1000) if i % 5 == 0 else random.choice(MID) * random.choice(MID[-60:]) for i in range(MAXN)])
add(spread(MAXN, 5, 0.52))
add(mostly(MAXN, 9_699_690, 0.7))
add(spread(MAXN, 2, 0.6))
add(spread(MAXN, 3, 0.53))
add([random.choice(MID) * random.choice(MID[-60:]) if i % 2 else random.choice(BIGP) for i in range(MAXN)])
add([random.choice(BIGP) if i % 3 else 2 ** ri(1, 23) for i in range(MAXN)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
