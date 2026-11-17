# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(11804)
MAXN = 200_000
V = 10**9
tests = []


def add(k, p):
    n = len(p)
    assert 1 <= n <= MAXN
    assert -V <= k <= V
    assert all(-V <= x <= V for x in p)
    tests.append(f"{n} {k}\n" + " ".join(map(str, p)) + "\n")


def from_b(k, b):
    """profits p_i = K + b_i"""
    add(k, [k + x for x in b])


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


# samples
add(5, [3, 8, 4, 6, 1, 7])
add(10, [4, 9, -2, 7])
add(0, [-1, 2, -1, 2, -1, 2])
add(3, [3, 3, 3])
add(-2, [-5, -1, -6, 0, -4])
add(4, [1, 9, 1, 1, 9, 1])
# hidden (small)
add(V, [V])
add(V, [V - 1])
add(-V, [-V, -V])
add(1, [0, 2, 0, 2, 0])
from_b(7, rnd(10, -3, 2))
from_b(0, rnd(50, -2, 2))
from_b(-1000, rnd(300, -10, 9))
from_b(123456, rnd(2000, -5, 3))
from_b(-7, rnd(3000, -3, 3))
from_b(500_000_000, rnd(3000, -500_000_000, 500_000_000))
b = [0] * 3000                                   # equal-length zero runs: the first one wins
for x in range(400, 3000, 401):
    b[x] = -1
add(0, b)
# large
n = MAXN
add(V, [V] * n)                                  # every day exactly on target
add(-V, [V] * n)                                 # huge totals
add(V, [-V] * n)                                 # nothing reaches the target
from_b(-3, rnd(n, -V + 3, -1))                   # nothing, random
add(1, [V if i % 2 == 0 else -V for i in range(n)])
from_b(0, rnd(n, -5, 3))                         # drifting down: short answer
from_b(-1, rnd(n, -3, 3))                        # no drift: long answer
from_b(400_000_000, rnd(n, -V + 400_000_000, 590_000_000))
b = [-1] * n
b[n // 2] = 30_000                               # one spike in a falling year
from_b(5, b)
b = rnd(n, -1000, 1000)
b[-1] -= sum(b)                                  # whole period exactly on average
assert -V <= b[-1] <= V
from_b(-12345, b)
b = [-V] * n                                     # zero runs: 999, then 1000, 1000, 1000 ...
pos = 0
lens = [999] + [1000] * 150
for L in lens:
    pos += 1
    for x in range(pos, pos + L):
        b[x] = 0
    pos += L
from_b(0, b)
b = []
while len(b) < n:                                # many equal prefix-sum minima
    b += [-1, 1] * random.randint(1, 50) + [-random.randint(1, 3)]
from_b(-V // 2, b[:n])
b = rnd(n, -2, 1)
b[:5000] = [1] * 5000
b[-5000:] = [1] * 5000
from_b(V // 3, b)
add(0, [V] * 40_000 + [-V] * (n - 40_000))       # big totals, answer 80000
from_b(-V // 3, rnd(n, -4, 3))                   # drifting down: short answer
b = [-1] * n                                     # three equal zero blocks: the first one wins
for start in (40_000, 90_000, 150_000):
    b[start:start + 3000] = [0] * 3000
from_b(-V + 5, b)
b = [-V] * n                                     # isolated good days: answer 1
for x in random.sample(range(0, n, 2), 50):
    b[x] = random.randint(0, 5)
from_b(0, b)
from_b(0, rnd(n, -V, V - 30_000_000))            # large values, downward drift

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
