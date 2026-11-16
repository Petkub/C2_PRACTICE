# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, re

random.seed(15011)
MAXN = 100_000
MAXQ = 50_000
MAXSIZE = 10 ** 12
MAXOUT = 2_000_000      # total length of the outline lines
MAXQLEN = 1_000_000     # total length of the query lines
NAMECH = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-"
ALLOWED = bytes(range(32, 127)) + b"\n"
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


NAME_RE = re.compile(r"[A-Za-z0-9._-]{1,20}")
PATH_RE = re.compile(r"[A-Za-z0-9._-]{1,20}(/[A-Za-z0-9._-]{1,20})*")


def ok_name(s):
    return NAME_RE.fullmatch(s) is not None


def add(outline, queries):
    """outline: list of (depth, name, size or None for a folder); queries: list of path strings"""
    n, q = len(outline), len(queries)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    lines = []
    prev_d, prev_folder = -1, True
    open_names = []          # names used inside each open folder (index = depth)
    for i, (d, name, size) in enumerate(outline):
        assert ok_name(name)
        assert d == 0 if i == 0 else 0 <= d <= prev_d + 1
        assert d <= prev_d or prev_folder or i == 0
        del open_names[d + 1:]
        if len(open_names) <= d:
            open_names.append(set())
        assert name not in open_names[d]
        open_names[d].add(name)
        if size is None:
            lines.append("  " * d + name + "/")
        else:
            assert 0 <= size <= MAXSIZE
            lines.append("  " * d + name + " " + str(size))
        prev_d, prev_folder = d, size is None
    assert sum(len(x) for x in lines) <= MAXOUT
    for p in queries:
        assert PATH_RE.fullmatch(p)
    assert sum(len(p) for p in queries) <= MAXQLEN
    t = f"{n} {q}\n" + "".join(x + "\n" for x in lines) + "".join(p + "\n" for p in queries)
    assert t.encode().translate(None, ALLOWED) == b"" and " \n" not in t
    tests.append(t)


def from_text(text):
    out = []
    for ln in text.strip("\n").split("\n"):
        sp = len(ln) - len(ln.lstrip(" "))
        body = ln[sp:]
        if body.endswith("/"):
            out.append((sp // 2, body[:-1], None))
        else:
            a, b = body.split(" ")
            out.append((sp // 2, a, int(b)))
    return out


def rname(lo=1, hi=8):
    return "".join(random.choices(NAMECH, k=ri(lo, hi)))


# ---------- trees ----------
class Tree:
    def __init__(self):
        self.parent, self.name, self.size, self.kids = [], [], [], []

    def node(self, par, folder, size=0, name=None):
        sib = self.kids[par] if par >= 0 else self.roots
        used = self.used.get(par)
        if used is None:
            used = self.used[par] = set()
        lo, hi = self.namelen
        while name is None or name in used:
            name = "".join(random.choices(NAMECH, k=lo + int(random.random() * (hi - lo + 1))))
        used.add(name)
        v = len(self.parent)
        self.depth.append(self.depth[par] + 1 if par >= 0 else 0)
        self.parent.append(par)
        self.name.append(name)
        self.size.append(None if folder else size)
        self.kids.append([])
        sib.append(v)
        return v

    def start(self, namelen=(1, 8)):
        self.roots, self.used, self.namelen, self.depth = [], {}, namelen, []
        return self

    def outline(self, shuffle=True):
        res, paths = [], {}
        name, size, parent, kids_of = self.name, self.size, self.parent, self.kids
        stack = [(v, 0) for v in reversed(self.roots)]
        while stack:
            v, d = stack.pop()
            res.append((d, name[v], size[v]))
            p = parent[v]
            paths[v] = paths[p] + "/" + name[v] if p >= 0 else name[v]
            kids = kids_of[v]
            if kids:
                if shuffle and len(kids) > 1:
                    random.shuffle(kids)
                stack.extend([(c, d + 1) for c in reversed(kids)])
        self.paths = paths
        return res


def rsize(big=False):
    c = random.random()
    if big:
        return MAXSIZE - ri(0, 1000) if c < 0.5 else ri(0, MAXSIZE)
    return 0 if c < 0.05 else ri(1, 10 ** 6) if c < 0.8 else ri(0, MAXSIZE)


def random_tree(n, folder_p=0.3, roots=3, namelen=(1, 8), big=False, deep_bias=0.0, maxdepth=6, hub=0.0):
    t = Tree().start(namelen)
    folders = []
    for i in range(n):
        if i < roots or not folders:
            par = -1
        elif hub and random.random() < hub:
            par = folders[0]                                           # one folder holding many entries
        elif deep_bias and random.random() < deep_bias:
            par = folders[-1 - min(len(folders) - 1, ri(0, 3))]
        else:
            par = folders[int(len(folders) * random.random() ** 3)]   # mostly shallow folders
        if par >= 0 and t.depth[par] >= maxdepth:
            par = folders[int(len(folders) * random.random() ** 3)]
            if t.depth[par] >= maxdepth:
                par = -1
        f = random.random() < folder_p or i < roots
        v = t.node(par, f, rsize(big))
        if f:
            folders.append(v)
    return t


def make_queries(t, q, p_folder=0.5, p_bad=0.2):
    folders = [v for v in range(len(t.parent)) if t.size[v] is None]
    files = [v for v in range(len(t.parent)) if t.size[v] is not None]
    res, used = [], 0
    while len(res) < q:
        c = random.random()
        if c < p_bad:
            v = random.randrange(len(t.parent))
            p = t.paths[v]
            k = ri(0, 5)
            if k == 0:
                p = p + "/" + rname()                        # one level too deep (maybe under a file)
            elif k == 1:
                parts = p.split("/")
                parts[-1] = parts[-1] + "x"                  # a name that does not exist (probably)
                p = "/".join(parts)
            elif k == 2:
                parts = p.split("/")
                parts[-1] = parts[-1].swapcase()             # names are case sensitive
                p = "/".join(parts)
            elif k == 3:
                p = t.name[v]                                # the bare name at the top level
            elif k == 4 and "/" in p:
                parts = p.split("/")
                parts[0] = rname()                           # wrong first folder
                p = "/".join(parts)
            else:
                p = p + "/" + t.name[v]
            if any(len(x) > 20 for x in p.split("/")):
                continue
        elif c < p_bad + p_folder * (1 - p_bad) and folders:
            p = t.paths[random.choice(folders)]
        elif files:
            p = t.paths[random.choice(files)]
        else:
            p = t.paths[random.choice(folders)]
        if used + len(p) > MAXQLEN:
            break
        used += len(p)
        res.append(p)
    return res


def build(t, q, **kw):
    out = t.outline()
    add(out, make_queries(t, q, **kw))


# samples
add(from_text("""
docs/
  a.txt 100
  img/
    cat.png 20
"""), ["docs", "docs/img", "img"])
add(from_text("""
x/
  x/
    x 7
  y 1
"""), ["x", "x/x/x", "X"])
add(from_text("""
src/
  a 1000000000000
  b 1000000000000
"""), ["src", "src/a/b"])
add(from_text("""
a/
  b/
"""), ["a", "a/b"])
add(from_text("""
f 0
"""), ["f", "f/f"])

# hidden: small (brute force checks them)
add(from_text("""
a/
  b/
c 0
"""), ["a", "a/b", "c", "Src", "src"])
add(from_text("""
bin/
  run 3
run 0
"""), ["run", "bin/run", "bin"])
add(from_text("""
docs/
  a.txt 100
  img/
    cat.png 2000
    dog.png 3000
  b.txt 5
music/
"""), ["docs", "docs/img", "docs/a.txt", "music", "img", "docs/img/cat.png/x", "docs/b.txt", "docs/music"])
add(from_text("""
x/
  x/
    x/
      x 7
  y 1
"""), ["x", "x/x", "x/x/x", "x/x/x/x", "X", "x/y", "y", "x/x/y"])
add([(0, "only", 5)], ["only", "only/x", "onl"])
add([(0, "empty", None)], ["empty"])
for n, q in ((8, 10), (30, 30), (200, 200), (1000, 500), (3000, 2000)):
    build(random_tree(n, 0.35, ri(1, 4), (1, 3), maxdepth=ri(3, 30)), q)
t = random_tree(2000, 0.5, 1, (1, 2), deep_bias=0.9, maxdepth=200)
build(t, 2000, p_folder=0.8)
t = Tree().start((1, 4))
root = t.node(-1, True, name="r")
for _ in range(3000):
    t.node(root, False, rsize())
build(t, 3000)

# hidden: large
build(random_tree(MAXN, 0.3, 1, (1, 6), hub=0.97), MAXQ)
build(random_tree(MAXN, 0.5, 1, (1, 4), big=True, hub=0.9), MAXQ, p_folder=0.8)
t = Tree().start((1, 5))                         # one folder holding everything: wide
root = t.node(-1, True, name="data")
for _ in range(MAXN - 1):
    t.node(root, random.random() < 0.01, rsize(True))
build(t, MAXQ, p_folder=0.1)
t = Tree().start((1, 5))                         # many top-level files and folders
for _ in range(MAXN):
    t.node(-1, random.random() < 0.5, rsize())
build(t, MAXQ)
t = Tree().start((1, 2))                         # a chain of 900 folders, files hanging all along it
chain = [t.node(-1, True)]
for _ in range(899):
    chain.append(t.node(chain[-1], True))
budget = sum(2 * d + 3 for d in range(900))
while budget < MAXOUT - 50_000:
    v = t.node(chain[int(400 * random.random() ** 3)], False, rsize(True))
    budget += 2 * t.depth[v] + len(t.name[v]) + 1 + len(str(t.size[v]))
build(t, 2000, p_folder=0.9)
t = Tree().start((1, 3))                         # broom: a chain of 300, then a wide fan of files
chain = [t.node(-1, True)]
for _ in range(299):
    chain.append(t.node(chain[-1], True))
while len(t.parent) < 1300:
    t.node(chain[-1], False, rsize(True))
fan = t.node(-1, True, name="fan")
while len(t.parent) < MAXN:
    t.node(fan, False, rsize())
build(t, 30_000, p_folder=0.5)
t = random_tree(60_000, 0.4, 2, (1, 3), deep_bias=0.95, maxdepth=10)
build(t, 50_000, p_folder=0.7)
build(random_tree(MAXN, 0.05, 50, (2, 6), hub=0.95), MAXQ, p_bad=0.5)
t = Tree().start((3, 4))                         # two levels: 300 folders with 300 files each
for _ in range(330):
    f = t.node(-1, True)
    for _ in range(300):
        t.node(f, False, rsize())
build(t, MAXQ, p_folder=0.3)
t = random_tree(MAXN, 0.3, 1, (1, 5), big=True, hub=0.97)
build(t, MAXQ, p_bad=0.0, p_folder=0.5)
t = Tree().start((1, 5))                         # 2000 small folders first, then many files beside them
home = t.node(-1, True, name="home")
for _ in range(2000):
    f = t.node(home, True)
    for _ in range(10):
        t.node(f, False, rsize())
while len(t.parent) < MAXN:
    t.node(home, False, rsize(True))
add(t.outline(shuffle=False), make_queries(t, MAXQ, p_folder=0.3))
t = Tree().start((1, 4))                         # a chain of 5 folders, 19999 files beside every link
chain = [t.node(-1, True)]
for _ in range(4):
    chain.append(t.node(chain[-1], True))
for v in chain:
    for _ in range(19999):
        t.node(v, False, rsize())
build(t, MAXQ, p_folder=0.6)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
