# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(11014)
MAXN = 1_000_000
tests = []


def add(s):
    n = len(s)
    assert 1 <= n <= MAXN and set(s) <= set("01")
    tests.append(f"{n}\n{s}\n")


def rs(n, p):
    return "".join("1" if random.random() < p else "0" for _ in range(n))


# samples
add("101")
add("00")
add("1")
add("111")
add("0110")
add("1001101")
# hidden: small (the brute tries every split)
add("0")
add("10")
add("1" * 18)
add(rs(17, 0.5))
add(rs(18, 0.2))
add("0" * 9 + "1" + "0" * 8)
# hidden: medium
add(rs(3000, 0.5))
add(rs(5000, 0.05))
# hidden: maximum size
N = MAXN
add("1" * N)
add(rs(N, 0.5))
add(rs(N, 0.01))
add(rs(N, 0.99))
add("0" * (N // 2) + "1" + "0" * (N - N // 2 - 1))   # one captain: N/2 * ... single team only
add("10" * (N // 2))
add("0" + "1" * (N - 2) + "0")
add("0" * N)                                       # no captain at all: 0
add(rs(N - 1, 0.3))
add("".join("1" if i % 997 == 0 else "0" for i in range(N)))

for t in tests:
    assert t.endswith("\n") and " " not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
