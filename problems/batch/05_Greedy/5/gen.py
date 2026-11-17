# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(5003)
MAXN, MAXQ, MAXV, MAXG = 100_000, 100_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(matches, gs):
    n, q = len(matches), len(gs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= s <= MAXV and 0 <= r <= MAXV for s, r in matches)
    assert all(0 <= g <= MAXG for g in gs)
    tests.append(f"{n} {q}\n" + "".join(f"{s} {r}\n" for s, r in matches) + " ".join(map(str, gs)) + "\n")


def match_with(d):
    """a match whose score difference r - s is d (d < 0: a win by -d points)"""
    if d >= 0:
        s = ri(0, MAXV - d)
        return (s, s + d)
    r = ri(0, MAXV + d)
    return (r - d, r)


def small_match(d):
    s = ri(0, 20)
    return (s, s + d) if d >= 0 else (s - d, s)


def thresholds(matches):
    """bonus amounts where the answer changes (each with its neighbours)"""
    draws = sum(1 for s, r in matches if s == r)
    need = sorted(r - s for s, r in matches if s < r)
    pts, acc = [], draws
    out = list(range(0, draws + 2))
    for d in need:
        out += [acc + d - 1, acc + d, acc + d + 1]
        acc += d + 1
    out += [acc - 1, acc, acc + 1]
    return [g for g in out if 0 <= g <= MAXG], acc


# samples
add([(2, 2), (1, 3), (5, 0), (0, 1)], [0, 1, 4, 6])
add([(0, 5), (2, 7), (10, 15)], [3, 6, 12, 18])
add([(10, 3)], [0, 5])
add([(7, 7), (0, 0), (4, 4)], [1, 2, 5])
add([(3, 9), (9, 3), (4, 4), (0, 2), (1, 1), (6, 6), (12, 13)], [0, 2, 3, 5, 8, 15])
# hidden: small
add([(0, 10**9)], [0, 10**9 - 1, 10**9])                      # one loss: nothing, a draw, still not a win
add([(5, 5)], [0, 1, 10**9])
add([(0, 3), (0, 3), (0, 3)], list(range(0, 14)))             # equal losses, every budget
add([(4, 0), (2, 1), (8, 3)], [0, 7, 10**9])                  # only wins
for n, q in [(6, 40), (10, 60), (25, 80)]:
    ms = [small_match(ri(-3, 6)) for _ in range(n)]
    gs, tot = thresholds(ms)
    gs += [ri(0, tot + 3) for _ in range(q)]
    random.shuffle(gs)
    add(ms, gs[:q])
ms = [small_match(ri(-50, 100)) for _ in range(2000)]
gs, tot = thresholds(ms)
random.shuffle(gs)
add(ms, gs[:3000] + [ri(0, tot) for _ in range(1000)])
ms = [match_with(ri(-MAXV, MAXV)) for _ in range(3000)]       # big differences: prefix sums pass 2^31 quickly
gs, tot = thresholds(ms)
gs = [g for g in gs if g <= MAXG]
random.shuffle(gs)
add(ms, gs[:3000] + [ri(0, MAXG) for _ in range(2000)])

ms = [small_match(ri(0, 50)) for _ in range(9000)] + [match_with(ri(MAXV // 2, MAXV)) for _ in range(1000)]
_, cheap = thresholds(ms[:9000])
random.shuffle(ms)
add(ms, [ri(cheap, MAXG) for _ in range(10000)])              # medium: past the cheap losses into the huge ones


# hidden: maximum size (every question affords many wins, so walking the losses per question is too slow)
def big(ms, gs):
    random.shuffle(ms)
    add(ms, gs)


def near(tot, lo_frac=0.5):
    return [ri(int(tot * lo_frac), max(int(tot * lo_frac), tot - 1)) for _ in range(MAXQ)]


def huge_losses(k):
    return [match_with(ri(MAXV // 2, MAXV)) for _ in range(k)]


def cheap_then_huge(cheap, gs_desc=False):
    """cheap matches plus 10% losses by more than 5 * 10^8; questions afford every cheap loss"""
    _, tot = thresholds(cheap)
    gs = [ri(tot, MAXG) for _ in range(MAXQ)]
    if gs_desc:
        gs.sort(reverse=True)
    big(cheap + huge_losses(N // 10), gs)


N = MAXN
ms = [small_match(ri(-5, 1000)) for _ in range(N)]
_, tot = thresholds(ms)
big(ms, near(tot))                                            # mixed results, small differences
ms = [small_match(ri(1, 10**4)) for _ in range(N)]            # only losses
th, tot = thresholds(ms)
gs = [g for g in th if g <= MAXG and g >= tot // 3]
random.shuffle(gs)
big(ms, (gs + near(tot, 0.4))[:MAXQ])                        # many questions on the draw/win boundaries
cheap_then_huge([small_match(ri(1, 100)) for _ in range(N - N // 10)])
ms = [(s, s) for s in (ri(0, MAXV) for _ in range(N * 3 // 10))] + [small_match(1) for _ in range(N * 7 // 10)]
_, tot = thresholds(ms)
big(ms, [ri(tot - 5, MAXG) for _ in range(MAXQ)])            # draws and losses by one: everything is affordable
cheap_then_huge([match_with(ri(0, 2000)) for _ in range(N - N // 10)])
ms = [small_match(7) for _ in range(N)]
th, tot = thresholds(ms)
gs = [8 * k + 7 for k in range(N // 2, N)] + [8 * k + 6 for k in range(N // 2, N)]
random.shuffle(gs)
big(ms, gs[:MAXQ])                                            # all losses by 7: answers end in a draw or not
cheap_then_huge([small_match(ri(-3, 10)) for _ in range(N - N // 10)], True)    # questions descending
cheap_then_huge([match_with(ri(1, 2 * 10**4)) for _ in range(N - N // 10)])       # large scores

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
