# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(286031)
MAXN, MAXV = 200_000, 10**9
tests = []
depth = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    d = m = 0
    for x in a:
        d += 1 if x < 0 else -1
        m = max(m, d)
    depth.append(m)
    assert 1 <= n <= MAXN
    assert all(x != 0 and -MAXV <= x <= MAXV for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def forest(k, stay, top=0.0005):
    """parent of each of k boxes (-1 = outermost), in the order their opening numbers are written.
    With chance `stay` a new box goes inside the box opened last; otherwise a few open boxes are closed first
    (all of them with chance `top`, so the new box is outermost)."""
    parent, path = [], []
    for v in range(k):
        if path and random.random() >= stay:
            if random.random() < top:
                del path[:]
            else:
                del path[max(0, len(path) - ri(1, 6)):]
        parent.append(path[-1] if path else -1)
        path.append(v)
    return parent


def sizes(parent, slack):
    """smallest valid sizes plus a random slack in [1, slack] for every box"""
    k = len(parent)
    assert k * slack <= 2 * MAXV
    inside = [0] * k
    size = [0] * k
    for v in range(k - 1, -1, -1):      # children come after their parent
        size[v] = inside[v] + ri(1, slack)
        if parent[v] >= 0:
            inside[parent[v]] += size[v]
    return size


def write(parent, size):
    """the record: -m, the boxes directly inside, m"""
    k = len(parent)
    kids = [[] for _ in range(k)]
    tops = []
    for v in range(k):
        (kids[parent[v]] if parent[v] >= 0 else tops).append(v)
    out, st = [], [(v, 0) for v in reversed(tops)]
    while st:
        v, done = st.pop()
        if done:
            out.append(size[v])
        else:
            out.append(-size[v])
            st.append((v, 1))
            st.extend((c, 0) for c in reversed(kids[v]))
    return out


def valid(k, stay, slack):
    p = forest(k, stay)
    return p, sizes(p, slack)


def tight(parent, size, count):
    """make `count` boxes with something inside exactly as big as the boxes directly inside them (not valid)"""
    k = len(parent)
    inside = [0] * k
    for v in range(k):
        if parent[v] >= 0:
            inside[parent[v]] += size[v]
    cand = [v for v in range(k * 9 // 10, k) if inside[v] > 0]     # late in the record
    for v in random.sample(cand, min(count, len(cand))):
        size[v] = inside[v]          # smaller box: its parent stays fine
    return size


def overflow_box(m=MAXV, kids=5):
    """one box of size m with `kids` boxes of size m - 1 directly inside (the total passes 2^32)"""
    return [-m] + [-(m - 1), m - 1] * kids + [m]


# samples
add([-10, -3, 3, -4, -1, 1, 4, 10])
add([-5, -2, 2, -2, 2, 5, -7, 7])
add([-6, -2, 2, -4, 4, 6])
add([-3, -1, 3, 1])
add([-9, -8, -1, 1, 8, 9, -2])
# hidden: small
add([5])
add([-1, 1])
add([-1000000000, 1000000000, -1, 1])
add([-3, -1, 1, -1, 1, 3, 3])
add([-4, -1, 1, -2, 2, 4] + overflow_box(MAXV, 4))
add(overflow_box(MAXV, 3))
p, s = valid(30, 0.6, 3)
add(write(p, s))
p, s = valid(40, 0.5, 2)
add(write(p, tight(p, s, 1)))
p, s = valid(200, 0.8, 5)
add(write(p, s) + overflow_box())
p, s = valid(1000, 0.95, 2)
a = write(p, s)
j = max(i for i in range(len(a)) if a[i] > 1 and a[i - 1] < 0)   # a box with nothing inside, late
a[j] += 1                                                        # its closing number no longer matches
add(a)
# hidden: maximum size (every one is deep)
K = MAXN // 2
p, s = valid(K, 0.98, 1000)
add(write(p, s))
p, s = valid(K, 0.995, 3)
add(write(p, s))
p, s = valid(K, 0.98, 10)
add(write(p, tight(p, s, 1)))
p = list(range(-1, K - 1))                  # one long chain of boxes
add(write(p, sizes(p, 1)))
p, s = valid(K - 6, 0.98, 2000)
add(write(p, s) + overflow_box())
p, s = valid(K - 4, 0.97, 50)
add(write(p, s) + overflow_box(MAXV, 3))
p, s = valid(K - 11, 0.99, 100)
add(write(p, s) + overflow_box(MAXV, 9))
p, s = valid(K - 2, 0.99, 7)
a = write(p, s)
add(a + [-5, -1, 1])                        # the last box is never closed
add(a + [a[-1]])                            # one closing number too many
p, s = valid(K, 0.96, 30)
a = write(p, s)
j = max(i for i in range(len(a) // 2, len(a)) if a[i] > 1 and a[i - 1] < 0)
a[j] -= 1
add(a)
p, s = valid(K, 0.995, 1)
add(write(p, s))
p, s = valid(K - 6, 0.9, 5)
add(write(p, s) + overflow_box())
p = forest(K, 0.995, 0.002)                 # many outermost boxes
add(write(p, sizes(p, 50)))
p = forest(K, 0.99, 0.001)                  # sizes close to 10^9
add(write(p, sizes(p, 19_000)))
p = forest(K, 0.99, 0.001)                  # every box only just big enough
add(write(p, sizes(p, 1)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
