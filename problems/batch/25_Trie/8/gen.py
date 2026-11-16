# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(250008)
MAXN, MAXC = 200_000, 1_000_000
tests = []


def add(ws):
    n = len(ws)
    assert 1 <= n <= MAXN
    assert sum(len(w) for w in ws) <= MAXC
    assert len(set(ws)) == n
    assert all(len(w) >= 1 and all("a" <= c <= "z" for c in w) for w in ws)
    tests.append(f"{n}\n" + "".join(w + "\n" for w in ws))


def word(alpha, lo, hi):
    return "".join(random.choices(alpha, k=random.randint(lo, hi)))


def distinct(n, make):
    seen, ws, tries = set(), [], 0
    while len(ws) < n:
        tries += 1
        assert tries < 20 * n + 1000
        w = make()
        if w not in seen:
            seen.add(w)
            ws.append(w)
    return ws


# samples
add(["print", "the", "poem"])
add(["ab", "a"])
add(["zzz"])
add(["abc", "abd", "b", "ab"])
add(["ba", "aab", "bab", "a", "abba"])
# hidden: small (N <= 15)
add(["q", "r"])
add(distinct(6, lambda: word("ab", 1, 4)))
add(distinct(9, lambda: word("abc", 1, 6)))
add(distinct(12, lambda: word("ab", 1, 8)))
add(distinct(15, lambda: word("abcd", 1, 10)))
add(["zzzzzzzzzz", "a", "b", "c", "ab", "abc", "abcd", "z"])                 # the longest word is last in order
add(distinct(14, lambda: word("xy", 3, 7)))
# hidden: larger
add(distinct(3000, lambda: word("abcdefghijklmnopqrstuvwxyz", 1, 8)))
# hidden: maximum size
def fixed(n, alpha, L):
    """n distinct words of length L over alpha, in random order"""
    k = len(alpha)
    out = []
    for x in random.sample(range(k ** L), n):
        w = []
        for _ in range(L):
            w.append(alpha[x % k])
            x //= k
        out.append("".join(w))
    return out


AZ = "abcdefghijklmnopqrstuvwxyz"
N = MAXN
ws = fixed(10_000, AZ, 3) + fixed(189_999, AZ, 5) + ["abcdefgh"]
random.shuffle(ws)
add(ws)
ws = fixed(7776, "abcdef", 5) + fixed(40_000, "abcdef", 6) + fixed(100_000, "abcdef", 7) + ["a" * 12]
random.shuffle(ws)
add(ws)
add(["kitti" + w for w in fixed(50_000, "abc", 11)] + ["kitta" + "b" * 20])
add(["a" * k for k in range(1, 1414)])                                       # each word is a prefix of the next
add(["m" * 500_000, "b" * 499_000] + distinct(100, lambda: word("abc", 1, 9)))   # two very long words
ws = fixed(600, AZ, 2) + fixed(17_000, AZ, 3) + fixed(N - 17_601, AZ, 4)
random.shuffle(ws)
add(ws + ["a" * 100_000])                                                     # the longest word is lexicographically small
add(sorted(fixed(50_000, "wxyz", 8) + fixed(50_000, "wxyz", 9) + ["w" * 12]))
add(["d" * 30 + w for w in fixed(25_000, "abcdefgh", 5)] + ["d" * 29 + "a" * 10])
add(distinct(1000, lambda: word("ab", 900, 990)))
base = word("st", 5000, 5000)
add(distinct(100, lambda: base + word("st", 4800, 4900)))                    # long words with a long common start

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
