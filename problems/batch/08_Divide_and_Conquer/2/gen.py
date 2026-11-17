# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(80220)
MAXN = 20
MAXQ = 100_000
tests = []


def add(n, s, xs):
    assert 1 <= n <= MAXN and len(s) == 1 << n and set(s) <= {"0", "1"}
    assert 1 <= len(xs) <= MAXQ and all(1 <= x <= 1 << n for x in xs)
    tests.append(f"{n} {len(xs)}\n{s}\n" + "".join(f"{x}\n" for x in xs))


def rnd_s(n, dens=0.5):
    m = 1 << n
    if dens == 0.5:
        return format(random.getrandbits(m), "b").zfill(m)
    return "".join("1" if random.random() < dens else "0" for _ in range(m))


def rnd_x(n, q):
    return [random.randint(1, 1 << n) for _ in range(q)]


add(3, "11001001", [8, 3, 6])
add(3, "00000000", [5, 5, 8])
add(1, "11", [1, 2, 1])
add(2, "1111", [2, 4, 1, 3, 2])
add(4, "1011000101110100", [7, 16, 1, 9, 12])


add(1, "00", [1])
add(1, "10", [1, 2, 2, 1, 1, 2])
add(2, "0000", [1, 2, 3, 4, 1, 2, 3, 4])
add(5, rnd_s(5), rnd_x(5, 500))
add(8, rnd_s(8, 0.1), rnd_x(8, 2000))
add(10, rnd_s(10), rnd_x(10, 2000))
add(10, "1" * 1024, list(range(1, 1025)) + list(range(1024, 0, -1)))
add(12, "0" * 4096, [random.choice([1, 2048, 2049, 4096]) for _ in range(2000)])
add(14, rnd_s(14, 0.9), rnd_x(14, 1000))

M = 1 << MAXN
add(MAXN, rnd_s(MAXN), rnd_x(MAXN, MAXQ))
add(MAXN, "1" * M, rnd_x(MAXN, MAXQ))
add(MAXN, "0" * M, rnd_x(MAXN, MAXQ))
add(MAXN, "10" * (M // 2), [2 * random.randint(1, M // 2) for _ in range(MAXQ)])
add(MAXN, "1000" * (M // 4), [random.randint(1, M) for _ in range(MAXQ)])
add(MAXN, "0" * M, [random.choice([1, M]) for _ in range(MAXQ)])
add(MAXN, rnd_s(MAXN, 0.01), rnd_x(MAXN, MAXQ))
add(MAXN, rnd_s(MAXN, 0.99), rnd_x(MAXN, MAXQ))
add(MAXN, "01" * (M // 2), [x for k in range(MAXQ // 2) for x in (2 * k + 1, 2 * k + 1)])
add(MAXN, rnd_s(MAXN), [random.randint(1, 64) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
