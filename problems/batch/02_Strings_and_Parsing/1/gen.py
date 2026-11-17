# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(734519)
MAXS, MAXQ, MAXV, MAXK = 1_000_000, 100_000, 10**9, 10**15
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


class Tree:

    def __init__(self):
        self.val, self.left, self.right = [], [], []

    def new(self, v):
        self.val.append(v)
        self.left.append(-1)
        self.right.append(-1)
        return len(self.val) - 1

    def text(self):
        if not self.val:
            return "()"
        out, st = [], [0]
        L, R, V = self.left, self.right, self.val
        push, pop, emit = st.append, st.pop, out.append
        while st:
            v = pop()
            if v.__class__ is str:
                emit(v)
                continue
            emit("(" + str(V[v]))
            push(")")
            push(R[v] if R[v] >= 0 else "()")
            push(L[v] if L[v] >= 0 else "()")
        return "".join(out)

    def totals(self):
        ends, half = [], []
        if not self.val:
            return ends, half
        st = [(0, self.val[0])]
        while st:
            v, s = st.pop()
            l, r = self.left[v], self.right[v]
            if l < 0 and r < 0:
                ends.append(s)
            elif l < 0 or r < 0:
                half.append(s)
            for c in (l, r):
                if c >= 0:
                    st.append((c, s + self.val[c]))
        return ends, half


def build(shape, budget, vals):
    t = Tree()
    used = 2
    free = []
    last = -1

    def put(p, side, v):
        nonlocal used, last
        c = t.new(v)
        if p >= 0:
            (t.left, t.right)[side][p] = c
        used += len(str(v)) + 4
        if shape in ("random", "deep"):
            free.append((c, 0))
            free.append((c, 1))
        last = c
        return c

    def pop_free():
        while True:
            j = ri(0, len(free) - 1)
            free[j], free[-1] = free[-1], free[j]
            p, side = free.pop()
            if (t.left, t.right)[side][p] < 0:
                return p, side

    put(-1, 0, vals())
    while True:
        v = vals()
        if used + len(str(v)) + 4 > budget:
            break
        if shape == "random":
            p, side = pop_free()
        elif shape in ("chain", "comb", "ladder"):
            p, side = last, ri(0, 1)
        elif shape == "deep":
            if random.random() < 0.998:
                p, side = last, ri(0, 1)
            else:
                p, side = pop_free()
        else:
            raise ValueError(shape)
        put(p, side, v)
        if shape == "comb":
            v2 = vals()
            if used + len(str(v2)) + 4 > budget:
                break
            put(p, 1 - side, v2)
            last = (t.left, t.right)[side][p]
        elif shape == "ladder":
            c = (t.left, t.right)[side][p]
            q, ok = p, True
            for _ in range(ri(1, 3)):
                v2 = vals()
                if used + len(str(v2)) + 4 > budget:
                    ok = False
                    break
                put(q, (1 - side) if q == p else ri(0, 1), v2)
                q = last
            last = c
            if not ok:
                break
    assert used <= budget
    t.used = used
    return t


def bump(t, k, v):
    used = getattr(t, "used", None)
    for i in range(min(k, len(t.val))):
        if used is not None:
            used += len(str(v)) - len(str(t.val[i]))
        t.val[i] = v
    if used is not None:
        t.used = used
    return t


def complete(depth, vals):
    t = Tree()
    t.new(vals())
    level = [0]
    for _ in range(depth - 1):
        nxt = []
        for p in level:
            a, b = t.new(vals()), t.new(vals())
            t.left[p], t.right[p] = a, b
            nxt += [a, b]
        level = nxt
    return t


def queries(t, q, mix=(0.5, 0.2, 0.3)):
    ends, half = t.totals()
    pool = ends + half
    n1 = int(q * mix[0]) if ends else 0
    n2 = int(q * mix[1]) if half else 0
    n3 = int(q * mix[2] * 0.7) if pool else 0
    out = random.choices(ends, k=n1) + random.choices(half, k=n2)
    out += [k + ri(-3, 3) for k in random.choices(pool, k=n3)]
    out += [ri(-10**6, 10**6) for _ in range(q - len(out))]
    random.shuffle(out)
    return [max(-MAXK, min(MAXK, k)) for k in out]


def add_text(s, ks):
    assert 2 <= len(s) <= MAXS and 1 <= len(ks) <= MAXQ
    assert all(-MAXK <= k <= MAXK for k in ks)
    tests.append(s + "\n" + str(len(ks)) + "\n" + " ".join(map(str, ks)) + "\n")


def add(t, q, mix=(0.5, 0.2, 0.3)):
    assert all(-MAXV <= v <= MAXV for v in t.val)
    s = t.text()
    assert len(s) == getattr(t, "used", len(s)) <= MAXS
    add_text(s, queries(t, q, mix))


add_text("(5(-2()())(3(4()())()))", [3, 12, 7])
add_text("(1(2(3()())(3()()))(-4()(9()())))", [6, 3])
add_text("()", [0, 5])
add_text("(7()())", [7, -7])
add_text("(-3(-3(-3()())())(10()(-16()())))", [-9, 0, 1])

small = lambda: ri(-5, 5)
add(build("random", 60, small), 20)
add(build("chain", 80, small), 15)
add(build("comb", 120, small), 30)
add(build("deep", 300, lambda: ri(-20, 20)), 50)
add(complete(6, lambda: ri(0, 3)), 40)
add(build("random", 3000, lambda: ri(-MAXV, MAXV)), 200)
add(build("chain", 20000, lambda: ri(MAXV - 100, MAXV)), 300, (0.4, 0.4, 0.2))
add(build("comb", 50000, lambda: ri(-1, 1)), 1000)

Q = MAXQ
B = MAXS - 100
add(build("random", MAXS, lambda: ri(-9, 9)), Q)
add(bump(build("random", B, lambda: ri(-99, 99)), 4, MAXV), Q, (0.4, 0.4, 0.2))
add(build("comb", MAXS, lambda: ri(0, 9)), Q)
add(bump(build("comb", B, lambda: ri(0, 99)), 3, MAXV), Q, (0.4, 0.4, 0.2))
add(bump(build("comb", B, lambda: -ri(0, 9)), 4, -MAXV), Q, (0.4, 0.4, 0.2))
add(build("ladder", MAXS, lambda: ri(-2, 2)), Q, (0.3, 0.5, 0.2))
add(bump(build("ladder", B, lambda: ri(0, 9)), 5, MAXV), Q, (0.3, 0.5, 0.2))
add(build("random", MAXS, lambda: ri(0, 1)), Q, (0.2, 0.6, 0.2))
add(complete(17, lambda: ri(0, 2)), Q)
add(bump(complete(17, lambda: ri(-9, 9)), 3, -MAXV), Q)
add(build("ladder", MAXS, lambda: ri(-9, 9)), Q, (0.3, 0.5, 0.2))
add(bump(build("random", B, lambda: ri(-9, 9)), 6, -MAXV), Q, (0.4, 0.4, 0.2))

add(build("chain", 300_000, lambda: MAXV), 1000, (0.3, 0.5, 0.2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
