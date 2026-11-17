# Test generator of this problem (the judge runs it to rebuild the big tests).
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


add(["apple", "apricot", "banana", "band", "ban"])
add(["dog", "cat", "cow", "c"])
add(["x"])
add(["abc", "a", "abd", "ab"])
add(["bab", "ba", "aab", "bbab", "abab", "babb"])

add(["z", "zz"])
add(distinct(10, lambda: word("ab", 1, 4)))
add(distinct(40, lambda: word("abc", 1, 5)))
add(distinct(200, lambda: word("ab", 1, 10)))
add(distinct(1000, lambda: word("abcdefghijklmnopqrstuvwxyz", 2, 6)))
add(distinct(2000, lambda: "q" * random.randint(0, 30) + word("pq", 1, 6)))


AZ = "abcdefghijklmnopqrstuvwxyz"


def nodes(ws):
    return len({w[:i] for w in ws for i in range(1, len(w) + 1)})


def longpart(ws, B=20_000, alpha="xy"):
    room = MAXC - sum(len(w) for w in ws)
    have = set(ws)
    base = word(alpha, B, B)
    extra = [base, base[:B - 7]]
    while room - sum(len(w) for w in extra) >= B + 4 and len(ws) + len(extra) < MAXN:
        w = base + word(AZ, 1, 3)
        if w not in have and w not in extra:
            extra.append(w)
    extra = [w for w in extra if w not in have]
    random.shuffle(extra)
    k = random.randint(0, len(ws))
    return ws[:k] + extra + ws[k:]


def many_nodes(chars, lo, hi, alpha=AZ):
    ws, seen, used = [], set(), 0
    while used < chars:
        w = word(alpha, lo, hi)
        if w not in seen:
            seen.add(w); ws.append(w); used += len(w)
    assert nodes(ws) > 225_000
    return ws


add(longpart(many_nodes(265_000, 12, 20)))
add(longpart(distinct(50_000, lambda: word("abcdef", 4, 7))))
add(longpart(distinct(15_000, lambda: "kitti" + word("abc", 10, 12))))
add(longpart(["a" * k for k in range(1, 701)], alpha="ab"))
ws = ["m" * 400_000 + "a", "m" * 400_000 + "b", "m" * 199_990]
add(ws)
add(longpart(many_nodes(270_000, 5, 30)))
ws = distinct(4_600, lambda: word("ab", 50, 60))
ws += distinct(1_500, lambda: "b" * 25 + word("cd", 1, 16))
ws = sorted(set(ws))
random.shuffle(ws)
assert nodes(ws) > 200_000
add(longpart(ws, alpha="cd"))

add(longpart(distinct(8_000, lambda: "d" * 30 + word("abcdefgh", 3, 6))))
ws = distinct(19_000, lambda: word(AZ, 10, 16))
have = set(ws)
ws += [w + "s" for w in ws[:8_000] if w + "s" not in have]
ws = sorted(set(ws), key=lambda w: (len(w), w))[::-1]
assert nodes(ws) > 200_000
add(longpart(ws))


base = word("ab", 9000, 9000)
add(distinct(100, lambda: base + word("ab", 950, 1000)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
