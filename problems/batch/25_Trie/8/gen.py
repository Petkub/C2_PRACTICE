# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(250008)
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


add(["print", "the", "poem"])
add(["ab", "a"])
add(["zzz"])
add(["abc", "abd", "b", "ab"])
add(["ba", "aab", "bab", "a", "abba"])

add(["q", "r"])
add(distinct(6, lambda: word("ab", 1, 4)))
add(distinct(9, lambda: word("abc", 1, 6)))
add(distinct(12, lambda: word("ab", 1, 8)))
add(distinct(15, lambda: word("abcd", 1, 10)))
add(["zzzzzzzzzz", "a", "b", "c", "ab", "abc", "abcd", "z"])
add(distinct(14, lambda: word("xy", 3, 7)))

add(distinct(3000, lambda: word("abcdefghijklmnopqrstuvwxyz", 1, 8)))

def fixed(n, alpha, L):
    k = len(alpha)
    out = []
    for x in random.sample(range(k ** L), n):
        w = []
        for _ in range(L):
            w.append(alpha[x % k])
            x //= k
        out.append("".join(w))
    return out


AZ = "abcdefghijklmnopqrstuvwxyz"
N = MAXN


def longpart(ws, B=36_000, alpha="no"):
    room = MAXC - sum(len(w) for w in ws)
    have = set(ws)
    base = word(alpha, B, B)
    extra = []
    while room >= B + 3 and len(ws) + len(extra) < MAXN:
        w = base + word(AZ, 1, 3)
        if w not in have:
            have.add(w); extra.append(w); room -= len(w)
    random.shuffle(extra)
    k = random.randint(0, len(ws))
    return ws[:k] + extra + ws[k:]


ws = fixed(5_000, AZ, 3) + distinct(25_000, lambda: word(AZ, 10, 14)) + ["abcdefgh"]
ws = sorted(set(ws))
random.shuffle(ws)
assert len({w[:i] for w in ws for i in range(1, len(w) + 1)}) > 210_000
add(longpart(ws))
ws = fixed(7776, "abcdef", 5) + fixed(10_000, "abcdef", 6) + fixed(20_000, "abcdef", 7) + ["a" * 12]
random.shuffle(ws)
add(longpart(ws))
add(longpart(["kitti" + w for w in fixed(15_000, "abc", 11)] + ["kitta" + "b" * 20]))
add(longpart(["a" * k for k in range(1, 701)], alpha="ab"))
add(["m" * 500_000, "b" * 499_000] + distinct(100, lambda: word("abc", 1, 9)))
ws = fixed(600, AZ, 2) + fixed(17_000, AZ, 3) + fixed(N - 17_601, AZ, 4)
random.shuffle(ws)
add(ws + ["a" * 100_000])
add(sorted(longpart(fixed(15_000, "wxyz", 8) + fixed(15_000, "wxyz", 9) + ["w" * 12])))
add(longpart(["d" * 30 + w for w in fixed(7_000, "abcdefgh", 5)] + ["d" * 29 + "a" * 10]))
add(longpart(distinct(250, lambda: word("ab", 900, 990))))
base = word("st", 5000, 5000)
add(distinct(100, lambda: base + word("st", 4800, 4900)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
