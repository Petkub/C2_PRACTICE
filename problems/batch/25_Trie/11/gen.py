# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(250011)
MAXN, MAXC = 200_000, 1_000_000
tests = []


def add(ws):
    n = len(ws)
    assert 1 <= n <= MAXN
    assert sum(len(w) for w in ws) <= MAXC
    assert all(len(w) >= 1 and all("a" <= c <= "z" for c in w) for w in ws)
    tests.append(f"{n}\n" + "".join(w + "\n" for w in ws))


def word(alpha, lo, hi):
    return "".join(random.choices(alpha, k=random.randint(lo, hi)))


AZ = "abcdefghijklmnopqrstuvwxyz"

add(["ba", "a", "bb", "c"])
add(["apple", "apply", "ape", "app", "bat"])
add(["solo"])
add(["aa", "aa", "aa"])
add(["abc", "abd", "bcd", "abc", "bce", "a"])

add(["x", "y"])
add([word("ab", 1, 4) for _ in range(7)])
add([word("abc", 1, 5) for _ in range(10)])
add([word("ab", 1, 6) for _ in range(13)])
add([word("ab", 2, 8) for _ in range(16)])
add([word("abcd", 1, 6) for _ in range(15)])

add([word("ab", 1, 10) for _ in range(500)])
add([word("abc", 1, 7) for _ in range(2001)])


N = MAXN


def nodes(ws):
    return len({w[:i] for w in set(ws) for i in range(1, len(w) + 1)})


def longpart(ws, B=36_000, alpha="xy"):
    room = MAXC - sum(len(w) for w in ws)
    base = word(alpha, B, B)
    extra = []
    while room >= B + 3 and len(ws) + len(extra) < MAXN:
        w = random.choice(extra) if extra and random.random() < 0.2 else base + word(AZ, 1, 3)
        extra.append(w)
        room -= len(w)
    random.shuffle(extra)
    k = random.randint(0, len(ws))
    return ws[:k] + extra + ws[k:]


def many_nodes(chars, lo, hi):
    ws, used = [], 0
    while used < chars:
        ws.append(word(AZ, lo, hi))
        used += len(ws[-1])
    assert nodes(ws) > 210_000
    return ws


add(longpart(many_nodes(260_000, 10, 18)))
add(longpart([word("ab", 1, 8) for _ in range(50_001)]))
add(longpart(many_nodes(270_000, 5, 30)))
ws = ["same"] * 20_001 + many_nodes(260_000, 10, 18)
random.shuffle(ws)
add(longpart(ws))
add(longpart(["a" * random.randint(1, 8) for _ in range(50_000)], alpha="ab"))
base = word("ab", 990, 990)
add(longpart([base[:random.randint(900, 990)] + word("ab", 0, 8) for _ in range(251)], alpha="cd"))
add(["k" * 499_990, "k" * 499_990 + "x"] + ["k" + word("ab", 0, 2) for _ in range(9)])
ws = [word("pq", 20, 30) for _ in range(5_000)]
add(longpart([random.choice(ws) for _ in range(10_001)]))
ws = sorted(many_nodes(270_000, 10, 16))
add(longpart(ws))
ws = []
for _ in range(40_000):
    c = random.choice(AZ)
    ws.append(c + "a" + word("z", 0, 2))
    ws.append(c + "b" + word("y", 0, 2))
random.shuffle(ws)
add(longpart(ws))


base = word("ab", 36_000, 36_000)
add([base + word("ab", 1, 40) for _ in range(27)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
