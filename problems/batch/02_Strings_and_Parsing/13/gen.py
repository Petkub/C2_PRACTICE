# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(15012)
MAXN = 10 ** 6
L = "ACGT"
tests = []


def add(s, t):
    n = len(s)
    assert 1 <= n <= MAXN and set(s) <= set(L)
    assert len(t) == 4 and all(x >= 0 for x in t) and sum(t) == n
    tests.append(f"{n}\n{s}\n{t[0]} {t[1]} {t[2]} {t[3]}\n")


def counts(s):
    return [s.count(ch) for ch in L]


def rnd(n, w=(1, 1, 1, 1)):
    return "".join(random.choices(L, weights=w, k=n))


def rnd_target(n):
    cuts = sorted(random.randint(0, n) for _ in range(3))
    return [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], n - cuts[2]]


def shifted(s, moves):
    # counts of s with `moves` letters moved from one kind to another (a small repair)
    t = counts(s)
    for _ in range(moves):
        a = random.choice([k for k in range(4) if t[k] > 0])
        b = random.randrange(4)
        t[a] -= 1
        t[b] += 1
    return t


# samples
add("AACGTAAA", [2, 2, 2, 2])
add("GAAG", [2, 1, 1, 0])
add("TGCA", [1, 1, 1, 1])
add("AAAAA", [0, 0, 0, 5])
add("CATTGCATTA", [3, 3, 2, 2])
# hidden: small and medium (brute force checks them)
add("C", [0, 1, 0, 0])
add("C", [0, 0, 1, 0])
add("ACGTACGTAC", [3, 3, 2, 2])
for n in (7, 20, 60):
    for _ in range(2):
        add(rnd(n), rnd_target(n))
add(rnd(300, (5, 1, 1, 1)), [75, 75, 75, 75])
add(rnd(2000), rnd_target(2000))
s = rnd(3000)
add(s, shifted(s, 40))
s = "A" * 1500 + "CGT" * 500
add(s, [500, 1000, 500, 1000])
# hidden: large (the answer is long in most of them, so trying every window is far too slow)
add("A" * MAXN, [0, 0, 0, MAXN])
add("A" * MAXN, [MAXN // 2, MAXN // 2, 0, 0])
add("A" * (MAXN // 2) + "C" * (MAXN // 2), [0, MAXN // 2, MAXN // 2, 0])
s = rnd(MAXN)
add(s, rnd_target(MAXN))
s = rnd(MAXN, (8, 1, 1, 1))
add(s, [MAXN // 4] * 4)
s = rnd(MAXN)
t = counts(s)
t[0] -= 20000  # 20000 surplus A spread over the whole string
t[1] += 20000
add(s, t)
s = rnd(MAXN)
t = counts(s)
t[2] -= 1  # one G too many: the answer is a single letter
t[3] += 1
add(s, t)
s = ("ACGT" * (MAXN // 4))
add(s, [MAXN // 4 + 1, MAXN // 4 - 1, MAXN // 4, MAXN // 4])  # many shortest windows: leftmost
s = rnd(MAXN // 2) + "G" * (MAXN // 2)
t = counts(s[:MAXN // 2])
t = [t[0] + MAXN // 8, t[1] + MAXN // 8, t[2] + MAXN // 8, t[3] + MAXN // 8]
add(s, t)  # the repair is at the right end
s = "T" * 10 + rnd(MAXN - 20, (1, 1, 1, 0)) + "T" * 10
add(s, [0, 0, 0, MAXN])
s = rnd(MAXN, (1, 3, 3, 1))
add(s, [MAXN - 3, 1, 1, 1])
s = rnd(MAXN)
add(s, [MAXN // 10, MAXN // 10, MAXN // 10, MAXN - 3 * (MAXN // 10)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert all(32 <= b <= 126 or b == 10 for b in t.encode())
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
