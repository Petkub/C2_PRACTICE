# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(250001)
MAXQ, MAXC = 200_000, 1_000_000
tests = []


def add(ops):
    q = len(ops)
    assert 1 <= q <= MAXQ
    assert sum(len(w) for _, w in ops) <= MAXC
    box = {}
    for op, w in ops:
        assert op in "+-?" and len(w) >= 1 and all("a" <= c <= "z" for c in w)
        if op == "+":
            box[w] = box.get(w, 0) + 1
        elif op == "-":
            assert box.get(w, 0) >= 1
            box[w] -= 1
    assert any(op == "?" for op, _ in ops)
    tests.append(f"{q}\n" + "".join(f"{op} {w}\n" for op, w in ops))


def word(alpha, lo, hi):
    return "".join(random.choices(alpha, k=random.randint(lo, hi)))


def churn(q, alpha, lo, hi, p_add, p_del, qlo=1, qhi=None):
    """random operations; queries are prefixes / extensions of stored words or random words"""
    if qhi is None:
        qhi = hi
    ops, bag = [], []
    for _ in range(q):
        r = random.random()
        if r < p_add or not bag:
            w = word(alpha, lo, hi) if not bag or random.random() < 0.7 else random.choice(bag)
            ops.append(("+", w))
            bag.append(w)
        elif r < p_add + p_del:
            i = random.randrange(len(bag))
            bag[i], bag[-1] = bag[-1], bag[i]
            ops.append(("-", bag.pop()))
        else:
            k = random.random()
            if k < 0.4:
                w = random.choice(bag)
                w = w[:random.randint(1, len(w))]
                w = w[:qhi] if len(w) > qlo else w
            elif k < 0.6:
                w = random.choice(bag)[:qhi] + word(alpha, 0, 2)
            else:
                w = word(alpha, qlo, qhi)
            ops.append(("?", w))
    if not any(op == "?" for op, _ in ops):
        ops.append(("?", alpha[0]))
    return ops


# samples
add([("+", "car"), ("+", "cart"), ("+", "cat"), ("?", "ca"), ("?", "cars"), ("-", "cart"), ("?", "cart"), ("?", "dog")])
add([("+", "ab"), ("+", "ab"), ("?", "a"), ("-", "ab"), ("?", "ab"), ("-", "ab"), ("?", "ab")])
add([("+", "apple"), ("+", "app"), ("?", "app"), ("?", "apply"), ("-", "app"), ("?", "app")])
add([("+", "abba"), ("+", "ab"), ("+", "baab"), ("?", "abab"), ("+", "abab"), ("?", "ab"), ("-", "abba"),
     ("?", "abb"), ("?", "b")])
add([("?", "b"), ("+", "b"), ("+", "ba"), ("-", "b"), ("?", "b")])
# hidden: small
add([("?", "z")])
add(churn(30, "ab", 1, 4, 0.5, 0.2))
add(churn(100, "abc", 1, 5, 0.45, 0.25))
add(churn(300, "ab", 1, 8, 0.4, 0.3))
add(churn(1000, "abcdefghijklmnopqrstuvwxyz", 1, 6, 0.5, 0.15))
add(churn(5000, "abc", 1, 7, 0.4, 0.3))
# hidden: maximum size
add(churn(MAXQ, "ab", 1, 6, 0.6, 0.1, 1, 2))                       # short queries matching very many words
add(churn(MAXQ, "abcdefghijklmnopqrstuvwxyz", 1, 8, 0.45, 0.15))
add(churn(MAXQ, "abc", 2, 6, 0.35, 0.35, 1, 3))                    # many deletions
# long words with a long common part: every prefix of a word is long
base = word("ab", 9000, 9000)
ops, bag = [], []
for i in range(100):
    if i % 10 == 9 and bag:
        ops.append(("-", bag.pop(random.randrange(len(bag)))))
    elif i % 2 == 0:
        w = base + word("ab", 1, 800)
        ops.append(("+", w))
        bag.append(w)
    else:
        w = random.choice(bag) if bag else base
        ops.append(("?", w[:random.randint(8500, len(w))] + word("ab", 0, 3)))
add(ops)
# insert, delete everything, ask the deleted words again (nodes stay, counters are 0)
ws = [word("abc", 4, 6) for _ in range(50_000)]
ops = [("+", w) for w in ws] + [("-", w) for w in ws]
others = [word("de", 3, 6) for _ in range(20_000)]
ops += [("+", w) for w in others]
for _ in range(MAXQ - len(ops)):
    ops.append(("?", random.choice(ws)[:random.randint(1, 6)] if random.random() < 0.7 else random.choice(others)))
add(ops)
# the same word again and again
ops = [("+", "zzzz")] * 100_000 + [("?", random.choice(["z", "zz", "zzz", "zzzz", "zzzzz", "zy"])) for _ in range(99_000)]
ops += [("-", "zzzz")] * 999 + [("?", "zz")]
add(ops)
# nested words a, aa, aaa, ... and long queries
ops = [("+", "a" * k) for k in range(1, 1001)]
for _ in range(750):
    r = random.random()
    k = random.randint(1, 1000)
    if r < 0.15:
        ops.append(("-", "a" * k)); ops.append(("+", "a" * k))
    else:
        ops.append(("?", "a" * random.randint(1, 1000) + ("b" if r < 0.5 else "")))
add(ops)
# medium long words over two letters
ops, bag = [], []
for i in range(320):
    r = random.random()
    if r < 0.5 or not bag:
        w = "ab" * 1000 + word("ab", 500, 1000)
        ops.append(("+", w)); bag.append(w)
    elif r < 0.6:
        ops.append(("-", bag.pop(random.randrange(len(bag)))))
    else:
        w = random.choice(bag)
        ops.append(("?", w[:random.randint(1900, len(w))]))
add(ops)
add(churn(MAXQ, "abcdefghij", 1, 5, 0.5, 0.2, 1, 2))
# very long words: a handful of words of length about 10^5
base = word("ab", 100_000, 100_000)
ops = []
for i in range(4):
    ops.append(("+", base[:random.randint(95_000, 100_000)] + word("ab", 1, 3)))
ops.append(("?", base[:99_000] + "b"))
ops.append(("-", ops[1][1]))
ops.append(("+", base[:60_000] + "a" * 30_000))
ops.append(("?", base[:97_000]))
ops.append(("?", base[:60_000] + "a" * 29_000 + "b"))
add(ops)
# about thirty words of length 30 000 that differ only near the end
ops, bag = [], []
for i in range(32):
    if i % 4 == 3:
        w = random.choice(bag)
        ops.append(("?", w[:random.randint(29_000, len(w))]))
    else:
        w = "c" * 29_990 + word("cd", 1, 10)
        ops.append(("+", w)); bag.append(w)
add(ops)

# about a hundred words of length about 10^4 with a long common start: every prefix is long (review)
base = word("ab", 9000, 9000)
ops, bag = [], []
for i in range(100):
    if i % 10 == 9:
        w = random.choice(bag)
        ops.append(("?", w[:random.randint(9000, len(w))]))
    else:
        w = base + word("ab", 950, 1000)
        ops.append(("+", w)); bag.append(w)
add(ops)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
