# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(60016)
MAXM, MAXQ, MAXV = 200, 200_000, 200_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(moves, piles):
    m, q = len(moves), len(piles)
    assert 1 <= m <= MAXM and 1 <= q <= MAXQ
    assert len(set(moves)) == m and all(1 <= x <= MAXV for x in moves)
    assert all(1 <= x <= MAXV for x in piles)
    tests.append(f"{m} {q}\n" + " ".join(map(str, moves)) + "\n" + " ".join(map(str, piles)) + "\n")


def piles_upto(q, hi):
    p = [ri(1, hi) for _ in range(q)]
    p[ri(0, q - 1)] = hi
    return p


def moves_in(m, hi):
    return random.sample(range(1, hi + 1), m)


# samples
add([1, 3], [2, 4])
add([2], [1, 2, 4])
add([1, 2, 3], [4, 5, 6, 7, 8])
add([3, 2], [1, 5, 6, 7, 8])
add([7, 2, 5, 4], [1, 9, 15, 12])
add([10], [9, 20, 199999])
# hidden: small (the game tree is searched directly)
add([1], list(range(1, 25)))
add([1, 2], list(range(1, 25)))
add([2, 5], list(range(1, 25)))
add([1, 4, 6], list(range(1, 25)))
add([3, 4, 5, 6], list(range(1, 23)))
add([24], [23, 24])
# hidden: medium (the full table of brute.cpp still checks these)
add(moves_in(30, 60), list(range(1, 2001)))
add(list(range(1, 51)), piles_upto(2000, 3000))
add(moves_in(80, 3000), piles_upto(3000, 3000))
# hidden: maximum size
Q, V = MAXQ, MAXV
add(list(range(1, 201)), piles_upto(Q, V))                 # long scans for every position
add(list(range(200, 0, -1)), list(range(V, V - Q, -1)))
add(list(range(1, 400, 2)), piles_upto(Q, V))              # odd sizes only
add([1] + list(range(2, 400, 2))[:199], piles_upto(Q, V))
add(moves_in(200, 500), piles_upto(Q, V))
add(moves_in(200, 1000), piles_upto(Q, V))
add(moves_in(200, 5000), piles_upto(Q, V))
add(moves_in(200, V), piles_upto(Q, V))
add(sorted(moves_in(199, 300)) + [V], piles_upto(Q, V))
add([1, 2], piles_upto(Q, V))
add([ri(1000, 2000) for _ in range(1)] + [V], piles_upto(Q, 999))   # no move fits at all
add([3 * i + 1 for i in range(200)], [V] * Q)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
