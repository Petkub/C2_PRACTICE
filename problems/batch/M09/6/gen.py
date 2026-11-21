# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(490006)
MAXN = 100000
MAXM = 150000
MAXV = 10 ** 9
tests = []


def add(n, ev):
    m = len(ev)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM
    assert any(e[0] == 4 for e in ev)
    for e in ev:
        assert e[0] in (1, 2, 3, 4)
        assert 1 <= e[1] <= n
        if e[0] in (1, 2):
            assert len(e) == 3 and 1 <= e[2] <= n
        elif e[0] == 3:
            assert len(e) == 3 and -MAXV <= e[2] <= MAXV
        else:
            assert len(e) == 2
    tests.append(f"{n} {m}\n" + "".join(" ".join(map(str, e)) + "\n" for e in ev))


def rv(lo=-MAXV, hi=MAXV):
    return random.randint(lo, hi)


def rand_events(n, m, w=(2, 2, 3, 3), pick=None, vr=(-MAXV, MAXV)):
    pick = pick or (lambda: random.randint(1, n))
    ev = []
    for t in random.choices((1, 2, 3, 4), weights=w, k=m - 1):
        if t == 4:
            ev.append((4, pick()))
        elif t == 3:
            ev.append((3, pick(), rv(*vr)))
        else:
            ev.append((t, pick(), pick()))
    ev.append((4, pick()))
    return ev


def sample(text):
    lines = text.strip().split("\n")
    n, m = map(int, lines[0].split())
    ev = [tuple(map(int, l.split())) for l in lines[1:]]
    assert len(ev) == m
    add(n, ev)


sample("4 7\n3 1 5\n1 1 2\n3 2 3\n2 1 3\n3 3 10\n4 1\n4 3")
sample("3 7\n3 1 7\n1 1 2\n3 2 1\n2 3 1\n3 3 4\n4 1\n4 3")
sample("1 3\n3 1 -1000000000\n3 1 -999999999\n4 1")
sample("5 6\n1 1 2\n2 3 3\n3 1 6\n1 4 1\n3 4 -2\n4 2")
sample("3 5\n1 1 2\n3 2 1000000000\n2 1 3\n3 3 999999999\n4 1")

add(2, rand_events(2, 30, vr=(-9, 9)))
add(5, rand_events(5, 60, vr=(-20, 20)))
add(8, rand_events(8, 100, w=(1, 4, 3, 3)))
add(8, rand_events(8, 120, w=(4, 1, 3, 3)))
add(30, rand_events(30, 300, w=(3, 3, 2, 3)))
add(50, rand_events(50, 400, w=(2, 5, 2, 3), vr=(MAXV - 10, MAXV)))

add(2000, rand_events(2000, 10000))
add(1000, rand_events(1000, 10000, w=(1, 3, 3, 3), pick=lambda: random.randint(1, 20) if random.random() < 0.5 else random.randint(1, 1000)))
add(3000, rand_events(3000, 12000, w=(5, 2, 2, 2)))


def chains(n, m, s, k, w, vr=(-MAXV, MAXV), hot=0.3):
    ev = [(1, i, i + k) for i in range(1, s - k + 1)]
    h = 2 * k + 10
    pick = lambda: random.randint(1, h) if random.random() < hot else random.randint(1, n)
    ev += rand_events(n, m - len(ev), w=w, pick=pick, vr=vr)
    return ev


def grow_into_singletons(n, m, w):
    ev = []
    for i in range(2, n + 1):
        ev.append((1, 1, i))
        if i % 3 == 0:
            ev.append((3, i, rv()))
        if len(ev) >= m // 2:
            break
    ev += rand_events(n, m - len(ev), w=w)
    return ev


add(MAXN, chains(MAXN, MAXM, 50000, 1, (0, 2, 5, 3)))
add(MAXN, chains(MAXN, MAXM, 50000, 1, (1, 3, 4, 3), vr=(MAXV - 1000, MAXV)))
add(MAXN, chains(MAXN, MAXM, 60000, 1, (0, 3, 5, 2), vr=(-MAXV, -MAXV + 1000), hot=0.5))
add(MAXN, grow_into_singletons(MAXN, MAXM, (1, 2, 3, 4)))
add(MAXN, grow_into_singletons(MAXN, MAXM, (0, 3, 3, 3)))
add(MAXN, chains(MAXN, MAXM, 60000, 3, (1, 2, 5, 3)))
add(MAXN, chains(MAXN, MAXM, 30000, 1, (2, 2, 4, 3), hot=0.1))
add(MAXN, chains(MAXN, MAXM, 50000, 1, (0, 6, 3, 3)))
add(MAXN, chains(MAXN, MAXM, 50000, 1, (0, 0, 5, 3)))
add(MAXN, grow_into_singletons(MAXN, MAXM - 7, (0, 1, 4, 3)))
add(MAXN, chains(MAXN, MAXM, 50000, 2, (1, 6, 3, 3), vr=(MAXV - 5, MAXV)))
add(MAXN, chains(MAXN, MAXM, 45000, 1, (0, 4, 4, 3), hot=0.6))
add(MAXN, chains(MAXN, MAXM, 50000, 1, (3, 3, 3, 3)))
add(MAXN, chains(MAXN, MAXM, 55000, 4, (1, 3, 5, 3), vr=(0, MAXV)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
