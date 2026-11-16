# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(11703)
MAXN = 200_000
MAXQ = 100_000
tests = []


def add(s, qs):
    n, q = len(s), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(ch in "<>." for ch in s)
    assert all(1 <= l <= r <= n for l, r in qs)
    tests.append(f"{n} {q}\n{s}\n" + "".join(f"{l} {r}\n" for l, r in qs))


def rnd_str(n, w=(1, 1, 1)):
    return "".join(random.choices("><.", weights=w, k=n))


def rnd_q(n, q):
    out = []
    for _ in range(q):
        l = random.randint(1, n)
        r = random.randint(1, n)
        out.append((min(l, r), max(l, r)))
    return out


def wide_q(n, q):
    """long ranges: l near the start, r near the end"""
    out = []
    for _ in range(q):
        l = random.randint(1, max(1, n // 20))
        r = random.randint(min(n, n - n // 20), n)
        out.append((l, r))
    return out


def all_q(n):
    return [(l, r) for l in range(1, n + 1) for r in range(l, n + 1)]


# samples
add(">.<><<", [(1, 6), (2, 5), (4, 6), (3, 3), (1, 3)])
add("<<>>", [(1, 4), (2, 3)])
add(">>><<<", [(1, 6), (2, 5), (3, 4), (4, 6)])
add(".>.<.", [(1, 5), (2, 4), (1, 1)])
add("><><><", [(1, 6), (2, 6), (2, 5), (3, 6)])
# hidden (small)
add(">", [(1, 1)])
add("<", [(1, 1)])
s = rnd_str(10)
add(s, all_q(10))
s = rnd_str(30, (3, 3, 1))
add(s, all_q(30))
s = ">" * 20 + "<" * 20
add(s, all_q(40))
s = rnd_str(1000)
add(s, rnd_q(1000, 1000))
s = rnd_str(3000, (5, 5, 1))
add(s, wide_q(3000, 3000))
# large
n = MAXN
s = ">" * (n // 2) + "<" * (n // 2)
add(s, [(1, n)] * MAXQ)                                  # answer 10^10 every time
qs = [(random.randint(2, n // 2), random.randint(n // 2 + 1, n)) for _ in range(MAXQ)]
add(s, qs)                                               # many '>' before l
add("><" * (n // 2), wide_q(n, MAXQ))
add(rnd_str(n), rnd_q(n, MAXQ))
add(rnd_str(n, (10, 10, 1)), wide_q(n, MAXQ))
add(rnd_str(n, (1, 1, 20)), rnd_q(n, MAXQ))
add("." * n, wide_q(n, MAXQ))
add("<" * (n // 2) + ">" * (n // 2), wide_q(n, MAXQ))   # nobody faces anybody in the full range
s = "".join(random.choice("><") * random.randint(1, 3000) for _ in range(400))[:n]
s += ">" * (n - len(s))
qs = rnd_q(n, MAXQ // 2) + [(l, l) for l in random.sample(range(1, n + 1), MAXQ // 2)]
random.shuffle(qs)
add(s, qs)
s = rnd_str(n, (2, 1, 0))
qs = []
for _ in range(MAXQ):                                    # l right after a '>' and r on a '<'
    l = random.randint(2, n // 3)
    r = random.randint(2 * n // 3, n)
    qs.append((l, r))
add(s, qs)
s = rnd_str(n, (1, 2, 0))
add(s, [(1, r) for r in random.sample(range(1, n + 1), MAXQ)])
add(rnd_str(n), [(l, n) for l in random.sample(range(1, n + 1), MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
