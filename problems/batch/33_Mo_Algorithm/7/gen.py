# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33010)
MAXN, MAXQ = 100_000, 100_000
LET = "abcdefghij"
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(s, qs):
    n, q = len(s), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(c in LET for c in s)
    assert all(1 <= l <= r <= n for l, r in qs)
    tests.append(f"{n} {q}\n{s}\n" + "".join(f"{l} {r}\n" for l, r in qs))


def rand_s(n, k):
    return "".join(random.choice(LET[:k]) for _ in range(n))


def blocks(n, k, run):
    out = []
    while len(out) < n:
        out += random.choice(LET[:k]) * ri(1, run)
    return "".join(out[:n])


def mirror(n, k):
    out = []
    while len(out) < n:
        w = rand_s(ri(1, 30), k)
        out += w + w[::-1]
    return "".join(out[:n])


def any_q(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_q(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def short_q(n, d):
    l = ri(1, n)
    return l, min(n, l + ri(0, d))


def queries(q, *makers):
    return [random.choice(makers)() for _ in range(q)]


add("aabbacd", [(1, 5)])
add("cabbac", [(2, 6)])
add("j", [(1, 1)])
add("abcabcaa", [(4, 5), (3, 6), (1, 8)])
add("ajajjaaabj", [(5, 6), (2, 9), (1, 10)])

add(rand_s(8, 2), [(l, r) for l in range(1, 9) for r in range(l, 9)])
add(rand_s(30, 4), queries(300, lambda: any_q(30)))
add(mirror(120, 3), queries(300, lambda: any_q(120), lambda: short_q(120, 5)))
add(blocks(200, 10, 6), queries(300, lambda: any_q(200)))
add(rand_s(200, 10), queries(300, lambda: any_q(200), lambda: long_q(200, 20)))
add(rand_s(3000, 10), queries(3000, lambda: any_q(3000)))

N, Q = MAXN, MAXQ
add(rand_s(N, 10), queries(Q, lambda: long_q(N, 3000)))
add(rand_s(N, 10), queries(Q, lambda: any_q(N)))
add("a" * N, queries(Q, lambda: long_q(N, 20000), lambda: (1, N)))
add(rand_s(N, 2), queries(Q, lambda: long_q(N, 10000)))
add(blocks(N, 3, 50), queries(Q, lambda: long_q(N, 25000), lambda: short_q(N, 100)))
add(mirror(N, 10), queries(Q, lambda: long_q(N, 5000), lambda: any_q(N)))
add(rand_s(N, 1) [:N // 2] + rand_s(N - N // 2, 10), queries(Q, lambda: long_q(N, 40000)))
add("".join(LET[i % 10] for i in range(N)), queries(Q, lambda: long_q(N, 2000)))
add(rand_s(N, 5), queries(Q, lambda: (ri(1, 3), ri(N - 3, N)), lambda: short_q(N, 3)))
add(blocks(N, 10, 4), queries(Q, lambda: any_q(N), lambda: long_q(N, 1000)))
add(rand_s(N, 3), queries(Q, lambda: long_q(N, 15000)))
add(mirror(N, 2), queries(Q, lambda: long_q(N, 8000), lambda: short_q(N, 0)))
add(blocks(N, 2, 30), queries(Q, lambda: long_q(N, 6000), lambda: any_q(N)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
