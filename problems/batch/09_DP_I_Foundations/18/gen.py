# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(90018)
MAXN, MAXM, MAXC = 200000, 100, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(s, p, c):
    n, m = len(s), len(p)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and len(c) == n
    assert all("a" <= ch <= "z" for ch in s + p)
    assert 1 <= min(c) and max(c) <= MAXC
    tests.append(f"{n} {m}\n{s}\n{p}\n" + " ".join(map(str, c)) + "\n")


def rs(n, alpha):
    return "".join(random.choices(alpha, k=n))


def rc(n, lo=1, hi=MAXC):
    return [ri(lo, hi) for _ in range(n)]


# samples
add("abab", "ab", [1, 5, 5, 1])
add("banana", "ana", [4, 2, 3, 1, 3, 5])
add("hello", "oh", [1, 1, 1, 1, 1])
add("success", "s", [2, 7, 1, 1, 3, 5, 4])
add("abc", "abcd", [5, 5, 5])
add("abacabadab", "aab", [3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
# hidden: small (brute.cpp tries every subset)
add("a", "a", [7])
add("z", "y", [1000000000])
add(rs(16, "ab"), "ab", rc(16, 1, 20))
add(rs(18, "ab"), "aba", rc(18, 1, 10))
add(rs(18, "abc"), "abcab", rc(18))
add(rs(17, "a"), "aaaa", rc(17, 1, 100))
add(rs(18, "xyz"), "zyx", rc(18, 1, 5))
add("ab" * 9, "abab", rc(18, 1, 9))
add(rs(18, "pq"), "ppqqp", [1] * 18)
# hidden: maximum size
N = MAXN


def blocks(n, letters, k):
    """k long blocks, each of one letter: removing one letter everywhere is rarely best"""
    out, left = [], n
    for t in range(k):
        size = left // (k - t)
        out.append(letters[t % len(letters)] * size)
        left -= size
    return "".join(out)


add(rs(N, "ab"), "ab", rc(N))
add(blocks(N, "ab", 40), "ab", rc(N, 1, 1000))
add(blocks(N, "abc", 60), "abcabc", rc(N))
add(rs(N, "a"), "a", [MAXC] * N)                       # everything must go: 2 * 10^14
add(rs(N, "ab"), "aabbaabbab" * 10, rc(N))
pat = rs(100, "abcd")
add(pat * (N // 100), pat, rc(N))
add(rs(N, "abcdefghijklmnopqrstuvwxyz"), "z" * 100, rc(N))
add(rs(N, "abc"), "cab" * 33 + "c", rc(N, 1, 100))
add(rs(N, "xy"), "xyx", rc(N, 1, 3))
add(rs(N, "ab"), "b" * 60 + "a" * 40, rc(N))
add(rs(N, "abcdefghijklmnopqrstuvwxyz"), "q", rc(N))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
