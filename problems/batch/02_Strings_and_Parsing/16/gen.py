# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(151601)
MAXN = 5000
MAXQ = 300_000
tests = []


def add(s, qs):
    n = len(s)
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    assert all("a" <= c <= "z" for c in s)
    for l, r in qs:
        assert 1 <= l <= r <= n
    t = f"{n} {len(qs)}\n{s}\n" + "".join(f"{l} {r}\n" for l, r in qs)
    assert all(32 <= ord(c) <= 126 or c == "\n" for c in t)
    tests.append(t)


def rand_str(n, alpha):
    return "".join(random.choice(alpha) for _ in range(n))


def rand_q(n, q, long_ranges=False):
    rnd = random.random
    qs = []
    for _ in range(q):
        if long_ranges:
            w = n // 20
            l = 1 + int(rnd() * min(n, w + 1))
            lo = max(l, n - w)
            r = lo + int(rnd() * (n - lo + 1))
        else:
            l = 1 + int(rnd() * n)
            r = l + int(rnd() * (n - l + 1))
        qs.append((l, r))
    return qs


def pal_noise(n, alpha, core):
    # a palindrome of length core somewhere inside random text
    half = rand_str(core // 2, alpha)
    p = half + (random.choice(alpha) if core % 2 else "") + half[::-1]
    pos = random.randint(0, n - core)
    return rand_str(pos, alpha) + p + rand_str(n - core - pos, alpha)


def fib(n):
    a, b = "a", "ab"
    while len(b) < n:
        a, b = b, b + a
    return b[:n]


# samples
add("abacabad", [(1, 8), (2, 4), (4, 8), (8, 8)])
add("aabbcc", [(1, 6), (2, 5), (4, 6)])
add("z", [(1, 1)])
add("abcde", [(1, 5), (2, 4), (3, 5)])
add("racecarxabba", [(1, 12), (2, 12), (6, 12), (2, 6), (8, 11)])
# hidden: small (brute checks these)
add("aaaa", [(l, r) for l in range(1, 5) for r in range(l, 5)])
add("abab", [(l, r) for l in range(1, 5) for r in range(l, 5)])
for n, alpha in [(12, "ab"), (25, "abc"), (40, "ab"), (60, "aab")]:
    s = rand_str(n, alpha)
    add(s, [(l, r) for l in range(1, n + 1) for r in range(l, n + 1)])
add(pal_noise(200, "ab", 61), rand_q(200, 3000))
add(fib(300), rand_q(300, 2000))
add(rand_str(400, "abc"), rand_q(400, 1500))
# hidden: large (n = 5000, mostly long ranges)
big = [
    ("a" * MAXN, MAXQ, True),
    (rand_str(MAXN, "ab"), MAXQ, True),
    (rand_str(MAXN, "abcdefghijklmnopqrstuvwxyz"), MAXQ, True),
    (pal_noise(MAXN, "ab", 1999), MAXQ, True),
    (pal_noise(MAXN, "abc", 4001), 250_000, True),
    (fib(MAXN), MAXQ, True),
    (("ab" * MAXN)[:MAXN - 1] + "c", 250_000, True),
    ("".join(random.choice("ab") * random.randint(1, 30) for _ in range(MAXN))[:MAXN], 250_000, False),
    (rand_str(MAXN, "ab"), 250_000, False),
    (pal_noise(MAXN, "abcdefghij", 2500), 250_000, True),
    (("abcba" * MAXN)[:MAXN], 250_000, True),
]
for s, q, lr in big:
    add(s, rand_q(len(s), q, lr))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
