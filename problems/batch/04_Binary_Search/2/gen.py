# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(40203)
MAXS = 10**6
tests = []


def add(s, t, D):
    assert 1 <= len(t) <= len(s) <= MAXS and 1 <= D <= len(s)
    assert all("a" <= c <= "z" for c in s + t)
    tests.append(f"{s}\n{t}\n{D}\n")


def zone(n, letters, weights, D, breaks, noise="x"):
    """n letters: random ones, with `breaks` runs of D + 1 noise letters (they cut every chain) at random places"""
    z = random.choices(letters, weights, k=n - breaks * (D + 1))
    for _ in range(breaks):
        p = random.randrange(n + 1)
        z[p:p] = [noise] * (D + 1)
    return "".join(z)


def runs(total, letter, D, lens):
    """runs of `letter` (lengths from lens) separated by gaps longer than D"""
    out = []
    for k in lens:
        out.append(letter * k)
        out.append("x" * (D + random.randint(1, 3)))
    s = "".join(out)
    return s[:total]


# samples
add("hhheeelllllloooo", "hello", 16)
add("yyxyeeesssxy", "yes", 1)
add("pqrrqp", "pqp", 3)
add("zzzyzzz", "zy", 1)
add("abc", "abd", 1)
# hidden: small (checked by brute force)
add("a", "a", 1)
add("ab", "ba", 2)
add("aaxxaaaxa", "a", 2)                                          # the longest chain starts right after a gap
add("aaxaaxxaaa", "a", 1)
add("hhxheeyellxlllooo", "hello", 2)                              # two groups of l need two chains
add("abcabcabc", "abc", 3)
add(zone(60, "abx", [3, 3, 2], 2, 3), "ab", 2)
add(zone(200, "ab", [1, 1], 1, 0), "aba", 1)
add(zone(300, "nox", [4, 4, 1], 3, 6), "no", 3)
add(zone(150, "ab", [2, 1], 4, 4) + zone(150, "ab", [1, 2], 4, 4), "ab", 4)
add(zone(2000, "abcx", [1, 1, 1, 1], 5, 10), "cab", 5)
add(zone(3000, "lox", [5, 5, 1], 4, 20), "lol", 4)
add(runs(3000, "q", 2, [random.randint(1, 60) for _ in range(80)]), "q", 2)
# hidden: maximum size
N = MAXS
add(zone(N // 2, "abx", [8, 1, 1], 10, 30) + zone(N // 2, "abx", [1, 8, 1], 10, 30), "ab", 10)
add(zone(N // 3, "ab", [5, 1], 6, 50) + zone(N // 3, "ab", [1, 5], 6, 50) + zone(N - 2 * (N // 3), "ab", [5, 1], 6, 50), "aba", 6)
add(runs(N, "z", 1, [random.randint(1, 500) for _ in range(2400)] + [60000] + [random.randint(1, 500) for _ in range(1400)]), "z", 1)
add("".join(zone(N // 5, "helox", w, 20, 8) for w in ([9, 1, 1, 1, 1], [1, 9, 1, 1, 1], [1, 1, 9, 1, 1], [1, 1, 9, 1, 1], [1, 1, 1, 9, 1])), "hello", 20)
add(zone(N, "ab", [1, 1], N, 0), "ab", N)                           # no limit at all
add(zone(N, "abx", [3, 3, 1], 30, 0), "ba", 30)
add(zone(N // 2, "abx", [12, 3, 1], 20, 100) + zone(N // 2, "abx", [3, 12, 1], 20, 100), "aab", 20)
add(zone(N, "mnx", [10, 10, 1], 30, 30), "mnm", 30)
add(runs(N // 2, "c", 3, [random.randint(1000, 30000) for _ in range(40)]) + "d" * (N // 2), "cd", 3)
add(zone(N, "ytx", [6, 6, 1], 25, 30), "tty", 25)

for t in tests:
    assert t.endswith("\n") and " " not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
