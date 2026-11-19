# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4203)
MAXN = 10**6
tests = []


def add(s):
    n = len(s)
    assert 1 <= n <= MAXN and all("0" <= c <= "9" for c in s)
    tests.append(f"{n}\n{s}\n")


def chain(k):
    return "72" * k + "7"


def filler(n, digits="0123456789"):
    return "".join(random.choice(digits) for _ in range(n))


def blocks(n, ks, glue, stick=0.0):
    parts, size = [], 0
    while size < n:
        c = chain(random.choice(ks))
        if parts and random.random() >= stick:
            g = glue()
            parts.append(g)
            size += len(g)
        parts.append(c)
        size += len(c)
    s = "".join(parts)[:n]
    return s


def safe_glue(lo, hi):
    return lambda: "".join(random.choice("01345689") for _ in range(random.randint(lo, hi)))


add("1727277270")
add("12345")
add("727")
add("7272")
add("72727072727")

add("7")
add("727727")
add("72727727277272")
add("7277272727727")
add("27" * 10)
for n in (30, 60, 120, 300):
    add(filler(n, "27"))
add(filler(400, "2770"))
add(blocks(500, [1, 2, 3], safe_glue(0, 2), 0.5))
add(blocks(2000, [1, 2], safe_glue(1, 3), 0.6))

N = MAXN
add("7" * N)
add(filler(N, "0123456789"))
add(("727" * N)[:N])
add(("72727" * N)[:N])
add(chain((N - 1) // 2))
add(filler(N, "27"))
add(blocks(N, [3], safe_glue(0, 1), 0.7))
add(blocks(N, [1, 2, 3, 4], safe_glue(1, 2), 0.5))
s = blocks(N - 42, [5], safe_glue(0, 1), 0.9)
add(s + "0" + chain(20))
s = ("727" * N)[:N]
add("".join("0" if i % 99991 == 50 else c for i, c in enumerate(s)))
add(("7272727" * N)[:N])
add(filler(N, "013456789"))
add(filler(N, "012345689"))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
