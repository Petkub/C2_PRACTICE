# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, re, string

random.seed(150404)
MAXN = MAXQ = 10 ** 5
MAXLINE = 100
NAME_CH = string.ascii_letters + string.digits + "_-"
VAL_CH = [chr(c) for c in range(33, 127)]
VAL_CH_SP = VAL_CH + [" "] * 16
tests = []


def pick(lst):
    return lst[int(random.random() * len(lst))]


def rint(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


NAME_RE = re.compile(r"[A-Za-z0-9_-]{1,20}")


def is_name(s):
    return NAME_RE.fullmatch(s) is not None


def check_file(lines):
    for l in lines:
        assert len(l) <= MAXLINE and not l.endswith(" ")
        s = l.lstrip(" ")
        if s == "" or s[0] in ";#":
            continue
        if s[0] == "[":
            assert s[-1] == "]" and is_name(s[1:-1])
            continue
        assert "=" in s
        assert is_name(s[:s.index("=")].strip(" "))


def add(lines, queries):
    assert 1 <= len(lines) <= MAXN and 1 <= len(queries) <= MAXQ
    check_file(lines)
    for q in queries:
        assert "." in q
        sec, key = q.split(".", 1)
        assert (sec == "" or is_name(sec)) and is_name(key)
    t = f"{len(lines)}\n" + "".join(l + "\n" for l in lines) + f"{len(queries)}\n" + "".join(q + "\n" for q in queries)
    assert not t.encode().translate(None, bytes(range(32, 127)) + b"\n")
    tests.append(t)


def rname(lo=1, hi=8):
    return "".join(random.choices(NAME_CH, k=rint(lo, hi)))


CASES = {}


def rcase(s):
    # one of a few fixed random-case spellings of s (cached: keeps the generator fast)
    if s not in CASES:
        CASES[s] = [s.lower(), s.upper(), s] + ["".join(c.upper() if random.random() < 0.5 else c.lower() for c in s)
                                              for _ in range(3)]
    return pick(CASES[s])


VALUES = {}


def rvalue(hi=12):
    # drawn from a fixed pool of random values for each maximum length (keeps the generator fast)
    if hi not in VALUES:
        VALUES[hi] = [make_value(hi) for _ in range(3000)]
    return pick(VALUES[hi])


def make_value(hi):
    k = rint(0, hi)
    if k == 0:
        return ""
    v = "".join(random.choices(VAL_CH_SP, k=k))
    return v.strip(" ") or "x"


def sp(hi=2):
    return " " * rint(0, hi)


def keyline(key, val, lead=2, around=2):
    after = sp(around) if val else ""
    return sp(lead) + key + sp(around) + "=" + after + val


class Config:
    """builds a random file and remembers every (section, key) written, to make queries"""
    def __init__(self, sec_pool, key_pool, p_header=0.05, p_comment=0.05, p_empty=0.03, vhi=12, lead=2, around=2):
        self.secs = [rname() for _ in range(sec_pool)]
        self.keys = [rname() for _ in range(key_pool)]
        self.p = (p_header, p_comment, p_empty)
        self.vhi, self.lead, self.around = vhi, lead, around
        self.written = []

    def lines(self, n):
        out, cur = [], ""
        ph, pc, pe = self.p
        for _ in range(n):
            r = random.random()
            if r < ph:
                cur = pick(self.secs)
                out.append(sp(self.lead) + "[" + rcase(cur) + "]")
            elif r < ph + pc:
                c = pick(";#") + rvalue(15)
                if random.random() < 0.3:
                    c = pick(";#") + sp(1) + pick(self.keys) + " = " + rvalue(5)
                out.append(sp(self.lead) + c.rstrip(" "))
            elif r < ph + pc + pe:
                out.append("")
            else:
                k = pick(self.keys)
                self.written.append((cur, k))
                out.append(keyline(rcase(k), rvalue(self.vhi), self.lead, self.around))
        return out

    def queries(self, q, p_hit=0.5, p_sec_only=0.25):
        out = []
        for _ in range(q):
            r = random.random()
            if r < p_hit and self.written:
                s, k = pick(self.written)
                s, k = rcase(s), rcase(k)
            elif r < p_hit + p_sec_only:
                s = rcase(pick(self.secs)) if random.random() < 0.9 else ""
                k = rcase(pick(self.keys)) if random.random() < 0.9 else rname()
            else:
                s, k = pick([rname(), ""]), rname()
            out.append(s + "." + k)
        return out


# samples
add(["name = Pet Shop", "[Owner]", "  Name=Somchai", "[OWNER]", "name = Somsri"], [".NAME", "owner.name"])
add(["[db]", "user=", "#user = root", "", "  pass =  a;b #c"], ["db.user", "db.pass"])
add(["[s]", "x=1", "X = 2"], ["S.x"])
add(["[a-b_c]", "k_1 = [x] = y"], ["A-B_C.K_1"])
add(["  ;a=1"], [".a"])
# hidden: small (brute checks these)
add([""], [".x", "x.x"])
add(["[only]"], ["only.only", ".only"])
add(["  k=  v  w", "K =", "[K]", "k   =k=k"], [".k", "k.k", "K.K", ".K"])
c = Config(3, 5); add(c.lines(30), c.queries(30))
c = Config(10, 20, 0.2, 0.2, 0.1); add(c.lines(300), c.queries(300))
c = Config(1, 50, 0.0); add(c.lines(1000), c.queries(1000, 0.7))
c = Config(50, 3, 0.3, vhi=40, lead=6, around=5); add(c.lines(2000), c.queries(2000))
c = Config(200, 200, 0.1, 0.1, 0.1); add(c.lines(5000), c.queries(5000))
# hidden: large
N, Q = MAXN, MAXQ
c = Config(10, 5000, 0.001); add(c.lines(N), c.queries(Q, 0.5, 0.3))               # few sections, many keys
c = Config(20000, 30, 0.3); add(c.lines(N), c.queries(Q, 0.4, 0.4))                # many sections
c = Config(1, 20000, 0.0, 0.02, 0.02); add(c.lines(N), c.queries(Q, 0.5, 0.5))     # unnamed section only
c = Config(500, 500, 0.05, 0.1, 0.05); add(c.lines(N), c.queries(Q, 0.0, 0.3))     # almost every query misses
c = Config(100, 100, 0.02, 0.3, 0.2, vhi=30, lead=8, around=6); add(c.lines(N), c.queries(Q, 0.6, 0.2))
c = Config(3, 3, 0.01, 0.0, 0.0, vhi=4); add(c.lines(60000), c.queries(60000, 0.9, 0.1))  # one key rewritten often
c = Config(1000, 1000); add(c.lines(N), c.queries(Q, 0.5, 0.2))
c = Config(50, 2000, 0.02); ls = c.lines(N)
first = c.written[:2000]
add(ls, [rcase(s) + "." + rcase(k) for s, k in random.choices(first, k=Q // 2)] + c.queries(Q - Q // 2, 0.0, 0.5))
c = Config(5000, 5000, 0.1, vhi=60, lead=1, around=1); add(c.lines(N // 2), c.queries(Q, 0.5, 0.3))
c = Config(20, 3000, 0.01, 0.01, 0.01, vhi=8); add(c.lines(N // 2), c.queries(Q, 0.3, 0.6))   # many distinct keys, many misses
c = Config(2000, 20, 0.02, 0.01, 0.01, vhi=8); add(c.lines(N // 2), c.queries(Q, 0.3, 0.6))

for t in tests:
    assert t.endswith("\n") and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
