# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(150201)
MAXN = 200_000
tests = []

_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(_rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def boss_of(s):
    """bosses of 2..n (list) if the roster is possible, else None (stack of open teams)"""
    n = len(s)
    if s[0] != n:
        return None
    last = [i + x for i, x in enumerate(s)]          # last[i - 1] = the last line of the team of line i
    st, b = [1], []
    for i in range(2, n + 1):
        while last[st[-1] - 1] < i:
            st.pop()
        j = st[-1]
        if last[i - 1] > last[j - 1]:
            return None
        b.append(j)
        st.append(i)
    return b


def add(s, valid=None):
    n = len(s)
    assert 2 <= n <= MAXN
    assert all(1 <= x <= n for x in s)
    if valid is not None:
        assert (boss_of(s) is not None) == valid
    tests.append(f"{n}\n" + " ".join(map(str, s)) + "\n")


def roster(ch, mix=True):
    """team sizes in roster order of the tree given by children lists (node 0 = president)"""
    n = len(ch)
    if mix:
        for c in ch:
            shuf(c)
    order, st = [], [0]
    while st:
        v = st.pop()
        order.append(v)
        st.extend(reversed(ch[v]))
    assert len(order) == n
    sz = [1] * n
    for v in reversed(order):
        for c in ch[v]:
            sz[v] += sz[c]
    return [sz[v] for v in order]


def shape(n, kind):
    ch = [[] for _ in range(n)]
    for i in range(1, n):
        if kind == "random":
            p = int(_rnd() * i)
        elif kind == "path":
            p = i - 1
        elif kind == "star":
            p = 0
        elif kind == "deep":
            p = ri(max(0, i - 3), i - 1)
        elif kind == "binary":
            p = (i - 1) // 2
        elif kind == "fewhubs":                 # almost everybody hangs under one of 3 people
            p = ri(0, min(i - 1, 2))
        else:
            raise ValueError(kind)
        ch[p].append(i)
    return ch


def hubs(sizes, depth=0):
    """roster of: the president, then a chain of `depth` people, then one hub per entry of sizes
    (in this order, all under the last person of the chain), each hub with that many direct reports
    who have nobody under them"""
    n = 1 + depth + len(sizes) + sum(sizes)
    s = [n - k for k in range(depth + 1)]
    for h in sizes:
        s.append(h + 1)
        s.extend([1] * h)
    assert len(s) == n
    return s


def stick_out(s, pos):
    """make the team of line pos (1-based, team size 1, not the last line of the roster) one person bigger:
    the next line belongs to somebody outside the team of its boss"""
    s = s[:]
    assert s[pos - 1] == 1 and pos < len(s)
    s[pos - 1] = 2
    return s


def closers(s, lo, hi):
    """lines i in [lo, hi) with team size 1 that are the last line of their boss's team (and not the last line)"""
    b = boss_of(s)
    return [i for i in range(max(lo, 2), min(hi, len(s))) if s[i - 1] == 1 and b[i - 2] + s[b[i - 2] - 1] - 1 == i]


def last_leaf_of_block(s, start):
    """the last line of the team of line start"""
    return start + s[start - 1] - 1


# samples
add([7, 4, 2, 1, 1, 2, 1], True)
add([5, 1, 3, 1, 2], False)
add([2, 1], True)
add([6, 1, 1, 1, 1, 1], True)
add([3, 2, 1, 1], False)
add([8, 7, 6, 1, 4, 2, 1, 1], True)
# hidden: small (the brute tries every boss array up to N = 9)
add(roster(shape(9, "random")), True)
add([9, 3, 2, 2, 1, 3, 1, 1, 1], False)                   # line 4 sticks out of the team of line 3
add(list(range(10, 0, -1)), True)                          # one long chain
s = roster(shape(50, "deep"))
add(s, True)
s = roster(shape(200, "random"))
# a person of size 1 whose team is not the last line of the boss's team: grow it by one
cand = closers(s, 2, 200)
add(stick_out(s, cand[len(cand) // 2]), False)
add(roster(shape(1000, "binary")), True)
s = roster(shape(3000, "fewhubs"))
cand = closers(s, 2, 3000)
add(stick_out(s, cand[-1]), False)
s = roster(shape(1000, "random"))
s[0] -= 1                                                  # the president's team misses the last person
add(s, False)
add(roster(shape(5000, "random")), True)
add(roster(shape(5000, "path")), True)
s = hubs([9000, 10990])
add(stick_out(s, last_leaf_of_block(s, 2)), False)        # last report of the first hub covers the second hub
# hidden: maximum size
N = MAXN
add([N] + [1] * (N - 1), True)                             # a star
s = [N] + [1] * (N - 1)
s[N - 1] = 2                                               # the last report claims somebody after the last line
add(s, False)
add(hubs([130_000, N - 130_003]), True)
s = hubs([150_000, N - 150_003])
add(stick_out(s, last_leaf_of_block(s, 2)), False)
add(hubs([N - 50_002], depth=50_000), True)       # a chain, then a hub at its bottom
add(hubs([66_665, 66_666, 66_665]), True)
s = hubs([100_000, 60_000, N - 160_004])
add(stick_out(s, last_leaf_of_block(s, 100_003)), False)  # inside the second hub
add(hubs([99_000, N - 100_003], depth=1000), True)
add(roster(shape(N, "fewhubs")), True)
s = hubs([30_000, 140_000, N - 170_005], depth=1)
add(stick_out(s, last_leaf_of_block(s, 30_004)), False)   # the last report of the second hub

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
