# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(15014)
MAXN = 100_000
MAXS = 5 * 10 ** 7
MAXV = 10 ** 18
MAXPRINT = 200_000
KEYWORDS = {"set", "add", "sub", "mul", "jnz", "print", "halt"}
ALLOWED = bytes(range(32, 127)) + b"\n"
LOWER = "abcdefghijklmnopqrstuvwxyz"
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def is_name(s):
    return 1 <= len(s) <= 10 and all(c in LOWER for c in s)


def is_lit(s):
    d = s[1:] if s.startswith("-") else s
    return d.isdigit() and (d == "0" or d[0] != "0") and s != "-0" and abs(int(s)) <= MAXV


def parse(lines):
    """validate the format; return (instructions, labels) like the statement defines them"""
    prog, labels, regs = [], {}, set()
    for ln in lines:
        assert len(ln) <= 100 and not ln.endswith(" ")
        code = ln.split(";")[0]
        tok = code.split()
        if not tok:
            continue
        if tok[0].endswith(":"):
            assert len(tok) == 1 and is_name(tok[0][:-1]) and tok[0][:-1] not in KEYWORDS
            assert tok[0][:-1] not in labels
            labels[tok[0][:-1]] = len(prog)
            continue
        op = tok[0]
        assert op in KEYWORDS
        if op == "halt":
            assert len(tok) == 1
        elif op == "print":
            assert len(tok) == 2 and (is_lit(tok[1]) or is_name(tok[1]))
        elif op == "jnz":
            assert len(tok) == 3 and (is_lit(tok[1]) or is_name(tok[1])) and is_name(tok[2])
        else:
            assert len(tok) == 3 and is_name(tok[1]) and (is_lit(tok[2]) or is_name(tok[2]))
        for x in (tok[1:2] if op == "jnz" else tok[1:]):
            if is_name(x):
                assert x not in KEYWORDS
                regs.add(x)
        prog.append(tok)
    for tok in prog:
        if tok[0] == "jnz":
            assert tok[2] in labels
    assert not (regs & set(labels))
    return prog, labels


def simulate(prog, labels, S):
    """Python run (small tests only): checks the value range and the number of prints"""
    reg = {}
    val = lambda x: int(x) if is_lit(x) else reg.get(x, 0)
    pc = steps = prints = 0
    while pc < len(prog) and steps < S:
        steps += 1
        w = prog[pc]
        pc += 1
        if w[0] == "halt":
            break
        if w[0] == "print":
            prints += 1
        elif w[0] == "jnz":
            if val(w[1]) != 0:
                pc = labels[w[2]]
        else:
            v = val(w[2])
            a = reg.get(w[1], 0)
            a = v if w[0] == "set" else a + v if w[0] == "add" else a - v if w[0] == "sub" else a * v
            if abs(a) > MAXV:
                return False
            reg[w[1]] = a
    return prints <= MAXPRINT


def add(lines, S, sim=True):
    assert 1 <= len(lines) <= MAXN and 1 <= S <= MAXS
    prog, labels = parse(lines)
    if sim:
        assert simulate(prog, labels, S)
    t = f"{len(lines)} {S}\n" + "".join(ln + "\n" for ln in lines)
    assert t.encode().translate(None, ALLOWED) == b"" and len(t) <= 3_000_000
    tests.append(t)


def sample(text, S):
    add(text.strip("\n").split("\n"), S)


# samples
sample("""
set n 5   ; n = 5
loop:
  add s n
  sub n 1
  jnz n loop
print s
""", 100)
sample("""
start:
  add x 1
  print x
  jnz 1 start
""", 7)
sample("""
set a -1000000000
mul a 1000000000
print a
sub b a
print b
""", 5)
sample("""
set k 3
again:  ; k = k - 1
  sub k 1
  jnz k again
halt
print k
""", 1000)
sample("""
   halt   ; stop
""", 1)


# ---------- helpers for random formatting ----------
def comment():
    s = "".join(chr(ri(33, 126)) for _ in range(ri(0, 15)))
    return ";" + (" " + s if s and random.random() < 0.5 else s)


def fmt(tok, cmt=0.2, indent=4, gaps=3):
    sep = lambda: " " * ri(1, gaps)
    line = " " * ri(0, indent) + tok[0]
    for x in tok[1:]:
        line += sep() + x
    if random.random() < cmt:
        line += " " * ri(0, 2) + comment()
    return line


def noise(lines, p):
    out = []
    for ln in lines:
        if random.random() < p:
            out.append(random.choice(["", " " * ri(0, 3) + comment()]))
        out.append(ln)
    return out


def rand_name(k=None):
    return "".join(random.choice(LOWER) for _ in range(k or ri(1, 10)))


def fresh_names(cnt, forbid, k=None):
    res, seen = [], set(forbid) | KEYWORDS
    while len(res) < cnt:
        x = rand_name(k)
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


def random_program(m, nreg, nlab, S, tries=200):
    """random small program; retried until it stays in range"""
    for _ in range(tries):
        regs = fresh_names(nreg, [])
        labs = fresh_names(nlab, regs)
        body = []
        for _ in range(m):
            c = random.random()
            r = random.choice(regs)
            x = random.choice(regs) if random.random() < 0.4 else str(ri(-20, 20))
            if c < 0.18:
                body.append(["set", r, x])
            elif c < 0.38:
                body.append(["add", r, x])
            elif c < 0.55:
                body.append(["sub", r, x])
            elif c < 0.62:
                body.append(["mul", r, random.choice(regs + ["2", "-1", "0", "3"])])
            elif c < 0.80:
                body.append(["jnz", random.choice(regs + ["1", "0"]), random.choice(labs)])
            elif c < 0.95:
                body.append(["print", random.choice(regs + ["-5", "0"])])
            else:
                body.append(["halt"])
        pos = sorted(random.sample(range(m + 1), nlab))
        lines = []
        for i in range(m + 1):
            while pos and pos[0] == i:
                lab = labs[len(labs) - len(pos)]
                lines.append(" " * ri(0, 2) + lab + ":" + (" " + comment() if random.random() < 0.3 else ""))
                pos.pop(0)
            if i < m:
                lines.append(fmt(body[i]))
        lines = noise(lines, 0.1)
        prog, labels = parse(lines)
        if simulate(prog, labels, S):
            return lines
    raise RuntimeError("no program")


# hidden: small (checked by brute force and by the Python run above)
sample("""
set f 1
set k 5

again:  ; f = f * k
  mul f k
  sub k 1
  jnz k again
print f
halt
print 999
""", 1000)
add([";;; only comments", "", "   ; still nothing"], 5)
add(["print 3", "halt"], 1)                     # the limit comes before halt
add(["x:", "jnz 1 x"], 10)
add(["set a 5", "sub b a", "jnz b end", "print b", "end:"], 10)                     # a jump to a label with nothing after it ends the run
add(["a:", "jnz 0 a", "  print -1000000000000000000", "print 1000000000000000000"], 3)
for m, nreg, nlab, S in [(10, 2, 2, 50), (30, 3, 4, 300), (60, 5, 6, 2000), (200, 8, 15, 20000),
                         (500, 20, 40, 50000), (2000, 50, 100, 100000)]:
    add(random_program(m, nreg, nlab, S), S)


# ---------- big programs (values bounded by construction, not simulated) ----------
def countdown(n, S, extra_regs=0):
    regs = fresh_names(extra_regs, ["n", "s", "loop"], 10)
    lines = ["set " + r + " " + str(ri(-9, 9)) for r in regs]
    lines += ["set n " + str(n), "loop:   ; main loop", "    add s n", "    sub n 1", "    jnz n loop", "print s"]
    return lines


# B1: exact boundary: steps = extra + 1 + 3n + 1 (print) -> past the end => HALT when S equals it
n = 16_660_000
state = random.getstate()  # the extra registers here must not shift the random tests below
add(countdown(n, 0, 2000), 2000 + 1 + 3 * n + 1, sim=False)
add(countdown(n, 0, 2000), 2000 + 3 * n + 1, sim=False)          # one step short: LIMIT before the print
random.setstate(state)
add(countdown(n, 0, 2000), MAXS, sim=False)


def hot_many_regs(nregs, body_len, S, prefix):
    # many long, similar register names; a hot loop over a long body; never stops by itself
    regs = [prefix + rand_name(10 - len(prefix)) for _ in range(nregs)]
    regs = sorted(set(regs) - KEYWORDS)
    lines = [fmt(["set", r, str(ri(-1000, 1000))], 0.1) for r in regs]
    lines.append("top:")
    pattern = [random.random() for _ in range(6)]  # op kinds repeat with period 6
    for i in range(body_len):
        r = random.choice(regs)
        c = pattern[i % 6]
        if c < 0.3:
            lines.append(fmt(["add", r, str(ri(-10 ** 6, 10 ** 6))], 0.05))
        elif c < 0.5:
            lines.append(fmt(["sub", r, str(ri(-10 ** 6, 10 ** 6))], 0.05))
        elif c < 0.7:
            lines.append(fmt(["set", r, random.choice(regs)], 0.05))
        elif c < 0.8:
            lines.append(fmt(["mul", r, random.choice(["-1", "1", "0"])], 0.05))
        else:
            lines.append(fmt(["set", r, str(ri(-10 ** 9, 10 ** 9))], 0.05))
    lines.append("jnz 1 top")
    return lines


add(hot_many_regs(3000, 40, MAXS, "reg"), MAXS, sim=False)
add(hot_many_regs(20000, 1000, MAXS, "qqqqqq"), MAXS, sim=False)
add(hot_many_regs(1000, 90000, MAXS, ""), 2 * 10 ** 7, sim=False)


def printer(cnt, S):
    # prints cnt values then halts
    return ["set i " + str(cnt), "set v -1000000", "again:", " add v 7", " print v", " sub i 1", " jnz i again", "halt"]


add(printer(MAXPRINT - 1, MAXS), MAXS, sim=False)


def jump_chain(k, S):
    # labels l0..lk: each block jumps forward over a dead print, the last jumps back to l0
    labs = fresh_names(k + 1, ["c", "z"], 8)
    lines = []
    for i in range(k):
        lines += [labs[i] + ":", "  add c 1", "  jnz c " + labs[i + 1], "  print 1"]
    lines += [labs[k] + ":", "  sub z 1", "  jnz z " + labs[0]]
    return lines


add(jump_chain(20000, MAXS), MAXS, sim=False)


def nested(a, b):
    # two nested countdown loops; total about a * (3b + 5) steps, halts with prints of the outer counter
    return ["set outer " + str(a), "o:", " set inner " + str(b), " i:", "   add total inner", "   sub inner 1",
            "   jnz inner i", " print outer", " sub outer 1", " jnz outer o", "print total", "halt"]


add(nested(1500, 11000), MAXS, sim=False)
add(nested(1, 16_500_000), MAXS, sim=False)


def padded(lines, total):
    # the same hot program hidden in a long file of comments, empty lines and dead code after a halt
    pad = []
    while len(lines) + len(pad) < total - 1:
        c = random.random()
        if c < 0.3:
            pad.append("")
        elif c < 0.6:
            pad.append(" " * ri(0, 6) + comment())
        else:
            pad.append(fmt(["add", "dead", str(ri(-99, 99))], 0.5, 8, 4))
    return lines + ["halt"] + pad


state = random.getstate()
t = padded(countdown(15_000_000, 0, 1000), MAXN)
random.setstate(state)
padded(countdown(15_000_000, 0), MAXN)  # advance the generator as before, so the tests below stay the same
add(t, MAXS, sim=False)
add(padded(hot_many_regs(500, 30, MAXS, "x"), MAXN), MAXS, sim=False)
add(noise(hot_many_regs(2000, 30000, MAXS, "abcd"), 0.3), MAXS, sim=False)

for t in tests:
    assert t.endswith("\n") and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
