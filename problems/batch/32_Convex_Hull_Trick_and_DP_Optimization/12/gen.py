# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(321201)
MAXN = MAXM = 100_000
MAXQ = 70_000
MAXV = 10**9
rr = random.randrange
tests = []


def add(r1, d, c, qs):
    n, m = len(d) + 1, len(c)
    assert 2 <= n <= MAXN and 2 <= m <= MAXM and 1 <= len(qs) <= MAXQ
    assert all(d[i] <= d[i + 1] for i in range(len(d) - 1))
    r = r1
    assert 1 <= r <= MAXV
    for v in d:
        r += v
        assert 1 <= r <= MAXV
    assert all(1 <= v <= MAXV for v in c)
    assert all(1 <= a <= b <= n and 1 <= y <= m for a, b, y in qs)
    tests.append(f"{n} {m} {len(qs)}\n" + " ".join(map(str, [r1] + d)) + "\n" + " ".join(map(str, c)) + "\n"
                 + "".join(f"{a} {b} {y}\n" for a, b, y in qs))


def rows(n, kind):
    k = n - 1
    if kind == "valley":
        a = min(20_000, 1_800_000_000 // max(1, k))
        d = sorted(rr(-a, a + 1) for _ in range(k))
    elif kind == "incr":
        a = min(20_000, 1_900_000_000 // max(1, k))
        d = sorted(rr(a + 1) for _ in range(k))
    elif kind == "decr":
        a = min(20_000, 1_900_000_000 // max(1, k))
        d = sorted(-rr(a + 1) for _ in range(k))
    elif kind == "flat":
        d = [0] * k
    elif kind == "few":
        vals = sorted(rr(-15_000, 15_001) for _ in range(4))
        d = sorted(vals[rr(4)] for _ in range(k))
    elif kind == "square":
        d = [t // 5 for t in range(1, k + 1)]
    else:
        raise ValueError(kind)
    low = cur = 0
    high = 0
    for v in d:
        cur += v
        low, high = min(low, cur), max(high, cur)
    spare = MAXV - (high - low) - 1
    assert spare >= 0
    r1 = 1 - low + rr(min(spare, 1000) + 1)
    return r1, d


def cols(m, kind):
    if kind == "rand":
        return [1 + rr(MAXV) for _ in range(m)]
    if kind == "small":
        return [1 + rr(10) for _ in range(m)]
    if kind == "convex":
        p, den = m // 2, max(1, (m // 2) ** 2 // 500_000_000 + 1)
        return [1 + (y - p) ** 2 // den + rr(30) for y in range(1, m + 1)]
    if kind == "convinc":
        den = max(1, m * m // 1_000_000_000 + 1)
        return [1 + y * y // den + rr(30) for y in range(1, m + 1)]
    if kind == "decr":
        step = max(1, (MAXV - 1) // m)
        return [MAXV - step * (y - 1) - rr(step) for y in range(1, m + 1)]
    if kind == "steps":
        return [1 + rr(100) if rr(1000) == 0 else MAXV - rr(1000) for _ in range(m)]
    raise ValueError(kind)


def queries(n, m, q, kind):
    out = []
    for _ in range(q):
        if kind == "rand":
            a = 1 + rr(n)
            b = a + rr(n - a + 1)
            y = 1 + rr(m)
        elif kind == "far":
            a = 1 + rr(1 + n // 50)
            b = n - rr(1 + n // 50)
            y = m - rr(1 + m // 50)
        elif kind == "wide":
            a = 1 + rr((n + 1) // 2)
            b = n // 2 + 1 + rr(n - n // 2)
            y = 1 + rr(m)
        elif kind == "mixed":
            t = rr(6)
            a = 1 if t == 0 else 1 + rr(n) if t == 1 else 1 + rr((n + 1) // 2)
            b = a if t == 1 else n if t == 2 else a + n // 3 + rr(n - a - n // 3 + 1)
            y = 1 if t == 3 else m if t == 4 else 1 + rr(m)
        else:
            raise ValueError(kind)
        out.append((a, b, y))
    if kind == "mixed":
        out[0] = (1, n, m)
    return out


def case(n, m, q, rk, ck, qk):
    r1, d = rows(n, rk)
    add(r1, d, cols(m, ck), queries(n, m, q, qk))


def write_all():
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


add(4, [-2, 1], [6, 5, 2, 3], [(1, 3, 4), (2, 3, 4), (3, 3, 2)])
add(5, [0, 0, 0], [3, 1, 4], [(1, 4, 3), (2, 3, 2)])
add(7, [-3, -1, 0, 1], [9, 4, 5, 8, 9, 3], [(1, 3, 6), (2, 5, 4), (4, 5, 6)])
add(10, [-3, -2, -1, -1, 0], [7, 2, 5, 6, 6], [(1, 6, 5), (3, 6, 4), (4, 4, 1)])
add(MAXV, [-(MAXV - 1), 0], [MAXV, 1, MAXV], [(1, 3, 2), (1, 3, 3), (2, 3, 1)])

add(1, [0], [1, 1], [(1, 1, 1), (1, 2, 2), (1, 1, 2), (1, 2, 1), (2, 2, 2), (2, 2, 1)])
add(MAXV, [0], [MAXV, MAXV], [(1, 2, 2), (1, 1, 2), (1, 2, 1), (2, 2, 2)])
case(6, 7, 20, "valley", "small", "rand")
case(9, 12, 60, "valley", "convex", "wide")
case(8, 8, 30, "few", "rand", "mixed")
case(40, 30, 200, "valley", "convex", "rand")
case(60, 80, 300, "square", "rand", "far")
case(200, 150, 300, "incr", "convinc", "rand")
case(300, 300, 300, "decr", "decr", "mixed")
case(250, 300, 300, "valley", "steps", "far")
case(3000, 2000, 200, "valley", "convex", "rand")
case(20_000, 30_000, 20_000, "few", "rand", "mixed")

case(MAXN, MAXM, MAXQ, "valley", "convex", "rand")
case(MAXN, MAXM, MAXQ, "valley", "rand", "far")
case(MAXN, MAXM, MAXQ, "incr", "convinc", "mixed")
case(MAXN, MAXM, MAXQ, "decr", "decr", "wide")
case(MAXN, MAXM, MAXQ, "few", "convex", "far")
case(MAXN, MAXM, MAXQ, "flat", "rand", "mixed")
case(MAXN, MAXM, MAXQ, "square", "convex", "rand")
case(MAXN, MAXM, MAXQ, "valley", "steps", "mixed")
case(MAXN, MAXM, MAXQ, "incr", "small", "far")
case(MAXN, MAXM, MAXQ, "valley", "convinc", "wide")
case(MAXN, MAXM, MAXQ, "few", "decr", "mixed")
case(MAXN, MAXM, MAXQ, "square", "steps", "wide")
write_all()
