# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(170009)
MAXN, MAXQ, MAXT, MAXTIME = 200_000, 100_000, 10**6, 10**12
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(init, ops):
    n, q = len(init), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= t <= MAXT for t in init)
    asked = False
    out = []
    for op in ops:
        if op[0] == 1:
            assert len(op) == 3 and 1 <= op[1] <= n and 1 <= op[2] <= MAXT
            out.append("1 %d %d\n" % op[1:])
        elif op[0] == 2:
            assert len(op) == 2 and 1 <= op[1] <= n
            asked = True
            out.append("2 %d\n" % op[1])
        else:
            assert op[0] == 3 and len(op) == 2 and 0 <= op[1] <= MAXTIME
            asked = True
            out.append("3 %d\n" % op[1])
    assert asked
    tests.append(f"{n} {q}\n" + " ".join(map(str, init)) + "\n" + "".join(out))


class Sheet:

    def __init__(self, init):
        n = len(init)
        self.n = n
        self.who = list(range(1, n + 1))
        self.sec = list(init)
        self.line = list(range(-1, n))
        self.total = sum(init)
        self.head = 0

    def submit(self, x, t):
        self.total += t - self.sec[self.line[x]]
        self.line[x] = len(self.who)
        self.who.append(x)
        self.sec.append(t)

    def valid(self, i):
        return self.line[self.who[i]] == i

    def recent(self, depth):
        while True:
            i = ri(max(0, len(self.who) - depth), len(self.who) - 1)
            if self.valid(i):
                return self.who[i]

    def first(self):
        while not self.valid(self.head):
            self.head += 1
        return self.who[self.head]

    def tail_time(self, k):
        t, i = self.total, len(self.who) - 1
        for _ in range(ri(1, k)):
            while i >= 0 and not self.valid(i):
                i -= 1
            if i < 0:
                break
            t -= self.sec[i]
            i -= 1
        return t

    def start_of(self, x):
        return sum(self.sec[i] for i in range(self.line[x]) if self.valid(i))


def build(init, q, p_sub, dur, who_again, ask):
    sh, ops = Sheet(init), []
    for _ in range(q):
        if random.random() < p_sub:
            x, t = who_again(sh), dur()
            sh.submit(x, t)
            ops.append((1, x, t))
        else:
            ops.append(ask(sh))
    return ops


def anyone(sh):
    return ri(1, sh.n)


def ask_small(sh):
    r = random.random()
    if r < 0.35:
        return (2, ri(1, sh.n))
    if r < 0.7:
        return (3, max(0, sh.start_of(ri(1, sh.n)) + ri(-1, 1)))
    if r < 0.8:
        return (3, sh.total + ri(-1, 2))
    return (3, ri(0, sh.total))


def ask_mix(p2, p_tail, k=5, depth=0):
    def f(sh):
        r = random.random()
        if r < p2:
            return (2, sh.recent(depth) if depth else ri(1, sh.n))
        if r < p2 + p_tail:
            return (3, max(0, sh.tail_time(k) - ri(0, 1)))
        if r < p2 + p_tail + 0.03:
            return (3, min(MAXTIME, sh.total + ri(0, 2)))
        return (3, ri(sh.total // 5, sh.total))
    return f


add([30, 20, 45], [(2, 3), (1, 1, 10), (2, 3), (3, 65)])
add([5, 3], [(3, 5), (3, 8), (1, 1, 4), (3, 5)])
add([10], [(1, 1, 4), (2, 1), (3, 3), (3, 4)])
add([MAXT, MAXT, MAXT - 1], [(3, 2 * MAXT), (1, 1, MAXT), (2, 1), (3, MAXTIME)])
add([12, 8, 8, 6], [(1, 1, 2), (1, 3, 9), (2, 1), (3, 13), (3, 0)])

add([1], [(3, 0), (3, 1), (2, 1), (1, 1, 1), (3, 0)])
add([7, 7, 2, 1], [(1, 4, 5), (2, 4), (1, 2, 3), (3, 8), (3, 9), (2, 2), (3, 6), (3, 7), (3, 17)])
for n, q, tmax, p in ((2, 30, 5, 0.5), (6, 80, 3, 0.4), (20, 300, 100, 0.5), (200, 2000, MAXT, 0.3),
                      (10, 3000, MAXT, 0.5), (1500, 3000, MAXT, 0.4)):
    init = [ri(1, tmax) for _ in range(n)]
    add(init, build(init, q, p, lambda: ri(1, tmax), anyone, ask_small))
init = [ri(MAXT - 9, MAXT) for _ in range(12_000)]
add(init, build(init, 14_000, 0.3, lambda: ri(MAXT - 9, MAXT), anyone, ask_mix(0.4, 0.3)))

N, Q = MAXN, MAXQ
big = lambda: ri(MAXT // 2, MAXT)
init = [big() for _ in range(N)]
add(init, build(init, Q, 0.1, big, anyone, ask_mix(0.5, 0.05)))
init = [ri(1, MAXT) for _ in range(N)]
add(init, build(init, Q, 0.15, lambda: ri(1, MAXT), lambda sh: sh.first(), ask_mix(0.45, 0.1)))
init = [MAXT] * N
add(init, build(init, Q, 0.12, lambda: MAXT, anyone, ask_mix(0.4, 0.2, 3)))
init = [1] * N
add(init, build(init, Q, 0.1, lambda: 1, anyone, ask_mix(0.5, 0.1, 9)))
init = [big() for _ in range(N)]
add(init, build(init, Q, 0.08, big, lambda sh: sh.recent(50), ask_mix(0.6, 0.2, 4)))
init = [random.choice((1, MAXT)) for _ in range(N)]
add(init, build(init, Q, 0.2, lambda: random.choice((1, MAXT)), lambda sh: sh.first(), ask_mix(0.5, 0.05, 7)))
init = [big() for _ in range(N)]
add(init, build(init, Q, 0.1, big, anyone, ask_mix(0.65, 0.1, 6, 150_000)))
init = [ri(1, 1000) for _ in range(N)]
add(init, build(init, Q, 0.12, lambda: ri(1, 1000), lambda sh: sh.first(), ask_mix(0.5, 0.1, 6)))
init = [ri(MAXT - 99, MAXT) for _ in range(N)]
add(init, build(init, Q, 0.25, lambda: ri(MAXT - 99, MAXT), anyone, ask_mix(0.45, 0.0)))
init = [big() for _ in range(N)]
add(init, build(init, Q, 0.05, big, lambda sh: sh.first(), ask_mix(0.1, 0.1, 10)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
