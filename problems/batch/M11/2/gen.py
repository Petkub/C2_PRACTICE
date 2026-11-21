# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(511002)
MAXN = 180000
tests = []


def add(n, ops):
    assert 1 <= n <= MAXN and len(ops) == n - 1
    alive = [True] * (n + 1)
    for t, x, y in ops:
        assert t in (1, 2) and 1 <= x <= n and 1 <= y <= n and x != y and alive[x] and alive[y]
        alive[y] = False
    tests.append(f"{n}\n" + "".join(f"{t} {x} {y}\n" for t, x, y in ops))


def flips(p):
    return 2 if random.random() < p else 1


def rnd_ops(n, p=0.5):
    alive = list(range(1, n + 1))
    ops = []
    while len(alive) > 1:
        i, j = random.sample(range(len(alive)), 2)
        ops.append((flips(p), alive[i], alive[j]))
        alive[j] = alive[-1]
        alive.pop()
    return ops


def chain(n, p=0.5, flip_roles=False):

    lab = list(range(1, n + 1))
    random.shuffle(lab)
    ops, cur = [], lab[0]
    for v in lab[1:]:
        if flip_roles:
            ops.append((flips(p), v, cur))
            cur = v
        else:
            ops.append((flips(p), cur, v))
    return ops


def balanced(n, p=0.5):
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    ops, level = [], lab
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level) - 1, 2):
            a, b = level[i], level[i + 1]
            if random.random() < 0.5:
                a, b = b, a
            ops.append((flips(p), a, b))
            nxt.append(a)
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return ops


def mixed(n, p=0.5):

    lab = list(range(1, n + 1))
    random.shuffle(lab)
    ops, i, cur = [], 1, lab[0]
    while i < n:
        k = min(n - i, random.randint(1, 6))
        part = lab[i:i + k]
        for v in part[1:]:
            ops.append((flips(p), part[0], v))
        if random.random() < 0.5:
            ops.append((flips(p), cur, part[0]))
        else:
            ops.append((flips(p), part[0], cur))
            cur = part[0]
        i += k
    return ops


add(4, [(2, 1, 2), (1, 3, 4), (2, 3, 1)])
add(6, [(2, 2, 1), (1, 5, 6), (2, 4, 5), (2, 4, 2), (1, 3, 4)])
add(5, [(1, 5, 4), (1, 5, 3), (1, 5, 2), (1, 5, 1)])
add(1, [])
add(7, [(2, 5, 4), (1, 6, 3), (2, 2, 5), (2, 2, 6), (2, 1, 7), (2, 2, 1)])

add(2, [(2, 2, 1)])
add(3, [(2, 1, 2), (2, 3, 1)])
add(8, balanced(8, 1.0))
add(10, rnd_ops(10))
add(12, chain(12, 0.7, True))
add(16, balanced(16, 0.6))
add(15, mixed(15))

add(3000, rnd_ops(3000))
add(4096, balanced(4096, 0.5))
add(5000, chain(5000, 0.5, True))
add(40000, rnd_ops(40000))
add(50000, balanced(50000, 0.5))
add(30000, rnd_ops(30000, 0.95))

add(MAXN, chain(MAXN, 0.5, False))
add(MAXN, chain(MAXN, 0.5, True))
add(MAXN, chain(MAXN, 1.0, True))
add(MAXN, mixed(MAXN, 0.5))
add(MAXN, mixed(MAXN, 0.9))
add(MAXN, chain(MAXN, 0.0, True))
add(MAXN - 1, chain(MAXN - 1, 0.3, False))
add(MAXN, mixed(MAXN, 0.2))
add(MAXN, chain(MAXN, 0.8, False))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
