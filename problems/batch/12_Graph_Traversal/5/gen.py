# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7005)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges):
    m = len(edges)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in edges))


def shuffled(n, edges):
    """random student numbers, random order of pairs and of the two ends"""
    p = list(range(1, n + 1))
    random.shuffle(p)
    res = [(p[a - 1], p[b - 1]) if random.random() < 0.5 else (p[b - 1], p[a - 1]) for a, b in edges]
    random.shuffle(res)
    return res


def bip(n, m, side=None):
    """random pairs between a hidden split of the students (always possible)"""
    if side is None:
        side = [random.random() < 0.5 for _ in range(n + 1)]
    left = [i for i in range(1, n + 1) if side[i]]
    right = [i for i in range(1, n + 1) if not side[i]]
    if not left or not right:
        return []
    return [(left[ri(0, len(left) - 1)], right[ri(0, len(right) - 1)]) for _ in range(m)]


def path(n):
    return [(i, i + 1) for i in range(1, n)]


# samples
add(5, [(1, 3), (3, 5), (2, 4)])
add(3, [(1, 2), (2, 3), (3, 1)])
add(1, [])
add(4, [(4, 2), (2, 3)])
add(6, [(1, 2), (2, 3), (3, 4), (4, 1), (2, 1), (5, 6)])
add(7, [(1, 2), (3, 4), (4, 5), (5, 6), (6, 7), (7, 3)])
# hidden: small (every assignment is tried)
add(2, [(2, 1), (1, 2)])
add(3, [])
add(4, [(4, 3), (3, 2), (2, 1)])
add(8, shuffled(8, path(8)))
add(9, shuffled(9, path(9) + [(9, 1)]))                      # an odd cycle
add(10, shuffled(10, path(10) + [(10, 1)]))                  # an even cycle
add(12, bip(12, 15))
add(14, bip(14, 10))
add(16, bip(16, 20) + [(3, 5)])                              # one extra pair may spoil it
add(18, [(i, i + 2) for i in range(1, 17)])
add(20, bip(20, 25))
add(20, bip(20, 30) + [(7, 13), (13, 19), (19, 7)])
# hidden: medium
add(2000, bip(2000, 3000))
add(3000, shuffled(3000, path(3000) + [(1, 3000)]))
# hidden: large
N = MAXN
add(N, shuffled(N, path(N)))                                 # one long chain
add(N, shuffled(N, path(N) + [(1, N - 1)]))                  # an odd cycle through almost everybody
add(N, shuffled(N, path(N) + [(1, N)]))                      # an even cycle through everybody
add(N, [(1, i) for i in range(2, N + 1)])                    # a star
add(N, bip(N, MAXM))
chords = []
while len(chords) < MAXM - N:                                # chain with chords of odd length (still possible)
    a = ri(1, N - 1)
    b = a + 2 * ri(0, min(1000, (N - a - 1) // 2)) + 1
    chords.append((a, b))
x = ri(1000, N - 1000)
add(N, shuffled(N, path(N) + chords[:-1] + [(x, x + 2)]))    # ... and one chord of even length
add(N, [])
add(N, bip(N, N // 3))                                       # many groups
add(N, bip(N, MAXM - 3) + [(N - 2, N - 1), (N - 1, N), (N, N - 2)])   # a triangle among the last students
add(N, [(2 * i - 1, 2 * i) for i in range(1, N // 2 + 1)])
add(N, shuffled(N, chords + path(N)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
