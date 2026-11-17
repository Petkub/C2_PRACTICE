# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(151901)
MAXL = 1_000_000
tests = []


def add(e):
    assert 1 <= len(e) <= MAXL and set(e) <= set("01!&|()")
    check(e)
    s = e + "\n"
    assert all(32 <= ord(c) <= 126 or c == "\n" for c in set(s))
    tests.append(s)


def check(e):


    depth, want_operand = 0, True
    for c in e:
        if want_operand:
            assert c in "01!(", e[:50]
            if c == "(":
                depth += 1
            elif c in "01":
                want_operand = False
        else:
            assert c in "&|)", e[:50]
            if c == ")":
                depth -= 1
                assert depth >= 0
            else:
                want_operand = True
    assert depth == 0 and not want_operand


def small(budget, depth=0):

    r = random.random()
    if budget <= 1 or depth > 12 or r < 0.2:
        return random.choice("01")
    if r < 0.32:
        return "!" + small(budget - 1, depth + 1)
    if r < 0.44:
        return "(" + small(budget - 2, depth + 1) + ")"
    k = random.randint(2, 4)
    ops = [random.choice("&|") for _ in range(k - 1)]
    parts = [small(budget // k, depth + 1) for _ in range(k)]
    out = parts[0]
    for o, p in zip(ops, parts[1:]):
        out += o + p
    return out


def flat(n, ops, digits):
    return "".join(random.choice(digits) + (random.choice(ops) if i < n - 1 else "") for i in range(n))


def deep(levels, side):

    pre, suf = [], []
    for _ in range(levels):
        r = random.random()
        if r < 0.25:
            pre.append("!")
        elif r < 0.45:
            pre.append("(")
            suf.append(")")
        elif r < 0.7:
            pre.append(side() + random.choice("&|") + "(")
            suf.append(")")
        else:
            pre.append("(")
            suf.append(")" + random.choice("&|") + side())
    return "".join(pre) + random.choice("01") + "".join(reversed(suf))


def balanced(levels, ops):

    e = "1"
    for d in range(levels):
        o = ops[d % len(ops)]
        e = "(" + e + o + e + ")"
    return e


add("1|0&0")
add("!(1&1)|0&0")
add("0")
add("!!!1")
add("(1|1)&(1|1)")
add("1|1|1")

add("1")
add("!0")
add("((((0))))")
add("0&1|1&0|!(1|0)&1")
for b in [8, 40, 60]:
    add(small(b))
add(balanced(3, "&|"))
add("!(" + flat(12, "&|", "01") + ")")

add(small(3000))
add(balanced(12, "&|"))
add(flat(20000, "&|", "01"))

add("(" * 499_999 + "1" + ")" * 499_999)
add("!" * 999_999 + "0")
add("!(" * 333_333 + "1" + ")" * 333_333)
add(flat(500_000, "|", "1"))
add(flat(500_000, "&|", "01"))
add(balanced(17, "&|"))
add(deep(60_000, lambda: small(12)))
add(deep(100_000, lambda: random.choice(["1", "0", "!1", "1&1", "0|0"])))
add(small(990_000))
parts = []
while sum(len(x) + 1 for x in parts) < 950_000:
    parts.append(small(random.randint(500, 4000)))
add("".join(x + random.choice("&|") for x in parts[:-1]) + parts[-1])
add("&".join("(" + flat(random.randint(4, 12), "|", "1") + ")" for _ in range(30_000)))
add("!(" + flat(300_000, "&|", "01") + ")&!(" + flat(150_000, "|", "0") + ")")

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
