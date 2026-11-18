# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(320202)
MAXN, MAXA, MAXB = 150_000, 1_000_000, 10 ** 9
tests = []


def add(a, b):
    n = len(b)
    assert 2 <= n <= MAXN and len(a) == n - 1
    assert all(1 <= v <= MAXA for v in a)
    assert b[-1] == 0 and all(b[i] > b[i + 1] for i in range(n - 1)) and b[0] <= MAXB
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")


def costs(n, kind):
    rnd = random.random
    if kind == "rand":
        s = set()
        while len(s) < n - 1:
            s.add(1 + int(rnd() * MAXB))
        return sorted(s, reverse=True) + [0]
    if kind == "convex":
        v, out = MAXB, []
        for i in range(n - 1):
            out.append(v)
            v = max(n - 2 - i, v - max(1, int(v * 0.0004 * (1 + rnd()))))
        return out + [0]
    if kind == "linear":
        step = MAXB // n - 1
        return [step * (n - 1 - i) + (n - 1 - i) for i in range(n - 1)] + [0]
    if kind == "small":
        return list(range(n - 1, 0, -1)) + [0]
    raise ValueError(kind)


def need(n, kind):
    rnd = random.random
    a = [1 + int(rnd() * MAXA) for _ in range(n - 1)]
    if kind == "rand":
        return a
    if kind == "desc":
        return sorted(a, reverse=True)
    if kind == "zigzag":
        return [1 + int(rnd() * 1000) if i % 2 else MAXA - int(rnd() * 1000) for i in range(n - 1)]
    if kind == "max":
        return [MAXA] * (n - 1)
    if kind == "lastbig":
        return [1 + int(rnd() * 100) for _ in range(n - 2)] + [MAXA]
    raise ValueError(kind)


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_000_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


add([2, 3, 5, 10], [10, 6, 4, 1, 0])
add([7, 1], [8, 5, 0])
add([5], [7, 0])
add([1, 4, 6, 9, 20], [100, 50, 20, 10, 3, 0])
add([3, 8, 2, 6], [9, 7, 3, 2, 0])

for n, ak, bk in [(6, "rand", "small"), (10, "zigzag", "small"), (40, "desc", "rand"), (200, "rand", "convex"),
                  (1000, "zigzag", "linear"), (5000, "lastbig", "rand"), (30_000, "desc", "convex"),
                  (60_000, "rand", "small")]:
    add(need(n, ak), costs(n, bk))

for ak, bk in [("rand", "rand"), ("desc", "rand"), ("zigzag", "convex"), ("rand", "convex"), ("max", "linear"),
               ("lastbig", "rand"), ("desc", "convex"), ("zigzag", "linear"), ("rand", "small"), ("desc", "small")]:
    add(need(MAXN, ak), costs(MAXN, bk))
write_all()
