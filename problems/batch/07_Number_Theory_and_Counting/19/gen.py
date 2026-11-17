# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random
from math import gcd

random.seed(141901)
MAXQ = 100_000
MAXV = 10 ** 18
SMALL = 1 << 21
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def a_pair(n):
    x, y = 1, 1
    for b in bin(n)[3:]:
        if b == "1":
            x = x + y
        else:
            y = x + y
    return x, y


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    for qu in qs:
        if qu[0] == 1:
            assert len(qu) == 2 and 1 <= qu[1] <= MAXV
        else:
            assert len(qu) == 3 and 1 <= qu[1] <= MAXV and 1 <= qu[2] <= MAXV and gcd(qu[1], qu[2]) == 1
    tests.append(f"{len(qs)}\n" + "".join(" ".join(map(str, qu)) + "\n" for qu in qs))


def from_n(n):
    u, v = a_pair(n)
    return (2, u, v)


def rand_coprime(lo, hi):
    while True:
        u, v = ri(lo, hi), ri(lo, hi)
        if gcd(u, v) == 1:
            return (2, u, v)


fib = [1, 1]
while fib[-1] + fib[-2] <= MAXV:
    fib.append(fib[-1] + fib[-2])
F1, F2 = fib[-2], fib[-1]


def huge_quotient():

    c = ri(0, 5)
    if c == 0:
        return (2, 1, ri(MAXV // 2, MAXV))
    if c == 1:
        return (2, ri(MAXV // 2, MAXV), 1)
    if c == 2:
        k = ri(2, 1000)
        return (2, k, k * ri(MAXV // 2000, (MAXV - 1) // k) + 1)
    if c == 3:
        k = ri(2, 1000)
        return (2, k * ri(MAXV // 2000, (MAXV - 1) // k) + 1, k)
    if c == 4:
        return (2, 2, 2 * ri(MAXV // 4, MAXV // 2 - 1) + 1)
    return (2, MAXV - 1, MAXV)


add([(1, 5), (1, 10), (2, 3, 2), (2, 1, 1)])
add([(2, 1, 4), (2, 4, 1), (2, 2, 7)])
add([(1, MAXV), (2, 1, MAXV), (2, MAXV, 1)])
add([(1, 1), (1, 2), (2, 1, 2), (2, 2, 1), (1, 1000)])
add([(2, 832040, 514229), (2, 7, 1000), (1, 123456789), (1, 1 << 40)])

add([(1, n) for n in range(1, 301)] + [from_n(n) for n in range(1, 301)])
add([(1, 1), (1, (1 << 59) + 1), (2, F1, F2), (2, F2, F1), (2, 999_999_999_999, 1_000_000_000_000)])
add([(1, ri(1, SMALL)) for _ in range(3000)] + [from_n(ri(1, SMALL - 1)) for _ in range(3000)])
add([from_n(n) for n in [SMALL - 1, SMALL - 2, SMALL // 2, SMALL // 2 - 1, (SMALL // 3) | 1, 1, 2, 3]] +
    [(1, SMALL), (1, SMALL - 1), (1, SMALL // 2)])
qs = [from_n(ri(1, SMALL - 1)) if i % 2 else (1, ri(1, SMALL)) for i in range(5000)]
add(qs)

add([(1, ri(1, MAXV)) for _ in range(MAXQ)])
add([rand_coprime(1, MAXV) for _ in range(MAXQ)])
add([huge_quotient() for _ in range(MAXQ)])
add([(2, F1, F2), (2, F2, F1)] * (MAXQ // 2))
add([huge_quotient() if i % 3 == 0 else rand_coprime(1, MAXV) for i in range(MAXQ)])
add([huge_quotient() if i % 2 else (1, ri(MAXV // 2, MAXV)) for i in range(MAXQ)])
add([(1, MAXV - ri(0, 10 ** 6)) if i % 2 else from_n(ri(MAXV // 2, MAXV)) for i in range(MAXQ)])
add([from_n(ri(1, MAXV)) if i % 4 else huge_quotient() for i in range(MAXQ)])
add([(2, 1, ri(1, MAXV)) if i % 2 else (2, ri(1, MAXV), 1) for i in range(MAXQ)])
add([huge_quotient() if i % 10 == 0 else rand_coprime(1, 10 ** 6) for i in range(MAXQ)])
add([rand_coprime(1, MAXV) if i % 50 else huge_quotient() for i in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
