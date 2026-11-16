# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(250005)
MAXS, MAXK, MAXW, MAXC = 100_000, 100_000, 500, 1_000_000
tests = []


def add(s, words):
    k = len(words)
    assert 1 <= len(s) <= MAXS and 1 <= k <= MAXK
    assert len(set(words)) == k
    assert all(1 <= len(w) <= MAXW for w in words) and sum(len(w) for w in words) <= MAXC
    assert all("a" <= c <= "z" for c in s + "".join(words))
    tests.append(s + "\n" + f"{k}\n" + "".join(w + "\n" for w in words))


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


def concat(words, n, tail=""):
    """a text of length about n made of random dictionary words, cut to at most n"""
    parts, total = [], 0
    while total < n - len(tail):
        w = random.choice(words)
        if total + len(w) > n - len(tail):
            break
        parts.append(w)
        total += len(w)
    return "".join(parts) + tail


# samples
add("catsanddog", ["cat", "cats", "and", "sand", "dog"])
add("aaaa", ["aa", "a"])
add("abc", ["ab", "bc"])
add("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"])
add("abababa", ["ab", "aba", "ba", "bab", "b"])
# hidden: small
add("a", ["b"])
ws = distinct(10, lambda: word("ab", 1, 4))
add(concat(ws, 20), ws)
ws = distinct(30, lambda: word("abc", 1, 5))
add(concat(ws, 200), ws)
add(word("ab", 1000, 1000), [w for w in ["a", "b", "aa", "ab", "ba", "bb", "aab", "bba", "abab"]])
ws = distinct(300, lambda: word("abc", 1, 8))
add(concat(ws, 3000), ws)
ws = distinct(50, lambda: word("ab", 1, 6))
add(concat(ws, 2000, "c"), ws + ["cc"])                                   # the last letter cannot be covered
# hidden: maximum size
add("a" * MAXS, ["a" * L for L in range(MAXW, 0, -1)])                   # every length 1..500 is a word
ws = distinct(MAXK, lambda: word("abc", 4, 11))
add(concat(ws, MAXS), ws)
ws = distinct(2000, lambda: word("ab", 1, MAXW))
add(concat(ws, MAXS), ws)
ws = ["a", "b", "ab", "ba", "aba", "bab", "abab", "baba"] + ["ab" * L for L in range(3, 250)]
add("ab" * (MAXS // 2), ws)
add("a" * (MAXS - 1) + "b", ["a" * L for L in range(1, MAXW + 1)])        # no split, full work
s = word("abcdefghijklmnopqrstuvwxyz", MAXS, MAXS)
ws = []
seen = set()
while len(ws) < MAXK:
    i = random.randrange(MAXS)
    w = s[i:i + random.randint(1, 10)]
    if w not in seen:
        seen.add(w)
        ws.append(w)
for c in "abcdefghijklmnopqrstuvwxyz":
    if c not in seen:
        ws[random.randrange(len(ws))] = c
        seen.add(c)
ws = sorted(set(ws))
random.shuffle(ws)
add(s, ws)
ws = ["a"] + ["a" * L + "b" for L in range(1, MAXW)]                     # long walks that rarely end in a word
add("a" * MAXS, ws)
ws = ["a"] + ["a" * L + "b" for L in range(1, MAXW)] + ["a" * MAXW]
add("a" * (MAXS // 2) + "b" + "a" * (MAXS // 2 - 1), ws)
ws = distinct(20_000, lambda: "x" * random.randint(0, 40) + word("xy", 1, 20))
add(concat(ws, MAXS), ws)
ws = distinct(1000, lambda: word("ab", 1, 10)) + ["a" * L for L in range(11, MAXW + 1)]
ws = sorted(set(ws))
random.shuffle(ws)
add(concat(ws, MAXS), ws)
# very many words that start like the text at every position but stop matching later
ws = ["a", "aa"] + distinct(90_000, lambda: "a" * random.randint(1, 8) + "b" + word("bcdefghij", 3, 5))
add("a" * (MAXS - 20) + ws[-1] + "a" * (20 - len(ws[-1])), ws)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
