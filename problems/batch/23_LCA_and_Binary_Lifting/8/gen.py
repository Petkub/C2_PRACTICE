import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    """par[i] (< i) for the nodes 2..n of a tree of the given shape, before relabelling"""
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":                        # depth about n / 2, a few short branches
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "caterpillar":                 # a spine of n / 2 nodes with legs
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":                       # a long handle ending in a star
            p = i - 1 if i <= half else half
        elif kind == "twopaths":                    # two long chains meeting at node 1
            p = 1 if i <= 3 else i - 2
        elif kind == "chains":                      # chains of length about sqrt(n) glued at random
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def shuffle(a):
    """Fisher-Yates with random.random (faster than random.shuffle, same on every Python 3 version)"""
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def relabel(par, root_first=False):
    """random labels (node 1 of the shape keeps label 1 if root_first), shuffled edges and ends;
    lab[i - 1] is the label of shape node i"""
    n = len(par) - 1
    assert all(1 <= par[i] < i for i in range(2, n + 1))       # so the edges below always form a tree
    lab = list(range(1, n + 1))
    shuffle(lab)
    if root_first:
        j = lab.index(1)
        lab[0], lab[j] = lab[j], lab[0]
    rnd = random.random
    edges = [(lab[i - 1], lab[par[i] - 1]) if rnd() < 0.5 else (lab[par[i] - 1], lab[i - 1]) for i in range(2, n + 1)]
    shuffle(edges)
    return edges, lab


def random_ancestors(par, stay):
    """for every shape node i a random proper ancestor (i itself for the root): with probability stay the
    choice of the parent is inherited, so the jump is about 1 / (1 - stay) levels on average (O(n) total)"""
    n = len(par) - 1
    far = list(range(n + 1))
    rnd = random.random
    for i in range(2, n + 1):
        far[i] = far[par[i]] if par[i] != 1 and rnd() < stay else par[i]
    return far


def check_tree(n, edges):
    """the N - 1 edges connect all N nodes (union-find)"""
    assert len(edges) == n - 1
    root = list(range(n + 1))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for e in edges:
        u, v = e[0], e[1]
        assert 1 <= u <= n and 1 <= v <= n and u != v
        a, b = find(u), find(v)
        assert a != b
        root[a] = b


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)

random.seed(230107)
MAXN, MAXQ, MAXK = 100_000, 100_000, 200_000


def add(n, edges, qs, tree_ok=False):
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    assert sum(len(s) for s in qs) <= MAXK
    for s in qs:
        assert 1 <= len(s) <= n and len(set(s)) == len(s) and 1 <= min(s) and max(s) <= n
    tests.append(f"{n} {len(qs)}\n" + "".join(f"{a} {b}\n" for a, b in edges)
                 + "".join(f"{len(s)} " + " ".join(map(str, s)) + "\n" for s in qs))


def sample(pop, k):
    """k distinct items of pop (partial Fisher-Yates on a copy, only random.random)"""
    a = list(pop)
    rnd = random.random
    n = len(a)
    for i in range(k):
        j = i + int(rnd() * (n - i))
        a[i], a[j] = a[j], a[i]
    return a[:k]


class Tree:
    def __init__(self, n, kind):
        self.n = n
        self.par = shape(n, kind)
        self.edges, self.lab = relabel(self.par)
        self._kids, self.mark, self.stamp = None, None, 0

    @property
    def kids(self):
        """children lists in shape numbering (built on first use: cater() never needs them)"""
        if self._kids is None:
            self._kids = [[] for _ in range(self.n + 1)]
            for i in range(2, self.n + 1):
                self._kids[self.par[i]].append(i)
            self.mark = [0] * (self.n + 1)
        return self._kids

    def down(self, x, m):
        """a random walk of up to m steps down from x (x not included)"""
        out, rnd, kids = [], random.random, self.kids
        for _ in range(m):
            ch = kids[x]
            if not ch:
                break
            x = ch[int(rnd() * len(ch))]
            out.append(x)
        return out

    def pool(self, length):
        """the nodes of a random path of about `length` nodes (shape numbering)"""
        rnd, kids, par = random.random, self.kids, self.par
        z = 1 + int(rnd() * self.n)
        ch = kids[z]
        if len(ch) >= 2 and rnd() < 0.7:
            i = int(rnd() * len(ch))
            j = (i + 1 + int(rnd() * (len(ch) - 1))) % len(ch)
            p = [z, ch[i], ch[j]] + self.down(ch[i], length // 2) + self.down(ch[j], length // 2)
        else:
            p = [z] + self.down(z, length // 2)
            y = z
            for _ in range(length // 2):     # and up from z
                if y == 1:
                    break
                y = par[y]
                p.append(y)
        return p, z

    def query(self, k, length, bad):
        """k nodes from one path (YES), and if bad: one of them replaced by a node next to the path"""
        rnd = random.random
        p, z = self.pool(max(length, k))
        k = min(k, len(p))
        s = sample(p, k)
        if bad:
            self.stamp += 1
            kids = self.kids                 # builds kids and mark on first use
            mark, st = self.mark, self.stamp
            for x in p:
                mark[x] = st
            cand = [c for y in [z] + s[:3] for c in kids[y][:4] if mark[c] != st]
            if self.par[z] and mark[self.par[z]] != st:
                cand.append(self.par[z])
            s[int(rnd() * k)] = cand[int(rnd() * len(cand))] if cand else 1 + int(rnd() * self.n)
            s = list(dict.fromkeys(s))
        return [self.lab[x - 1] for x in s]


def make(n, kind, sizes, length=None, pbad=0.5):
    t = Tree(n, kind)
    rnd = random.random
    qs = []
    for k in sizes:
        if rnd() < 0.08:                     # any k points
            s = sample(range(1, n + 1), min(k, n)) if k > 50 else list(dict.fromkeys(1 + int(rnd() * n) for _ in range(k)))
        else:
            s = t.query(k, length or 2 * k, rnd() < pbad)
        qs.append(s)
    add(n, t.edges, qs, True)


def cater(n, sizes):
    """caterpillar: spine 1..h (a path) and legs; each list = spine points spread over the whole spine plus
    one or two legs, at the ends of the chosen spine part (YES) or inside it (NO): long paths, few points"""
    t = Tree(n, "caterpillar")
    h = n // 2
    rnd = random.random
    leg = [0] * (h + 1)
    for c in range(h + 1, n + 1):
        leg[t.par[c]] = c
    with_leg = [p for p in range(1, h + 1) if leg[p]]
    lab1 = [0] + t.lab                       # lab1[x] = label of shape node x
    qs = []
    for k in sizes:
        p = with_leg[int(rnd() * len(with_leg))]
        r = rnd()
        if r < 0.4:                          # leg at the low end: spine points above p
            sp = [p + 1 + int(rnd() * (h - p)) for _ in range(k - 1)] if p < h else [p]
        elif r < 0.7:                        # spine points on both sides of p
            sp = [1 + int(rnd() * h) for _ in range(k - 1)]
            if p > 1 and p < h:
                sp[0], sp[-1] = 1 + int(rnd() * (p - 1)), p + 1 + int(rnd() * (h - p))
        else:                                # two legs at the two ends
            q2 = with_leg[int(rnd() * len(with_leg))]
            lo, hi = min(p, q2), max(p, q2)
            sp = [lo + int(rnd() * (hi - lo + 1)) for _ in range(k - 2)] + [leg[q2]]
        s = list(dict.fromkeys([leg[p]] + sp))
        qs.append([lab1[x] for x in s])
    add(n, t.edges, qs, True)


def deeplong(n, q, kind="deep", kmax=3):
    """deep tree (depth about n / 2) or caterpillar; every list = k (3..kmax) nodes along one long path (the root
    path of shape node n, or the caterpillar's spine), spread over the whole path, so the ends are thousands of
    nodes apart: the lowest = a path node or a leaf hanging on it, the highest = a leaf hanging on a higher path
    node, the others = path nodes between them (YES), or one of them replaced by a leaf hanging on it (NO)"""
    t = Tree(n, kind)
    par, kids = t.par, t.kids
    chain = [n if kind == "deep" else n // 2]       # from the bottom
    while chain[-1] != 1:
        chain.append(par[chain[-1]])
    on = set(chain)
    leaf = [0] * (n + 1)                     # a leaf child that is not on the path
    for i in range(2, n + 1):
        if not kids[i] and i not in on:
            leaf[par[i]] = i
    good = [y for y in chain if leaf[y]]
    rnd = random.random
    qs, total, g = [], 0, len(good)
    while len(qs) < q:
        k = 3 + int(rnd() * (kmax - 2))
        idx = [int(rnd() * g) for _ in range(k)]
        idx.sort()
        if any(idx[i] == idx[i + 1] for i in range(k - 1)):
            continue
        s = [good[idx[0]] if rnd() < 0.5 else leaf[good[idx[0]]]] + [good[i] for i in idx[1:-1]] \
            + [leaf[good[idx[-1]]]]
        if rnd() < 0.5:
            j = 1 + int(rnd() * (k - 2))
            s[j] = leaf[s[j]]
        r = int(rnd() * k)
        s = [t.lab[x - 1] for x in s[r:] + s[:r]]
        if rnd() < 0.5:
            s.reverse()
        if total + k > MAXK:
            break
        total += k
        qs.append(s)
    add(n, t.edges, qs, True)


# samples
add(7, [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (5, 7)], [[4, 1, 6], [4, 5, 3], [7, 2, 3, 6], [5, 4]])
add(4, [(1, 2), (1, 3), (1, 4)], [[3], [2, 3, 4], [4, 1, 2]])
add(1, [], [[1]])
add(6, [(2, 5), (5, 1), (1, 6), (6, 3), (5, 4)], [[2, 3, 1], [4, 3, 2], [6, 5, 4, 3]])
add(8, [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (3, 7), (7, 8)], [[8, 6, 2], [4, 6, 8], [6, 1, 3, 4], [7, 5]])
# hidden: small and medium
make(8, "random", [3] * 40)
make(15, "binary", [ri(1, 6) for _ in range(60)])
make(30, "caterpillar", [ri(2, 8) for _ in range(80)])
make(60, "chains", [ri(3, 10) for _ in range(100)])
make(2000, "deep", [ri(3, 30) for _ in range(500)])
make(3000, "random", [3] * 2000)
# hidden: maximum size
cater(MAXN, [3] * 66_000)
cater(MAXN, [5] * 40_000)
deeplong(MAXN, 66_000)
cater(MAXN, [4] * 50_000)
deeplong(MAXN, 45_000, "deep", 6)
deeplong(MAXN, 66_000, "caterpillar")
deeplong(MAXN, 36_000, "caterpillar", 8)
deeplong(MAXN, 28_000, "deep", 12)
deeplong(MAXN, 50_000, "caterpillar", 5)
cater(MAXN, [8] * 25_000)
# hidden: wide trees or few long lists (not maximum size)
make(20_000, "random", [3] * 8000, 8)
make(30_000, "deep", [6000] * 5, 9000)
cater(30_000, [15_000, 14_999])
make(20_000, "binary", [ri(2, 40) for _ in range(2000)], pbad=0.6)

write_all()
