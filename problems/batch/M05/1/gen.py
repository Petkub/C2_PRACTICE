# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(45002)
MAXN, MAXA = 200000, 10**6
tests = []

SMALL = [n for n in range(2, 1000) if all(n % d for d in range(2, n))]
PRIMES = SMALL + [n for n in range(1001, MAXA + 1, 2) if all(n % p for p in SMALL)]


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def pick(lst):
    return lst[ri(0, len(lst) - 1)]


def shuffled(a):
    a = list(a)
    for i in range(len(a) - 1, 0, -1):
        j = ri(0, i)
        a[i], a[j] = a[j], a[i]
    return a


def primes_in(lo, hi):
    return [p for p in PRIMES if lo <= p <= hi]


def add(a):
    assert 1 <= len(a) <= MAXN
    assert all(2 <= v <= MAXA for v in a)
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")


add([10, 4, 7, 6, 3])
add([18, 8, 12, 27, 9, 8])
add([999983])
add([6, 8, 9, 15, 27])
add([1000000, 999983, 524288, 2, 999999])


add([2])
add([MAXA, MAXA])
add(shuffled([2**k for k in range(1, 20)] + [3**k for k in range(1, 13)]))
add(shuffled(range(2, 61)))
add([ri(2, 50) for _ in range(30)])
add([ri(2, 1000) for _ in range(200)])
smooth = [2**a * 3**b * 5**c for a in range(20) for b in range(13) for c in range(9)
          if 2 <= 2**a * 3**b * 5**c <= MAXA]
add(shuffled(smooth))
add([ri(2, MAXA) for _ in range(2000)])
add(shuffled(range(2, 5002)))

add([ri(2, MAXA) for _ in range(20000)])
big = primes_in(60000, 111111)
add([pick([2, 4, 8, 3, 9, 6]) * pick(big) for _ in range(50000)])


N = MAXN
top = primes_in(500000, MAXA)
add([pick(top) for _ in range(N)])
add([999983] * N)
half = primes_in(250000, 499999)
quarter = primes_in(125000, 249999)
third = primes_in(170000, 333333)
sixth = primes_in(85000, 166666)
eighth = primes_in(62500, 125000)
a = []
for _ in range(N):
    k = ri(0, 5)
    if k == 0:
        a.append(pick(top))
    elif k == 1:
        a.append(2 * pick(half))
    elif k == 2:
        a.append(4 * pick(quarter))
    elif k == 3:
        a.append(3 * pick(third))
    elif k == 4:
        a.append(6 * pick(sixth))
    else:
        a.append(8 * pick(eighth))
add(a)
near = primes_in(700, 1000)
add([pick(near) * pick(near) for _ in range(N)])
add(sorted(pick(top) for _ in range(N)))
add(sorted((pick(top) for _ in range(N)), reverse=True))
p3 = primes_in(300, 499)
ninth = primes_in(60000, 111111)
p9 = primes_in(200, 330)
a = []
for _ in range(N):
    k = ri(0, 3)
    if k == 0:
        a.append(4 * pick(quarter))
    elif k == 1:
        a.append(4 * pick(p3) * pick(p3))
    elif k == 2:
        a.append(9 * pick(ninth))
    else:
        a.append(9 * pick(p9) * pick(p9))
add(a)
a = [ri(MAXA - 2000, MAXA) for _ in range(N // 2)] + [pick(top) for _ in range(N // 2)]
add(shuffled(a))
add(shuffled(range(MAXA - N + 1, MAXA + 1)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
