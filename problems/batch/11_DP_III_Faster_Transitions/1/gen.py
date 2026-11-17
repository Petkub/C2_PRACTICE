# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(60002)
MAXN = 10**6
tests = []


def add(k, s):
    n = len(s)
    assert 1 <= k <= n <= MAXN
    assert set(s) <= set("01?")
    tests.append(f"{n} {k}\n{s}\n")


def rnd(n, p1, p0):
    out = []
    for _ in range(n):
        x = random.random()
        out.append("1" if x < p1 else "0" if x < p1 + p0 else "?")
    return "".join(out)


add(2, "?1??0?")
add(3, "?11?11?")
add(3, "0111?")
add(3, "?????")
add(1, "?")
add(4, "??1?0???1??1")

add(1, "0")
add(1, "1")
add(1, "??????????")
add(20, "?" * 20)
add(2, "?" * 24)
add(5, rnd(25, 0.2, 0.05))
add(3, rnd(25, 0.3, 0.0))
add(7, rnd(25, 0.1, 0.1))
add(4, "1?" * 12)
add(6, "?" * 24 + "1")

N = MAXN
add(N // 2, "?" * N)
add(N, "?" * N)
add(N - 1, "?" * N)
add(300_000, rnd(N, 0.0, 0.00001))
add(123_456, rnd(N, 0.3, 0.0))
add(20, "?" * N)
add(1, "?" * N)
add(N // 3, rnd(N, 0.05, 0.000005))
add(50_000, "?" * (N - 1) + "1")
s = list("?" * N)
for i in range(0, N, 200_000):
    for j in range(i, i + 99_999):
        s[j] = "1"
add(100_000, "".join(s))
add(400_000, "1" * 399_999 + "?" * (N - 399_999))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
