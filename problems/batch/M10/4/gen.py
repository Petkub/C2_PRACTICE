# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(500004)
MAXT = 30000
MAXQ = 1000
MAXM = 10 ** 6
MAXC = 1000
MAXS = 10 ** 6
tests = []
R = random.randint


def add(cases):
    assert 1 <= len(cases) <= MAXT
    for q, m1, c1, m2, c2, s, l in cases:
        assert 2 <= q <= MAXQ and 0 <= m1 <= MAXM and 0 <= m2 <= MAXM and m1 + m2 >= 1
        assert 1 <= c1 <= MAXC and 1 <= c2 <= MAXC and 0 <= s <= MAXS and 0 <= l <= MAXS and s + l >= 1
    tests.append(f"{len(cases)}\n" + "".join(" ".join(map(str, c)) + "\n" for c in cases))


def full():
    m1, m2 = R(0, MAXM), R(0, MAXM)
    if m1 + m2 == 0:
        m1 = 1
    return (R(2, MAXQ), m1, R(1, MAXC), m2, R(1, MAXC), R(0, MAXS), R(1, MAXS))


def few():
    m1, m2 = R(0, 3), R(0, 3)
    if m1 + m2 == 0:
        m2 = 1
    return (R(500, MAXQ), m1, R(500, MAXC), m2, R(500, MAXC), R(0, MAXS), R(1, MAXS))


def long_heavy():
    m1, m2 = R(1, 2000), R(0, 2000)
    q = R(100, MAXQ)
    return (q, m1, R(10, 100), m2, R(100, MAXC), R(0, 1000), min(MAXS, (m1 + m2) * R(1, 3) + R(1, 50)))


def one_kind():
    q, m, c, s, l = R(2, MAXQ), R(1, MAXM), R(1, MAXC), R(0, MAXS), R(1, MAXS)
    other_c = R(1, MAXC)
    return (q, m, c, 0, other_c, s, l) if R(0, 1) else (q, 0, other_c, m, c, s, l)


def same_speed():
    c = R(1, MAXC)
    return (R(2, MAXQ), R(0, 1000), c, R(1, 1000), c, R(0, MAXS), R(1, MAXS))


def worst():
    return (MAXQ, 0, MAXC, 1, MAXC, MAXS, MAXS) if R(0, 1) else (MAXQ, 1, MAXC, 0, R(1, MAXC), MAXS, MAXS)


def mixed(fns, cnt):
    return [random.choice(fns)() for _ in range(cnt)]


add([(3, 2, 1, 1, 2, 5, 2)])
add([(2, 0, 5, 3, 4, 7, 0), (10, 1, 1, 0, 1, 0, 1)])
add([(4, 3, 2, 2, 3, 20, 3)])
add([(2, 1, 1, 1, 1, 1, 1), (7, 2, 1, 3, 4, 30, 2), (3, 1, 7, 2, 2, 0, 2)])
add([(2, 1, 1, 0, 9, 0, 3)])


small = []
for _ in range(60):
    m1, m2 = R(0, 3), R(0, 3)
    if m1 + m2 == 0:
        m1 = 1
    s, l = R(0, 8), R(0, 5)
    if s + l == 0:
        l = 1
    small.append((R(2, 5), m1, R(1, 4), m2, R(1, 4), s, l))
add(small)
small = []
for _ in range(60):
    m1, m2 = R(1, 2), R(1, 3)
    small.append((R(3, 6), m1, R(1, 2), m2, R(3, 6), R(0, 3), R(1, 7)))
add(small)
add([(R(2, 4), 1, 1, 1, R(2, 5), R(0, 4), R(1, 4)) for _ in range(40)])


add(mixed([full, long_heavy, one_kind, same_speed], 2000))
add(mixed([few, long_heavy], 2000))


add(mixed([full], MAXT))
add(mixed([few], MAXT))
add(mixed([long_heavy], MAXT))
add(mixed([one_kind], MAXT))
add(mixed([same_speed], MAXT))
add(mixed([worst, few, full], MAXT))
add(mixed([full, few, long_heavy, one_kind, same_speed, worst], MAXT))
add(mixed([long_heavy, few], MAXT))
add(mixed([long_heavy, one_kind], MAXT))
add(mixed([full, long_heavy], MAXT))
add(mixed([worst], MAXT))
add(mixed([few, same_speed, long_heavy], MAXT))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
