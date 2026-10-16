# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7014)
MAXN, MAXL = 20_000, 8
ALL = "abcdef"
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(words, a, b, shuffle=True):
    n = len(words)
    assert 1 <= n <= MAXN and len(set(words)) == n
    assert all(1 <= len(x) <= MAXL and set(x) <= set(ALL) for x in words)
    assert a in words and b in words
    words = list(words)
    if shuffle:
        random.shuffle(words)
    tests.append(f"{n}\n{a} {b}\n" + " ".join(words) + "\n")


def rword(lo, hi, alpha):
    return "".join(alpha[ri(0, len(alpha) - 1)] for _ in range(ri(lo, hi)))


def edit(x, alpha):
    """one random change / deletion / insertion that keeps the length in 1..MAXL"""
    while True:
        k = ri(0, 2)
        if k == 0:
            i = ri(0, len(x) - 1)
            ch = alpha[ri(0, len(alpha) - 1)]
            if ch != x[i]:
                return x[:i] + ch + x[i + 1:]
        elif k == 1 and len(x) > 1:
            i = ri(0, len(x) - 1)
            return x[:i] + x[i + 1:]
        elif k == 2 and len(x) < MAXL:
            i = ri(0, len(x))
            return x[:i] + alpha[ri(0, len(alpha) - 1)] + x[i:]


def walk(start, steps, alpha, used):
    """a random walk of edits through new words; returns the words in order"""
    path = [start]
    used.add(start)
    x = start
    for _ in range(steps):
        for _ in range(50):
            y = edit(x, alpha)
            if y not in used:
                break
        else:
            break
        used.add(y)
        path.append(y)
        x = y
    return path


def random_dict(n, lo, hi, alpha, used=None):
    used = set() if used is None else used
    res = []
    while len(res) < n:
        x = rword(lo, hi, alpha)
        if x not in used:
            used.add(x)
            res.append(x)
    return res


# samples
add(["dab", "dad", "dead", "deed", "feed", "fee"], "dab", "fee", False)
add(["abc", "fed", "abd"], "abc", "fed", False)
add(["added"], "added", "added", False)
add(["a", "fade", "ad", "faded", "fad"], "faded", "a", False)
add(["ab", "ba", "a", "b", "aba"], "ab", "ba", False)
add(["face", "fade", "fad", "bad", "bead", "bed", "ace"], "face", "bed", False)
# hidden: small and medium
add(["a", "b"], "a", "b")
add(["a", "ab", "abc", "abcd", "abcde"], "abcde", "a")
add(["abcd", "abdc"], "abcd", "abdc")                        # a swap is not one edit
add(["f", "ff", "fff", "ffff", "ffffffff"], "f", "ffffffff")  # cannot jump four letters
used = set()
p = walk("faded", 30, ALL, used)
add(p + random_dict(200, 1, 8, ALL, used), p[0], p[-1])
used = set()
w = random_dict(300, 1, 6, "abc", used)
add(w, w[0], w[1])
used = set()
w = random_dict(2000, 1, 6, "abcd", used)
add(w, w[0], w[-1])
used = set()
p = walk("aaaaaaaa", 400, "ab", used)
add(p + random_dict(1500, 3, 8, "abc", used), p[0], p[-1])
used = set()
p = walk("deadbeef", 3000, ALL[:6], used)
add(p + random_dict(2000, 1, 8, ALL[:6], used), p[0], p[-1])
used = set()
w = random_dict(5000, 1, 8, ALL, used)
add(w, w[0], w[1])                                            # almost surely not connected
# hidden: large
N = MAXN
used = set()                                                  # every word over {a, b, c} of length 1..8 (except a few)
allw = []
for L in range(1, MAXL + 1):
    cur = [""]
    for _ in range(L):
        cur = [x + ch for x in cur for ch in "abc"]
    allw += cur
random.shuffle(allw)
add(allw[:9800], "abcabcab" if "abcabcab" in allw[:9800] else allw[0], "c" if "c" in allw[:9800] else allw[1])
used = set()
w = random_dict(N, 1, 8, "abcd", used)                        # a dense dictionary
add(w, w[0], w[1])
used = set()
w = random_dict(N, 4, 8, "abcde", used)
add(w, w[0], w[2])
used = set()
p = walk("decaf", 15000, ALL, used)                          # one long random walk plus noise
add(p + random_dict(N - len(p), 1, 8, ALL, used), p[0], p[-1])
used = set()
p = walk("aaaa", 15000, "abc", used)                          # a walk over {a, b, c} until it gets stuck
add(p + random_dict(N - len(p), 1, 8, ALL, used), p[0], p[-1])
used = set()
p = walk("beaded", 300, ALL, used)
w = random_dict(N - len(p), 1, 8, ALL, used)
add(p + w, p[0], p[-1])
used = set()
p = walk("ceded", 300, ALL, used)
w = random_dict(N - len(p), 1, 8, ALL, used)
add(p + w, p[0], w[0])                                        # no ladder at all
words = []
for L in range(1, MAXL + 1):                                  # all words over {a, b} plus random ones
    cur = [""]
    for _ in range(L):
        cur = [x + ch for x in cur for ch in "ab"]
    words += cur
used = set(words)
words += random_dict(N - len(words), 1, 8, ALL, used)
add(words, "a", "bbbbbbbb")
used = set()
w = random_dict(N - 1, 7, 8, "abcde", used)                  # the target is far from everything
add(w + ["fffffff"], w[0], "fffffff")
used = set()
w = random_dict(N - 1, 5, 8, "abcde", used)                  # dense enough to be one big component
add(w + ["ff"], w[0], "ff")
used = set()
p = walk("fedcbafe", 5000, ALL, used)
add(p + random_dict(N - len(p), 6, 8, ALL, used), p[0], p[len(p) // 2])
used = set()
p = walk("abcdabcd", 15000, "abcd", used)                     # a long walk through a dense dictionary
add(p + random_dict(N - len(p), 1, 8, "abcd", used), p[0], p[-1])
used = set()
w = random_dict(N - 1, 3, 8, "abcd", used)                    # everything reachable is visited
add(w + ["fff"], w[-1], "fff")

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
