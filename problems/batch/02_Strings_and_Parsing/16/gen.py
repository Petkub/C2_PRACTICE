# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random, re

random.seed(2016)
MAXL, MAXN, MAXA, MAXC, MAXK, MAXP = 1_000_000, 200_000, 10**9, 10**9, 1000, 1000
tests = []


TOKEN = re.compile(r"[0-9]+\*?|[x()+\-]")


def check(e):
    # grammar: E = T (op T)*, T = [k*] A, A = number | x | ( E ); numbers without leading zeros,
    # 2 <= k <= MAXK, and the product of the multipliers acting on any atom is <= MAXP
    toks = TOKEN.findall(e)
    assert sum(map(len, toks)) == len(e)
    prod = [1]                     # product of the multipliers of the open brackets
    want_term, mul = True, 1
    for t in toks:
        if want_term:
            if t == "(":
                assert prod[-1] * mul <= MAXP
                prod.append(prod[-1] * mul)
                mul = 1
            elif t == "x":
                assert prod[-1] * mul <= MAXP
                want_term, mul = False, 1
            else:
                assert t[0].isdigit(), t
                d = t.rstrip("*")
                assert d[0] != "0" or len(d) == 1
                v = int(d)
                if t[-1] == "*":
                    assert mul == 1 and 2 <= v <= MAXK      # one multiplier per term
                    mul = v
                else:
                    assert v <= MAXC and prod[-1] * mul <= MAXP
                    want_term, mul = False, 1
        else:
            assert t in "+-)", t
            if t == ")":
                prod.pop()
                assert prod
            else:
                want_term = True
    assert len(prod) == 1 and not want_term


def add(e, a):
    n = len(a)
    assert 1 <= len(e) <= MAXL and set(e) <= set("0123456789x+-()*")
    assert 1 <= n <= MAXN and e.count("x") == n
    assert all(-MAXA <= v <= MAXA for v in a)
    check(e)
    tests.append(e + "\n" + str(n) + "\n" + " ".join(map(str, a)) + "\n")


def const(big):
    return str(random.randint(0, MAXC) if big else random.randint(0, 99))


def mult(cur, p, kmax):
    # maybe a multiplier "k*" that keeps the product <= MAXP
    if random.random() < p and cur * 2 <= MAXP:
        k = random.randint(2, min(kmax, MAXP // cur))
        return k, f"{k}*"
    return 1, ""


def build(nx, nc, p_open, p_close, maxd, p_minus, p_mul=0.2, kmax=9, big=False):
    items = ["x"] * nx + ["c"] * nc
    random.shuffle(items)
    out, prod = [], [1]
    for idx, it in enumerate(items):
        if idx > 0:
            while len(prod) > 1 and random.random() < p_close:
                out.append(")")
                prod.pop()
            out.append("-" if random.random() < p_minus else "+")
        while len(prod) <= maxd and random.random() < p_open:
            k, s = mult(prod[-1], p_mul, kmax)
            out.append(s + "(")
            prod.append(prod[-1] * k)
        k, s = mult(prod[-1], p_mul, kmax)
        out.append(s + ("x" if it == "x" else const(big)))
    out.append(")" * (len(prod) - 1))
    return "".join(out)


def chain(levels, tail, muls=()):
    # x-(x-(x-( ... tail ... ))) ; the levels listed in muls get a multiplier 10 before their bracket
    m = set(muls)
    return "".join("x-10*(" if k in m else "x-(" for k in range(levels)) + tail + ")" * levels


def nest(levels, inner, minus_every=1, muls=()):
    m = set(muls)
    pre = []
    for k in range(levels):
        s = "x-" if k % minus_every == 0 else ""
        pre.append(s + ("10*(" if k in m else "("))
    return "".join(pre) + inner + ")" * levels


def vals(n, lo=-MAXA, hi=MAXA):
    return [random.randint(lo, hi) for _ in range(n)]


def slots(n, kmax=9, p=0.5):
    # n terms "x" or "k*x" joined by random operators
    return "".join(("" if i == 0 else random.choice("+-")) + (f"{random.randint(2, kmax)}*x" if random.random() < p else "x")
                   for i in range(n))


# samples
add("2*(x-x)+x", [4, -2, 7])
add("10-3*(x)-x+(3+2*x)", [1, 2, 5])
add("x", [-MAXA])
add("(((x)))-x", [3, 8])
add("1000000000-x-(x)", [999999999, -MAXA])
add("5*(3*(x-x)-x)", [-1, 2, 3])

# hidden: small, checked by trying every placement
add("2*3+4*(x-2*(x+5))-7", [10, -3])
add("x-(x+3*x-(x-3))+(9*x-x)", [-4, 9, 0, 7, -1, 2])
for t in range(5):
    nx = random.randint(1, 8)
    e = build(nx, random.randint(0, 6), 0.4, 0.35, 6, 0.6, 0.4)
    add(e, vals(nx, -20, 20) if t % 2 else vals(nx))
add(build(8, 3, 0.5, 0.2, 8, 0.8, 0.5, 1000), [MAXA] * 4 + [-MAXA] * 4)
add("0-(0-(0-(1000*x)))", [MAXA])
# hidden: medium
add(build(300, 200, 0.3, 0.3, 50, 0.6, 0.3), vals(300))
add(chain(2000, slots(3), [5, 700]), vals(2003, -1000, 1000))


# hidden: maximum size
def big(e, lo=-MAXA, hi=MAXA, fixed=None):
    n = e.count("x")
    add(e, [fixed] * n if fixed is not None else vals(n, lo, hi))


big(chain(150_000, slots(30_000), [10, 140_000]), 0, MAXA)        # deep, alternating signs
big(nest(250_000, slots(40_000), 3, [7, 99_999]))                          # depth 2.5e5, minus groups
big(build(150_000, 50_000, 0.45, 0.45, 10**6, 0.7, 0.25))                  # random, deep
big(build(150_000, 40_000, 0.3, 0.3, 40, 0.7, 0.3, 1000, True))           # shallow, big numbers and multipliers
big(slots(MAXN, 1000, 0.6), MAXA - 1000, MAXA)                             # flat, coefficient * card overflows int
big("x-7*(" + slots(160_000, 30) + ")", 0, MAXA)                           # one minus group, all flip
big(build(100_000, 30_000, 0.4, 0.4, 10**6, 0.5, 0.3, 50, True), fixed=MAXA)
big(build(120_000, 60_000, 0.6, 0.3, 10**6, 0.9, 0.2), -MAXA, -MAXA + 10**6)
big(nest(150_000, "9+" + slots(50_000, 5), 1, [3]))                        # all x at the bottom
big(build(170_000, 20_000, 0.2, 0.2, 5, 0.5, 0.5, 20), -5, 5)              # shallow, many ties
big("(" + chain(120_000, "x") + ")-3*(" + slots(60_000) + ")", -MAXA, MAXA)
big(build(140_000, 40_000, 0.5, 0.5, 10**6, 0.3, 0.3), fixed=-MAXA)
big(build(MAXN, 0, 0.35, 0.35, 10**6, 0.6, 0.3, 12), 0, MAXA)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
