# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(15015)
MAXK = 10
MAXQ = 200_000
MAXS = 200_000
MAXINS = 1_000_000
MAXMOVE = 10_000_000
LOWER = "abcdefghijklmnopqrstuvwxyz"
ALLOWED = bytes(range(32, 127)) + b"\n"
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, s, cmds):
    assert 1 <= k <= MAXK and 1 <= len(s) <= MAXS and s.isalpha() and s.islower() and s.isascii()
    assert 1 <= len(cmds) <= MAXQ
    ins = mv = 0
    for u, op, x in cmds:
        assert 1 <= u <= k and op in "ILRBD"
        if op == "I":
            assert x and x.isalpha() and x.islower() and x.isascii()
            ins += len(x)
        else:
            assert isinstance(x, int) and x >= 1
            mv += x
    assert ins <= MAXINS and mv <= MAXMOVE
    t = f"{k} {len(cmds)}\n{s}\n" + "".join(f"{u} {op} {x}\n" for u, op, x in cmds)
    assert t.encode().translate(None, ALLOWED) == b"" and "  " not in t and " \n" not in t
    tests.append(t)


def word(lo, hi):
    return "".join(random.choices(LOWER, k=ri(lo, hi)))


def parse(text):
    out = []
    for ln in text.strip().split("\n"):
        u, op, x = ln.split()
        out.append((int(u), op, x if op == "I" else int(x)))
    return out


add(2, "abcdef", parse("""
1 R 2
2 R 3
1 D 2
2 I xy
"""))
add(2, "ab", parse("""
1 R 5
2 R 2
1 I cd
1 B 9
"""))
add(1, "cat", parse("""
1 R 1
1 I o
1 R 9
1 I s
"""))
add(3, "abc", parse("""
1 I x
2 R 1
3 R 2
2 D 1
"""))
add(2, "zz", parse("""
1 D 1
1 D 1
2 I q
1 L 4
"""))


def random_cmds(k, q, ins_budget, mv_budget, len0, w=(3, 2, 2, 2, 2), ins_len=(1, 5), mv_max=6):
    cmds, ins, mv = [], 0, 0
    for op in random.choices("ILRBD", weights=w, k=q):
        u = ri(1, k)
        if op == "I":
            x = word(*ins_len)
            if ins + len(x) > ins_budget:
                op = "R"
            else:
                ins += len(x)
                cmds.append((u, "I", x))
                continue
        x = ri(1, mv_max)
        if mv + x > mv_budget:
            continue
        mv += x
        cmds.append((u, op, x))
    return cmds


add(2, "ab", parse("""
1 R 5
2 R 2
1 I cd
2 L 1
2 D 9
1 B 3
"""))
add(1, "a", [(1, "D", 1)])
add(1, "a", [(1, "B", 5), (1, "L", 3), (1, "I", "b")])
add(10, "q", [(u, "I", "x") for u in range(1, 11)])
for k, n, q in ((2, 5, 20), (3, 10, 60), (5, 30, 300), (10, 100, 2000), (4, 1000, 5000), (10, 3000, 10000)):
    add(k, word(n, n), random_cmds(k, q, 10 ** 9, 10 ** 9, n, mv_max=max(3, n // 5)))
add(6, word(50, 50), random_cmds(6, 3000, 10 ** 9, 10 ** 9, 50, w=(1, 1, 1, 3, 3), mv_max=8))


S = word(MAXS, MAXS)


def long_tail(k, start, w, ins_len=(1, 3), mv_max=3, build=800_000):
    cmds = [(1, "R", MAXS)]
    ins = 0
    while ins < build:
        x = word(100, 100)
        ins += len(x)
        cmds.append((1, "I", x))
    mv = MAXS
    if start:
        for u in range(2, k + 1):
            x = start + ri(0, 1000)
            cmds.append((u, "R", x))
            mv += x
    rest = random_cmds(k - 1, MAXQ - len(cmds), MAXINS - ins, MAXMOVE - mv, MAXS, w=w, ins_len=ins_len, mv_max=mv_max)
    cmds += [(u + 1, op, x) for u, op, x in rest]
    return cmds


add(10, S, long_tail(10, 0, (1, 0, 0, 0, 2)))
add(2, S, long_tail(2, 0, (0, 0, 0, 0, 1)))
add(10, S, long_tail(10, 0, (2, 1, 1, 2, 2)))
add(5, S, long_tail(5, 0, (3, 0, 0, 3, 0)))
add(10, S, long_tail(10, 100_000, (2, 1, 1, 1, 2)))
add(4, S, long_tail(4, 30, (1, 1, 1, 0, 3), mv_max=2))
add(10, S, long_tail(10, 0, (1, 0, 0, 0, 1), ins_len=(1, 1), mv_max=1, build=500_000))


add(10, S, long_tail(10, 150_000, (4, 2, 2, 1, 1), ins_len=(3, 7), mv_max=20, build=600_000))
add(5, S, long_tail(5, 50_000, (4, 2, 2, 1, 1), ins_len=(4, 6), mv_max=20))
add(10, S, long_tail(10, 199_000, (2, 3, 3, 0, 0), ins_len=(1, 2), mv_max=20, build=750_000))


def wipe_and_refill(k):

    cmds, ins, mv = [], 0, 0
    while len(cmds) < MAXQ - 20:
        for _ in range(ri(1, 3)):
            u = ri(1, k)
            x = ri(1, 40_000)
            if mv + x > MAXMOVE:
                continue
            mv += x
            cmds.append((u, random.choice("BD"), x))
        for _ in range(ri(50, 3000)):
            u = ri(1, k)
            c = random.random()
            if c < 0.7 and ins + 5 <= MAXINS:
                x = word(1, 5)
                ins += len(x)
                cmds.append((u, "I", x))
            else:
                x = ri(1, 30)
                if mv + x > MAXMOVE:
                    continue
                mv += x
                cmds.append((u, random.choice("LR"), x))
            if len(cmds) >= MAXQ - 20:
                break
    return cmds


add(10, S, wipe_and_refill(10))
build = long_tail(2, 0, (1, 0, 0, 0, 0), build=800_000)[:8001]
add(10, S, build + [(u, "I", word(1, 1)) if i % 2 == 0 else (u, "L", 1) for i, u in
                    enumerate(random.choices(range(2, 11), k=MAXQ - len(build)))])
add(3, S, build + [(2, "R", MAXS // 2)] + [(2, "I", "a") if i % 3 else (3, "D", 2)
                                          for i in range(MAXQ - len(build) - 1)])
add(10, S, [(ri(1, 10), "R", 50) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and len(t) <= 3_100_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
