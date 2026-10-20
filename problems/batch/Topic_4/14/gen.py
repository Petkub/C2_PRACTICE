# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(30114)
MAXN = 500_000
ABC = "abcdefghijklmnopqrstuvwxyz"
tests = []


def add(k, s):
    n = len(s)
    assert 1 <= k <= n <= MAXN
    assert all(c in ABC for c in s)
    tests.append(f"{n} {k}\n{s}\n")


def rnd(n, letters, weights=None):
    return "".join(random.choices(letters, weights=weights, k=n))


def shuffled(s):
    a = list(s)
    random.shuffle(a)
    return "".join(a)


def dominant(n, k, big, others, extra=0):
    """letter big as often as k * (others + 1) allows (plus extra), the rest from the letters others"""
    nb = n * k // (k + 1)
    while nb > k * (n - nb + 1):
        nb -= 1
    while nb + 1 <= k * (n - nb):
        nb += 1
    nb = min(n, nb + extra)
    return shuffled(big * nb + rnd(n - nb, others))


# samples
add(2, "aaabbc")
add(1, "aabbb")
add(2, "aaaaab")
add(6, "banana")
add(2, "aaaaaaabbb")
add(2, "bbbbbbaac")
# hidden: small (every choice is tried)
add(1, "z")
add(3, "bbbabbb")
add(1, "cbcacbc")
for n, letters, k in ((8, "ab", 1), (10, "abc", 2), (12, "abcd", 1), (12, "ab", 3), (11, "abc", 1)):
    add(k, rnd(n, letters, [random.random() ** 2 + 0.01 for _ in letters]))
add(1, dominant(300, 1, "b", "ac"))
add(2, dominant(400, 2, "c", "ab"))
add(3, dominant(2000, 3, "a", "b"))
# hidden: large
N = MAXN
add(1, rnd(N, ABC))
add(1, dominant(N, 1, "z", ABC[:25]))                    # z exactly at the limit
add(1, dominant(N, 1, "m", ABC, extra=1))                # one too many: -1
add(2, dominant(N, 2, "a", "bc"))
add(3, dominant(N - 1, 3, "q", "pr"))
add(1, "ab" * (N // 2))
add(N, rnd(N, ABC))                                      # no limit at all
add(N - 1, "a" * N)                                      # one letter, not allowed
add(N, "y" * N)
add(5, rnd(N, "abc", [20, 2, 1]))
add(1, shuffled("a" * (N // 2 - 1000) + rnd(N // 2 + 1000, ABC[1:])))
add(4, dominant(N, 4, "k", ABC[:5]))
add(1000, rnd(N, "ab", [1000, 1]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
