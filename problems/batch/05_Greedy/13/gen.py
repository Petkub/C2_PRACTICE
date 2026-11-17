# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(30112)
MAXN = 100_000
MAXL = 1_000_000
tests = []


def add(strs):
    n = len(strs)
    assert 1 <= n <= MAXN
    assert all(len(t) >= 1 and set(t) <= {"s", "h"} for t in strs)
    assert sum(len(t) for t in strs) <= MAXL
    tests.append(f"{n}\n" + "".join(t + "\n" for t in strs))


def word(length, ps):
    return "".join("s" if random.random() < ps else "h" for _ in range(length))


def rnd(n, lmax, total=None):
    lens = [random.randint(1, lmax) for _ in range(n)]
    if total is not None and sum(lens) > total:
        f = total / sum(lens)
        lens = [max(1, int(x * f)) for x in lens]
    return [word(L, random.random()) for L in lens]


add(["h", "ssh", "hhs"])
add(["hhh", "s"])
add(["shh", "h", "ss"])
add(["hs", "hs", "sh", "s"])
add(["hhss"])
add(["shs", "hhh", "sssh", "hsh", "s", "hhsh"])

add(["s"])
add(["h", "s"])
for n in (5, 8, 10, 12, 14, 16, 16):
    add(rnd(n, 8))
add(["s" * 3 + "h", "s" * 6 + "h" * 2, "sh", "ssh", "hs", "h" * 3, "s" * 9 + "h" * 3, "hhhs"])
add(rnd(16, 2000))
add(rnd(2000, 10))

add(rnd(MAXN, 19, MAXL))
add(rnd(MAXN, 10, MAXL))
add([word(10, 0.5) for _ in range(MAXN)])
add([word(MAXL // 20, random.random()) for _ in range(20)])
add([word(MAXL // 4, p) for p in (0.3, 0.7, 0.45, 0.55)])
strs = []
for _ in range(MAXN // 2):
    strs.append("s" * random.randint(5, 10) + "h" * random.randint(5, 10))
    strs.append("s" * random.randint(1, 2) + "h" * random.randint(0, 1))
add(strs)
add(["h" * 5 + "s" * 5] * MAXN)
add(["s"] * (MAXN // 2) + ["h"] * (MAXN // 2))
add(["h"] * (MAXN // 2) + ["s" * 18] * (MAXN // 2))
strs = [word(random.randint(1, 3), random.random()) for _ in range(MAXN - 8)]
strs += [word(90000, random.random()) for _ in range(8)]
random.shuffle(strs)
add(strs)
add(rnd(MAXN, 19, MAXL))
strs = []
for _ in range(MAXN):
    k = random.randint(4, 5)
    strs.append(word(2 * k + random.randint(-1, 1), 0.5))
add(strs)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
