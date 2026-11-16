# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(19006)
MAXN, MAXQ, MAXX, MAXH = 10**6, 100_000, 10**6, 10**12
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ops):
    q = len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert any(op[0] == 'W' for op in ops)
    lines = []
    for op in ops:
        if op[0] == 'D':
            l, r, x = op[1], op[2], op[3]
            assert 1 <= l <= r <= n and 1 <= abs(x) <= MAXX
            lines.append(f"D {l} {r} {x}")
        else:
            p, h = op[1], op[2]
            assert op[0] == 'W' and 1 <= p <= n and abs(h) <= MAXH
            lines.append(f"W {p} {h}")
    tests.append(f"{n} {q}\n" + "\n".join(lines) + "\n")


class Ground:
    """the current heights: range add, point value (Fenwick tree over the differences)"""
    def __init__(self, n):
        self.n, self.f = n, [0] * (n + 2)

    def _add(self, i, x):
        while i <= self.n:
            self.f[i] += x
            i += i & -i

    def add(self, l, r, x):
        self._add(l, x)
        if r + 1 <= self.n:
            self._add(r + 1, -x)

    def at(self, i):
        s = 0
        while i > 0:
            s += self.f[i]
            i -= i & -i
        return s


def scenario(n, q, pw, pt, wall_w, wall_h, terr, ask_p, delta, cap=10**9):
    """walls: short ranges raised by wall_h (taken down again later), terrain: ranges from terr() changed by
    a small amount; questions at ask_p() with level a_p + delta()"""
    g, walls, ops = Ground(n), [], []
    for _ in range(q):
        r = random.random()
        if r < pw:
            if walls and (len(walls) >= cap or random.random() < 0.3):
                j = ri(0, len(walls) - 1)
                walls[j], walls[-1] = walls[-1], walls[j]
                l, rr, x = walls.pop()
                x = -x
            else:
                l = ri(1, n)
                rr = min(n, l + ri(0, wall_w))
                x = ri(wall_h // 2, wall_h)
                walls.append((l, rr, x))
            ops.append(('D', l, rr, x))
            g.add(l, rr, x)
        elif r < pw + pt:
            l, rr = terr()
            x = random.choice((-1, 1)) * ri(1, 3)
            ops.append(('D', l, rr, x))
            g.add(l, rr, x)
        else:
            p = ask_p()
            ops.append(('W', p, g.at(p) + delta()))
    if not any(op[0] == 'W' for op in ops):
        ops[-1] = ('W', 1, 0)
    return ops


def any_rng(n):
    l = ri(1, n)
    return l, ri(l, n)


def short_rng(n, d):
    l = ri(1, n)
    return l, min(n, l + ri(0, d))


# samples
add(8, [('D', 3, 3, 5), ('D', 6, 6, 4), ('D', 1, 8, -1), ('W', 4, 2), ('W', 4, 4), ('W', 3, 4), ('W', 1, 10)])
add(5, [('W', 3, 1), ('D', 2, 4, -3), ('W', 3, 0), ('D', 3, 3, 5), ('W', 2, 0), ('W', 2, -3)])
add(1, [('W', 1, 0), ('W', 1, 1), ('D', 1, 1, -MAXX), ('W', 1, -999999)])
add(10, [('D', 1, 10, 2), ('D', 4, 7, -5), ('D', 6, 6, 4), ('W', 5, 0), ('W', 7, -1), ('D', 1, 3, -6), ('W', 5, 2)])
add(MAXN, [('D', 500000, 500000, MAXX), ('W', 1, 1), ('W', MAXN, 1000001), ('W', 500000, 7)])
# hidden: small (the brute force checks these)
for n, q, ww in ((1, 12, 0), (6, 40, 1), (15, 100, 2), (60, 500, 4), (500, 3000, 10), (3000, 4000, 30)):
    add(n, scenario(n, q, 0.25, 0.3, ww, 20, lambda: any_rng(n), lambda: ri(1, n), lambda: ri(-3, 15)))
n = 2000                                                    # deep valleys: long floods
add(n, scenario(n, 4000, 0.1, 0.3, 3, 1000, lambda: any_rng(n), lambda: ri(1, n), lambda: ri(1, 400), cap=8))
n = 2500                                                    # levels exactly at a wall top and just below
add(n, scenario(n, 4000, 0.3, 0.2, 2, 50, lambda: short_rng(n, 30), lambda: ri(1, n),
                lambda: random.choice((0, 1, 50, 51, 25))))
# hidden: maximum size
N, Q = MAXN, MAXQ
mid = lambda: ri(N // 2 - 1000, N // 2 + 1000)
add(N, scenario(N, Q, 0.05, 0.25, 5, MAXX, lambda: any_rng(N), lambda: ri(1, N), lambda: ri(1, 3000), cap=10))
add(N, scenario(N, Q, 0.1, 0.2, 50, MAXX, lambda: any_rng(N), mid, lambda: ri(1, 5000), cap=40))
add(N, scenario(N, Q, 0.3, 0.2, 100, 10**5, lambda: any_rng(N), lambda: ri(1, N), lambda: ri(-100, 5 * 10**4)))
add(N, scenario(N, Q, 0.02, 0.4, 0, MAXX, lambda: (ri(1, 10), ri(N - 10, N)), lambda: ri(1, N),
                lambda: ri(1, 10**4), cap=3))       # almost no walls: whole-road floods
add(N, scenario(N, Q, 0.2, 0.3, 1000, MAXX, lambda: any_rng(N), lambda: ri(1, N), lambda: ri(-5, 50)))
add(N, scenario(N, Q, 0.4, 0.1, 3, 1000, lambda: any_rng(N), lambda: ri(1, N), lambda: ri(0, 2000)))
add(N, scenario(N, Q, 0.08, 0.3, 2, MAXX, lambda: any_rng(N), lambda: random.choice((1, N, ri(1, N))),
                lambda: ri(1, 10**6), cap=20))
add(N, scenario(N, Q, 0.15, 0.35, 10, 5000, lambda: short_rng(N, 3000), mid, lambda: ri(-2, 3000), cap=20))
add(N, scenario(N, Q, 0.05, 0.05, 0, MAXX, lambda: any_rng(N), lambda: ri(1, N), lambda: ri(1, 2 * 10**6),
                cap=30))                             # mostly questions
add(N, scenario(N, Q, 0.25, 0.25, 20_000, MAXX, lambda: any_rng(N), lambda: ri(1, N), lambda: ri(-10, 10**6)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
