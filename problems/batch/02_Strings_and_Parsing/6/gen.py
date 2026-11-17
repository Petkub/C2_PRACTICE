# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random, re

random.seed(150601)
MAXN = MAXM = 100_000
MAXTEXT = 1_000_000
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def word():
    return "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(ri(1, 6)))


POOL = [" ".join(word() for _ in range(ri(1, 2))) for _ in range(10000)]


class Doc:

    def __init__(self, n):
        self.n = n
        self.nxt = [(i + 1) % (n + 1) for i in range(n + 1)]
        self.prv = [(i + n) % (n + 1) for i in range(n + 1)]
        self.alive = list(range(1, n + 1))
        self.where = list(range(-1, n))
        self.cmds = []

    def is_alive(self, v):
        return 1 <= v <= self.n and self.where[v] >= 0

    def delete(self, x):
        assert self.is_alive(x)
        nxt, prv = self.nxt, self.prv
        nxt[prv[x]] = nxt[x]
        prv[nxt[x]] = prv[x]
        i, last = self.where[x], self.alive[-1]
        self.alive[i] = last
        self.where[last] = i
        self.alive.pop()
        self.where[x] = -1
        self.cmds.append(f"DEL {x}")

    def block(self, x, y):
        out = [x]
        v = x
        while v != y:
            v = self.nxt[v]
            assert v != 0
            out.append(v)
        return out

    def move(self, x, y, z, blk=None):
        assert self.is_alive(x) and self.is_alive(y)
        if blk is None:
            blk = self.block(x, y)
        assert z == 0 or (self.is_alive(z) and z not in set(blk))
        nxt, prv = self.nxt, self.prv
        a, b = prv[x], nxt[y]
        nxt[a] = b
        prv[b] = a
        c = nxt[z]
        nxt[z] = x
        prv[x] = z
        nxt[y] = c
        prv[c] = y
        self.cmds.append(f"MOVE {x} {y} {z}")


def emit(texts, doc):
    n, m = len(texts), len(doc.cmds)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and doc.n == n
    assert sum(len(t) for t in texts) <= MAXTEXT
    assert re.fullmatch(r"([a-z]+( [a-z]+)*\n)+", "".join(t + "\n" for t in texts))
    tests.append(f"{n} {m}\n" + "".join(t + "\n" for t in texts) + "".join(c + "\n" for c in doc.cmds))


def hand(texts, cmds):
    d = Doc(len(texts))
    for c in cmds:
        p = c.split()
        if p[0] == "DEL":
            d.delete(int(p[1]))
        else:
            d.move(int(p[1]), int(p[2]), int(p[3]))
    emit(texts, d)


def rand_test(n, m, pdel=0.1, pz0=0.1, small=4, pbig=0.0, texts=None, final_empty=False):
    if texts is None:
        texts = random.choices(POOL, k=n)
    d = Doc(n)
    nxt, prv, alive, cmds = d.nxt, d.prv, d.alive, d.cmds
    rnd = random.random
    for k in range(m):
        if not alive:
            break
        if (final_empty and len(alive) >= m - k) or (rnd() < pdel and len(alive) > 1):
            d.delete(alive[int(rnd() * len(alive))])
            continue
        x = alive[int(rnd() * len(alive))]
        steps = int(rnd() * (small + 1)) if rnd() >= pbig else ri(0, n)
        blk = [x]
        y = x
        for _ in range(steps):
            if nxt[y] == 0:
                break
            y = nxt[y]
            blk.append(y)
        if len(blk) == len(alive) or rnd() < pz0:
            z = 0
        else:
            s = set(blk) if len(blk) > 8 else blk
            z = alive[int(rnd() * len(alive))]
            while z in s:
                z = alive[int(rnd() * len(alive))]
        a, b = prv[x], nxt[y]
        nxt[a] = b
        prv[b] = a
        c = nxt[z]
        nxt[z] = x
        prv[x] = z
        nxt[y] = c
        prv[c] = y
        cmds.append(f"MOVE {x} {y} {z}")
    emit(texts, d)


hand(["the cat sat", "on a mat", "it was warm", "the end"], ["MOVE 2 3 4", "DEL 1", "MOVE 3 3 0"])
hand(["hello world", "bye"], ["MOVE 1 1 2", "DEL 1", "DEL 2"])
hand(["one", "two", "three"], ["MOVE 2 3 1", "MOVE 1 2 3"])
hand(["a b c", "dd ee", "f"], ["DEL 2", "MOVE 3 3 0", "MOVE 3 1 0"])
hand(["x"], ["MOVE 1 1 0"])

hand(["z"], ["DEL 1"])
rand_test(8, 10, pdel=0.15)
rand_test(50, 60, pdel=0.05, small=10)
rand_test(300, 400, pdel=0.0, pz0=0.3, small=50)
rand_test(1000, 1500, pdel=0.02, pbig=0.2)
rand_test(2000, 2000, pdel=0.3, final_empty=True)
rand_test(3000, 3000, pdel=0.0, pz0=0.5, small=2)
rand_test(5000, 5000, pdel=0.01, pz0=0.3, small=25)

long_texts = [f"{v >> 7:02b} {v & 127:07b}".replace("0", "p").replace("1", "q")
              for v in (random.getrandbits(9) for _ in range(MAXN))]
rand_test(MAXN, MAXM, pdel=0.05, pz0=0.1, small=4)
rand_test(MAXN, MAXM, pdel=0.0, pz0=0.5, small=1)
rand_test(MAXN, MAXM, pdel=0.0, pz0=0.0, small=0, texts=long_texts)
rand_test(MAXN, MAXM, pdel=0.6, pz0=0.1, small=3, final_empty=True)
rand_test(MAXN, MAXM, pdel=0.0, pz0=0.05, small=10, pbig=0.0002)
rand_test(MAXN, MAXM, pdel=0.2, pz0=0.2, small=8)
rand_test(MAXN, MAXM, pdel=0.01, pz0=0.3, small=25)
rand_test(MAXN, MAXM, pdel=0.001, pz0=0.2, small=2)
for t in tests:
    assert t.endswith("\n") and " \n" not in t
    assert t.encode().translate(None, bytes(range(32, 127)) + b"\n") == b""
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
