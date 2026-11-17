# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(140202)
MAXN, MAXM = 200_000, 200_000
LET = "abcdefghijklmnopqrstuvwxyz"
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(s, rules):
    n, m = len(s), len(rules)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM
    assert all(c == "?" or c in LET for c in s)
    assert all(1 <= a <= n and 1 <= b <= n for a, b in rules)
    tests.append(f"{n} {m}\n{s}\n" + "".join(f"{a} {b}\n" for a, b in rules))


def code(n, p_known, letters=LET):
    return "".join(random.choice(letters) if random.random() < p_known else "?" for _ in range(n))


def rnd_rules(n, m):
    return [(ri(1, n), ri(1, n)) for _ in range(m)]


def flip(a, b):
    return (a, b) if random.random() < 0.5 else (b, a)


def tree_rules(n, deep=False):
    p = list(range(1, n + 1))
    random.shuffle(p)
    res = []
    for i in range(1, n):
        j = max(0, i - ri(1, 3)) if deep else ri(0, i - 1)
        res.append(flip(p[i], p[j]))
    random.shuffle(res)
    return res


add("a??b?", [(1, 2), (3, 5), (2, 3), (4, 5), (1, 1)])
add("????", [(1, 2), (3, 4), (2, 1), (4, 1)])
add("?", [(1, 1)])
add("ab?ba?", [(3, 6), (1, 5), (2, 6), (1, 3)])
add("abc", [(2, 2), (1, 2), (3, 3)])


add("z", [(1, 1), (1, 1)])
add("??", [(2, 1), (1, 2)])
for n, m, pk in ((5, 8, 0.3), (6, 10, 0.0), (7, 12, 0.5), (8, 15, 0.2), (8, 6, 1.0)):
    add(code(n, pk, "ab"), rnd_rules(n, m))
add(code(40, 0.1, "abc"), rnd_rules(40, 60))
add(code(300, 0.02), tree_rules(300) + rnd_rules(300, 100))
add(code(3000, 0.0), rnd_rules(3000, 5000))
s = "".join(random.choice("xy") if random.random() < 0.01 else "?" for _ in range(5000))
add(s, tree_rules(5000))


N, M = MAXN, MAXM
add("?" * N, rnd_rules(N, M))
add("?" * N, [(k, 1) for k in range(2, N + 1)] + [(N, 1)])
add(code(N, 0.001, "q"), tree_rules(N, True) + rnd_rules(N, 1))
s = list("?" * N)
s[ri(0, N - 1)] = "a"
s[ri(0, N - 1)] = "b"
add("".join(s), tree_rules(N) + [(1, 1)])
add(code(N, 0.0005, "abcdefghij"), rnd_rules(N, M))
half = N // 2
pal = [(i, N + 1 - i) for i in range(1, half + 1)]
random.shuffle(pal)
s = code(half, 0.001, "m")
add(s + s[::-1], pal + rnd_rules(N, M - half))
add("?" * N, [flip(k, k + 1) for k in range(1, N)] + [(1, N)])
add(code(N, 0.0, LET), [(k, k) for k in range(1, M // 2 + 1)] + rnd_rules(N, M // 2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_300_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
