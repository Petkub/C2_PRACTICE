# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1106)
MAXN, MAXA = 200_000, 10**9
tests = []

def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(1 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

def runs(n, runlen, kind):
    """increasing runs of about runlen days; between runs one 'bad' day.
    kind 'high': the bad day is too high (delete it to join), 'low': too low,
    'nojoin': the next run starts below the end of the previous one, 'mix': any."""
    a = []
    base = random.randint(1, 1000)
    while len(a) < n:
        ln = random.randint(max(1, runlen // 2), runlen)
        for _ in range(ln):
            base += random.randint(1, 3)
            a.append(base)
        k = kind if kind != "mix" else random.choice(["high", "low", "nojoin", "eq"])
        if k == "high":
            a.append(base + random.randint(10**6, 2 * 10**6))
        elif k == "low":
            a.append(max(1, base - random.randint(10**5, 2 * 10**5)))
        elif k == "eq":
            a.append(base)
        else:
            base -= random.randint(10**5, 2 * 10**5)
            a.append(base + random.randint(10**6, 2 * 10**6))
        if base < 10**6:
            base += 3 * 10**6
    a = a[:n]
    assert all(x <= MAXA for x in a)
    return a

# samples
add([1, 2, 5, 3, 4, 6, 2])
add([5, 4, 3, 2, 1])
add([7])
add([1, 2, 3, 3, 4, 5])
add([4, 4, 4, 4])
add([3, 8, 4, 5, 1, 6, 7, 9])
# hidden: small
add([2, 1])
add([1, 2])
add([5, 1, 2, 3])                       # deleting the first day does not help
add([1, 2, 3, 5, 2, 3, 4])              # cannot join
add([1, 2, 3, 4, 1, 5, 6])              # delete the low day
add(rnd(10, 1, 5))
add(rnd(200, 1, 30))
add(runs(1000, 15, "mix"))
add(runs(5000, 40, "high"))
add(runs(5000, 40, "low"))
add(runs(15000, 100, "mix"))
# hidden: maximum size
add(list(range(1, MAXN + 1)))                                   # already increasing
a = list(range(1, MAXN + 1)); a[MAXN // 2] = MAXA; add(a)       # one spike in the middle
a = list(range(10, MAXN + 10)); a[MAXN // 3] = 1; add(a)        # one dip
add(runs(MAXN, 2000, "mix"))
add(runs(MAXN, 30000, "nojoin"))
add(runs(MAXN, 50000, "high"))
add([MAXA - (i % 2) for i in range(MAXN)])                       # zigzag, answer 2
add(rnd(MAXN, 1, MAXA))
add(list(range(MAXN, 0, -1)))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
