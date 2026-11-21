# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(120016)
MAXN, MAXM, MAXL = 500, 1000, 250000
tests = []


def add(m, lists):
    n = len(lists)
    assert 1 <= n <= MAXN and n <= m <= MAXM
    assert sum(len(w) for w in lists) <= MAXL
    for i, w in enumerate(lists, 1):
        assert len(set(w)) == len(w) and all(1 <= g <= m and g != i for g in w)
    tests.append(f"{n} {m}\n" + "".join(" ".join(map(str, [len(w)] + w)) + "\n" for w in lists))


def relabel(m, lists):
    n = len(lists)
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    spare = list(range(n + 1, m + 1))
    random.shuffle(spare)
    new = {g: perm[g - 1] for g in range(1, n + 1)}
    new.update({g: spare[g - n - 1] for g in range(n + 1, m + 1)})
    out = [None] * n
    for i, w in enumerate(lists, 1):
        out[new[i] - 1] = [new[g] for g in w]
    return out


def rnd(n, m, dens):
    lists = []
    for i in range(1, n + 1):
        w = [g for g in range(1, m + 1) if g != i and random.random() < dens]
        random.shuffle(w)
        lists.append(w)
    return lists


def blocks(sizes, m, fwd, inner, spare_p, spare_cnt, last_dag=False, seq0=0):
    n = sum(sizes)
    assert n <= m
    start, bl = [], []
    s = 0
    for b, z in enumerate(sizes):
        start.append(s)
        bl += [b] * z
        s += z
    spares = list(range(n + 1, m + 1))
    lists = []
    for i in range(1, n + 1):
        b = bl[i - 1]
        lo, hi = start[b] + 1, start[b] + sizes[b]
        later = list(range(hi + 1, n + 1))
        w = random.sample(later, min(fwd, len(later)))
        own = [g for g in range(lo, hi + 1) if g != i and (not last_dag or b < len(sizes) - 1 or g > i)]
        w += random.sample(own, min(inner[b], len(own)))
        if b == 0 and spares and random.random() < spare_p:
            w += random.sample(spares, min(spare_cnt, len(spares)))
        lists.append(w)
    for k in range(seq0):
        i = k + 1
        keep = [g for g in lists[i - 1] if g <= n and bl[g - 1] > 0]
        lists[i - 1] = keep + [i + 1 if k + 1 < seq0 else spares[0]]
    return lists


add(5, [[2, 3], [3], [1], [1, 5]])
add(4, [[3, 4], [3]])
add(3, [[2], [3], []])
add(1, [[]])
add(7, [[6, 2], [3, 1], [4], [2, 5], [6], [1], [5]])
add(6, [[2, 3], [1], [6], [5, 3]])

add(4, [[2], [3], [4], []])
for n, extra, dens in ((6, 0, 0.5), (7, 3, 0.3), (8, 2, 0.25), (12, 5, 0.2), (30, 10, 0.1)):
    add(n + extra, rnd(n, n + extra, dens))
add(9, relabel(9, blocks([5, 4], 9, 2, [2, 2], 0.0, 0)))
add(16, relabel(16, blocks([8, 4, 3], 16, 3, [2, 2, 2], 0.3, 1, last_dag=True, seq0=5)))
add(60, relabel(60, blocks([20, 15, 15], 60, 10, [4, 4, 12], 0.2, 2, last_dag=True, seq0=8)))

add(MAXM, relabel(MAXM, blocks([250, 250], MAXM, 250, [6, 240], 0.05, 2, seq0=40)))
add(MAXM, relabel(MAXM, blocks([150, 350], MAXM, 350, [10, 300], 0.1, 3, seq0=120)))
add(MAXN, relabel(MAXN, blocks([250, 250], MAXN, 240, [8, 240], 0.0, 0)))
add(700, relabel(700, blocks([150, 200, 150], 700, 280, [5, 199, 149], 0.03, 1, seq0=100)))
add(MAXM, relabel(MAXM, blocks([100, 400], MAXM, 360, [4, 380], 0.0, 0)))
add(800, relabel(800, blocks([200, 300], 800, 300, [30, 250], 0.02, 2, seq0=150)))
add(MAXN, relabel(MAXN, blocks([MAXN], MAXN, 0, [MAXN - 1], 0.0, 0, last_dag=True)))
add(MAXM, relabel(MAXM, blocks([250, 250], MAXM, 230, [40, 249], 0.01, 1, seq0=200)))
add(MAXM, relabel(MAXM, blocks([180, 320], MAXM, 300, [120, 280], 0.005, 1, seq0=170)))
add(MAXM, relabel(MAXM, blocks([120, 380], MAXM, 380, [60, 370], 0.2, 2, seq0=100)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
