# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(12006)
MAXN = 300_000
MAXM = 100_000
MAXD = 1000
tests = []


def add(n, cmds, batches):
    m, k = len(cmds), len(batches)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and 1 <= k <= MAXM
    assert all(1 <= l <= r <= n and 1 <= d <= MAXD for l, r, d in cmds)
    assert all(1 <= x <= y <= m for x, y in batches)
    tests.append(f"{n} {m} {k}\n" + "".join(f"{l} {r} {d}\n" for l, r, d in cmds)
                 + "".join(f"{x} {y}\n" for x, y in batches))


def rng(n, lo_len=1, hi_len=None):
    """a random range of 1..n with length between lo_len and hi_len"""
    hi_len = n if hi_len is None else min(hi_len, n)
    ln = random.randint(min(lo_len, hi_len), hi_len)
    s = random.randint(1, n - ln + 1)
    return s, s + ln - 1


def cmds_of(n, m, lo_len=1, hi_len=None, dmax=MAXD):
    return [rng(n, lo_len, hi_len) + (random.randint(1, dmax),) for _ in range(m)]


def batches_of(m, k, lo_len=1, hi_len=None):
    return [rng(m, lo_len, hi_len) for _ in range(k)]


# samples
add(5, [(1, 3, 2), (2, 5, 1), (4, 4, 5)], [(1, 2), (2, 3)])
add(4, [(1, 4, 1), (2, 3, 10)], [(2, 2), (1, 1), (2, 2)])
add(6, [(1, 1, 7), (6, 6, 3), (2, 5, 1)], [(1, 3)])
add(3, [(1, 3, 1000)], [(1, 1)] * 4)
add(7, [(3, 7, 4), (1, 2, 9), (2, 6, 1), (5, 5, 6)], [(2, 4), (1, 1), (3, 3)])
# hidden (small)
add(1, [(1, 1, 1)], [(1, 1)])
add(1, [(1, 1, MAXD)] * 3, [(1, 3), (2, 3), (3, 3)])
add(30, cmds_of(30, 20, dmax=5), batches_of(20, 40))
add(200, cmds_of(200, 150), batches_of(150, 200))
add(300, [(1, 300, MAXD)] * 300, [(1, 300)] * 300)
# large: "run every command of every batch" needs sum of batch lengths (up to K M = 10^10) steps,
# "add d * times over every lamp of every command" needs sum of command lengths (up to M N = 3*10^10)
n, m, k = MAXN, MAXM, MAXM
add(n, [(1, n, MAXD)] * m, [(1, m)] * k)                            # every lamp gets 10^13
add(n, cmds_of(n, m), batches_of(m, k))
add(n, cmds_of(n, m, n - 1000, dmax=9), batches_of(m, k, m - 1000))  # long commands, long batches
add(n, cmds_of(n, m, 1, 20), batches_of(m, k, m - 1000))           # short commands, long batches
add(n, cmds_of(n, m, n - 1000, dmax=9), batches_of(m, k, 1, 3))    # long commands, short batches
add(n, cmds_of(n, m), batches_of(m, k, 1, 5))                    # random commands, short batches
add(m, [(i, i, MAXD) for i in range(1, m + 1)], [(1, m)] * k)      # one command per lamp
add(n, [(1, n - i + 1, random.randint(1, MAXD)) for i in range(1, m + 1)], [(x, m) for x in range(1, k + 1)])
add(n, [(i, n, MAXD) for i in range(1, m + 1)], [(1, y) for y in range(1, k + 1)])
add(n, cmds_of(n, m), [(1, 1)] * (k // 2) + [(m, m)] * (k // 2))   # only the end commands run
add(n, cmds_of(n, m, n // 2, dmax=9), [(random.randint(1, 100), random.randint(m - 100, m)) for _ in range(k)])
add(n, [(1, n, random.randint(1, MAXD)) for _ in range(m)], batches_of(m, k, 1, 2))   # whole street, short batches
add(n, cmds_of(n, m, n - 5000, dmax=9), batches_of(m, k, 1, 50))
add(n, cmds_of(n, m, n // 2, dmax=99), batches_of(m, k, m // 2))
add(2000, cmds_of(2000, m), batches_of(m, k))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
