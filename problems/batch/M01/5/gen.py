# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4105)
MAXN, MAXL, MAXS, MAXT = 100000, 10**9, 1000, 200000
tests = []


def add(L, floors):
    n = len(floors)
    assert 1 <= n <= MAXN and 1 <= L <= MAXL
    assert sum(len(st) for _, st in floors) <= MAXT
    for i, (s, st) in enumerate(floors):
        assert 1 <= s <= MAXS
        assert len(set(st)) == len(st) and all(1 <= q <= L for q in st)
        assert (len(st) == 0) == (i == n - 1)
    out = [f"{n} {L}"]
    for s, st in floors:
        out.append(" ".join(map(str, [s, len(st)] + st)))
    tests.append("\n".join(out) + "\n")


def rooms(L, t):
    if t * 3 >= L:
        r = random.sample(range(1, L + 1), t)
    else:
        r = set()
        while len(r) < t:
            r.add(random.randint(1, L))
        r = list(r)
        random.shuffle(r)
    return r


def building(L, ts, smax):
    floors = [(random.randint(1, smax), rooms(L, t)) for t in ts]
    floors.append((random.randint(1, smax), []))
    return floors


def heavy(L, n, heavy_t, at, smax):
    ts = [1] * (n - 1)
    ts[at] = ts[at + 1] = heavy_t
    return building(L, ts, smax)


add(10, [(2, [9, 4]), (5, [3]), (1, [])])
add(5, [(3, [])])
add(1, [(7, [1]), (7, [])])
add(1000000000, [(1, [1000000000]), (1000, [1000000000]), (1000, [1000000000]), (1000, [])])
add(8, [(3, [2, 7]), (1, [5, 8]), (4, [6, 3, 5]), (2, [])])

add(7, [(2, [3, 6]), (9, [5]), (3, [1, 3]), (5, [])])
add(8, [(5, [3, 6]), (7, [2, 4]), (9, [3, 4, 5]), (2, [])])
add(1, [(MAXS, [1])] * 5 + [(MAXS, [])])
add(MAXL, [(MAXS, [])])
add(20, building(20, [random.randint(1, 6) for _ in range(6)], 9))
add(50, building(50, [random.randint(1, 10) for _ in range(20)], 100))
add(1000, building(1000, [random.randint(1, 200) for _ in range(30)], MAXS))
add(MAXL, building(MAXL, [random.randint(1, 50) for _ in range(300)], MAXS))

add(MAXL, building(MAXL, [100000, 99999], MAXS))
add(MAXL, heavy(MAXL, 3, 99999, 0, MAXS))
add(200000, building(200000, [100000, 100000], 10))
add(MAXL, heavy(MAXL, 1000, 99500, 400, MAXS))
add(MAXL, heavy(MAXL, 20000, 90000, 7000, MAXS))
add(MAXL, [(MAXS, rooms(MAXL, 99999)), (MAXS, rooms(MAXL, 99999)), (MAXS, [1]), (MAXS, [])])
add(100000, building(100000, [100000, 100000], MAXS))
add(MAXL, heavy(MAXL, 5000, 97000, 2500, 3))
f = building(MAXL, [99000, 99000], MAXS)
f[0] = (1, [2] + [q for q in f[0][1] if q != 2])
add(MAXL, f)
add(MAXL, [(1, [2]), (MAXS, rooms(MAXL, 99998)), (MAXS, rooms(MAXL, 99998)), (MAXS, [])])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
