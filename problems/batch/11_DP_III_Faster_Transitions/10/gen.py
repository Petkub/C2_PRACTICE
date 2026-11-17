# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(11011)
MAXL, MAXD = 200_000, 100
ABC = "abcdefghijklmnopqrstuvwxyz"
tests = []


def add(D, s, t):
    assert 0 <= D <= MAXD and 1 <= len(s) <= MAXL and 1 <= len(t) <= MAXL
    assert all(c in ABC for c in s + t)
    tests.append(f"{D}\n{s}\n{t}\n")


def rstr(n, letters=ABC):
    return "".join(random.choices(letters, k=n))


def mutate(s, k, letters=ABC, kinds="rid", gap=3):
    """k edits (replace / insert / delete) at random positions at least `gap` apart"""
    s = list(s)
    n = len(s)
    k = min(k, max(0, (n - 2) // gap))
    pos = sorted(random.sample(range(1, (n - 1) // gap), k)) if k else []
    for p in reversed(pos):
        p *= gap
        kind = random.choice(kinds)
        if kind == "r":
            s[p] = random.choice([c for c in letters if c != s[p]] or letters)
        elif kind == "i":
            s.insert(p, random.choice(letters))
        else:
            del s[p]
    return "".join(s)


# samples
add(2, "banana", "bandana")
add(2, "abc", "xyz")
add(0, "same", "same")
add(2, "abcdef", "bcdefa")
add(5, "short", "muchlongertext")
add(6, "algorithm", "rhythm")
# hidden: small
add(0, "a", "b")
add(1, "a", "b")
add(100, "z", "z" * 101)
add(3, "ab" * 5, "ba" * 5)
add(3, "abcab", "ab")
add(30, rstr(40), rstr(35))
# hidden: medium (the brute checks these)
s = rstr(3000, "ab"); add(50, s, mutate(s, 50, "ab", "d"))
s = rstr(2500); add(25, s, mutate(s, 25, ABC, "i"))
s = rstr(3000, "abc"); add(100, s, mutate(s, 100, "abc", gap=1))
# hidden: maximum size
L, D = MAXL, MAXD
for k, letters, kinds in [(100, ABC, "rid"), (100, ABC, "d"), (101, ABC, "rid"), (60, "ab", "rid"),
                          (100, ABC, "r"), (130, "abc", "id"), (100, "ab", "i")]:
    s = rstr(L - 150, letters)
    add(D, s, mutate(s, k, letters, kinds))
s = rstr(L)
add(0, s, s)
add(0, s, s[:-1] + ("a" if s[-1] != "a" else "b"))
add(D, s, rstr(L))                               # far apart: -1
add(D, rstr(L, "a"), "a" * (L - 100))
add(D, "a" * L, "a" * (L - 101))                 # length difference D + 1
s = rstr(L, "ab")
add(D, s, s[50:] + s[:50])                       # rotation by 50: distance 100
add(D, "ab" * (L // 2), "ba" * (L // 2))         # distance 2
add(D, s[:L - 100], mutate(s[:L - 100], 50, "ab", "id", gap=1))      # dense edits

for t in tests:
    assert t.endswith("\n") and " " not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
