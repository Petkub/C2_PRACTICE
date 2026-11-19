# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(43004)
MAXN, MAXQ, MAXY = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, k, ev):
    q = len(ev)
    assert 1 <= k <= n <= MAXN and 1 <= q <= MAXQ
    ys = [e[2] for e in ev if e[0] == 1]
    assert len(set(ys)) == len(ys) and all(0 <= y <= MAXY for y in ys)
    assert all(1 <= e[1] <= n for e in ev if e[0] == 1)
    assert any(e[0] == 2 for e in ev)
    tests.append(f"{n} {k} {q}\n" + "".join("2\n" if e[0] == 2 else f"1 {e[1]} {e[2]}\n" for e in ev))


def values(cnt, lo=0, hi=MAXY):
    return random.sample(range(lo, hi + 1), cnt)


def events(n, q, cook, kindf, order=None):
    plan = [2 if random.random() < cook else 1 for _ in range(q)]
    if 2 not in plan:
        plan[-1] = 2
    ys = values(plan.count(1))
    if order == "up":
        ys.sort()
    elif order == "down":
        ys.sort(reverse=True)
    it = iter(ys)
    return [(2,) if p == 2 else (1, kindf(), next(it)) for p in plan]


def heavy(n, share):
    return lambda: 1 if random.random() < share else ri(1, n)


def tiny(n, k, q, cook):
    ev, stock = [], 0
    ys = iter(values(q, 0, 10 * q))
    for _ in range(q):
        if stock >= 12 or (stock > 0 and random.random() < cook):
            ev.append((2,))
            stock = max(0, stock - k) if stock >= k else stock
        else:
            ev.append((1, ri(1, n), next(ys)))
            stock += 1
    if all(e[0] == 1 for e in ev):
        ev.append((2,))
    return ev


add(3, 2, [(1, 1, 5), (1, 2, 3), (2,), (2,), (1, 1, 7), (1, 1, 4), (1, 3, 6), (2,), (2,)])
add(4, 1, [(1, 2, 10), (1, 4, 30), (1, 2, 20), (2,), (2,), (1, 1, 15), (2,), (2,), (2,)])
add(3, 3, [(1, 1, 4), (1, 2, 8), (2,), (1, 3, 6), (2,), (1, 1, 9), (2,)])
add(5, 3, [(1, 5, 1000000000), (1, 3, 999999999), (1, 1, 999999998), (1, 2, 0), (2,), (2,)])
add(2, 2, [(2,), (1, 2, 6), (1, 1, 2), (1, 2, 1), (2,), (1, 1, 5), (2,)])


add(1, 1, [(2,), (1, 1, 0), (2,), (2,)])
add(2, 1, [(1, 1, 5), (1, 1, 9), (1, 2, 7), (2,), (2,), (2,), (2,)])
add(3, 2, [(1, 1, 9), (1, 1, 8), (1, 2, 1), (2,), (2,)])
add(3, 2, [(1, 1, 9), (1, 1, 8), (1, 1, 7), (2,), (1, 3, 1), (2,)])
add(2, 1, [(1, 2, 3), (1, 2, 10), (1, 1, 5), (2,), (2,)])
for n, k, q, c in [(3, 2, 30, 0.3), (5, 3, 80, 0.35), (6, 3, 120, 0.25), (4, 4, 150, 0.3), (8, 2, 300, 0.4)]:
    add(n, k, tiny(n, k, q, c))
add(5, 2, events(5, 3000, 0.3, heavy(5, 0.6)))


add(1000, 1000, events(1000, MAXQ, 0.002, lambda: ri(1, 1000)))


N, Q = MAXN, MAXQ
add(N, 1, events(N, Q, 0.5, lambda: ri(1, N)))
add(N, 2, events(N, Q, 0.45, heavy(N, 0.5)))
add(N, 5, events(N, Q, 0.3, lambda: ri(1, N), "up"))
add(N, 3, events(N, Q, 0.35, heavy(N, 0.7), "down"))
add(N, 50, events(N, Q, 0.4, lambda: ri(1, 30)))
add(N, 2, events(N, Q, 0.4, lambda: ri(1, 3)))
add(N, 1000, events(N, Q, 0.3, lambda: ri(1, N)))
add(N, N, events(N, Q, 0.3, lambda: ri(1, N)))
ev = [(1, x, y) for x, y in zip(range(1, N // 2 + 1), values(N // 2))] + [(2,)] * (Q - N // 2)
add(N, 1, ev)
add(N, 4, events(N, Q, 0.25, heavy(N, 0.3)))
add(N, 10, events(N, Q, 0.4, lambda: ri(1, N)))
add(N, 2, events(N, Q, 0.4, heavy(N, 0.4), "up"))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
