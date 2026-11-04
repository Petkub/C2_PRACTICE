# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(151801)
MAXN = 200_000
tests = []
LOWER = set("abcdefghijklmnopqrstuvwxyz")


def add(t, pieces):
    assert 1 <= len(t) <= MAXN and set(t) <= LOWER
    assert len(pieces) >= 1 and all(len(p) >= 1 and set(p) <= LOWER for p in pieces)
    assert sum(len(p) for p in pieces) <= 100
    s = f"{t}\n{'*'.join(pieces)}\n"
    assert all(32 <= ord(c) <= 126 or c == "\n" for c in set(s))
    tests.append(s)


def rs(n, alpha):
    return "".join(random.choices(alpha, k=n))


def plant(t, word, positions):
    t = list(t)
    for p in positions:
        t[p:p + len(word)] = word
    return "".join(t)


# samples
add("abzzzcdabcd", ["ab", "cd"])
add("aaa", ["aa", "aa"])
add("mississippi", ["ssi"])
add("abcabc", ["a", "c"])
add("programming", ["r", "g", "m", "n"])
add("aabaab", ["a", "a", "b"])
# hidden: small (brute checks these)
add("a", ["a"])
add("a", ["b"])
add("ab", ["a", "b"])
add("abab", ["ab", "ab"])
for n, alpha, k, pl in [(30, "ab", 3, 2), (80, "abc", 2, 3), (200, "ab", 5, 2), (1000, "ab", 4, 4)]:
    add(rs(n, alpha), [rs(random.randint(1, pl), alpha) for _ in range(k)])
add(rs(3000, "ab"), [rs(random.randint(3, 6), "ab") for _ in range(6)])
t = rs(5000, "abcd")
add(t, [t[100:105], t[2000:2004], t[4900:4903]])
# hidden: large
N = MAXN
H = N // 2
# many starts and the later pieces only at the far right: every scan from a start is long
add("b" * H + "x" * (N - H - 1) + "c", ["b", "xc"])
add("a" * (N - 1) + "b", ["a", "ab"])
add("a" * N, ["aa", "a", "aaa"])
add("a" * (N - 1) + "b", ["a"] * 98 + ["ab"])
add("ab" * (H // 2) + "x" * (N - 2 * (H // 2) - 3) + "abc", ["ab", "ab", "abc"])
add(rs(N, "ab"), [rs(random.randint(3, 5), "ab") for _ in range(8)])
add("c" * H + "a" * (N - H - 2) + "ab", ["c", "a", "ab"])
add(("abc" * N)[:N - 2] + "d", ["abc", "abc", "cd"])
add("q" * H + "z" * (N - H - 1) + "q", ["q", "z" * 49, "zq"])
add("ab" * (N // 8) + "c" * (N - N // 4 - 2) + "cd", ["ab", "c", "cd"])
add(rs(N // 4, "ab") + "z" * (N - N // 4 - 3) + "zzy", ["a", "b", "zzy"])
add("k" * (N // 3) + "m" * (N - N // 3 - 4) + "mmmp", ["k", "kmm", "mmmp"])
add("d" * H + "e" * (N - H - 1) + "f", ["d"] + ["e"] * 97 + ["ef"])
add(rs(H, "ab") + "a" * (N - H - 1) + "c", ["ab", "ba", "ac"])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
