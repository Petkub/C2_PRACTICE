# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random
from collections import OrderedDict

random.seed(4601)
MAXQ, MAXX = 400000, 10**9
tests = []


def add(ops):
    assert 1 <= len(ops) <= MAXQ
    line = OrderedDict()
    for op in ops:
        if op[0] == 1:
            x = op[1]
            assert len(op) == 2 and 1 <= x <= MAXX and x not in line
            line[x] = None
        elif op[0] == 2:
            assert len(op) == 2 and op[1] in line
            del line[op[1]]
        else:
            assert len(op) == 1 and op[0] == 3 and line
            line.popitem(last=False)
    tests.append(ops)


class Line:

    def __init__(self):
        self.mem, self.pos, self.line = [], {}, OrderedDict()

    def join(self, x):
        self.pos[x] = len(self.mem)
        self.mem.append(x)
        self.line[x] = None

    def leave(self, x):
        i = self.pos.pop(x)
        last = self.mem.pop()
        if last != x:
            self.mem[i] = last
            self.pos[last] = i
        del self.line[x]

    def serve(self):
        x = next(iter(self.line))
        self.leave(x)
        return x


def mixed(q, prefill, pool, wj, wl, ws, rejoin=0.5, tail_leave=0):
    ln, ops, gone = Line(), [], []
    fresh = iter(random.sample(range(1, MAXX + 1), min(pool, q + 5)))

    def new_id():
        if gone and random.random() < rejoin:
            i = random.randrange(len(gone))
            gone[i], gone[-1] = gone[-1], gone[i]
            return gone.pop()
        return next(fresh)

    for _ in range(prefill):
        x = new_id()
        ln.join(x)
        ops.append((1, x))
    while len(ops) < q - tail_leave:
        r = random.random() * (wj + wl + ws)
        if r < wj or not ln.mem:
            x = new_id()
            ln.join(x)
            ops.append((1, x))
        elif r < wj + wl:
            x = random.choice(ln.mem)
            ln.leave(x)
            gone.append(x)
            ops.append((2, x))
        else:
            x = ln.serve()
            gone.append(x)
            ops.append((3,))
    while len(ops) < q and ln.mem:
        x = ln.mem[-1]
        ln.leave(x)
        ops.append((2, x))
    return ops


def J(x):
    return (1, x)


def L(x):
    return (2, x)


S = (3,)


add([J(15), J(7), J(42), L(7), S, S, J(7), J(8), S])
add([J(5), J(9), S, J(5), L(9), S])
add([J(1000000000), J(1), J(500)])
add([J(3), J(1), J(4), L(1), J(5), S, S, S])
add([J(20), J(30), L(20), J(40), S, J(20), L(40), S, J(60), J(70), S])

add([J(1), S])
add([J(7), J(7 + 1), L(7), J(7), S, S])
add(mixed(12, 3, 30, 3, 3, 2))
add(mixed(40, 5, 12, 3, 3, 2, rejoin=0.9))
add(mixed(200, 20, 60, 3, 3, 2, rejoin=0.9))
add(mixed(2000, 100, 3000, 3, 3, 2, rejoin=0.7))
add(mixed(5000, 1000, 6000, 2, 3, 1, rejoin=0.9, tail_leave=300))
add(mixed(20000, 5000, 30000, 1, 1, 1, rejoin=0.8))
add(mixed(40000, 10000, 60000, 2, 2, 1, rejoin=0.9, tail_leave=5000))

Q = MAXQ


def heavy(prefill, leaves, rejoins, lo, hi, where=None):
    ids = random.sample(range(lo, hi + 1), prefill)
    order = where(list(ids)) if where else random.sample(ids, prefill)
    when = set(random.sample(range(1, leaves), rejoins))
    ops, left = [J(x) for x in ids], []
    for k, x in enumerate(order[:leaves]):
        ops.append(L(x))
        left.append(x)
        if k in when:
            i = random.randrange(len(left))
            left[i], left[-1] = left[-1], left[i]
            ops.append(J(left.pop()))
    waiting = prefill - leaves + rejoins
    ops += [S] * min(Q - len(ops), waiting)
    return ops


add(heavy(Q // 2, Q // 2, 0, 1, 250000))


def backish(o, block):
    o = o[::-1]
    out = []
    for i in range(0, len(o), block):
        out += random.sample(o[i:i + block], len(o[i:i + block]))
    return out


add(heavy(185000, 175000, 30000, 1, 250000, where=lambda o: backish(o, 20000)))
add(heavy(190000, 170000, 20000, 1, 250000, where=lambda o: o[::-1]))
add(heavy(180000, 160000, 30000, 1, 250000, where=lambda o: random.sample(o[90000:], 90000) + o[:90000]))
add(heavy(185000, 165000, 25000, 1, 250000, where=lambda o: backish(o, 1000)))
add(heavy(185000, 165000, 40000, 1, 250000, where=lambda o: backish(o, 60000)))
add(heavy(200000, 190000, 5000, 1, 250000, where=lambda o: sorted(o)))

os.makedirs("tests", exist_ok=True)
for i, ops in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(f"{len(ops)}\n" + "".join("%d %d\n" % op if len(op) == 2 else "3\n" for op in ops))
