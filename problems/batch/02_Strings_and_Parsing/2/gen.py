# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(150202)
MAXN = 10 ** 6
LOW = string.ascii_lowercase
tests = []


def add(t, p):
    assert 1 <= len(p) <= len(t) <= MAXN
    assert set(t) <= set(LOW + "?") and set(p) <= set(LOW)
    tests.append(t + "\n" + p + "\n")


def rnd(n, alpha, weights=None):
    return "".join(random.choices(alpha, weights=weights, k=n))


def shuffled(s):
    l = list(s)
    random.shuffle(l)
    return "".join(l)


def planted(n, p, copies, alpha, qprob=0.2):
    # random text with shuffled copies of p (some letters turned into '?') at random places
    t = list(rnd(n, alpha))
    m = len(p)
    for _ in range(copies):
        s = random.randint(0, n - m)
        for i, c in enumerate(shuffled(p)):
            t[s + i] = "?" if random.random() < qprob else c
    return "".join(t)


# samples
add("xbacbabc?d", "abc")
add("cc?a?cc", "cab")
add("hello", "world")
add("aaaa", "aa")
add("ab?ba?c", "abc")
# hidden: small (brute checks these)
add("a", "a")
add("?", "z")
add("b", "a")
add(rnd(30, "ab?"), "abaab")
add(rnd(2000, "abc?", [3, 3, 3, 1]), "a" * 230 + "b" * 240 + "c" * 230)
add(planted(5000, shuffled(LOW), 40, LOW + "?"), shuffled(LOW))
p = rnd(100, "abcdefgh")
add(planted(10000, p, 60, "abcdefgh?"), p)
add(rnd(20000, "?" * 30 + "xy"), rnd(10000, "xy"))
add(rnd(40000, "ab?", [45, 45, 10]), "a" * 450 + "b" * 550)
# hidden: large
m = MAXN // 2
add("?" * MAXN, rnd(m, LOW))                                                    # every window
p = "a" * (m // 2) + "b" * (m - m // 2)
add(rnd(MAXN, "ab"), p)                                                         # near the border
p = rnd(400000, LOW[:10])
add("b" * (MAXN - len(p)) + shuffled(p), p)                                     # only the last window
p = rnd(300000, LOW[:6])
add(planted(MAXN, p, 6, LOW[:6] + "?", 0.1), p)
add("".join("b" if i % (m // 2) == 0 else random.choice("a?") for i in range(MAXN)), "a" * m)  # never
p = rnd(MAXN, LOW[:3])
add(shuffled(p[:-1] + "d"), p)                                                  # one window, one letter over
add(shuffled(p[:-5] + "?????"), p)                                              # one window, a hit
pa = int(0.6 * 0.45 * MAXN)
add(rnd(MAXN, "ab?", [45, 45, 10]), "a" * pa + "b" * (600000 - pa))
add(rnd(MAXN, "abc?", [30, 30, 30, 10]), "a" * 135000 + "b" * 135000 + "c" * 180000)
add(rnd(MAXN, LOW + "?"), rnd(1, LOW))
add(planted(MAXN, shuffled(LOW), 5000, LOW, 0.0), shuffled(LOW))
t = rnd(MAXN, LOW + "?")
add(t, t[300000:300000 + m].replace("?", "a"))                                      # a window of t itself
add(rnd(MAXN, "ab?", [40, 40, 20]), "a" * 100000 + "b" * 100000)                   # shorter P, many hits
add(rnd(MAXN, "abcd?", [24, 24, 24, 24, 4]), "".join(sorted(rnd(150000, "abcd"))))

for t in tests:
    assert t.endswith("\n") and " " not in t
    assert not t.encode().translate(None, bytes(range(32, 127)) + b"\n")
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
