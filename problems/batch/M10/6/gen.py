# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(500006)
MAXN = 100000
MAXQ = 200000
MAXP = 1000
tests = []


def add(n, events):
    q = len(events)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    clears = {}
    for op, t, p in events:
        assert op in "+-" and 1 <= t <= n and 1 <= p <= MAXP
        key = t * (MAXP + 1) + p
        if op == "+":
            clears[key] = clears.get(key, 0) + 1
        else:
            assert clears.get(key, 0) > 0
            clears[key] -= 1
    tests.append(f"{n} {q}\n" + "".join("%s %d %d\n" % e for e in events))


class Season:

    def __init__(self, n):
        self.n = n
        self.times = [[] for _ in range(n + 1)]
        self.events = []

    def plus(self, t, p):
        self.times[t].append(p)
        self.events.append(("+", t, p))

    def minus(self, t, i=None):
        lst = self.times[t]
        if not lst:
            return False
        i = random.randrange(len(lst)) if i is None else i
        lst[i], lst[-1] = lst[-1], lst[i]
        self.events.append(("-", t, lst.pop()))
        return True

    def random_events(self, cnt, p1=0.2, pminus=0.2, plo=1, phi=MAXP, teams=None):
        teams = teams or self.n
        while len(self.events) < cnt:
            t = 1 if random.random() < p1 else random.randint(1, teams)
            if random.random() < pminus and self.minus(t):
                continue
            self.plus(t, random.randint(plo, phi))

    def emit(self):
        add(self.n, self.events)


def heavy(n, q, fast):
    s = Season(n)
    while len(s.events) < q:
        for t in ([2, 3, 4, 5, 6, 1] if 1 in fast else [1, 2, 3, 4, 5, 6]):
            if len(s.events) < q:
                s.plus(t, random.randint(1, 3) if t in fast else random.randint(990, MAXP))
        if random.random() < 0.3 and len(s.events) < q:
            t = random.randint(7, n)
            if not (random.random() < 0.3 and s.minus(t)):
                s.plus(t, random.randint(1, MAXP))
    s.emit()


add(4, [("+", 3, 40), ("+", 2, 25), ("+", 1, 30), ("-", 2, 25), ("+", 4, 10)])
add(3, [("+", 2, 30), ("+", 1, 20), ("+", 1, 40), ("-", 1, 40), ("+", 2, 5)])
add(1, [("+", 1, 7), ("+", 1, 3), ("-", 1, 7)])
add(5, [("+", 4, 9), ("+", 1, 9), ("+", 5, 8), ("+", 4, 1), ("-", 4, 9), ("+", 1, 1), ("+", 2, 4)])
add(3, [("+", 2, 100), ("+", 3, 100), ("+", 1, 100), ("+", 2, 1), ("-", 3, 100), ("+", 1, 1)])


for n, q in [(2, 8), (4, 15), (6, 30), (10, 60), (30, 200)]:
    s = Season(n)
    s.random_events(q, 0.3, 0.3, 1, 20)
    s.emit()

s = Season(2000)
s.random_events(20000, 0.2, 0.3, 1, 50)
s.emit()
heavy(500, 15000, [1])
heavy(2000, 20000, [2])


N, Q = MAXN, MAXQ
s = Season(N)
s.random_events(Q)
s.emit()
s = Season(N)
s.random_events(Q, 0.05, 0.1, 1, 3)
s.emit()
s = Season(N)
for t in range(1, N + 1):
    s.plus(t, 600 if t == 1 else 500)
while len(s.events) < Q:
    s.plus(1, 1)
    s.minus(1, len(s.times[1]) - 1)
s.emit()
s = Season(N)
for t in range(1, N + 1):
    s.plus(t, random.randint(400, 600))
s.plus(1, 1)
while len(s.events) < Q:
    r = random.random()
    if r < 0.4:
        s.plus(1, random.randint(1, 5))
    elif r < 0.8:
        s.minus(1, len(s.times[1]) - 1) or s.plus(1, 7)
    elif r < 0.9:
        s.plus(random.randint(2, N), random.randint(1, MAXP))
    else:
        t = random.randint(2, N)
        s.minus(t) or s.plus(t, 3)
s.emit()
s = Season(N)
s.random_events(Q // 2, 0.3, 0.0)
while len(s.events) < Q:
    if not s.minus(1):
        s.plus(1, random.randint(1, MAXP))
s.emit()
s = Season(N)
big = [1, 2, 3, 4, 5]
while len(s.events) < Q:
    t = random.choice(big) if random.random() < 0.9 else random.randint(1, N)
    if random.random() < 0.15 and s.minus(t):
        continue
    s.plus(t, random.randint(MAXP - 3, MAXP))
s.emit()
s = Season(N)
while len(s.events) < Q:
    t = random.randint(1, 50)
    if random.random() < 0.3 and s.minus(t):
        continue
    s.plus(t, random.randint(990, MAXP))
s.emit()
for fast in ([2], [2, 4, 6], [1], [3, 5]):
    heavy(N, Q, fast)
s = Season(N)
s.random_events(Q, 1.0, 0.3)
s.emit()
s = Season(N)
s.random_events(Q, 0.25, 0.45, 1, 100)
s.emit()
s = Season(N)
s.random_events(Q, 0.3, 0.35, 1, 10, teams=20)
s.emit()

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
