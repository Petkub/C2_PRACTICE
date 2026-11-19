# Test generator of this problem (the judge runs it to rebuild the big tests).
import gc, os, random
from operator import itemgetter

gc.disable()
random.seed(4601)
MAXQ, MAXX = 400000, 10**9
tests = []


def J(x):
    return (1, x)


def L(x):
    return (2, x)


def S(x):
    return (3, x)


def add(ops):
    assert 1 <= len(ops) <= MAXQ
    here = set()
    for kind, x in ops:
        assert kind in (1, 2, 3) and 1 <= x <= MAXX
        if kind == 1:
            assert x not in here
            here.add(x)
        else:
            assert x in here
            here.remove(x)
    tests.append(f"{len(ops)}\n" + "".join("%d %d\n" % op if op[0] != 3 else "3\n" for op in ops))


def flow(q, parts, hi=MAXX):
    rnd = random.random
    fresh = random.sample(range(1, hi + 1), sum(p[0] for p in parts))
    events, ends = [], []
    t = hold = 0.0
    for visits, step, back, walk, a, b, c, lag in parts:
        for _ in range(visits):
            t += rnd() * step
            x = 0
            if ends and rnd() < back:
                for _ in range(4):
                    i = int(rnd() * len(ends))
                    if ends[i][0] < t:
                        x = ends[i][1]
                        ends[i] = ends[-1]
                        ends.pop()
                        break
            if not x:
                x = fresh.pop()
            events.append((t, (1, x)))
            if rnd() < walk:
                end = a + b * t
                if end < t:
                    end = t
                end += rnd() * c
                if hold < end:
                    hold = end
                events.append((end, (2, x)))
            else:
                if hold < t:
                    hold = t
                hold = end = hold + rnd() * lag
                events.append((end, (3, x)))
            ends.append((end, x))
    assert len(events) >= q
    events.sort(key=itemgetter(0))
    return [e[1] for e in events[:q]]


add([J(15), J(7), J(42), L(7), S(15), S(42), J(7), J(8), S(7)])
add([J(5), J(9), S(5), J(5), L(9), S(5)])
add([J(1000000000), J(1), J(500)])
add([J(3), J(1), J(4), L(1), J(5), S(3), S(4), S(5)])
add([J(20), J(30), L(20), J(40), S(30), J(20), L(40), S(20), J(60), J(70), S(60)])

add([J(1), S(1)])
add([J(7), J(8), L(7), J(7), S(8), S(7)])
add(flow(12, [(8, 1, 0.5, 0.5, 0, 1, 3, 1)], 30))
add(flow(40, [(25, 1, 0.9, 0.5, 0, 1, 4, 1)], 40))
add(flow(200, [(120, 1, 0.9, 0.6, 0, 1, 12, 1)], 200))
add(flow(2000, [(1100, 1, 0.7, 0.6, 0, 1, 60, 2)]))
add(flow(5000, [(1000, 0.01, 0, 0.7, 20, 0, 300, 1), (1800, 1, 0.9, 0.6, 0, 1, 200, 1)]))
add(flow(20000, [(5000, 0.01, 0, 0.5, 50, 1, 3000, 1), (5500, 1, 0.8, 0.5, 0, 1, 1500, 2)]))
add(flow(40000, [(10000, 0.01, 0, 0.7, 100, 0, 9000, 1), (11000, 1, 0.9, 0.7, 0, 1, 4000, 1)]))
add(flow(60000, [(32000, 1, 0.6, 0.5, 0, 1, 12000, 3)], 99999))

Q = MAXQ
PARTS = [
    [(180000, 0.01, 0, 0.84, 200000, -100, 20000, 0.5), (35000, 12, 0.9, 0.4, 0, 1, 20000, 0.5)],
    [(180000, 0.01, 0, 0.84, 200000, -100, 0, 0.5), (35000, 11, 0.9, 0.4, 0, 1, 20000, 0.5)],
    [(180000, 0.01, 0, 0.84, 200000, -100, 30000, 0.5), (35000, 13, 0.9, 0.3, 0, 1, 50000, 0.5)],
    [(180000, 0.01, 0, 0.84, 200000, -100, 5000, 0.5), (35000, 12, 0.9, 0.5, 0, 1, 20000, 0.2)],
    [(180000, 0.01, 0, 0.84, 200000, -100, 10000, 0.5), (35000, 12, 0.6, 0.4, 0, 1, 5000, 0.5)],
    [(200000, 0.01, 0, 0.8, 200000, -100, 2000, 0.5), (1000, 400, 0.9, 0.4, 0, 1, 20000, 0.5)],
    [(180000, 0.01, 0, 0.84, 200000, -100, 15000, 0.5), (35000, 12, 0.5, 0.4, 0, 1, 20000, 0.5)],
]
for parts in PARTS:
    add(flow(Q, parts, 250000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
