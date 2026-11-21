# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(500056)
MAXN = 100000
MAXM = 200000
tests = []


def add(n, edges, shuffle=True):
    m = len(edges)
    assert 3 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v in edges)
    assert len({u * (n + 1) + v if u < v else v * (n + 1) + u for u, v in edges}) == m
    deg = [0] * (n + 1)
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    assert min(deg[1:]) >= 2
    if shuffle:
        perm = list(range(1, n + 1))
        random.shuffle(perm)
        perm = [0] + perm
        flip = format(random.getrandbits(m), "0%db" % m)
        edges = [(perm[u], perm[v]) if f == "1" else (perm[v], perm[u]) for f, (u, v) in zip(flip, edges)]
    tests.append(f"{n} {m}\n" + "".join("%d %d\n" % e for e in edges))


class Town:

    def __init__(self):
        self.n = 0
        self.edges = []

    def fresh(self, cnt):
        vs = list(range(self.n + 1, self.n + cnt + 1))
        self.n += cnt
        return vs

    def cycle(self, cnt):
        vs = self.fresh(cnt)
        self.edges += [(vs[i], vs[(i + 1) % cnt]) for i in range(cnt)]

    def grid(self, rows, cols, wrap=False):
        vs = self.fresh(rows * cols)
        for r in range(rows):
            for c in range(cols):
                v = vs[r * cols + c]
                if c + 1 < cols or wrap:
                    self.edges.append((v, vs[r * cols + (c + 1) % cols]))
                if r + 1 < rows or wrap:
                    self.edges.append((v, vs[(r + 1) % rows * cols + c]))

    def hub(self, cnt, hubs=2):
        vs = self.fresh(cnt)
        self.edges += [(h, v) for h in vs[:hubs] for v in vs[hubs:]]

    def web(self, cnt, extra):
        vs = self.fresh(cnt)
        have, deg, new = set(), [0] * cnt, []

        def link(i, j):
            if i == j or (min(i, j), max(i, j)) in have:
                return False
            have.add((min(i, j), max(i, j)))
            deg[i] += 1
            deg[j] += 1
            new.append((vs[i], vs[j]))
            return True

        for i in range(1, cnt):
            link(i, random.randrange(i))
        for _ in range(extra):
            link(random.randrange(cnt), random.randrange(cnt))
        for i in range(cnt):
            while deg[i] < 2:
                link(i, random.randrange(cnt))
        self.edges += new

    def mix(self, pieces, small, big):
        for _ in range(pieces):
            r, k = random.random(), random.randint(small, big)
            if r < 0.25:
                hubs = random.randint(2, 3)
                self.hub(max(k, hubs + 2), hubs)
            elif r < 0.5:
                self.cycle(k)
            elif r < 0.75:
                rows = random.randint(2, 5)
                self.grid(rows, max(2, k // rows))
            else:
                self.web(max(k, 4), random.randint(0, k))

    def emit(self):
        add(self.n, self.edges)


add(7, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 7), (7, 4)], False)
add(8, [(1, 2), (2, 3), (3, 4), (4, 1), (5, 6), (6, 7), (7, 8), (8, 5)], False)
add(5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3)], False)
add(3, [(1, 2), (2, 3), (3, 1)], False)
add(8, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (6, 7), (7, 8), (8, 6)], False)


add(3, [(1, 2), (2, 3), (3, 1)])
add(4, [(1, 2), (2, 3), (3, 4), (4, 1)])
add(5, [(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])
add(11, [(1, 2), (2, 3), (3, 4), (4, 1), (5, 6), (6, 7), (7, 8), (8, 5), (9, 10), (10, 11), (11, 9)])
add(9, [(1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (7, 8), (8, 9), (9, 7)])
add(9, [(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (6, 7), (7, 8), (8, 9), (9, 6)])
t = Town()
t.hub(7)
t.cycle(8)
t.grid(3, 3)
t.emit()


t = Town()
t.mix(60, 4, 16)
t.emit()
t = Town()
for _ in range(40):
    t.hub(random.randint(4, 30)) if random.random() < 0.5 else t.grid(random.randint(2, 4), random.randint(2, 6))
t.emit()
t = Town()
t.grid(20, 20)
t.grid(19, 20)
t.hub(300)
t.cycle(101)
t.emit()
t = Town()
t.grid(40, 50)
t.mix(60, 4, 20)
t.emit()
t = Town()
t.hub(900)
t.hub(700)
t.grid(20, 25, True)
t.cycle(999)
t.emit()


t = Town()
t.hub(48000)
t.hub(46000)
while t.n + 3 <= MAXN:
    t.cycle(3)
t.emit()
t = Town()
t.grid(300, 333)
t.emit()
t = Town()
t.grid(316, 316, True)
t.emit()
t = Town()
t.grid(250, 300)
t.grid(100, 240)
t.emit()
t = Town()
t.grid(200, 200)
t.grid(190, 190)
t.hub(20000)
while t.n + 5 <= MAXN:
    t.cycle(5)
t.emit()
t = Town()
t.web(MAXN, 85000)
t.emit()
t = Town()
t.grid(200, 200)
t.grid(180, 200)
t.web(20000, 15000)
t.emit()
t = Town()
t.grid(200, 200)
t.grid(170, 200)
t.hub(25000)
t.emit()
t = Town()
t.grid(250, 250)
while t.n + 30 <= MAXN:
    t.hub(random.randint(4, 30))
t.emit()
t = Town()
t.cycle(MAXN)
t.emit()
t = Town()
t.hub(60000)
t.hub(39998)
t.emit()
t = Town()
t.grid(300, 333, True)
t.emit()
t = Town()
t.grid(170, 200)
t.grid(160, 200)
t.mix(1000, 20, 40)
t.emit()

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
