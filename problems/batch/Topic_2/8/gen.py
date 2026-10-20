# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(10108)
MAXN = 1_000_000
tests = []


def add(s):
    n = len(s)
    assert 1 <= n <= MAXN
    assert set(s) <= {"0", "1"}
    tests.append(f"{n}\n{s}\n")


def rnd(n, p):
    return "".join("1" if random.random() < p else "0" for _ in range(n))


def rotate(s, k):
    return s[k:] + s[:k]


# samples
add("1001010")
add("10101010")
add("00000")
add("110011")
add("1")
add("0110100110")
# hidden (small)
add("0")
add("1111111")
add("1000000001")
add("0110110110110")
for n in (8, 11, 13, 14):
    add(rnd(n, 0.5))
add(rnd(200, 0.4))
add(rnd(3000, 0.6))
add(rotate("1" * 6000 + "0" * 4000 + rnd(8000, 0.5), 9000))
# large
add(rnd(MAXN, 0.5))
add(rnd(MAXN, 0.3))
add(rnd(MAXN, 0.8))
add("10" * (MAXN // 2))
add("1" * MAXN)
add("0" * MAXN)
add(rotate("1" * 400_000 + "0" * 600_000, 750_000))           # already together across the end
add(rotate("1" * 500_000 + "0" * 499_999 + "1", 123_456))       # one friend far away
add("0" * (MAXN - 1) + "1")
add("1" * (MAXN - 1) + "0")
s = list("1" * 300_000 + "0" * 700_000)
for i in random.sample(range(MAXN), 2000):
    s[i] = "0" if s[i] == "1" else "1"
add(rotate("".join(s), 654_321))
add("100" * (MAXN // 3) + "1")
add(rnd(MAXN - 7, 0.5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
