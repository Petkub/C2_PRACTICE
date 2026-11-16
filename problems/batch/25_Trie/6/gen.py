# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(250006)
MAXN, MAXC = 200_000, 1_000_000
tests = []


def add(ws):
    n = len(ws)
    assert 1 <= n <= MAXN
    assert sum(len(w) for w in ws) <= MAXC
    assert all(len(w) >= 1 and all("a" <= c <= "z" for c in w) for w in ws)
    tests.append(f"{n}\n" + "".join(w + "\n" for w in ws))


def word(alpha, lo, hi):
    return "".join(random.choices(alpha, k=random.randint(lo, hi)))


# samples
add(["car", "cat", "cart", "dog"])
add(["ab", "ab", "a"])
add(["x"])
add(["abc", "abd", "b", "abc", "ab"])
add(["baa", "bab", "aab", "b", "ba", "aba"])
# hidden: small
add(["q", "r"])
add([word("ab", 1, 4) for _ in range(10)])
add([word("abc", 1, 6) for _ in range(100)])
add([word("ab", 1, 12) for _ in range(1000)])
add(["z" * random.randint(1, 50) + word("yz", 0, 5) for _ in range(2000)])
add([word("abcdefghijklmnopqrstuvwxyz", 1, 8) for _ in range(3000)])
# hidden: maximum size
N = MAXN
add([word("abcdefghijklmnopqrstuvwxyz", 1, 8) for _ in range(N)])
add([word("ab", 1, 8) for _ in range(N)])                                # many shared prefixes
add(["same"] * N)                                                        # every pair shares the whole word
add(["a" * random.randint(1, 8) for _ in range(N)])
base = word("ab", 990, 990)
add([base[:random.randint(950, 990)] + word("ab", 0, 8) for _ in range(1000)])   # long common prefixes
add(["k" * 499_990, "k" * 499_990 + "x"] + ["k"] * 10)
add(["m" * 800_000] + ["m"] * (N - 1))                                    # one long word, many short ones
add([word("abc", 3, 5) for _ in range(N)])
ws = [word("pq", 20, 30) for _ in range(30_000)]
add([random.choice(ws) for _ in range(35_000)])                          # repeated long-ish words
add(sorted(word("ab", 2, 7) for _ in range(N)))

# a hundred words of length about 10^4 with a long common start (review)
base = word("ab", 9000, 9000)
add([base + word("ab", 950, 1000) for _ in range(100)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
