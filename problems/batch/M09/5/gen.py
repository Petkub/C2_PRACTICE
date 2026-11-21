# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(490005)
MAXT = 200000
MAXP = 10 ** 9
tests = []


def add(k, shelves):
    t = sum(len(s) for s in shelves)
    assert 2 <= k and 1 <= len(shelves) and 1 <= t <= MAXT
    assert all(len(s) >= 1 for s in shelves)
    count = {}
    for s in shelves:
        for p in s:
            assert 1 <= p <= MAXP
            count[p] = count.get(p, 0) + 1
    assert all(c == k for c in count.values())
    tests.append(f"{len(shelves)} {k}\n" + "".join(f"{len(s)} {' '.join(map(str, s))}\n" for s in shelves))


def distinct_prices(n, lo=1, hi=MAXP):
    return sorted(random.sample(range(lo, hi + 1), n))


def cut(seq, r):
    pos = sorted(random.sample(range(1, len(seq)), r - 1)) if r > 1 else []
    return [seq[a:b] for a, b in zip([0] + pos, pos + [len(seq)])]


def layout(k, upper, inner):
    rows, fi = [], 0
    for e in upper:
        seg = [e]
        for _ in range(k - 1):
            for _ in range(random.randint(0, 2)):
                if fi < len(inner):
                    seg += [inner[fi]] * k
                    fi += 1
            seg.append(e)
        rows.append(seg)
    while fi < len(inner):
        rows.append([inner[fi]] * k)
        fi += 1
    random.shuffle(rows)
    return rows


def build(k, models, r, rank, scramble=0, same=False):
    nf = len(models) * 2 // 5
    inner, upper = models[:nf], models[nf:]
    random.shuffle(inner)
    special = upper[len(upper) - 1 - rank] if rank is not None else None
    rest = [e for e in upper if e != special]
    spread = [e for e in rest if special is not None and e < special][:scramble]
    spread_set = set(spread)
    rest = [e for e in rest if e not in spread_set]
    random.shuffle(rest)
    segs = layout(k, rest, inner)
    assert len(segs) >= r >= 1
    tail = 5 if len(segs) >= r + 10 else 1
    pos = sorted(random.sample(range(1, len(segs) - tail), r - 2)) + [len(segs) - tail] if r > 1 else []
    shelves = [segs[a:b] for a, b in zip([0] + pos, pos + [len(segs)])]
    def put_late(x, g):
        shelves[x].insert(len(shelves[x]) - random.randint(0, min(3, len(shelves[x]))), g)
    if special is not None:
        if r == 1 or same:
            x = r - 1
            other = next(g for g in shelves[x] if g[0] > special) if any(g[0] > special for g in shelves[x]) else None
            if other is None:
                x = next(i for i in range(r) if any(g[0] > special for g in shelves[i]))
                other = next(g for g in shelves[x] if g[0] > special)
            shelves[x].remove(other)
            shelves[r - 1] += [[special], other, [special] * (k - 1)]
        else:
            put_late(r - 2, [special])
            put_late(r - 1, [special] * (k - 1))
    for e in spread:
        for _ in range(k):
            put_late(random.choice([r - 1, max(0, r - 2)]), [e])
    return [[p for g in sh for p in g] for sh in shelves]


add(2, [[5, 8, 8, 5, 2, 2], [7, 7, 1, 3, 1, 3]])
add(3, [[4, 4, 4, 9, 9, 9], [1, 1, 1]])
add(3, [[3, 10, 10, 10, 3, 3], [1, 1, 1], [7, 7, 7]])
add(2, [[1, 1000000000, 1000000000, 1]])
add(2, [[2, 2, 5, 9, 9, 5], [3, 3]])

add(2, [[9, 1, 1, 9]])
add(2, [[4, 6, 4, 6], [8, 8]])
add(2, build(2, distinct_prices(10, 1, 50), 2, 2))
add(3, build(3, distinct_prices(8, 1, 40), 3, 1))
add(2, build(2, distinct_prices(12, 1, 100), 1, None))
add(4, build(4, distinct_prices(6, 1, 30), 2, 0))
add(2, [random.sample([p for p in range(1, 9) for _ in range(2)], 16)])

add(1000, build(1000, distinct_prices(150), 4, 10))
add(2, build(2, distinct_prices(20000), 3, None))
add(2, cut(random.sample([p for p in distinct_prices(10000) for _ in range(2)], 20000), 2))

add(2, build(2, distinct_prices(100000), 2, 50, same=True))
add(2, build(2, distinct_prices(100000), 3, 200, scramble=500))
add(3, build(3, distinct_prices(66666), 10, 30))
add(2, build(2, distinct_prices(100000), 1000, 100, scramble=50))
add(4, build(4, distinct_prices(50000), 2, 20, same=True))
add(2, build(2, distinct_prices(100000, MAXP - 200000, MAXP), 2, 5))
add(2, build(2, distinct_prices(100000), 50000, 300))
add(3, build(3, distinct_prices(66666), 2, 1000, scramble=2000))
add(2, build(2, distinct_prices(100000), 2, 0))
add(5, build(5, distinct_prices(40000), 3, 40, same=True))
add(2, build(2, distinct_prices(100000), 7, 2, scramble=100))
add(3, build(3, distinct_prices(66666), 1, 3))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
