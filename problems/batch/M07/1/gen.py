# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(47001)
MAXN, MAXQ = 2 * 10**9, 100_000
tests = []


def add(n, evs):
    assert 1 <= n <= MAXN and 1 <= len(evs) <= MAXQ
    lines = []
    for e in evs:
        if e[0] == "SEND":
            assert len(e) == 3 and 1 <= e[1] <= n and 1 <= e[2] <= n
        else:
            assert e[0] in ("SLEEP", "WAKE") and len(e) == 2 and 1 <= e[1] <= n
        lines.append(" ".join(map(str, e)))
    tests.append(f"{n} {len(evs)}\n" + "\n".join(lines) + "\n")


def rnd(n, q, p_send=0.5, p_wake=0.3, span=None, pool=None, p_again=0.15, p_back=0.5):
    asleep, order, evs = set(), [], []
    for _ in range(q):
        r = random.random()
        if r < p_send:
            if span is None:
                x, y = random.randint(1, n), random.randint(1, n)
            else:
                ln = random.randint(0, min(span, n - 1))
                x = random.randint(1, n - ln)
                y = x + ln
            if (x < y) == (random.random() < p_back):
                x, y = y, x
            evs.append(("SEND", x, y))
        elif r < p_send + (1 - p_send) * p_wake and order:
            if random.random() < p_again:
                evs.append(("WAKE", pool() if pool else random.randint(1, n)))
            else:
                k = random.randrange(len(order))
                order[k], order[-1] = order[-1], order[k]
                x = order.pop()
                if x in asleep:
                    asleep.discard(x)
                    evs.append(("WAKE", x))
                else:
                    evs.append(("WAKE", x))
        else:
            if asleep and random.random() < p_again:
                x = random.choice(order) if order else random.randint(1, n)
            else:
                x = pool() if pool else random.randint(1, n)
            asleep.add(x)
            order.append(x)
            evs.append(("SLEEP", x))
    return evs


add(10, [("SEND", 2, 7), ("SLEEP", 6), ("SEND", 1, 7), ("SEND", 1, 5), ("SLEEP", 4), ("SEND", 1, 3),
         ("WAKE", 4), ("SEND", 5, 1)])
add(5, [("SLEEP", 3), ("SEND", 3, 3), ("SEND", 1, 3), ("SEND", 4, 5), ("WAKE", 3), ("SEND", 3, 3)])
add(2 * 10**9, [("SLEEP", 1000000000), ("SEND", 1, 999999999), ("SEND", 1, 2000000000),
                ("SEND", 2000000000, 1000000001), ("SLEEP", 2000000000), ("SEND", 1000000001, 2000000000)])
add(1, [("SEND", 1, 1), ("WAKE", 1), ("SLEEP", 1), ("SEND", 1, 1), ("SLEEP", 1)])
add(7, [("SLEEP", 2), ("SLEEP", 6), ("SEND", 3, 5), ("SEND", 4, 7), ("WAKE", 2), ("SEND", 1, 5),
        ("SEND", 5, 1)])

add(3, [("SLEEP", 2), ("SLEEP", 2), ("WAKE", 2), ("SEND", 1, 3), ("SEND", 3, 1)])
add(9, [("SLEEP", 5), ("SEND", 9, 1), ("SEND", 6, 4), ("SEND", 4, 6), ("SEND", 9, 6)])
add(6, [("SLEEP", 1), ("SLEEP", 6), ("SEND", 1, 6), ("SEND", 2, 5), ("SEND", 6, 2), ("SEND", 5, 1)])
add(20, rnd(20, 60))
add(50, rnd(50, 200, span=8))
add(1000, rnd(1000, 1000, span=40))
add(100, rnd(100, 2000, p_again=0.4))

add(10**6, rnd(10**6, 5000, span=3000))
add(MAXN, rnd(MAXN, 20000))

add(MAXN, rnd(MAXN, MAXQ))
add(MAXN, rnd(MAXN, MAXQ, p_send=0.6, span=10**5))
add(MAXN, rnd(MAXN, MAXQ, pool=lambda: random.randint(1, 1000)))
add(MAXN, rnd(MAXN, MAXQ, pool=lambda: random.choice((random.randint(1, 10), MAXN - random.randint(0, 9))),
               p_again=0.4))
add(MAXN, rnd(MAXN, MAXQ, p_send=0.3, p_wake=0.45, p_again=0.35))
add(MAXN, rnd(MAXN, MAXQ, p_back=0.9, span=10**8))
add(10**5, rnd(10**5, MAXQ, pool=lambda: random.randint(1, 10**5), span=200))
evs = [("SLEEP", x) for x in range(1, MAXQ // 2 + 1)]
evs += [("SEND", MAXN - random.randint(0, 10**9), MAXN - random.randint(0, 10**9)) for _ in range(MAXQ // 2 - 1)]
evs.append(("SEND", MAXN, 1))
add(MAXN, evs)
evs = []
for i in range(MAXQ // 4):
    evs += [("SLEEP", 10**9), ("SLEEP", 10**9), ("WAKE", 10**9), ("SEND", random.randint(1, 10**9), MAXN)]
add(MAXN, evs[:MAXQ])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
