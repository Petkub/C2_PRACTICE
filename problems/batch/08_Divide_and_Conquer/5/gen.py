# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, sys

random.seed(13005)
sys.setrecursionlimit(10000)
MAXN = 30
MAXL = 200_000
MAXQ = 100_000
tests = []


def check(n, code):
    """the code is one complete square of side 2^n with splits only on squares of side >= 2"""
    pos = 0

    def walk(s):
        nonlocal pos
        ch = code[pos]
        pos += 1
        if ch == "(":
            assert s >= 1
            for _ in range(4):
                walk(s - 1)
            assert code[pos] == ")"
            pos += 1
        else:
            assert ch in "BW"

    walk(n)
    assert pos == len(code)


def add(n, code, qs):
    assert 0 <= n <= MAXN and 1 <= len(code) <= MAXL and 1 <= len(qs) <= MAXQ
    check(n, code)
    assert all(1 <= r <= (1 << n) and 1 <= c <= (1 << n) for r, c in qs)
    tests.append(f"{n}\n{code}\n{len(qs)}\n" + "".join(f"{r} {c}\n" for r, c in qs))


class Node:
    __slots__ = ("kids", "col", "depth")

    def __init__(self, depth, col):
        self.kids = None
        self.col = col
        self.depth = depth


def split(v, colour):
    v.kids = [Node(v.depth + 1, colour()) for _ in range(4)]
    return v.kids


def text(root):
    out = []
    stack = [root]
    while stack:
        v = stack.pop()
        if v == ")":
            out.append(")")
        elif v.kids is None:
            out.append(v.col)
        else:
            out.append("(")
            stack.append(")")
            stack.extend(reversed(v.kids))
    return "".join(out)


def rnd_colour(pb=0.5):
    return lambda: "B" if random.random() < pb else "W"


def random_tree(n, length, pb=0.5):
    """split random leaves (depth < n) until the code has about `length` characters"""
    root = Node(0, rnd_colour(pb)())
    leaves = [root] if n > 0 else []
    size = 1
    col = rnd_colour(pb)
    while leaves and size + 5 <= length:
        i = random.randrange(len(leaves))
        v = leaves[i]
        leaves[i] = leaves[-1]
        leaves.pop()
        for k in split(v, col):
            if k.depth < n:
                leaves.append(k)
        size += 5
    return root


def comb(n, length):
    """three big random subtrees at every level, the path goes on in the last quadrant (SE) down to a cell"""
    root = Node(0, "W")
    v = root
    path = []
    for d in range(n):
        path.append(v)
        kids = split(v, rnd_colour())
        v = kids[3]
    budget = length - 5 * n - 10
    # put the extra splits in the NW/NE/SW children of the first levels
    spots = [p.kids[j] for p in path[:3] for j in range(3)]
    share = budget // len(spots)
    for s in spots:
        t = random_tree(n - s.depth, share)
        s.kids, s.col = t.kids, t.col
        fix_depth(s)
    return root


def fix_depth(v):
    stack = [v]
    while stack:
        u = stack.pop()
        if u.kids:
            for k in u.kids:
                k.depth = u.depth + 1
                stack.append(k)


def chain(n, corner_seq):
    """a single path of splits down to one cell; corner_seq(d) chooses the quadrant to go on in"""
    root = Node(0, "B")
    v = root
    for d in range(n):
        kids = split(v, rnd_colour())
        v = kids[corner_seq(d)]
    return root


def rq(n, q):
    m = 1 << n
    return [(random.randint(1, m), random.randint(1, m)) for _ in range(q)]


def far_q(n, q):
    """cells in the bottom-right part (the last quadrant at many levels)"""
    m = 1 << n
    out = []
    for _ in range(q):
        k = random.randint(0, min(n, 6))
        lo = m - (m >> k) + 1
        out.append((random.randint(lo, m), random.randint(lo, m)))
    return out


# samples
add(2, "(BW(WBBW)B)", [(1, 1), (1, 3), (3, 2), (4, 2)])
add(1, "(WBBB)", [(1, 1), (2, 1)])
add(0, "W", [(1, 1)])
add(30, "(B(WWWB)WW)", [(536870912, 536870913), (536870912, 1073741824)])
add(3, "((BBBW)WW(WBWB))", [(2, 2), (7, 5)])
# hidden: small (the brute force paints the whole map)
add(0, "B", [(1, 1), (1, 1)])
add(1, "B", rq(1, 4))
add(2, "((BBBB)(WWWW)BW)", rq(2, 16))
add(4, text(random_tree(4, 200)), rq(4, 256))
add(6, text(random_tree(6, 2000)), rq(6, 1000))
add(8, text(random_tree(8, 20000)), rq(8, 5000))
add(10, text(random_tree(10, 100000, 0.7)), rq(10, 5000))
add(10, text(chain(10, lambda d: 3)), rq(10, 3000))
add(10, text(comb(10, 50000)), far_q(10, 5000))
# hidden: large
add(MAXN, text(random_tree(MAXN, MAXL)), rq(MAXN, MAXQ))
add(MAXN, text(random_tree(MAXN, MAXL, 0.95)), far_q(MAXN, MAXQ))
add(MAXN, text(comb(MAXN, MAXL)), far_q(MAXN, MAXQ))
add(MAXN, text(comb(MAXN, MAXL)), [((1 << MAXN) - random.randint(0, 3), (1 << MAXN) - random.randint(0, 3)) for _ in range(MAXQ)])
add(MAXN, "B", rq(MAXN, MAXQ))
t = Node(0, "W"); split(t, lambda: "B")
add(MAXN, text(t), rq(MAXN, MAXQ))
add(MAXN, text(chain(MAXN, lambda d: d % 4)), rq(MAXN, MAXQ // 10))
add(MAXN, text(comb(MAXN, MAXL)), rq(MAXN, MAXQ))
add(29, text(random_tree(29, MAXL, 0.4)), far_q(29, MAXQ))
add(MAXN, text(chain(MAXN, lambda d: 3)), [((1 << MAXN) - random.randint(0, 1), (1 << MAXN) - random.randint(0, 1)) for _ in range(MAXQ)])
add(25, text(random_tree(25, MAXL, 0.3)), far_q(25, MAXQ))
add(MAXN, text(random_tree(MAXN, MAXL // 2)), rq(MAXN, MAXQ))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
