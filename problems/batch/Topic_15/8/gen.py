# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(150801)
MAXS = 1_000_000
MAXP = 50
tests = []


def add(s, p, r):
    assert 1 <= len(s) <= MAXS and 2 <= len(p) <= MAXP
    assert s.isalpha() and s.islower() and s.isascii() and p.isalpha() and p.islower() and p.isascii()
    assert r == "-" or (len(r) == 1 and "a" <= r <= "z")
    tests.append(f"{s}\n{p}\n{r}\n")


def rs(n, alpha):
    return "".join(random.choice(alpha) for _ in range(n))


def nested(p, r, depth, extra=""):
    """undo the process depth times: put p in place of one r (or anywhere when r is empty)"""
    if r == "-":
        k = random.randint(0, len(p))
        left, right = p[:k], p[k:]
    else:
        k = p.index(r)
        left, right = p[:k], p[k + 1:]
    return left * depth + (p if r == "-" else r) + right * depth + extra


def mixed(n, p, r, alpha):
    """random text with many short cascades inserted"""
    parts, size = [], 0
    while size < n:
        if random.random() < 0.5:
            parts.append(rs(random.randint(1, 5), alpha))
        else:
            parts.append(nested(p, r, random.randint(1, 20)))
        size += len(parts[-1])
    return "".join(parts)[:n]


# samples
add("xaabaay", "aba", "b")
add("aaabbbab", "ab", "-")
add("banana", "nab", "x")
add("aaaa", "aa", "a")
add("abcabcabc", "cab", "c")
# hidden: small
add("a", "aa", "a")
add(rs(30, "ab"), "ab", "b")
add(rs(200, "ab"), "aab", "b")
add(mixed(2000, "abc", "b", "abc"), "abc", "b")
add(mixed(3000, "aab", "-", "ab"), "aab", "-")
add(nested("abcdefghij", "e", 300), "abcdefghij", "e")
add(rs(5000, "a") + "b", "ab", "b")
add(mixed(5000, "abab", "a", "ab"), "abab", "a")
add(nested("aab", "b", 100), "aab", "b")
# hidden: large
H = MAXS // 2
add("b" * H + "a" * H, "ba", "-")                     # every removal happens in the middle
add("a" + "b" * (MAXS - 1), "ab", "a")                # every replacement happens at the front
add("a" * (MAXS - 1) + "b", "ab", "b")                # ... at the back, one after the other
add("b" * 20000 + "a" * (49 * 20000), "b" + "a" * 49, "-")
add(nested("x" + "y" * 48 + "z", "-", MAXS // 50 - 2), "x" + "y" * 48 + "z", "-")
add(nested("abcab", "c", (MAXS - 10) // 4), "abcab", "c")
add(mixed(MAXS, "abc", "-", "abc"), "abc", "-")
add(mixed(MAXS, "aab", "b", "ab"), "aab", "b")
add(rs(MAXS, "ab"), "ab", "b")
add(rs(MAXS, "ab"), "aab", "-")
add("a" * MAXS, "a" * 49 + "b", "b")
add(("ab" * 24 + "a") * (MAXS // 49), "ab" * 24 + "b", "-")   # almost-matches everywhere, no hit
add(mixed(MAXS, "ba" + "a" * 20, "b", "ab"), "ba" + "a" * 20, "b")
add(nested("xyzw", "w", (MAXS - 1) // 3), "xyzw", "w")
# the replacement letter itself completes the next occurrence, again and again
add("a" * 400000 + "b" + rs(MAXS - 400001, "ab"), "aab", "b")
add("".join(random.choice(["abc" * random.randint(1, 30) + "d", rs(random.randint(1, 4), "abcd")])
            for _ in range(MAXS // 10))[:MAXS], "abcd", "d")

for t in tests:
    assert t.endswith("\n") and t.count("\n") == 3
    assert t.encode().translate(None, bytes(range(32, 127)) + b"\n") == b""
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
