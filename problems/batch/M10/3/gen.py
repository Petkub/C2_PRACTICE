# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(500003)
MAXN = 200000
MAXV = 10 ** 9
tests = []


def add(v, like):
    n = len(v)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXV for x in v)
    assert len(like) == 3 and all(len(s) == n and set(s) <= {"0", "1"} for s in like)
    tests.append(f"{n}\n{' '.join(map(str, v))}\n" + "".join(s + "\n" for s in like))


def from_codes(v, masks):
    like = ["".join("0" if m >> k & 1 else "1" for m in masks) for k in range(3)]
    add(v, like)


def rv(n, lo=1, hi=MAXV):
    return [random.randint(lo, hi) for _ in range(n)]


add([5, 3, 8, 6, 4, 1], ["111010", "001111", "111001"])
add([10, 1, 9, 7], ["0111", "0100", "0111"])
add([7, 3, 6, 3, 8, 7, 1], ["1011111", "1111100", "1111001"])
add([9, 5, 4, 4, 6, 4], ["111011", "000011", "110001"])
add([5], ["0", "0", "0"])


for n in [1, 2, 5, 9, 14, 18, 20]:
    from_codes(rv(n, 1, 20), [random.randint(0, 7) for _ in range(n)])
from_codes(rv(20, 1, 9), [random.choice([1, 2, 4]) for _ in range(20)])

from_codes(rv(3000), [random.randint(0, 7) for _ in range(3000)])
from_codes(rv(4000, 1, 1000), [random.choice([1, 2, 4, 3, 5, 6]) for _ in range(4000)])


N = MAXN
from_codes(rv(N), [random.randint(0, 7) for _ in range(N)])
from_codes([MAXV] * N, [random.randint(0, 7) for _ in range(N)])
from_codes(rv(N), [random.choice([1, 2, 4]) for _ in range(N)])
from_codes(rv(N), [random.choice([3, 5, 6]) for _ in range(N)])
from_codes(rv(N), [random.choice([1, 2, 4, 3, 5, 6, 7]) for _ in range(N)])
v, m = [], []
while len(v) < N:
    base = random.randint(MAXV // 2, MAXV - 100)
    d = random.choice([1, 2, 4, 3, 5, 6])
    v.append(base)
    m.append(d)
    for _ in range(min(random.randint(1, 4), N - len(v))):
        v.append(base + random.randint(1, 50))
        m.append(d | random.choice([1, 2, 4]))
from_codes(v[:N], m[:N])
from_codes([random.randint(1, 10) if i % 2 else random.randint(MAXV // 2, MAXV) for i in range(N)],
           [0 if i % 2 else random.randint(1, 7) for i in range(N)])
from_codes(rv(N), [7] * N)
from_codes([MAXV - random.randint(0, 5) for _ in range(N)], [0] * N)
v, m = rv(N), []
while len(m) < N:
    d = random.choice([1, 2, 4, 6, 5, 3])
    m += [d] * random.randint(1, 30)
from_codes(v, m[:N])
from_codes(sorted(rv(N)), [[1, 2, 4, 3, 5, 6, 7][i % 7] for i in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
