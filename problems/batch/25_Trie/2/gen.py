# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(250002)
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
add(["apple", "apricot", "banana", "band", "ban"])
add(["dog", "cat", "cow", "c"])
add(["x"])
add(["abc", "a", "abd", "ab"])
add(["bab", "ba", "aab", "bbab", "abab", "babb"])
# hidden: small
add(["z", "zz"])
add(distinct(10, lambda: word("ab", 1, 4)))
add(distinct(40, lambda: word("abc", 1, 5)))
add(distinct(200, lambda: word("ab", 1, 10)))
add(distinct(1000, lambda: word("abcdefghijklmnopqrstuvwxyz", 2, 6)))
add(distinct(2000, lambda: "q" * random.randint(0, 30) + word("pq", 1, 6)))
# hidden: maximum size
add(distinct(MAXN, lambda: word("abcdefghijklmnopqrstuvwxyz", 2, 6)))
add(distinct(140_000, lambda: word("abcdef", 4, 7)))                # many words are prefixes of others
add(distinct(50_000, lambda: "kitti" + word("abc", 10, 12)))          # long common start
add(["a" * k for k in range(1, 1414)])                               # each word is a prefix of the next
ws = ["m" * 400_000 + "a", "m" * 400_000 + "b", "m" * 199_990]      # three very long words
add(ws)
add(distinct(100_000, lambda: word("wxyz", 6, 9)))
ws = distinct(15_000, lambda: word("ab", 25, 30))
ws += distinct(15_000, lambda: "b" * 25 + word("cd", 1, 16))
ws = sorted(set(ws))
random.shuffle(ws)
add(ws)
# many words of one long shape: d...d + 3 letters
add(distinct(25_000, lambda: "d" * 30 + word("abcdefgh", 3, 6)))
ws = distinct(MAXN // 2, lambda: word("abcdefghijklmnopqrstuvwxyz", 3, 6))
have = set(ws)
ws += [w + "s" for w in ws[:60_000] if w + "s" not in have]
add(sorted(set(ws), key=lambda w: (len(w), w))[::-1])

# a hundred words of length about 10^4 with a long common start (review)
base = word("ab", 9000, 9000)
add(distinct(100, lambda: base + word("ab", 950, 1000)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
