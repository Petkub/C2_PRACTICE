# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(10111)
MAXN = 500_000
tests = []


def add(s):
    n = len(s)
    assert 1 <= n <= MAXN
    assert set(s) <= set("ABC")
    tests.append(f"{n}\n{s}\n")


def rnd(n, w=(1, 1, 1)):
    return "".join(random.choices("ABC", weights=w, k=n))


def perm_blocks(m):
    """m blocks of 3 letters, each block a permutation of ABC"""
    out = []
    for _ in range(m):
        b = list("ABC")
        random.shuffle(b)
        out.extend(b)
    return "".join(out)


# samples
add("ABCCAB")
add("AABBAB")
add("A")
add("ABCABC")
add("CBAACB")
add("AAABBBCCC")
# hidden (small)
add("C")
add("BCA")
add("ABABCCBACC")
add(perm_blocks(10))
add(rnd(50))
add(rnd(300))
add(rnd(2000, (5, 4, 4)))
add(perm_blocks(1000) + rnd(1000))
add("A" * 1000 + "B" * 1000 + "C" * 1000)
add(rnd(3000, (1, 1, 0)))                              # no C at all
# large
N = MAXN
add(("ABC" * N)[:N])                                    # the largest answer
add(perm_blocks(N // 3) + "AB")
add(rnd(N))
add(rnd(N, (10, 9, 9)))
add("A" * N)
add(("AB" * N)[:N])
add("A" * (N // 3) + "B" * (N // 3) + "C" * (N // 3))
add(rnd(N - 1))
add("".join(random.choice(["ABC", "ACB", "BAC", "AABBCC", "CCBBAA", "A", "B", "C"]) for _ in range(N // 3))[:N])
add(("CBA" * N)[:N - 2])
add(rnd(N, (1, 1, 2)))
add(("ABC" * N)[:N // 2] + ("BAC" * N)[:N // 2])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
