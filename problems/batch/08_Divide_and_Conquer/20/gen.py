# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(131905)
MAXN = 300_000
tests = []


def add(p):
    n = len(p)
    assert 1 <= n <= MAXN and sorted(p) == list(range(1, n + 1))
    tests.append(f"{n}\n{' '.join(map(str, p))}\n")


def shuffled(n):
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


def local(n, w):
    """sorted, then every window of w consecutive positions shuffled (values stay close to their place)"""
    p = list(range(1, n + 1))
    for s in range(0, n, w):
        part = p[s:s + w]
        random.shuffle(part)
        p[s:s + w] = part
    return p


def jitter(n, d, times):
    """sorted, then many swaps of positions at distance <= d"""
    p = list(range(1, n + 1))
    for _ in range(times):
        i = random.randrange(n)
        j = min(n - 1, i + random.randint(1, d))
        p[i], p[j] = p[j], p[i]
    return p


def blocks(n, lo, hi, rev_prob, shuffle_blocks):
    """runs of consecutive values (each run ascending or descending), runs in random or sorted order"""
    runs, s = [], 1
    while s <= n:
        L = min(n - s + 1, random.randint(lo, hi))
        run = list(range(s, s + L))
        if random.random() < rev_prob:
            run.reverse()
        runs.append(run)
        s += L
    if shuffle_blocks:
        random.shuffle(runs)
    return [x for r in runs for x in r]


def fractal(vals, depth):
    """split the values into 2..4 consecutive groups, arrange them in a random order, recurse"""
    if len(vals) <= 2 or depth == 0:
        v = vals[:]
        if random.random() < 0.5:
            v.reverse()
        return v
    k = min(len(vals), random.randint(2, 4))
    cuts = sorted(random.sample(range(1, len(vals)), k - 1))
    parts = [vals[a:b] for a, b in zip([0] + cuts, cuts + [len(vals)])]
    random.shuffle(parts)
    out = []
    for part in parts:
        out += fractal(part, depth - 1)
    return out


# samples
add([3, 1, 2, 5, 4])
add([2, 4, 1, 3])
add([1])
add([1, 2, 3, 4, 5, 6])
add([4, 7, 5, 6, 1, 3, 2, 8])
# hidden: small (the brute force tries every segment)
add([1, 2])
add([2, 1])
add(shuffled(10))
add(local(50, 5))
add(fractal(list(range(1, 101)), 10))
add(shuffled(1000))
add(blocks(2000, 1, 20, 0.5, True))
add(fractal(list(range(1, 5001)), 30))
add(jitter(20000, 3, 5000))
add(list(range(30000, 0, -1)))
# hidden: large
N = MAXN
add(list(range(1, N + 1)))                     # every segment counts
add(list(range(N, 0, -1)))
add([i + 1 if i % 2 == 1 else i - 1 for i in range(1, N + 1)])     # 2 1 4 3 6 5 ...
add(local(N, 3))
add(local(N, 50))
add(jitter(N, 2, N // 3))
add(jitter(N, 10, N // 10))
add(blocks(N, 1, 8, 0.5, False))
add(blocks(N, 50, 500, 0.5, True))
add(fractal(list(range(1, N + 1)), 40))
add(fractal(list(range(1, N + 1)), 6))
add(shuffled(N))
add([x for i in range(N // 2) for x in (i + 1, N - i)])             # 1 N 2 N-1 ...

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
