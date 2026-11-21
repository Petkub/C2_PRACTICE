# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(500001)
MAXN = 100000
MAXC = 10 ** 9
MAXR = 2 * 10 ** 9
tests = []


def add(towers, spots):
    n = len(spots)
    assert len(towers) == 4 and 1 <= n <= MAXN
    assert all(abs(x) <= MAXC and abs(y) <= MAXC for x, y in towers)
    assert all(abs(x) <= MAXC and abs(y) <= MAXC and 0 <= r <= MAXR for x, y, r in spots)
    s = "".join(f"{x} {y}\n" for x, y in towers) + f"{n}\n"
    s += "".join(f"{x} {y} {r}\n" for x, y, r in spots)
    tests.append(s)


W = [(-3, 0), (3, 0), (0, -2), (0, 2)]
add(W, [(-2, -1, 3), (2, 1, 3), (0, 0, 2), (3, -1, 1)])
add(W, [(0, 0, 2), (-3, 1, 1), (-1, -1, 2)])
add([(0, 0), (4, 0), (0, 3), (4, 3)], [(5, 5, 1), (2, 1, 3), (0, 3, 0)])
add(W, [(0, 0, 2), (-3, 0, 0), (1, 1, 2), (3, 0, 1)])
add([(-5, 0), (5, 0), (0, -5), (0, 5)], [(0, 0, 4), (-5, 1, 1), (5, 0, 1), (1, -5, 2), (0, 4, 1)])


for n, c, rr in [(1, 5, 6), (6, 6, 5), (12, 8, 7), (30, 20, 15), (60, 50, 40)]:
    tw = [(random.randint(-c, c), random.randint(-c, c)) for _ in range(4)]
    add(tw, [(random.randint(-c, c), random.randint(-c, c), random.randint(0, rr)) for _ in range(n)])
add([(2, 2), (2, 2), (-4, 1), (7, -3)], [(2, 2, 0), (-4, 1, 0), (7, -3, 0), (0, 0, 1)])
add(W, [(0, 0, 2), (-2, -1, 3), (1, 0, 1), (2, 1, 3)])

D, E = 9 * 10 ** 8, 3 * 10 ** 8
T = [(-D, 0), (D, 0), (0, -E), (0, E)]


def isqrt_up(v):
    s = int(v ** 0.5)
    while s * s < v:
        s += 1
    while s > 0 and (s - 1) * (s - 1) >= v:
        s -= 1
    return s


def mid(a, b):
    (x1, y1), (x2, y2) = T[a], T[b]
    assert (x1 + x2) % 2 == 0 and (y1 + y2) % 2 == 0
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    return (mx, my, isqrt_up((x1 - mx) ** 2 + (y1 - my) ** 2))


def near(a, slack=0):
    x, y = T[a]
    dx, dy = random.randint(-1000, 1000), random.randint(-1000, 1000)
    return (x + dx, y + dy, isqrt_up(dx * dx + dy * dy) + slack)


def nowhere():
    return (random.randint(-MAXC, MAXC), random.choice([-1, 1]) * random.randint(7 * 10 ** 8, MAXC),
            random.randint(0, 10 ** 8))


def filler(n, kinds):
    out = []
    for _ in range(n):
        k = random.choice(kinds)
        if k == "v":
            out.append(mid(2, 3))
        elif k == "o":
            out.append(nowhere())
        else:
            out.append(near(k, random.randint(0, 50)))
    return out


add(T, filler(300, ["v", "o", 0, 2]) + [mid(0, 2)] + filler(200, ["o", 3]) + [mid(1, 3)])
add(T, [mid(2, 3)] + filler(400, ["o", 0, 1]) + [mid(0, 2), mid(1, 3)])


add(T, filler(MAXN - 2, ["v", "o", 0, 1, 2, 3]) + [mid(0, 2), mid(1, 3)])
add(T, [mid(2, 3)] + filler(MAXN - 3, ["o", 0, 2]) + [mid(0, 3), mid(1, 2)])
add(T, [mid(0, 2)] + filler(MAXN - 3, ["v", "o", 1, 3]) + [mid(0, 3), mid(1, 2)])
add(T, [mid(1, 3), mid(2, 3)] + filler(MAXN - 4, ["o", 0, 2, 3]) + [mid(1, 2), mid(0, 3)])
add(T, filler(MAXN, ["v", "o", 0, 1]))
add(T, filler(MAXN - 4, ["o", 0, 1, 2]) + [near(3)] + filler(3, ["o"]))
add(T, filler(MAXN, ["v", "o", 0, 2, 3]))
C = MAXC
Q = [(-C, -C), (C, -C), (-C, C), (C, C)]
k5 = 2 * 10 ** 8
sp = []
for _ in range(MAXN - 2):
    j = random.randint(0, 3)
    sx, sy = (1 if Q[j][0] < 0 else -1), (1 if Q[j][1] < 0 else -1)
    sp.append((Q[j][0] + sx * 3 * k5, Q[j][1] + sy * 4 * k5, 5 * k5 - random.randint(0, 1)))
sp.append((0, 0, 1414213562))
sp.append((C - 3 * k5, -C + 4 * k5, 5 * k5))
add(Q, sp)
add(Q, [(x, y, min(r, 5 * k5 - 1)) for x, y, r in sp])
add(Q, [(x, y, 5 * k5 - 1) for x, y, r in sp[:2000]] + [(0, 0, 1414213563)])
add([(-C, 0), (C, 0), (0, -C), (0, C)],
    [(random.randint(-C, C), random.randint(-C, C), random.randint(10 ** 9, 13 * 10 ** 8)) for _ in range(3000)])
add(T, [nowhere() for _ in range(MAXN - 4)] + [near(0), near(1), near(2), near(3)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
