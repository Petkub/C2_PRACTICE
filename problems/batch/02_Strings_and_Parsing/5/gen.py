# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random, string

random.seed(150505)
MAXS = 10 ** 6
MAXQ = 5 * 10 ** 5
MAXK = 2 * 10 ** 6
LOW = string.ascii_lowercase
tests = []


def add(s, cmds):
    assert 1 <= len(s) <= MAXS and set(s) <= set(LOW)
    assert 1 <= len(cmds) <= MAXQ
    for c in cmds:
        assert c in ("R", "F", "L") or (c[0] in "AP" and c[1] == " " and len(c) == 3 and c[2] in LOW) \
            or (c[:2] == "? " and 1 <= int(c[2:]) <= MAXK)
    t = s + "\n" + str(len(cmds)) + "\n" + "".join(c + "\n" for c in cmds)
    assert not t.encode().translate(None, bytes(range(32, 127)) + b"\n")
    tests.append(t)


def rs(n, alpha=LOW):
    return "".join(random.choices(alpha, k=n))


def cmds(n0, q, w, alpha=LOW, p_out=0.05):
    kinds = random.choices("RFLAP?", weights=w, k=q)
    out, n = [], n0
    for c in kinds:
        if c in "FL":
            n = max(0, n - 1)
            out.append(c)
        elif c in "AP":
            n += 1
            out.append(c + " " + random.choice(alpha))
        elif c == "?":
            if n == 0 or random.random() < p_out:
                k = random.choice([n + 1, n + random.randint(1, 10), random.randint(n + 1, MAXK)]) if n < MAXK else n
                k = max(1, min(k, MAXK))
            else:
                k = random.choice([1, n, random.randint(1, n), random.randint(1, n)])
            out.append(f"? {k}")
        else:
            out.append("R")
    return out


add("abc", ["A d", "R", "? 1", "F", "P z", "? 4"])
add("ab", ["L", "R", "F", "F", "? 1", "A x", "R"])
add("q", ["R", "L"])
add("hello", ["R", "P a", "? 9", "? 6"])
add("stop", ["R", "F", "L", "? 2", "A k"])

add("z", ["? 1"])
add("ab", ["F", "F", "F", "L", "R", "? 1", "? 2000000"])
add(rs(5, "ab"), cmds(5, 40, [3, 2, 2, 2, 2, 3], "abc"))
add(rs(30), cmds(30, 500, [2, 1, 1, 1, 1, 2]))
add(rs(3), cmds(3, 2000, [3, 3, 3, 1, 1, 3]))
add(rs(1000), cmds(1000, 20000, [1, 1, 1, 1, 1, 2]))
add(rs(20000), cmds(20000, 30000, [2, 1, 1, 1, 1, 2]))

add(rs(MAXS), ["R" if i % 2 == 0 else f"? {random.randint(1, MAXS)}" for i in range(360000)])
add(rs(MAXS), cmds(MAXS, MAXQ, [3, 0, 0, 3, 3, 1]))
add(rs(MAXS), cmds(MAXS, MAXQ, [2, 4, 1, 0, 0, 1]))
add(rs(MAXS), cmds(MAXS, 450000, [1, 1, 1, 1, 1, 1]))
add(rs(MAXS, "ab"), cmds(MAXS, 450000, [4, 1, 1, 1, 1, 2], "ab"))
add(rs(1), cmds(1, MAXQ, [2, 1, 1, 3, 3, 1]))
add(rs(400000), ["F", "L"] * 200000 + ["R", "? 1", "F", "L", "A q", "R", "? 1", "? 2"] * 12500)
add(rs(MAXS), ["R"] * 149999 + [f"? {k}" for k in random.sample(range(1, MAXS + 1), 120000)] +
    [f"? {random.randint(MAXS + 1, MAXK)}" for _ in range(40000)])
add(rs(MAXS), cmds(MAXS, 450000, [5, 1, 1, 1, 1, 3], p_out=0.3))
add(rs(500000), cmds(500000, MAXQ, [2, 2, 2, 2, 2, 1]))
add(rs(MAXS), [random.choice(["R", "P " + random.choice(LOW)]) for _ in range(MAXQ)])
add(rs(MAXS), [random.choice(["R", "F", "L", "F", f"? {random.randint(1, MAXS // 2)}"]) for _ in range(MAXQ)])
add(rs(MAXS), cmds(MAXS, MAXQ, [1, 2, 2, 2, 2, 1]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
