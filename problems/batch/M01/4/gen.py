# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4104)
MAXN, MAXV = 100000, 10**9
tests = []


def add(packs):
    n = len(packs)
    assert 1 <= n <= MAXN
    assert all(1 <= a <= MAXV and 1 <= b <= MAXV for a, b in packs)
    tests.append(f"{n}\n" + "".join(f"{a} {b}\n" for a, b in packs))


def designs(k, big):
    if not big:
        return list(range(1, k + 1))
    return random.sample(range(1, MAXV + 1), k)


def rnd_packs(n, ds, same_share):
    out = []
    for _ in range(n):
        a = random.choice(ds)
        b = a if random.random() < same_share else random.choice(ds)
        out.append((a, b) if random.random() < 0.5 else (b, a))
    return out


def blocks(n, x, y, cxx, cyy):
    out = [(x, x)] * cxx + [(y, y)] * cyy
    out += [(x, y) if random.random() < 0.5 else (y, x) for _ in range(n - cxx - cyy)]
    random.shuffle(out)
    return out


add([(1, 2), (1, 1), (2, 2), (2, 2), (3, 1), (1, 3)])
add([(5, 5), (5, 5), (5, 5), (5, 5)])
add([(7, 7), (1000000000, 7), (1000000000, 1000000000)])
add([(4, 4), (2, 4), (4, 2), (2, 2), (3, 3), (3, 2), (4, 3)])
add([(1, 1), (6, 6), (6, 1), (8, 8), (8, 6), (1, 6), (6, 6), (8, 6)])

add([(1, 2)])
add([(1, 2), (2, 1), (1, 2)])
add([(1, 1), (2, 2), (3, 3), (1, 2), (2, 3), (3, 1)])
add(rnd_packs(12, designs(3, False), 0.4))
add(rnd_packs(40, designs(4, True), 0.3))
add(rnd_packs(150, designs(6, False), 0.5))
add(blocks(200, 11, 22, 30, 70))
add(rnd_packs(300, designs(10, True), 0.6))

N = MAXN
x, y = designs(2, True)
add([(x, y)] * N)
add(blocks(N, x, y, N // 3, N // 3))
add(blocks(N, 1, 2, 30000, 30000))
add(rnd_packs(N, designs(5, False), 0.4))
add(rnd_packs(N, designs(40, True), 0.5))
add(rnd_packs(N, designs(300, True), 0.6))
add(blocks(N, 3, 4, 10000, 50000))
ds = designs(2 * N, True)
add([(ds[2 * i], ds[2 * i + 1]) for i in range(N)])
sh = []
for g in range(100):
    a, b = designs(2, True)
    sh += blocks(N // 100, a, b, random.randint(0, 400), random.randint(0, 400))
random.shuffle(sh)
add(sh)
add([(MAXV, MAXV)] * (N // 2) + [(MAXV - 1, MAXV)] * (N // 4) + [(MAXV - 1, MAXV - 1)] * (N // 4))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
