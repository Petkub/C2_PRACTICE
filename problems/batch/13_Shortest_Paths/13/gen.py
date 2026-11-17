# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(81212)
MAXN, MAXL, MAXSUM, MAXT, MAXP = 100_000, 100_000, 150_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, P, A, B, lines, shuffle=True):
    """lines: list of (stations, times)"""
    lines = list(lines)
    if shuffle:
        random.shuffle(lines)
    L = len(lines)
    assert 2 <= n <= MAXN and 1 <= L <= MAXL and 1 <= P <= MAXP and 1 <= A <= n and 1 <= B <= n
    assert sum(len(s) for s, t in lines) <= MAXSUM
    assert all(len(s) >= 2 and len(t) == len(s) - 1 and len(set(s)) == len(s) for s, t in lines)
    assert all(1 <= min(s) and max(s) <= n and 1 <= min(t) and max(t) <= MAXT for s, t in lines)
    tests.append(f"{n} {L} {P} {A} {B}\n" + "\n".join(
        f"{len(s)} {' '.join(map(str, s))}\n{' '.join(map(str, t))}" for s, t in lines) + "\n")


def distinct(lo, hi, k):
    """k different random integers in [lo, hi]"""
    if hi - lo >= 1000 * k:                 # collisions are rare: draw all, retry if needed
        while True:
            res = [lo + int(random.random() * (hi - lo + 1)) for _ in range(k)]
            if len(set(res)) == k:
                return res
    res, seen = [], set()
    while len(res) < k:
        x = ri(lo, hi)
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


def rnd_line(n, k, tlo, thi):
    return (distinct(1, n, k), [ri(tlo, thi) for _ in range(k - 1)])


def rnd_lines(n, L, kmin, kmax, tlo, thi):
    """up to L random lines, stopping before the total length passes MAXSUM"""
    res, used = [], 0
    for _ in range(L):
        k = ri(kmin, kmax)
        if used + k > MAXSUM:
            break
        res.append(rnd_line(n, k, tlo, thi))
        used += k
    return res


def relabel(n, A, B, lines):
    p = list(range(1, n + 1))
    random.shuffle(p)
    p = [0] + p
    return n, p[A], p[B], [([p[x] for x in s], t) for s, t in lines]


def grid_metro(r, c, tlo, thi):
    """stations on an r x c grid; one line along every row and every column"""
    lines = []
    for i in range(r):
        lines.append(([i * c + j + 1 for j in range(c)], [ri(tlo, thi) for _ in range(c - 1)]))
    for j in range(c):
        lines.append(([i * c + j + 1 for i in range(r)], [ri(tlo, thi) for _ in range(r - 1)]))
    return r * c, lines


def hub(n, L, tlo, thi):
    """station 1 is on every line; each line is short"""
    lines, used = [], 0
    for _ in range(L):
        k = 2 if random.random() < 0.85 else 3
        if used + k > MAXSUM:
            break
        used += k
        s = distinct(2, n, k - 1)
        s.insert(ri(0, k - 1), 1)
        lines.append((s, [ri(tlo, thi) for _ in range(k - 1)]))
    return lines


def express(n, k, P):
    """one slow line through every station, express lines that skip ahead but need transfers"""
    order = list(range(1, n + 1))
    random.shuffle(order)
    lines = [(order, [ri(1, 100) for _ in range(n - 1)])]
    used = n
    while used + k <= MAXSUM:
        i = ri(0, n - k * 50 - 1)
        s = [order[i + 50 * x] for x in range(k)]
        lines.append((s, [ri(1000, 4000) for _ in range(k - 1)]))
        used += k
    return lines, order[0], order[-1]


def traps(g, tlo, thi):
    """g blocks in a row: a -> x directly, or a -> y -> x on a line that goes on to b"""
    lines = []
    for i in range(g):
        a, x, y, b = 3 * i + 1, 3 * i + 2, 3 * i + 3, 3 * i + 4
        lines += [([a, x], [ri(tlo, thi)]), ([a, y, x, b], [ri(tlo, thi), ri(tlo, thi), ri(tlo, thi)])]
    return lines


def with_hub(lines, lo, hi, h, tlo, thi):
    """fill the rest of the total length with short lines through station h and stations of [lo, hi]"""
    lines = list(lines)
    used = sum(len(s) for s, t in lines)
    while used + 3 <= MAXSUM:
        k = 2 if random.random() < 0.85 else 3
        s = [x for x in distinct(lo, hi, k) if x != h][:k - 1]
        s.insert(ri(0, len(s)), h)
        lines.append((s, [ri(tlo, thi) for _ in range(len(s) - 1)]))
        used += len(s)
    return lines


# samples
add(6, 5, 1, 6, [([1, 2, 3, 4], [2, 2, 2]), ([5, 3, 6], [1, 3]), ([2, 6], [9])], False)
add(5, 100, 4, 3, [([4, 2, 1], [1, 1]), ([1, 5, 3], [1, 1]), ([2, 3], [150])], False)
add(4, 1, 1, 4, [([1, 2], [5]), ([3, 4], [5])], False)
add(3, MAXP, 2, 2, [([1, 3], [7])], False)
add(4, 3, 1, 4, [([1, 2, 3], [5, 5]), ([3, 2, 4], [1, 1])], False)
# hidden: small
add(2, 1, 1, 2, [([2, 1], [MAXT])])
add(3, 10, 1, 3, [([1, 2], [1]), ([2, 3], [1]), ([1, 3], [12]), ([1, 2, 3], [7, 7])])
for n, L, kmax, thi, P in ((6, 4, 3, 5, 3), (8, 6, 4, 10, 1), (10, 8, 5, 3, 7), (12, 10, 4, 20, 15),
                           (30, 20, 6, 100, 50), (60, 40, 8, 10, 25)):
    lines = rnd_lines(n, L, 2, kmax, 1, thi)
    add(n, P, ri(1, n), ri(1, n), lines)
n, lines = grid_metro(6, 7, 1, 9)
n, A, B, lines = relabel(n, 1, n, lines)
add(n, 6, A, B, lines)
add(40, 4, 1, 2, hub(40, 50, 1, 10))
n, lines = grid_metro(15, 15, 1, 50)
n, A, B, lines = relabel(n, 1, n, lines)
add(n, 30, A, B, lines)
lines = rnd_lines(500, 300, 2, 10, 1, 1000)
add(500, 700, 1, 2, lines)
lines = []
for g in range(30):                                                 # arriving first is not always best
    a, x, y, b = 3 * g + 1, 3 * g + 2, 3 * g + 3, 3 * g + 4
    lines += [([a, x], [10]), ([a, y, x, b], [5, 7, 1])]
add(91, 100, 1, 91, lines)
lines = rnd_lines(40, 60, 2, 8, 1, 30)
add(40, 200, 1, 2, lines)
# hidden: maximum size
n, lines = grid_metro(250, 300, 1, 1000)
n, A, B, lines = relabel(n, 1, n, lines)
add(n, 2000, A, B, lines)
n, lines = grid_metro(250, 300, 1, 10)
n, A, B, lines = relabel(n, 1, n, lines)
add(n, 1, A, B, lines)
lines = hub(MAXN, 90_000, 1, 1000)                               # every route changes at the hub
add(MAXN, 5, max(lines[0][0]), max(lines[-1][0]), lines, False)
lines = hub(MAXN, 90_000, 1, MAXT)
add(MAXN, MAXP, max(lines[0][0]), max(lines[1][0]), lines, False)
lines, A, B = express(MAXN, 20, 500)
add(MAXN, 500, A, B, lines)
lines, A, B = express(MAXN, 20, 10**6)
add(MAXN, 10**6, A, B, lines)
lines = traps(10_000, 1, 10)
add(MAXN, 100, 1, 30_001, with_hub(lines + [([1, 30_002], [1])], 30_002, MAXN, 30_002, 1, 50))
lines = with_hub(rnd_lines(MAXN, 4000, 2, 18, 1, 10**4), 1, MAXN, ri(1, MAXN), 1, 10**4)
add(MAXN, 10**5, lines[0][0][0], lines[1][0][-1], lines)
add(20_000, 3 * 10**4, 1, 2, rnd_lines(20_000, 10_000, 2, 38, 1, 10**4))
order = list(range(1, MAXN + 1))
random.shuffle(order)
order = order[:MAXSUM // 2]
lines = [(order[i:i + 2], [MAXT]) for i in range(len(order) - 1)]          # a line for every step, lengths near 10^14
add(MAXN, MAXP, order[0], order[-1], lines)
lines = rnd_lines(MAXN, 4000, 2, 18, 1, 10**4)
lines = [l for l in with_hub(lines, 1, MAXN, 3, 1, 10**4) if 2 not in l[0]]
add(MAXN, 50, lines[0][0][0], 2, lines)                          # station 2 is on no line
lines = []
used = 0
while used + 3 <= MAXSUM:                                            # two busy stations
    k = 2 if random.random() < 0.85 else 3
    s = distinct(3, MAXN, k - 1)
    s.insert(ri(0, k - 1), ri(1, 2))
    lines.append((s, [ri(1, 10**5) for _ in range(k - 1)]))
    used += k
add(MAXN, 10**5, lines[0][0][0], lines[-1][0][-1], lines)
add(30, 500, 1, 2, rnd_lines(30, 100_000, 2, 10, 1, 1000))         # every station is on thousands of lines

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
