# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(120017)
MAXRC = 2 * 10 ** 6
tests = []
LOW = "abcdefghijklmnopqrstuvwxyz"


def add(rows):
    r, c = len(rows), len(rows[0])
    assert 1 <= r and 1 <= c and r * c <= MAXRC
    assert all(len(x) == c and set(x) <= set(LOW + "#") for x in rows)
    assert rows[0][0] != "#" and rows[-1][-1] != "#"
    tests.append(f"{r} {c}\n" + "".join(x + "\n" for x in rows))


def fill(h, w, letters, weights):
    tot, table = sum(weights), bytearray()
    for v in range(256):
        acc = 0
        for ch, wt in zip(letters, weights):
            acc += wt
            if v * tot < 256 * acc:
                table.append(ord(ch))
                break
    n = h * w
    data = random.getrandbits(8 * n).to_bytes(n, "little").translate(bytes(table))
    return [bytearray(data[i * w:(i + 1) * w]) for i in range(h)]


def spine(h, w):
    turns = sorted(random.sample(range(h), w - 1) if w - 1 <= h else [random.randrange(h) for _ in range(w - 1)])
    span, col, k = [], 0, 0
    for i in range(h):
        lo = col
        while k < len(turns) and turns[k] == i:
            col += 1
            k += 1
        span.append((lo, col))
    span[-1] = (span[-1][0], w - 1)
    return span


def on_spine(span, i, j):
    return span is not None and span[i][0] <= j <= span[i][1]


def blocks(g, span, p):
    h, w = len(g), len(g[0])
    for _ in range(int(h * w * p)):
        i, j = random.randrange(h), random.randrange(w)
        if not on_spine(span, i, j) and (i, j) != (0, 0):
            g[i][j] = ord("#")


def notches(g, span, k, letter, length):
    h, w = len(g), len(g[0])
    for _ in range(k):
        i, j, ln = random.randrange(1, h - length - 1), random.randrange(w - 1), random.randint(1, length)
        cells = [(i + t, j) for t in range(ln)] + [(i + t, j + 1) for t in range(ln)] + [(i + ln, j)]
        if any(on_spine(span, a, b) for a, b in cells):
            continue
        for t in range(ln):
            g[i + t][j] = ord(letter)
            g[i + t][j + 1] = ord("#")
        g[i + ln][j] = ord("#")


def done(g):
    add([x.decode() for x in g])


def rnd_small(h, w, letters, p):
    g = fill(h, w, letters, [1] * len(letters))
    s = spine(h, w) if random.random() < 0.8 else None
    blocks(g, s, p)
    g[0][0] = ord(random.choice(letters))
    g[-1][-1] = ord(random.choice(letters))
    done(g)


add(["abca", "b#ba", "caab"])
add(["a#", "#a"])
add(["z"])
add(["hello"])
add(["coder", "o#ode", "d#dea", "ecode"])
add(["ab#", "ba#", "#ba", "aab"])

for h, w, letters, p in ((4, 5, "ab", 0.2), (6, 6, "ab", 0.3), (7, 9, "abc", 0.25), (10, 8, "ab", 0.35),
                         (12, 12, "az", 0.2), (40, 1, "cab", 0.0)):
    rnd_small(h, w, letters, p)
g = fill(300, 60, "bc", [3, 2])
s = spine(300, 60)
blocks(g, s, 0.02)
notches(g, s, 300, "a", 6)
done(g)

g = fill(700, 700, "ab", [1, 1])
s = spine(700, 700)
blocks(g, s, 0.25)
notches(g, s, 3000, "a", 5)
done(g)
g = fill(400, 1200, "abc", [1, 1, 1])
blocks(g, spine(400, 1200), 0.3)
done(g)

for h, w, letters, weights, p, k, ln in ((200000, 10, "bc", [1, 1], 0.0005, 3000, 8),
                                         (250000, 8, "bcd", [3, 2, 1], 0.0005, 3000, 12),
                                         (200000, 10, "ab", [3, 1], 0.001, 0, 0),
                                         (300000, 6, "xyz", [1, 1, 1], 0.0003, 0, 0),
                                         (500000, 4, "bc", [5, 2], 0.0002, 2000, 20),
                                         (400000, 5, "bc", [1, 1], 0.0, 0, 0),
                                         (250000, 8, "bc", [2, 1], 0.0005, 5000, 6)):
    g = fill(h, w, letters, weights)
    s = spine(h, w)
    blocks(g, s, p)
    notches(g, s, k, "a", ln)
    done(g)
add(["a" * 20] * 100000)
g = fill(200000, 10, "ab", [3, 1])
g[0][0] = ord("a")
g[-3] = bytearray(b"#" * 10)
done(g)
g = [bytearray(b"b" * 10) for _ in range(200000)]
for i in range(200000):
    g[i][3] = g[i][4] = ord("a")
for i in range(0, 199990, 37):
    g[i + random.randrange(5)][3 + random.randrange(2)] = ord("b")
g[-1][-1] = ord("a")
done(g)
g = fill(250000, 8, "ab", [1, 1])
s = spine(250000, 8)
g[-1000] = bytearray(b"#" * 8)
g[-1000][s[-1000][0]] = ord("a")
done(g)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
