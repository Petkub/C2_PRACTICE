# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(500055)
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


class City:
    def __init__(self):
        self.n = 0
        self.edges = []

    def fresh(self, cnt):
        vs = list(range(self.n + 1, self.n + cnt + 1))
        self.n += cnt
        return vs

    def ring(self, cnt, chords=0, kind=0):
        vs = self.fresh(cnt)
        have = set()
        for i in range(cnt):
            a, b = vs[i], vs[(i + 1) % cnt]
            self.edges.append((a, b))
            have.add((min(a, b), max(a, b)))
        done, tries = 0, 0
        while done < chords and tries < 20 * chords + 100:
            tries += 1
            i, j = random.randrange(cnt), random.randrange(cnt)
            a, b = vs[i], vs[j]
            if (j - i) % 2 == kind and a != b and (min(a, b), max(a, b)) not in have:
                have.add((min(a, b), max(a, b)))
                self.edges.append((a, b))
                done += 1

    def hub(self, cnt, hubs=2):
        vs = self.fresh(cnt)
        self.edges += [(h, v) for h in vs[:hubs] for v in vs[hubs:]]

    def emit(self):
        add(self.n, self.edges)


add(7, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 7), (7, 4)], False)
add(5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3)], False)
add(6, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)], False)
add(3, [(1, 2), (2, 3), (3, 1)], False)
add(8, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (6, 7), (7, 8), (8, 6)], False)


add(3, [(1, 2), (2, 3), (3, 1)])
add(4, [(1, 2), (2, 3), (3, 4), (4, 1)])
add(5, [(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])
add(8, [(1, 2), (2, 3), (3, 4), (4, 1), (5, 6), (6, 7), (7, 8), (8, 5)])
add(9, [(1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (7, 8), (8, 9), (9, 7)])
add(9, [(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (6, 7), (7, 8), (8, 9), (9, 6)])

c = City()
for _ in range(60):
    r = random.random()
    if r < 0.3:
        c.hub(random.randint(4, 15))
    elif r < 0.6:
        c.ring(2 * random.randint(2, 8), random.randint(0, 3), 1)
    else:
        c.ring(random.randint(3, 15), random.randint(0, 3), 0)
c.emit()
c = City()
for _ in range(40):
    c.hub(random.randint(4, 30)) if random.random() < 0.5 else c.ring(2 * random.randint(2, 12), 2, 1)
c.emit()
c = City()
c.ring(301, 5, 0)
c.hub(150)
c.hub(140)
c.ring(200, 10, 1)
c.emit()
c = City()
c.ring(2000, 300, 1)
for _ in range(60):
    c.ring(2 * random.randint(2, 10), 1, 1) if random.random() < 0.5 else c.hub(random.randint(4, 12))
c.emit()
c = City()
c.hub(900)
c.hub(700)
c.ring(500, 50, 1)
c.ring(999, 0, 0)
c.emit()


c = City()
c.hub(48000)
c.hub(46000)
while c.n + 3 <= MAXN:
    c.ring(3)
c.emit()
c = City()
c.ring(60000, 20000, 1)
while c.n + 12 <= MAXN:
    c.ring(2 * random.randint(2, 6), 1, 1)
c.emit()
c = City()
c.ring(MAXN, MAXM - MAXN, 1)
c.emit()
c = City()
c.ring(MAXN - 1, MAXM - MAXN, 0)
c.emit()
c = City()
c.hub(40000)
c.ring(30001, 1000, 0)
c.hub(29999)
c.emit()
c = City()
c.hub(30000, 3)
c.hub(34000, 2)
c.ring(36000, 5, 1)
c.emit()
c = City()
c.ring(40000, 30000, 1)
c.ring(20001, 10, 0)
while c.n + 40 <= MAXN:
    c.hub(random.randint(4, 40)) if random.random() < 0.5 else c.ring(random.randint(3, 30), 1, random.randint(0, 1))
c.emit()
c = City()
c.hub(50000)
c.ring(40000, 10000, 1)
while c.n + 15 <= MAXN:
    c.ring(random.randint(3, 15), 0, 0)
c.emit()
c = City()
c.hub(45000)
while c.n + 60 <= MAXN:
    r = random.random()
    if r < 0.5:
        c.hub(random.randint(30, 60))
    else:
        c.ring(random.randint(3, 60), random.randint(0, 3), random.randint(0, 1))
c.emit()

c = City()
c.ring(70000, 5000, 1)
while c.n + 24 <= MAXN:
    c.ring(2 * random.randint(2, 12), 2, 1) if random.random() < 0.5 else c.hub(random.randint(4, 24))
c.emit()
c = City()
c.hub(60000)
c.hub(39998)
c.emit()
c = City()
c.ring(50000, 0, 0)
c.hub(20000)
while c.n + 12 <= MAXN:
    c.ring(2 * random.randint(2, 6), 0, 0)
c.emit()

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
