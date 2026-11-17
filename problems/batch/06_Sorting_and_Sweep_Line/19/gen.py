# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(41800)
MAXL = 10**9
MAXQ = 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(L, ops):
    q = len(ops)
    assert 1 <= L <= MAXL and 1 <= q <= MAXQ
    arrived, present = 0, set()
    lines = []
    for op in ops:
        if op == 0:
            assert len(present) < L
            arrived += 1
            present.add(arrived)
            lines.append("IN")
        else:
            assert op in present
            present.remove(op)
            lines.append(f"OUT {op}")
    tests.append(f"{L} {q}\n" + "\n".join(lines) + "\n")


class Room:

    def __init__(self, L):
        self.L, self.ops, self.arrived = L, [], 0
        self.present, self.pos = [], {}

    def come(self, times=1):
        for _ in range(times):
            if len(self.present) == self.L:
                return
            self.arrived += 1
            self.pos[self.arrived] = len(self.present)
            self.present.append(self.arrived)
            self.ops.append(0)

    def leave(self, i=None):
        if not self.present:
            return
        if i is None:
            i = ri(0, len(self.present) - 1)
        p, last = self.present[i], self.present[-1]
        self.present[i], self.pos[last] = last, i
        self.present.pop()
        del self.pos[p]
        self.ops.append(p)

    def leave_ordered(self, k):
        self.leave(self.pos[k])


def mixed(L, q, p_in):
    r = Room(L)
    while len(r.ops) < q:
        if not r.present or (len(r.present) < L and random.random() < p_in):
            r.come()
        else:
            r.leave()
    return r.ops


add(10, [0, 0, 0, 0, 3, 0])
add(6, [0, 0, 0, 1, 0])
add(1, [0, 1, 0])
add(2, [0, 0, 1, 0])
add(8, [0, 0, 0, 0])

add(3, [0, 0, 0, 2, 0, 1, 3, 0])
add(5, mixed(5, 40, 0.55))
add(16, mixed(16, 200, 0.6))
add(17, mixed(17, 300, 0.5))
add(100, mixed(100, 1000, 0.7))
add(1000, mixed(1000, 2000, 0.6))
add(2000, [0] * 2000)
r = Room(3000)
r.come(1500)
for k in range(1, 1501):
    r.leave_ordered(k)
r.come(1000)
add(3000, r.ops)

Q = MAXQ
add(MAXL, [0] * Q)
add(Q, [0] * Q)
add(2 * Q - 1, [0] * Q)
r = Room(MAXL)
r.come(Q // 2)
while len(r.ops) < Q:
    r.leave()
    r.come()
add(MAXL, r.ops)
r = Room(2**29 + 1)
r.come(Q // 2)
while len(r.ops) + 1 < Q:
    r.leave(ri(0, 9))
    r.come()
add(2**29 + 1, r.ops)
add(MAXL, mixed(MAXL, Q, 0.7))
add(123_456_789, mixed(123_456_789, Q, 0.55))
r = Room(MAXL)
for _ in range(100):
    r.come(Q // 200 - 1)
    while r.present:
        r.leave()
    r.come(1)
    r.leave()
add(MAXL, r.ops[:Q])
r = Room(150_000)
r.come(140_000)
while len(r.ops) < Q:
    r.leave()
    r.come()
add(150_000, r.ops)
r = Room(MAXL)
r.come(Q * 3 // 4)
while len(r.ops) < Q:
    r.leave(len(r.present) - 1)
    r.come()
add(MAXL, r.ops)
r = Room(MAXL - 1)
r.come(Q // 2)
for k in range(2, Q // 4):
    r.leave_ordered(k)
r.come(Q - len(r.ops))
add(MAXL - 1, r.ops)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
