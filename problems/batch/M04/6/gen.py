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


def plain(length, digits):
    s = [random.choice([d for d in digits if d != "0"])]
    while len(s) < length:
        c = random.choice(digits)
        if c != s[-1] and (len(s) < 2 or c != s[-2]):
            s.append(c)
    return "".join(s)


def rich(length, digits, odd=False):
    s = list(plain(length, digits))
    k = ri(0, length - 3) if odd and length >= 3 else ri(0, length - 2)
    if odd and length >= 3:
        s[k + 2] = s[k]
    else:
        s[k + 1] = s[k]
    if s[0] == "0":
        s[0] = "1"
    return "".join(s)


def pool(count, lens, digits, rich_share=0.0, odd=False):
    res = []
    for _ in range(count):
        L = ri(*lens)
        res.append(rich(L, digits, odd) if random.random() < rich_share else plain(L, digits))
    return res


def draw(n, p):
    return [p[int(random.random() * len(p))] for _ in range(n)]


D10 = "0123456789"

add(["312", "2196", "58", "6907", "74"])
add(["45", "7117", "23", "60"])
add(["12"])
add(["12", "34", "56"])
add(["4412", "75", "5568", "2588", "23", "85"])
add(["10293847561029384756", "24", "65473829105647382901", "13579024681357902468", "86420975318642097531"])

add(["121", "343"])
add(["10", "10", "10"])
add(["91", "19", "91", "19"])
for n, lens, digs, rs in [(8, (2, 3), D10, 0.1), (12, (2, 5), "1234", 0.1), (30, (2, 4), D10, 0.05),
                          (100, (2, 8), "13579", 0.02), (300, (2, 6), D10, 0.0)]:
    add(pool(n, lens, digs, rs, odd=random.random() < 0.5))
add(pool(2000, (2, 100), D10, 0.0))

N = MAXN
add(draw(N, pool(3000, (2, 2), D10)))
add(draw(N, pool(3000, (2, 9), D10, 0.0)))
add(draw(N, pool(3000, (2, 9), D10, 0.003)))
add(draw(N, pool(3000, (3, 9), D10, 0.01, odd=True)))
add(draw(N, pool(3000, (2, 6), "1357", 0.0)))
add(draw(N, pool(3000, (2, 6), "02468", 0.0)))
add(draw(N, pool(3000, (2, 10), D10, 1.0)))
a = draw(N, pool(3000, (2, 4), "0123", 0.0)) [:N // 2] + draw(N, pool(3000, (2, 4), "56789", 0.0))[:N - N // 2]
add(a)
a = [plain(10, D10) for _ in range(1)] + draw(N - 1, pool(3000, (2, 8), D10, 0.0))
add(a)
add(["10"] * N)
add(draw(N, pool(3000, (2, 5), "019", 0.0)))
add(draw(N, pool(3000, (2, 9), D10, 0.0005, odd=True)))

add(draw(20_000, pool(3000, (90, 100), D10, 0.0005)))
add(draw(50_000, pool(3000, (2, 9), D10, 0.002, odd=True)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
