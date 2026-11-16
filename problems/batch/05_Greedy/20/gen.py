# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(30320)
MAXN = 50_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(pairs):
    n = len(pairs)
    assert 1 <= n <= MAXN
    lines = [f"{n}\n"]
    for q in pairs:
        assert len(q) == 4 and all(1 <= x <= MAXV for x in q)
        lines.append("%d %d %d %d\n" % q)
    tests.append("".join(lines))


def rnd(n, wlo, whi, slo, shi):
    return [(ri(wlo, whi), ri(slo, shi), ri(wlo, whi), ri(slo, shi)) for _ in range(n)]


def trap(n, big):
    """a heavy weak acrobat with a light, slightly stronger partner: the stronger one must stand on top"""
    res = []
    for _ in range(n):
        s = ri(big // 10, big)
        heavy = (ri(big // 2, big), ri(1, s - 1))
        light = (ri(1, big // 100), ri(s, min(MAXV, s + big // 50)))
        q = heavy + light if random.random() < 0.5 else light + heavy
        res.append(q)
    return res


def trap2(n, big):
    """a heavy but weak acrobat with a lighter strong partner: the heavy one must stand on top"""
    res = []
    for _ in range(n):
        heavy = (ri(big // 5, big // 3), ri(1, big // 100))
        light = (ri(big // 20, big // 10), ri(big // 2, big))
        q = heavy + light if random.random() < 0.5 else light + heavy
        res.append(q)
    return res


def same_key(n, total):
    """every acrobat has w + s = total"""
    res = []
    for _ in range(n):
        w1, w2 = ri(1, total - 1), ri(1, total - 1)
        res.append((w1, total - w1, w2, total - w2))
    return res


# samples
add([(3, 2, 1, 6), (2, 1, 2, 3)])
add([(100, 50, 1, 60)])
add([(5, 5, 5, 5), (1, 1, 1, 1), (3, 9, 4, 2)])
add([(10, 3, 2, 8), (6, 6, 1, 1), (4, 12, 7, 5)])
add([(2, 7, 3, 4), (8, 1, 1, 9), (5, 5, 5, 5), (1, 2, 9, 3)])
add([(4, 20, 6, 3), (1, 9, 2, 30)])
# hidden (small, every arrangement is tried by brute.cpp)
add([(1, 1, 1, 1)])
add([(MAXV, MAXV, MAXV, MAXV)] * 3)
add([(MAXV, 1, 1, MAXV)])
add(rnd(4, 1, 10, 1, 10))
add(rnd(5, 1, 100, 1, 300))
add(trap(6, 1000))
add(same_key(7, 50))
add(rnd(8, 1, MAXV, 1, MAXV))
add(rnd(8, 1, 1000, 1, 10))
add(trap2(8, 1000))
# large
N = MAXN
add(rnd(N, 1, MAXV, 1, MAXV))
add(rnd(N, 1, 1000, 1, MAXV))
add(rnd(N, 1, MAXV, 1, 1000))
add([(MAXV, MAXV, MAXV, MAXV)] * N)
add([(1, 1, 1, 1)] * N)
add(trap(N, MAXV))
mix = trap2(N // 2, 10**6) + trap(N // 2, MAXV)              # the trap blocks are at the bottom
random.shuffle(mix)
add(mix)
add(same_key(N, MAXV))
add(rnd(N, 1, 10**5, 1, 10**9))
add(sorted(rnd(N, 1, MAXV, 1, MAXV), key=lambda q: -(q[0] + q[1] + q[2] + q[3])))
add([(w, s, w, s) for w, s, _, _ in rnd(N, 1, MAXV, 1, MAXV)])
add(rnd(N, 1, 10, 1, 10))
add(trap2(N, MAXV))
mix = trap(N // 2, 10**6) + trap2(N // 2, MAXV)              # the trap2 blocks are at the bottom
random.shuffle(mix)
add(mix)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
