# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(13006)
MAXN = 200_000
MAXK = 10 ** 18
tests = []


def add(k, p):
    n = len(p)
    assert 1 <= n <= MAXN and 0 <= k <= MAXK
    assert sorted(p) == list(range(1, n + 1))
    tests.append(f"{n} {k}\n" + " ".join(map(str, p)) + "\n")


def from_cycles(n, lengths):
    """a permutation of 1..n whose cycles have the given lengths (the rest fixed points), placed at random"""
    pos = list(range(1, n + 1))
    random.shuffle(pos)
    p = list(range(n + 1))
    i = 0
    for ln in lengths:
        cyc = pos[i:i + ln]
        i += ln
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            p[a] = b
    assert i <= n
    return p[1:]


def perm(n):
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


def primes_upto(m):
    s = [True] * (m + 1)
    out = []
    for i in range(2, m + 1):
        if s[i]:
            out.append(i)
            for j in range(i * i, m + 1, i):
                s[j] = False
    return out


PR = primes_upto(5000)


def prime_cycles(n):
    """cycles of distinct prime lengths, largest first, filling n as far as possible"""
    lengths, total = [], 0
    for q in PR:
        if total + q > n:
            break
        lengths.append(q)
        total += q
    return from_cycles(n, lengths)


# samples
add(2, [2, 3, 1, 5, 4])
add(1, [2, 4, 1, 3])
add(0, [3, 1, 2])
add(10 ** 18, [4, 1, 2, 3, 6, 7, 5])
add(7, [1])
# hidden: small (the brute force shuffles k times)
add(1, [1, 2])
add(3, [2, 1])
add(5, perm(8))
add(100, perm(50))
add(999, from_cycles(30, [7, 11, 12]))
add(1000, perm(1000))
add(150, perm(20000))
add(MAXK, perm(1000))
add(MAXK - 1, prime_cycles(5000))
# hidden: large
N = MAXN
add(MAXK, perm(N))
add(random.randint(MAXK // 2, MAXK), perm(N))
add(MAXK - 7, from_cycles(N, [N]))
add(MAXK - 1, prime_cycles(N))
add(random.randint(1, MAXK), prime_cycles(N))
add(N - 1 + N * random.randint(10 ** 9, 10 ** 12), from_cycles(N, [N]))      # k mod N = N - 1
add(MAXK, list(range(N, 0, -1)))
add(MAXK - 1, list(range(N, 0, -1)))
add(MAXK, list(range(1, N + 1)))
add(0, perm(N))
add(random.randint(1, MAXK), from_cycles(N, [3] * (N // 3)))
add(random.randint(1, MAXK), from_cycles(N, [99_991, 99_989]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
