# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1101)
MAXN, MAXQ, MAXA = 100_000, 100_000, 10**9
tests = []

def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(-MAXA <= x <= MAXA for x in a)
    assert all(1 <= l <= n and 1 <= r <= n for l, r in qs)
    lines = [f"{n} {q}", " ".join(map(str, a))] + [f"{l} {r}" for l, r in qs]
    tests.append("\n".join(lines) + "\n")

def rand_q(n, q, mode):
    qs = []
    for _ in range(q):
        if mode == "wrap_long":            # length close to n, always wrapping
            r = random.randint(1, n - 1) if n > 1 else 1
            l = r + 1 if random.random() < 0.7 else min(n, r + random.randint(1, 5))
            if l <= r:
                l = r + 1 if r < n else 1
        elif mode == "full":               # l <= r long ranges
            l = random.randint(1, max(1, n // 50))
            r = random.randint(n - n // 50, n)
            l = min(l, r)
        else:
            l, r = random.randint(1, n), random.randint(1, n)
        qs.append((l, r))
    return qs

# samples
add([3, -1, 4, 1, 5], [(2, 4), (4, 2), (3, 3)])
add([10, -20, 30, -40], [(4, 1), (3, 1), (1, 4)])
add([-10**9], [(1, 1)])
add([10**9, 10**9], [(2, 1), (1, 1), (1, 2)])
add([5, -7, 2, 0, 9, -3], [(6, 1), (2, 5), (5, 4)])
# hidden: small
add([7], [(1, 1)] * 3)
add([1, 2], [(1, 1), (1, 2), (2, 1), (2, 2)])
for n, q in [(10, 30), (50, 100), (300, 500), (1000, 1000)]:
    a = [random.randint(-100, 100) for _ in range(n)]
    add(a, rand_q(n, q, "any"))
a = [random.randint(-MAXA, MAXA) for _ in range(2000)]
add(a, rand_q(2000, 2000, "wrap_long"))
add([MAXA] * 3000, rand_q(3000, 3000, "wrap_long"))          # 32-bit overflow
add([-MAXA] * 3000, rand_q(3000, 3000, "full"))
# hidden: maximum size
add([random.randint(-MAXA, MAXA) for _ in range(MAXN)], rand_q(MAXN, MAXQ, "wrap_long"))
add([random.randint(-MAXA, MAXA) for _ in range(MAXN)], rand_q(MAXN, MAXQ, "any"))
add([MAXA] * MAXN, rand_q(MAXN, MAXQ, "wrap_long"))
add([-MAXA] * MAXN, rand_q(MAXN, MAXQ, "full"))
add([random.choice([-MAXA, MAXA]) for _ in range(MAXN)], rand_q(MAXN, MAXQ, "wrap_long"))
add([random.randint(0, MAXA) for _ in range(MAXN)], [(n, n - 1) for n in [MAXN]] * MAXQ)
add([random.randint(-1000, 1000) for _ in range(MAXN)],
    [(random.randint(1, MAXN), random.randint(1, MAXN)) if i % 2 else (MAXN, MAXN - 1) for i in range(MAXQ)])
add([random.randint(-MAXA, MAXA) for _ in range(MAXN)], rand_q(MAXN, MAXQ, "full"))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
