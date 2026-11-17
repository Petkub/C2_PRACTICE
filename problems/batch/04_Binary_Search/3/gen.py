# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(40301)
MAXN = 100_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def answers(calls, wins, X, mode="good"):
    """direct count (small tests only); "nofilter" / "noshort" are the two classic mistakes"""
    res = []
    for a, w in wins:
        c = 0
        for s, t in calls:
            if mode == "good":
                ok = min(s + t, a + w) - max(s, a) >= X
            else:
                ok = s <= a + w - X and s + t >= a + X
                ok = ok and (w >= X if mode == "nofilter" else t >= X)
            c += ok
        res.append(c)
    return res


def add(X, calls, wins, sample=False):
    n, m = len(calls), len(wins)
    assert 1 <= n <= MAXN and 1 <= m <= MAXN and 1 <= X <= MAXV
    assert all(0 <= s <= MAXV and 1 <= t <= MAXV for s, t in calls)
    assert all(0 <= a <= MAXV and 1 <= w <= MAXV for a, w in wins)
    if sample:  # samples do not separate the correct method from the two classic mistakes
        good = answers(calls, wins, X)
        assert good == answers(calls, wins, X, "nofilter") == answers(calls, wins, X, "noshort")
    tests.append(f"{n} {m} {X}\n" + "".join(f"{s} {t}\n" for s, t in calls)
                 + "".join(f"{a} {w}\n" for a, w in wins))


def rnd_calls(n, hi, tlo, thi):
    return [(ri(0, hi), ri(tlo, thi)) for _ in range(n)]


def edge_wins(calls, m, X, wlo, whi):
    """sessions that start where a call ends, end where a call starts, or overlap a call by exactly X or X - 1"""
    res = []
    for _ in range(m):
        s, t = calls[ri(0, len(calls) - 1)]
        w = ri(wlo, whi)
        k = ri(0, 5)
        if k == 0:
            a = s + t                       # starts when the call ends
        elif k == 1:
            a = s - w                       # ends when the call starts
        elif k == 2:
            a = s + t - X                   # the end of the call overlaps by exactly X
        elif k == 3:
            a = s + t - X + 1               # ... by X - 1
        elif k == 4:
            a = s + X - w                   # the start of the call overlaps by exactly X
        else:
            a = s + ri(-w, t)
        res.append((min(MAXV, max(0, a)), w))
    return res


# samples
add(3, [(0, 10), (4, 3), (8, 6), (12, 5)], [(5, 5), (7, 4), (0, 20)], sample=True)
add(1, [(3, 4), (1, 9), (6, 7)], [(0, 3), (7, 3), (13, 5)], sample=True)
add(MAXV, [(0, MAXV)], [(0, MAXV)], sample=True)
add(5, [(MAXV, MAXV), (MAXV - 10, 20)], [(MAXV - 3, MAXV), (MAXV - 15, 9)], sample=True)
add(2, [(1, 4), (2, 2), (0, 9)], [(3, 3), (5, 2), (0, 1)], sample=True)
# hidden: small (checked by brute force)
add(1, [(5, 1)], [(4, 1), (5, 1), (6, 1), (4, 2), (0, 10)])
add(3, [(5, 2)], [(0, 10), (5, 2), (4, 1)])                     # a short call inside a long session
add(6, [(0, 20)], [(5, 3), (0, 6), (14, 6), (15, 6), (2, 5)])    # sessions shorter than X inside a long call
c = rnd_calls(60, 100, 1, 15)
add(7, c, edge_wins(c, 80, 7, 1, 20))
c = rnd_calls(800, 5000, 1, 400)
add(150, c, edge_wins(c, 900, 150, 1, 400))
c = rnd_calls(3000, MAXV, 1, MAXV)
add(ri(1, MAXV // 2), c, edge_wins(c, 3000, 1, 1, MAXV) + [(ri(0, MAXV), ri(1, MAXV)) for _ in range(500)])
c = rnd_calls(2000, MAXV, MAXV - 1000, MAXV)                     # every call ends after 2^31
add(MAXV - 500, c, [(ri(MAXV - 2000, MAXV), ri(MAXV - 1000, MAXV)) for _ in range(2000)])
# hidden: large values, smaller sizes (ends beyond 2^31)
N2 = 60_000
c = [(ri(MAXV // 2, MAXV), ri(MAXV // 2, MAXV)) for _ in range(N2)]
add(MAXV // 3, c, edge_wins(c, N2, MAXV // 3, 1, MAXV))
# hidden: maximum size
N, H = MAXN, 1_000_000
c = rnd_calls(N, H, 1, 1000)
add(1, c, edge_wins(c, N, 1, 1, 1000))                           # at least one second, touching ends
c = rnd_calls(N, H, 1, 1000)
add(500, c, edge_wins(c, N, 500, 1, 1000))                       # half the calls and sessions are too short
c = rnd_calls(N, H, 1, 600)
add(300, c, edge_wins(c, N, 300, 200, 5000))
c = [(ri(0, 1000), ri(H - 1000, H)) for _ in range(N)]           # long calls covering everything
add(2000, c, [(ri(0, H - 3000), ri(1, 3000)) for _ in range(N)])
c = rnd_calls(N, H, 1, 50) + []                                  # very short calls, very long sessions
add(40, c, [(ri(0, 1000), ri(H - 1000, H)) for _ in range(N)])
c = rnd_calls(N, 9999, 1, 9999)
add(ri(1, 9999), c, edge_wins(c, N, 5000, 1, 9999))
c = [(ri(0, H), 777) for _ in range(N)]                         # every call lasts exactly X
add(777, c, edge_wins(c, N, 777, 1, 2000))
c = rnd_calls(N // 2, H, 1, 99) + rnd_calls(N // 2, H, 100, 3000)
random.shuffle(c)
add(100, c, edge_wins(c, N, 100, 1, 3000))
c = rnd_calls(N, H, 1, H // 10)
add(ri(1, 30000), c, edge_wins(c, N, 30000, 1, H // 10))
c = [(ri(0, 100), ri(1, 2000)) for _ in range(N)]               # every call starts near 0
add(1000, c, [(ri(0, 2500), ri(1, 2500)) for _ in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
