# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(320707)
MAXN, MAXK, MAXA = 30_000, 20, 10 ** 9
tests = []


def add(k, a):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= k <= min(n, MAXK)
    assert all(1 <= v <= MAXA for v in a)
    tests.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")


def books(n, kind):
    ri = random.randint
    if kind == "rand":
        return [ri(1, MAXA) for _ in range(n)]
    if kind == "few":
        return [ri(1, 5) for _ in range(n)]
    if kind == "desc":
        return sorted((ri(1, MAXA) for _ in range(n)), reverse=True)
    if kind == "near":
        a = sorted(ri(1, MAXA) for _ in range(n))
        for _ in range(n // 3):
            i = ri(0, n - 1)
            j = min(n - 1, i + ri(0, 49))
            a[i], a[j] = a[j], a[i]
        return a
    if kind == "blocks":
        a, base = [], 1
        while len(a) < n:
            r = ri(0, 999)
            ln = 1 + r * r * n // 8_000_000
            a += [base + ri(0, 999) for _ in range(ln)]
            base += 1000
        return a[:n]
    if kind == "saw":
        a, v, ln = [], 10 ** 6, 1
        while len(a) < n:
            a += [v - t for t in range(ln)]
            v += 2 * ln
            ln += 7
        return a[:n]
    raise ValueError(kind)


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_000_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


add(2, [3, 1, 2, 6, 5, 4])
add(1, [4, 2, 2, 1])
add(3, [5, 5, 5])
add(2, [2, 1, 4, 3, 6, 5, 8, 7])
add(3, [5, 1, 4, 9, 2, 8, 3, 7, 6])

add(1, [7])
add(2, books(10, "few"))
add(3, books(40, "rand"))
add(5, books(200, "near"))
add(8, books(1000, "blocks"))
add(20, books(3000, "saw"))
add(12, books(10_000, "rand"))
add(20, books(20_000, "blocks"))

for k, kind in [(20, "rand"), (20, "desc"), (20, "near"), (20, "blocks"), (20, "saw"), (20, "few"),
                (15, "rand"), (20, "blocks"), (10, "saw"), (20, "near"), (2, "rand")]:
    add(k, books(MAXN, kind))
write_all()
