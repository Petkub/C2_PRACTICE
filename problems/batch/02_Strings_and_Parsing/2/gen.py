# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random, string

random.seed(150303)
MAXN = 5 * 10 ** 5
MAXM = 10 ** 5
MAXK = 10 ** 9
PRINT = [chr(c) for c in range(33, 127)]
ALNUM = string.ascii_letters + string.digits
tests = []


def add(s, ops):
    n = len(s)
    assert 1 <= n <= MAXN and 1 <= len(ops) <= MAXM
    assert all(33 <= ord(c) <= 126 for c in s)
    for l, r, k in ops:
        assert 1 <= l <= r <= n and -MAXK <= k <= MAXK
    tests.append(f"{s}\n{len(ops)}\n" + "".join(f"{l} {r} {k}\n" for l, r, k in ops))


def rs(n, alpha=PRINT, w=None):
    return "".join(random.choices(alpha, weights=w, k=n))


def rop(n, kr=MAXK, minlen=1):
    l = random.randint(1, n - minlen + 1)
    r = random.randint(l + minlen - 1, n)
    return (l, r, random.randint(-kr, kr))


def wide(n, k):

    l = random.randint(1, max(1, n // 20))
    r = random.randint(n - n // 20, n)
    return (l, r, k)


add("Hello,World9", [(1, 5, 1), (7, 12, -2)])
add("zZ9a", [(1, 4, 1), (1, 3, 27)])
add("a-b_c", [(1, 5, -1000000000)])
add("Code2026!", [(1, 9, 5), (3, 6, -30), (5, 5, 1000000000), (1, 1, -1)])
add("x", [(1, 1, 7), (1, 1, -7)])

add("~", [(1, 1, MAXK)])
add("0", [(1, 1, -1)] * 3)
add(rs(30), [rop(30, 60) for _ in range(30)])
add(rs(50, ALNUM), [rop(50) for _ in range(50)])
add(rs(200, "az09AZ"), [rop(200, 100) for _ in range(300)])
add(rs(2000), [rop(2000) for _ in range(2000)])
add(rs(5000, ALNUM + "#"), [wide(5000, random.choice([MAXK, -MAXK])) for _ in range(5000)])
add(rs(3000, "z9Z"), [(1, 3000, 26 * random.randint(1, 38 * 10 ** 6)) for _ in range(3000)])

n, m = MAXN, MAXM
add(rs(n, ALNUM), [(1, n, MAXK)] * m)
add(rs(n, ALNUM), [(1, n, -MAXK)] * m)
add(rs(n), [wide(n, random.randint(-MAXK, MAXK)) for _ in range(m)])
add(rs(n, "z9Z!"), [wide(n, 26 * random.randint(-38 * 10 ** 6, 38 * 10 ** 6)) for _ in range(m)])
add(rs(n, "a0A"), [wide(n, 10 * random.randint(-10 ** 8, 10 ** 8)) for _ in range(m)])
add(rs(n, "mM5"), [wide(n, random.choice([MAXK, -MAXK, MAXK - 1, 1 - MAXK])) for _ in range(m)])
add(rs(n, ALNUM), [rop(n) for _ in range(m)])
add(rs(n), [rop(n, MAXK, n // 2) for _ in range(m)])
add(rs(n, ALNUM), [(l, l + random.randint(0, 9), random.randint(-MAXK, MAXK))
                   for l in (random.randint(1, n - 10) for _ in range(m))])
add(rs(n, "z"), [(1, n, 1)] * (m // 2) + [(1, n, -1)] * (m // 2 - 1) + [(n // 2, n, 1)])
add(rs(n, string.ascii_lowercase), [(random.randint(1, 100), random.randint(n - 100, n), random.randint(-MAXK, MAXK))
                                    for _ in range(m)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert not t.encode().translate(None, bytes(range(32, 127)) + b"\n")
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
