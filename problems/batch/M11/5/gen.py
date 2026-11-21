# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(511005)
MAXQ = 200000
MAXX = 10 ** 9
tests = []


def add(ops):
    q = len(ops)
    assert 1 <= q <= MAXQ
    seen = set()
    for t, x in ops:
        assert t in (1, 2) and 1 <= x <= MAXX
        if t == 1:
            assert x not in seen
            seen.add(x)
        else:
            assert x in seen
    tests.append(f"{q}\n" + "".join(f"{t} {x}\n" for t, x in ops))


class Ops:

    def __init__(self, keys):
        self.keys = keys
        self.ins = []
        self.ops = []

    def insert(self, x=None):
        x = self.keys.pop() if x is None else x
        self.ins.append(x)
        self.ops.append((1, x))

    def attack_last(self, k):

        for x in self.ins[-1:-k - 1:-1]:
            self.ops.append((2, x))

    def attack_random(self, k):
        for _ in range(k):
            self.ops.append((2, random.choice(self.ins)))


def fresh(n, lo=1, hi=MAXX):
    return random.sample(range(lo, hi + 1), n)


def mixed(q, p_attack, p_last, keys):
    o = Ops(keys)
    while len(o.ops) < q:
        if o.ins and random.random() < p_attack:
            if random.random() < p_last:
                o.attack_last(min(len(o.ins), random.randint(1, 5), q - len(o.ops)))
            else:
                o.attack_random(1)
        else:
            o.insert()
    return o.ops[:q]


def ordered(q, rising, burst):

    keys = sorted(fresh(q), reverse=rising)
    o = Ops(keys)
    while len(o.ops) < q:
        if o.ins and random.random() < burst:
            o.attack_last(min(len(o.ins), random.randint(1, 30), q - len(o.ops)))
        else:
            o.insert()
    return o.ops[:q]


def zigzag(q, burst):

    lo, hi = 1, MAXX
    seq = []
    for i in range(q):
        if i % 2 == 0:
            seq.append(lo)
            lo += random.randint(1, 3000)
        else:
            seq.append(hi)
            hi -= random.randint(1, 3000)
    assert lo < hi
    o = Ops(seq[::-1])
    while len(o.ops) < q:
        if o.ins and random.random() < burst:
            o.attack_last(min(len(o.ins), random.randint(1, 4), q - len(o.ops)))
            o.attack_random(1)
        else:
            o.insert()
    return o.ops[:q]


add([(1, 50), (1, 30), (1, 70), (1, 60), (1, 90), (2, 70), (2, 60), (2, 70)])
add([(1, 40), (1, 20), (1, 10), (1, 30), (2, 20), (2, 30), (2, 20), (1, 25), (2, 30)])
add([(1, 7)])
add([(1, 1), (1, 2), (1, 3)])
add([(1, 8), (1, 3), (1, 12), (1, 5), (2, 3), (2, 5), (1, 10)])

add([(1, 5), (2, 5), (1, 3), (1, 8), (2, 3), (2, 8), (1, 6), (2, 6), (2, 5)])
add([(1, MAXX), (1, 1), (2, MAXX), (2, 1), (1, 2)])
add(mixed(30, 0.4, 0.5, fresh(30, 1, 100)))
add(mixed(60, 0.5, 0.3, fresh(60, 1, 1000)))
add(ordered(80, True, 0.2))
add(ordered(80, False, 0.3))
add(zigzag(70, 0.2))
add(mixed(200, 0.45, 0.6, fresh(200, 1, 500)))

add(mixed(20000, 0.4, 0.5, fresh(20000)))
add(ordered(20000, True, 0.1))
add(zigzag(15000, 0.15))

add(ordered(MAXQ, True, 0.0))
add(ordered(MAXQ, False, 0.01))
add(ordered(MAXQ, True, 0.02))
add(zigzag(MAXQ, 0.0))
add(zigzag(MAXQ, 0.03))

o = Ops(fresh(60000, 1, 2 * 10 ** 8 - 1))
for x in sorted(fresh(140000, 2 * 10 ** 8, MAXX)):
    o.insert(x)
while len(o.ops) < MAXQ:
    if random.random() < 0.2:
        o.attack_random(1)
    else:
        o.insert()
add(o.ops[:MAXQ])

keys = sorted(fresh(MAXQ), reverse=True)
o = Ops(keys)
for _ in range(110000):
    o.insert()
while len(o.ops) < MAXQ:
    o.attack_last(1)
    if len(o.ops) < MAXQ:
        o.insert()
add(o.ops[:MAXQ])

mid = MAXX // 2
o = Ops([])
o.insert(mid)
for i in range(1, MAXQ // 2):
    o.insert(mid - 3 * i)
    o.insert(mid + 3 * i)
o.attack_last(MAXQ - len(o.ops))
add(o.ops[:MAXQ])
add(zigzag(MAXQ, 0.01))
add(mixed(MAXQ, 0.05, 0.3, sorted(fresh(MAXQ))))
o = Ops(sorted(fresh(MAXQ), reverse=True))
while len(o.ops) < MAXQ:
    if o.ins and random.random() < 0.1:
        o.attack_random(1)
    else:
        o.insert()
add(o.ops[:MAXQ])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
