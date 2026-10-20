# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random, re, sys

random.seed(131301)
sys.setrecursionlimit(20000)
MAXLEN = 500000
MAXDEPTH = 1000
MAXNUM = 10**9
MAXEXP = 10**18
tests = []


TOKEN = re.compile(r"[0-9]+|[-+*^()]")


def check(s):
    """the expression follows the grammar of the statement, return its nesting depth"""
    assert 1 <= len(s) <= MAXLEN and set(s) <= set("0123456789+-*^()")
    toks = TOKEN.findall(s)
    assert sum(map(len, toks)) == len(s)
    depth = best = 0
    want_operand = True         # True: a number or "(" must come next
    can_pow = False             # the last thing is a number or ")" without an exponent yet
    i = 0
    while i < len(toks):
        t = toks[i]
        if want_operand:
            if t == "(":
                depth += 1
                best = max(best, depth)
            else:
                assert t[0].isdigit() and (t[0] != "0" or len(t) == 1) and int(t) <= MAXNUM, t
                want_operand, can_pow = False, True
        elif t == ")":
            depth -= 1
            assert depth >= 0
            can_pow = True
        elif t == "^":
            assert can_pow and i + 1 < len(toks)
            e = toks[i + 1]
            assert e[0].isdigit() and (e[0] != "0" or len(e) == 1) and int(e) <= MAXEXP, e
            i += 1
            can_pow = False
        else:
            assert t in "+-*"
            want_operand, can_pow = True, False
        i += 1
    assert not want_operand and depth == 0
    return best


def add(s):
    assert check(s) <= MAXDEPTH
    tests.append(s + "\n")


class Gen:
    def __init__(self, maxd, p_paren, p_pow, exp_hi, num_hi=MAXNUM, ops="++--**", wrap=0.0):
        self.maxd, self.pp, self.ppow, self.exp_hi, self.num_hi, self.ops = maxd, p_paren, p_pow, exp_hi, num_hi, ops
        self.wrap = wrap

    def num(self):
        r = random.random()
        if r < 0.1:
            return str(random.choice((0, 1, self.num_hi)))
        if r < 0.5:
            return str(random.randint(0, 9))
        return str(random.randint(0, self.num_hi))

    def exp(self):
        r = random.random()
        if r < 0.15:
            return str(random.choice((0, 1, self.exp_hi)))
        return str(random.randint(0, self.exp_hi))

    def factor(self, b, d):
        if b >= 5 and d < self.maxd and random.random() < self.pp:
            s = "(" + self.expr(b - 2, d + 1) + ")"
        else:
            s = self.num()
        extra = 0
        while d + extra < self.maxd and random.random() < self.wrap:   # redundant brackets
            s = "(" + s + ")"
            extra += 1
        if random.random() < self.ppow:
            s += "^" + self.exp()
        return s

    def expr(self, b, d=0):
        if b <= 8 or (b <= 30 and random.random() < 0.1):
            return self.factor(b, d)
        k = random.randint(2, min(6, b // 4))
        cuts = sorted(random.sample(range(1, b), k - 1))
        sizes = [y - x for x, y in zip([0] + cuts, cuts + [b])]
        out = [self.factor(sizes[0], d) if sizes[0] < 8 else self.expr(sizes[0], d)]
        for sz in sizes[1:]:
            out.append(random.choice(self.ops))
            out.append(self.factor(sz, d) if sz < 8 else self.expr(sz, d))
        return "".join(out)


def chains(total, depth, g, side=1.0):
    """several towers of `depth` nested parentheses joined by operators
    (each level has an operand before / after its brackets with probability side)"""
    parts = []
    length = 0
    while length < total:
        left, right = [], []
        for _ in range(depth):
            left.append(g.num() + random.choice(g.ops) + "(" if random.random() < side else "(")
            r = ")"
            if random.random() < g.ppow:
                r += "^" + g.exp()
            if random.random() < 0.5 * side:
                r += random.choice(g.ops) + g.num()
            right.append(r)
        s = "".join(left) + g.expr(20, g.maxd) + "".join(reversed(right))
        parts.append(s)
        length += len(s) + 1
    while length > total and len(parts) > 1:
        length -= len(parts.pop()) + 1
    return "+".join(parts)


def fit(s):
    assert len(s) <= MAXLEN, len(s)
    return s


def sized(g, target):
    """an expression from generator g whose length is close to (and at most) target"""
    b = target
    while True:
        s = g.expr(b)
        if 0.8 * target <= len(s) <= target:
            return s
        if len(s) < 0.8 * target:
            b = int(b * target * 0.9 / max(len(s), 1)) + 1
            continue
        b = int(b * target * 0.97 / len(s))


# samples
add("2+3*4^2-(5-7)*3")
add("(1-2)^3")
add("0^0*5+0^3")
add("10-4-3+2*3*4-1^5")
add("2^1000000000000000000")
add("((((1000000000))))*1000000000")
# hidden: small (the brute force checks these; exponents stay small)
add("7")
add("1000000000^2")
add("0-1000000000*1000000000")
add(sized(Gen(5, 0.3, 0.2, 30), 60))
add(sized(Gen(20, 0.4, 0.2, 50), 3000))
add(sized(Gen(3, 0.2, 0.5, 200), 5000))
add(sized(Gen(60, 0.5, 0.1, 10, ops="-"), 8000))
add(fit(chains(15000, MAXDEPTH, Gen(5, 0.3, 0.2, 20))))
add("(" * MAXDEPTH + "2" + ")^2" * MAXDEPTH)
add(sized(Gen(1000, 0.6, 0.15, 40), 20000))
# hidden: large
add(sized(Gen(40, 0.35, 0.3, MAXEXP, wrap=0.85), 475000))
add(sized(Gen(400, 0.45, 0.3, MAXEXP, wrap=0.9), 475000))
add(sized(Gen(8, 0.25, 0.6, MAXEXP, wrap=0.8), 475000))
add(fit(chains(485000, MAXDEPTH, Gen(5, 0.3, 0.1, MAXEXP), side=0.1)))
add(fit(chains(485000, 700, Gen(5, 0.3, 0.15, MAXEXP, ops="-*"), side=0.2)))
add(fit("+".join("(" + str(random.randint(0, 9)) + ")" for _ in range(122000))))           # many short brackets
add(fit("*".join("((" + str(random.randint(1, 9)) + ")-(" + str(random.randint(0, 9)) + "))^" + str(random.randint(1, 9))
                 for _ in range(35000))))
add(fit("*".join(str(random.randint(2, MAXNUM)) + "^" + str(random.randint(MAXEXP // 2, MAXEXP)) for _ in range(16500))))
add(fit("+".join(f"{MAXNUM}*{MAXNUM}" for _ in range(22500))))
add(fit("-".join(str(MAXNUM) for _ in range(45000))))
add(fit("(" * (MAXDEPTH - 1) + "+".join(["(1000000000-999999999)^999999999999999999"] * 11500) + ")" * (MAXDEPTH - 1)))
add(sized(Gen(1000, 0.7, 0.25, MAXEXP, num_hi=9, wrap=0.75), 485000))
add(fit("-".join("(" * 999 + str(random.randint(0, 9)) + ")" * 999 for _ in range(250))))   # tall towers
add(fit("(" * 999 + ")^1000000000000000000*(".join(["0^0+1"] * 15000) + ")" * 999))

for t in tests:
    assert t.endswith("\n") and " " not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
