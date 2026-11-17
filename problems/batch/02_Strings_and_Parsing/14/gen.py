# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(617349)
MAXM, MAXL = 14, 100_000
LET = "abcdefghijklmn"
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def valid(s):
    need = 1
    for c in s:
        if need <= 0:
            return False
        if c in "&|^":
            need += 1
        elif c != "!":
            need -= 1
    return need == 0


def add(m, s):
    assert 1 <= m <= MAXM and 1 <= len(s) <= MAXL
    assert all(c in "&|^!" or c in LET[:m] for c in s)
    assert valid(s)
    tests.append(f"{m}\n{s}\n")


def expr(m, length, p_not=0.15, ops="&|^", lean=0.5):
    """a random expression of exactly `length` characters, written left to right.
    lean: chance to write a binary operator when it fits (high = deep on the left, low = many variables early)."""
    out, need, left = [], 1, length
    vars_ = LET[:m]
    while need > 0:                         # `need` operands are still missing, each takes >= 1 character
        if left == need:
            c = random.choice(vars_)
        elif need == 1 and left >= 3:       # the expression must not end before its length
            c = random.choice(ops) if random.random() >= p_not else "!"
        elif need == 1:
            c = "!"
        elif left >= need + 2 and random.random() < lean:
            c = random.choice(ops)
        elif random.random() < p_not:
            c = "!"
        else:
            c = random.choice(vars_)
        out.append(c)
        need += 1 if c in ops else 0 if c == "!" else -1
        left -= 1
    assert left == 0
    return "".join(out)


def chain(m, length, op):
    """op op op ... v v v v (left-deep)"""
    k = (length + 1) // 2
    return op * (k - 1) + "".join(random.choice(LET[:m]) for _ in range(k))


def right_chain(m, length, ops="&|^"):
    """op v op v op v ... v (right-deep)"""
    k = (length + 1) // 2
    out = []
    for _ in range(k - 1):
        out.append(random.choice(ops))
        out.append(random.choice(LET[:m]))
    out.append(random.choice(LET[:m]))
    return "".join(out)


def all_vars(m, s):
    """makes sure every one of the m variables appears (replaces some letters)"""
    s = list(s)
    pos = [i for i, c in enumerate(s) if c in LET]
    random.shuffle(pos)
    for v, i in zip(LET[:m], pos):
        s[i] = v
    return "".join(s)


# samples (every variable appears in every sample)
add(3, "&a|b!c")
add(2, "^a|ab")
add(1, "!a")
add(4, "|&ab&cd")
add(2, "|^ab!^ab")
add(3, "&&a!a^bc")
# hidden: small
add(1, "a")
add(5, "!!!!!c")
add(6, expr(4, 30))                       # e, f never appear
add(8, expr(5, 60))                       # f, g, h never appear
add(10, all_vars(10, expr(10, 300, ops="^")))
x = expr(7, 400)
add(7, "|" + x + "!" + x)                 # always true
add(9, "^" + x + x)                       # always false
add(12, expr(11, 2000, lean=0.6))
add(13, chain(13, 5001, "^"))
add(11, expr(4, 15000, ops="&|"))
# hidden: maximum size
L, M = MAXL, MAXM
add(M, all_vars(M, expr(M, L)))
add(M, all_vars(M, expr(M, L, ops="^", p_not=0.3)))
add(M, all_vars(M, chain(M, L - 1, "^")))
add(M, all_vars(M, chain(M, L - 1, "&")))
add(M, all_vars(M, right_chain(M, L - 1)))
add(M, all_vars(M, expr(M, L, lean=0.7)))
add(M, all_vars(M, expr(M, L, lean=0.3, p_not=0.4)))
add(M, expr(10, L))                       # only 10 of the 14 variables appear
y = expr(M, (L - 3) // 2)
add(M, "|" + y + "!" + y)
add(M, "&" + y + "!" + y)
add(M, all_vars(M, "!" * (L - 4001) + expr(M, 4001, ops="^|")))   # a long run of "!" first
add(M, all_vars(13, expr(13, L, ops="|^")))   # n never appears
add(M, all_vars(M, expr(M, L - 7, ops="&|", p_not=0.5)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
