# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(44006)
MAXN, MAXLEN, MAXTOTAL = 200_000, 100, 2_000_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert sum(len(s) for s in a) <= MAXTOTAL
    assert all(2 <= len(s) <= MAXLEN and s.isdigit() and s[0] != "0" for s in a)
    tests.append(f"{n}\n" + "\n".join(a) + "\n")


def ring(length, digits, m):
    r = random.sample(digits, m)
    while r[0] == "0":
        r = random.sample(digits, m)
    return "".join(r[i % m] for i in range(length))


def noise(length, digits):
    s = random.choice(digits)
    while s == "0":
        s = random.choice(digits)
    return s + "".join(random.choice(digits) for _ in range(length - 1))


def pool(count, lens, digits, sizes, noisy=0.0):
    res = []
    for _ in range(count):
        L = ri(*lens)
        if random.random() < noisy:
            res.append(noise(L, digits))
        else:
            res.append(ring(L, digits, min(random.choice(sizes), len(digits))))
    return res


def draw(n, p):
    return [p[int(random.random() * len(p))] for _ in range(n)]


D10 = "0123456789"
BIG = (10,)

add(["312", "2196", "58", "6907", "74"])
add(["45", "7117", "23", "60"])
add(["12"])
add(["12", "34", "56"])
add(["4412", "75", "5568", "2588", "23", "85"])
add(["10293847561029384756", "24", "65473829105647382901", "13579024681357902468", "86420975318642097531"])

add(["121", "343"])
add(["10", "10", "10"])
add(["91", "19", "91", "19"])
add(pool(8, (2, 3), D10, BIG, 0.3))
add(pool(12, (2, 5), "1234", (2, 3, 4, 4, 4)))
add(pool(30, (2, 4), D10, BIG, 0.1))
add(pool(100, (2, 8), "13579", (1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)))
add(pool(300, (2, 6), D10, BIG))
add(pool(2000, (2, 100), D10, (3, 4, 5, 6, 7, 8, 9, 10)))

N = MAXN
add(draw(N, pool(3000, (2, 2), D10, BIG)))
add(draw(N, pool(3000, (2, 9), D10, BIG)))
add(draw(N, pool(3000, (2, 9), D10, BIG, 0.004)))
add(draw(N, pool(3000, (3, 9), D10, (2,) + BIG * 99)))
add(draw(N, pool(3000, (2, 6), "1357", (4,))))
add(draw(N, pool(3000, (2, 6), "02468", (5,))))
add(draw(N, pool(3000, (4, 10), D10, (1, 2), 0.5)))
a = draw(N, pool(3000, (2, 4), "0123", (4,)))[:N // 2] + draw(N, pool(3000, (2, 4), "56789", (5,)))[:N - N // 2]
add(a)
a = [ring(10, D10, 10)] + draw(N - 1, pool(3000, (2, 8), D10, (8, 9, 10)))
add(a)
add(["10"] * N)
add(draw(N, pool(3000, (2, 5), "019", (3,))))
add(draw(N, pool(3000, (2, 9), D10, (2,) + BIG * 1999)))

add(draw(20_000, pool(3000, (90, 100), D10, (3, 4, 5, 6, 7, 8, 9, 10), 0.0005)))
add(draw(50_000, pool(3000, (2, 9), D10, (2,) + BIG * 499)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
