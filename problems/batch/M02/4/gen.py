# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random
from math import gcd

random.seed(4804)
MAXN = 200000
tests = []


def add(a, b):
    n, l = len(a), len(b)
    assert 1 <= l <= n <= MAXN
    assert all(1 <= x <= n for x in b) and len(set(b)) == l
    keys = [x for x in a if x != 0]
    assert all(1 <= x <= l for x in keys) and len(set(keys)) == len(keys)
    tests.append(f"{n} {l}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")


def build(parts, order="random"):
    n = sum(k for _, k in parts)
    ids = list(range(1, n + 1))
    if order == "random":
        random.shuffle(ids)
    else:
        parts = parts[:]
        random.shuffle(parts)
    pos = 0
    comps = []
    for kind, k in parts:
        c = ids[pos:pos + k]
        pos += k
        if order == "down":
            c.sort(reverse=True)
        comps.append((kind, c))
    locked = [i for kind, c in comps for i in (c[1:] if kind == "open" else c)]
    l = len(locked)
    mul = random.randrange(1, l + 1)
    while gcd(mul, l) != 1:
        mul += 1
    off = random.randrange(l)
    b = [0] * l
    lock_of = [0] * (n + 1)
    for t, i in enumerate(locked):
        j = (t * mul + off) % l
        b[j] = i
        lock_of[i] = j + 1
    a = [0] * (n + 1)
    for kind, c in comps:
        for t in range(len(c) - 1):
            a[c[t]] = lock_of[c[t + 1]]
        if kind == "cycle":
            a[c[-1]] = lock_of[c[0]]
    return a[1:], b


def mix(n, kinds, maxlen):
    parts, left = [], n
    while left > 0:
        k = min(left, random.randint(1, maxlen))
        parts.append((random.choice(kinds), k))
        left -= k
    if all(kind == "open" and k == 1 for kind, k in parts):
        parts[0] = ("cycle", parts[0][1])
    if not any(kind != "open" or k > 1 for kind, k in parts):
        parts.append(("shut", 1))
    return parts


add([2, 4, 0, 3, 0, 0], [2, 4, 5, 6])
add([1, 2, 3, 0], [2, 3, 4])
add([3, 2, 0, 4, 1], [1, 4, 2, 5])
add([0, 3, 5, 2, 1], [3, 5, 1, 4, 2])
add([4, 5, 0, 0, 0, 2, 0], [6, 7, 2, 3, 5])

add([1], [1])
add([2, 1], [1, 2])
add([0, 3, 1, 2], [3, 4, 2])
for parts in ([("cycle", 3), ("cycle", 4), ("open", 2), ("shut", 2)],
              [("cycle", 1), ("cycle", 2), ("cycle", 5), ("shut", 3)],
              [("open", 4), ("cycle", 6), ("shut", 1), ("open", 1)],
              [("cycle", 7), ("cycle", 7)],
              [("shut", 2), ("shut", 3), ("open", 3), ("cycle", 2), ("cycle", 3), ("cycle", 1)]):
    add(*build(parts))

add(*build(mix(2000, ["open", "shut", "cycle"], 40)))
add(*build(mix(5000, ["cycle"], 300), "down"))

N = MAXN
add(*build([("cycle", N)], "down"))
add(*build([("shut", N // 2), ("cycle", N // 2)], "down"))
add(*build([("open", N - 3), ("cycle", 1), ("cycle", 2)], "down"))
p = list(range(1, N + 1))
random.shuffle(p)
add(p, random.sample(range(1, N + 1), N))
add(*build(mix(N, ["open", "shut", "cycle"], 30000), "down"))
add(*build([("cycle", N // 3), ("cycle", N // 3)] + [("cycle", 1)] * (N - 2 * (N // 3))))
add(*build([("cycle", 2)] * 1000 + [("open", 3)] * 1000 + [("cycle", N - 7000)], "down"))
add(*build([("shut", 1)] * (N // 4) + [("cycle", N - N // 4)], "down"))
add(*build(mix(N - 120000, ["cycle", "shut"], 50) + [("cycle", 120000)]))
add(*build([("open", 60000), ("shut", 60000), ("cycle", 80000)], "down"))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
