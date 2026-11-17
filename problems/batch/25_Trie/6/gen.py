# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(250006)
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


add(["car", "cat", "cart", "dog"])
add(["ab", "ab", "a"])
add(["x"])
add(["abc", "abd", "b", "abc", "ab"])
add(["baa", "bab", "aab", "b", "ba", "aba"])

add(["q", "r"])
add([word("ab", 1, 4) for _ in range(10)])
add([word("abc", 1, 6) for _ in range(100)])
add([word("ab", 1, 12) for _ in range(1000)])
add(["z" * random.randint(1, 50) + word("yz", 0, 5) for _ in range(2000)])
add([word("abcdefghijklmnopqrstuvwxyz", 1, 8) for _ in range(3000)])


N = MAXN
AZ = "abcdefghijklmnopqrstuvwxyz"


def nodes(ws):
    return len({w[:i] for w in set(ws) for i in range(1, len(w) + 1)})


def longpart(ws, B=20_000, alpha="xy"):
    room = MAXC - sum(len(w) for w in ws)
    base = word(alpha, B, B)
    extra = [base]
    room -= B
    while room >= B + 3 and len(ws) + len(extra) < MAXN:
        w = random.choice(extra) if random.random() < 0.2 else base + word(AZ, 1, 3)
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
    assert nodes(ws) > 225_000
    return ws


add(longpart(many_nodes(265_000, 12, 20)))
add(longpart([word("ab", 1, 8) for _ in range(60_000)]))
add(longpart(["same"] * 60_000))
add(longpart(["a" * random.randint(1, 8) for _ in range(60_000)], alpha="ab"))
base = word("ab", 990, 990)
add(longpart([base[:random.randint(950, 990)] + word("ab", 0, 8) for _ in range(300)], alpha="cd"))
add(["k" * 499_990, "k" * 499_990 + "x"] + ["k"] * 10)
add(["m" * 800_000] + ["m"] * (N - 1))
add(longpart(many_nodes(270_000, 5, 30)))
ws = [word("pq", 20, 30) for _ in range(9_000)]
add(longpart([random.choice(ws) for _ in range(11_000)]))
ws = sorted(many_nodes(285_000, 10, 16))
add(longpart(ws))


base = word("ab", 9000, 9000)
add([base + word("ab", 950, 1000) for _ in range(100)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
