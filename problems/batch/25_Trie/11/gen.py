# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
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
# samples
add(["ba", "a", "bb", "c"])
add(["apple", "apply", "ape", "app", "bat"])
add(["solo"])
add(["aa", "aa", "aa"])
add(["abc", "abd", "bcd", "abc", "bce", "a"])
# hidden: small (brute force over all pairings)
add(["x", "y"])
add([word("ab", 1, 4) for _ in range(7)])
add([word("abc", 1, 5) for _ in range(10)])
add([word("ab", 1, 6) for _ in range(13)])
add([word("ab", 2, 8) for _ in range(16)])
add([word("abcd", 1, 6) for _ in range(15)])
# hidden: medium (greedy check)
add([word("ab", 1, 10) for _ in range(500)])
add([word("abc", 1, 7) for _ in range(2001)])
# hidden: maximum size
N = MAXN
add([word(AZ, 1, 8) for _ in range(N)])
add([word("ab", 1, 8) for _ in range(N)])
add([word("abc", 3, 5) for _ in range(N - 1)])                         # odd: one word is left out
add(["same"] * (N - 1))
add(["a" * random.randint(1, 8) for _ in range(N)])
base = word("ab", 990, 990)
add([base[:random.randint(900, 990)] + word("ab", 0, 8) for _ in range(1001)])
add(["k" * 499_990, "k" * 499_990 + "x"] + ["k" + word("ab", 0, 2) for _ in range(9)])
ws = [word("pq", 20, 30) for _ in range(15_000)]
add([random.choice(ws) for _ in range(33_333)])
add(sorted(word("ab", 2, 7) for _ in range(N)))
ws = []
for _ in range(N // 2):                                                   # sorted neighbours are a bad pairing
    c = random.choice(AZ)
    ws.append(c + "a" + word("z", 0, 2))
    ws.append(c + "b" + word("y", 0, 2))
random.shuffle(ws)
add(ws)

# a hundred words of length about 10^4 with a long common start (review)
base = word("ab", 9000, 9000)
add([base + word("ab", 950, 1000) for _ in range(100)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
