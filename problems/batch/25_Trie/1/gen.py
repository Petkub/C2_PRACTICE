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
# hidden: maximum size. Every one ends with operations on one word of length 36 000 (its prefixes are long),
# and several first store about 2.2 * 10^5 letters of distinct words (more than 2 * 10^5 trie nodes)


def tail(ops, L=36_000, alpha="ab"):
    """fill the rest of the length budget with +, -, ? of one long word W and long prefixes of it"""
    room = MAXC - sum(len(w) for _, w in ops)
    W = word(alpha, L, L)
    ops.append(("+", W))
    room -= L
    have = 1
    while room >= L + 1 and len(ops) < MAXQ:
        r = random.random()
        if r < 0.6:
            t = W[:random.randint(L - 300, L)]
            if len(t) < L and random.random() < 0.5:
                t += random.choice(alpha)
            ops.append(("?", t))
        elif r < 0.8 or have == 1:
            ops.append(("+", W)); have += 1
        else:
            ops.append(("-", W)); have -= 1
        room -= len(ops[-1][1])
    return ops


def many_nodes(chars=250_000, alpha="abcdefghijklmnopqrstuvwxyz", lo=15, hi=25, p_del=0.0):
    """distinct words of total length about chars, with short queries and some deletions"""
    ops, bag, used, seen = [], [], 0, set()
    while used < chars:
        w = word(alpha, lo, hi)
        if w in seen:
            continue
        seen.add(w)
        ops.append(("+", w)); bag.append(w); used += len(w)
        r = random.random()
        if r < 0.5:
            v = random.choice(bag)
            ops.append(("?", v[:random.randint(1, 8)] if random.random() < 0.7 else word(alpha, 1, 6)))
        elif r < 0.5 + p_del:
            i = random.randrange(len(bag))
            bag[i], bag[-1] = bag[-1], bag[i]
            ops.append(("-", bag.pop()))
    nodes = len({w[:i] for w in seen for i in range(1, len(w) + 1)})
    assert nodes > 215_000, nodes
    return ops


add(tail(churn(60_000, "ab", 1, 6, 0.6, 0.1, 1, 2)))                  # short queries matching very many words
add(tail(many_nodes()))
add(tail(churn(50_000, "abc", 2, 6, 0.35, 0.35, 1, 3)))               # many deletions
add(tail(many_nodes(p_del=0.3)))
# insert, delete everything, ask the deleted words again (nodes stay, counters are 0)
ws = [word("abc", 4, 6) for _ in range(12_000)]
ops = [("+", w) for w in ws] + [("-", w) for w in ws]
others = [word("de", 3, 6) for _ in range(5_000)]
ops += [("+", w) for w in others]
for _ in range(30_000):
    ops.append(("?", random.choice(ws)[:random.randint(1, 6)] if random.random() < 0.7 else random.choice(others)))
add(tail(ops))
# the same word again and again
ops = [("+", "zzzz")] * 20_000 + [("?", random.choice(["z", "zz", "zzz", "zzzz", "zzzzz", "zy"])) for _ in range(19_000)]
ops += [("-", "zzzz")] * 999 + [("?", "zz")]
add(tail(ops, alpha="yz"))
# nested words a, aa, aaa, ... and long queries
ops = [("+", "a" * k) for k in range(1, 401)]
for _ in range(150):
    r = random.random()
    k = random.randint(1, 400)
    if r < 0.15:
        ops.append(("-", "a" * k)); ops.append(("+", "a" * k))
    else:
        ops.append(("?", "a" * random.randint(1, 400) + ("b" if r < 0.5 else "")))
add(tail(ops, alpha="ab"))
add(tail(many_nodes(chars=270_000, alpha="abcdefghij", lo=16, hi=24)))
add(tail(many_nodes(chars=270_000, lo=10, hi=14, p_del=0.15)))
# very long words: words of length about 10^5 (two different long starts: more than 2 * 10^5 trie nodes)
base = word("ab", 100_000, 100_000)
base2 = word("cd", 100_000, 100_000)
ops = []
for i in range(4):
    b = base if i % 2 == 0 else base2
    ops.append(("+", b[:random.randint(95_000, 100_000)] + word("ab" if i % 2 == 0 else "cd", 1, 3)))
ops.append(("?", base[:99_000] + "b"))
ops.append(("-", ops[1][1]))
ops.append(("+", base[:60_000] + "a" * 30_000))
ops.append(("+", base2[:50_000] + "c" * 40_000))
ops.append(("?", base2[:97_000]))
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
# medium long words with a common start of length 2000, then the long word
ops, bag = [], []
for i in range(60):
    r = random.random()
    if r < 0.5 or not bag:
        w = "ab" * 1000 + word("ab", 500, 1000)
        ops.append(("+", w)); bag.append(w)
    elif r < 0.6:
        ops.append(("-", bag.pop(random.randrange(len(bag)))))
    else:
        w = random.choice(bag)
        ops.append(("?", w[:random.randint(1900, len(w))]))
add(tail(ops, alpha="cd"))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
