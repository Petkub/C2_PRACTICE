# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(15013)
MAXN = 100_000
MAXT = 10 ** 9
MAXH = 10 ** 9
tests = []
ALLOWED = bytes(range(32, 127)) + b"\n"


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(ev):
    n = len(ev)
    assert 2 <= n <= MAXN and n % 2 == 0
    stacks = {}
    prev = 0
    for t, h, k, f in ev:
        assert prev <= t <= MAXT and 1 <= h <= MAXH and k in ("ENTER", "EXIT")
        assert 1 <= len(f) <= 20 and f.isascii() and f.isalpha() and f.islower()
        prev = t
        st = stacks.setdefault(h, [])
        if k == "ENTER":
            st.append(f)
        else:
            assert st and st[-1] == f
            st.pop()
    assert all(not st for st in stacks.values())
    tests.append(f"{n}\n" + "".join(f"{t} {h} {k} {f}\n" for t, h, k, f in ev))


def parse(text):
    return [(int(a), int(b), c, d) for a, b, c, d in (ln.split() for ln in text.strip().split("\n"))]


def rand_name(lo=1, hi=6):
    return "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(random.randint(lo, hi)))


def trace(n, threads, names, p_enter=0.5, step=(0, 3), start=0):
    ev = []
    stacks = {h: [] for h in threads}
    open_threads = []
    pos = {}
    opened = 0
    t = start
    for i in range(n):
        remaining = n - i
        t += ri(*step)
        if opened == 0 or (remaining > opened and random.random() < p_enter):
            h = random.choice(threads)
            f = random.choice(names)
            if not stacks[h]:
                pos[h] = len(open_threads)
                open_threads.append(h)
            stacks[h].append(f)
            opened += 1
            ev.append((t, h, "ENTER", f))
        else:
            h = random.choice(open_threads)
            f = stacks[h].pop()
            opened -= 1
            if not stacks[h]:
                j = pos.pop(h)
                last = open_threads.pop()
                if last != h:
                    open_threads[j] = last
                    pos[last] = j
            ev.append((t, h, "EXIT", f))
    return ev


def thread_ids(k, hi=MAXH):
    return random.sample(range(1, hi + 1), k)


add(parse("""
1 1 ENTER main
2 2 ENTER main
3 1 ENTER work
5 2 EXIT main
7 1 EXIT work
10 1 EXIT main
"""))
add(parse("""
0 5 ENTER f
4 5 ENTER f
6 5 ENTER g
6 5 EXIT g
9 5 EXIT f
20 5 EXIT f
"""))
add(parse("""
0 7 ENTER sort
3 7 EXIT sort
10 7 ENTER so
12 7 EXIT so
"""))
add(parse("""
0 2 ENTER go
0 1 ENTER go
1000000000 1 EXIT go
1000000000 2 EXIT go
"""))
add(parse("""
1 2 ENTER b
1 9 ENTER a
2 9 ENTER b
4 2 EXIT b
6 9 EXIT b
8 9 EXIT a
"""))

add(parse("""
7 4 ENTER a
7 4 EXIT a
"""))
add(trace(20, [1], ["a", "b"]))
add(trace(40, [3, 1, 2], ["main", "mai", "ma", "m"]))
add(trace(200, thread_ids(10), [rand_name() for _ in range(5)], step=(0, 10 ** 6)))
add(trace(2000, thread_ids(50), [rand_name(1, 20) for _ in range(30)], step=(0, 5)))
add(trace(3000, thread_ids(3), ["f", "g"], p_enter=0.7, step=(0, 2)))
ev = trace(4000, thread_ids(1000), ["zz", "z", "zzz"], p_enter=0.6, step=(0, 100))
add(ev)
names = ["a" * 20, "a" * 19 + "b", "b" * 20]
add(trace(5000, thread_ids(100), names, step=(0, 10 ** 5)))


def wide(k, names, hi=MAXH):

    hs = thread_ids(k, hi)
    ev = []
    t = 0
    for h in hs:
        ev.append((t, h, "ENTER", random.choice(names)))
        t += ri(0, 1)
    order = hs[:]
    random.shuffle(order)
    t = MAXT - 2 * k
    top = {ev[i][1]: ev[i][3] for i in range(k)}
    for h in order:
        ev.append((t, h, "EXIT", top[h]))
        t += ri(0, 2)
    return ev


def deep(depth, h, names, step=(0, 3)):
    ev = []
    t = 0
    st = []
    for _ in range(depth):
        f = random.choice(names)
        st.append(f)
        ev.append((t, h, "ENTER", f))
        t += ri(*step)
    while st:
        ev.append((t, h, "EXIT", st.pop()))
        t += ri(*step)
    return ev


add(wide(MAXN // 2, ["run"], 10 ** 6))
add(wide(MAXN // 2, ["a", "b", "c", "d", "e"], 10 ** 6))
add(deep(MAXN // 2, 77, ["f"], (0, 10 ** 4)))
add(deep(MAXN // 2, 12345678, ["a", "b", "ab"], (0, 19000)))
add(trace(MAXN, thread_ids(30000, 10 ** 6), [rand_name(1, 4) for _ in range(50)], p_enter=0.52, step=(0, 9000)))
add(trace(MAXN, thread_ids(50000, 10 ** 6), ["main", "solve", "dfs"], p_enter=0.6, step=(0, 9000)))
add(trace(MAXN, thread_ids(2, 10 ** 6), [rand_name(1, 3) for _ in range(500)], step=(0, 10 ** 4)))
add(trace(MAXN, thread_ids(20000, 10 ** 6), [rand_name(1, 5) for _ in range(3000)], p_enter=0.6, step=(0, 10 ** 4)))
ev = wide(MAXN // 4, ["io", "net"], 10 ** 6)
k = MAXN // 4
mid = trace(MAXN // 2, thread_ids(10, 10 ** 5), ["x", "y"], step=(0, 1), start=0)
add(ev[:k] + [(ev[k - 1][0] + 1 + t, h, a, f) for t, h, a, f in mid] + ev[k:])
add(trace(MAXN, list(range(1, 40001)), ["q"], p_enter=0.9, step=(0, 10 ** 4)))
add(trace(MAXN, thread_ids(30000, 10 ** 6), [rand_name(1, 4) for _ in range(20000)], p_enter=0.65, step=(0, 10 ** 4)))
add(trace(MAXN, [999_999_999, 1, 1_000_000_000], ["rec"], p_enter=0.5, step=(0, 10 ** 4)))
ev = wide(MAXN // 4, ["w"], 10 ** 6)
mid = deep(MAXN // 4, 10 ** 9, ["w", "d"], (0, 1))
add(ev[:k] + [(ev[k - 1][0] + 1 + t, h, a, f) for t, h, a, f in mid] + ev[k:])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert t.encode().translate(None, ALLOWED) == b""
    assert len(t) <= 3_100_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
