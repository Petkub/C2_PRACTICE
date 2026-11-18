# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(321101)
MAXN, MAXW, MAXC = 200_000, 1000, 10**12
tests = []


def add(c, w):
    n = len(w)
    assert 2 <= n <= MAXN and 0 <= c <= MAXC
    assert all(0 <= v <= MAXW for v in w)
    tests.append(f"{n} {c}\n" + " ".join(map(str, w)) + "\n")


def arr(n, kind):
    rr = random.randrange
    if kind == "rand":
        return [rr(MAXW + 1) for _ in range(n)]
    if kind == "max":
        return [MAXW] * n
    if kind == "zero":
        return [0] * n
    if kind == "zeros":
        return [0 if rr(10) else 1 + rr(MAXW) for _ in range(n)]
    if kind == "small":
        return [rr(4) for _ in range(n)]
    if kind == "spiky":
        return [MAXW - rr(10) if rr(50) == 0 else rr(20) for _ in range(n)]
    if kind == "blocks":
        out = []
        while len(out) < n:
            v = 0 if rr(2) else MAXW - rr(5)
            out += [v] * (1 + rr(60))
        return out[:n]
    raise ValueError(kind)


def write_all():
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


add(20, [1, 2, 5, 5, 2])
add(0, [3, 1, 2, 4])
add(10**12, [0, 5, 0, 7])
add(25, [0, 0, 6, 6, 5, 0])
add(25, [0, 3, 8, 4, 5, 7, 0, 0])

add(7, [4, 9])
add(MAXC, [MAXW, MAXW])
for n, c in ((7, 30), (9, 200), (10, 1)):
    add(c, [rr for rr in arr(n, "small")])
add(300, arr(60, "zeros"))
add(250_000, arr(200, "rand"))
add(40_000_000, arr(300, "blocks"))
add(1_000_000, arr(1000, "spiky"))
add(5_000_000_000, arr(30_000, "rand"))
add(123_456, arr(100_000, "zeros"))

add(10**9, arr(MAXN, "rand"))
add(MAXC, arr(MAXN, "max"))
add(0, arr(MAXN, "rand"))
add(MAXC, arr(MAXN, "zero"))
add(20_000_000, arr(MAXN, "zeros"))
add(3_000_000_000, arr(MAXN, "blocks"))
add(400_000, arr(MAXN, "spiky"))
add(25, arr(MAXN, "small"))
add(10**11, arr(MAXN, "rand"))
add(777_777_777, arr(MAXN, "max"))
add(50_000_000_000, arr(MAXN, "spiky"))
write_all()
