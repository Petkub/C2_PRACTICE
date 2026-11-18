# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(320404)
MAXN, MAXK, MAXX = 50_000, 100, 10 ** 9
tests = []


def add(k, x):
    n = len(x)
    assert 1 <= n <= MAXN and 1 <= k <= min(n, MAXK)
    assert all(1 <= v <= MAXX for v in x)
    tests.append(f"{n} {k}\n" + " ".join(map(str, x)) + "\n")


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]
    return a


def houses(n, kind):
    rnd = random.random
    if kind == "rand":
        x = [1 + int(rnd() * MAXX) for _ in range(n)]
    elif kind == "clusters":
        x = []
        while len(x) < n:
            c = 1 + int(rnd() * (MAXX - 10 ** 7))
            spread = 10 ** int(1 + rnd() * 7)
            cnt = 1 + int(rnd() ** 3 * n / 20)
            x += [c + int(rnd() * spread) for _ in range(cnt)]
        x = x[:n]
    elif kind == "expo":
        v, x = 1, []
        for i in range(n):
            x.append(v)
            v = min(MAXX, v + 1 + int(rnd() * (i + 1) * (MAXX // n // n + 1)))
    elif kind == "repeat":
        spots = [1 + int(rnd() * MAXX) for _ in range(150)]
        x = [spots[int(rnd() ** 2 * len(spots))] for _ in range(n)]
    elif kind == "same":
        x = [MAXX] * n
    elif kind == "ends":
        x = [MAXX // 2 + int(rnd() * 10 ** 6) for _ in range(n - 20)]
        x += [1 + int(rnd() * 1000) for _ in range(10)] + [MAXX - int(rnd() * 1000) for _ in range(10)]
    else:
        raise ValueError(kind)
    return shuffle(x)


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_000_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


add(2, [1, 2, 3, 10, 11, 30])
add(1, [5, 9, 2, 7])
add(3, [4, 4, 4, 4])
add(2, [5, 100, 6, 101, 5, 100, 7])
add(3, [100, 1, 50, 3, 102, 49, 2, 200])

add(1, [7])
add(2, houses(9, "clusters"))
add(4, houses(30, "rand"))
add(7, houses(120, "expo"))
add(10, houses(300, "clusters"))
add(25, houses(2000, "ends"))
add(60, houses(8000, "repeat"))
add(100, houses(20_000, "clusters"))

for k, kind in [(100, "rand"), (100, "clusters"), (99, "expo"), (100, "repeat"), (100, "same"), (100, "ends"),
                (50, "clusters"), (80, "rand"), (100, "clusters"), (2, "rand")]:
    add(k, houses(MAXN, kind))
write_all()
