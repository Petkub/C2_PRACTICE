# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(47004)
MAXN = MAXM = MAXQ = 100_000
MAXT = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, init, fr, calls):
    assert 1 <= n <= MAXN and 0 <= len(fr) <= MAXM and 0 <= len(calls) <= MAXQ
    assert 1 <= len(init) <= n and len(set(init)) == len(init) and all(1 <= s <= n for s in init)
    assert all(1 <= x <= n and 1 <= y <= n and x != y for x, y in fr)
    assert len({x * (n + 1) + y if x < y else y * (n + 1) + x for x, y in fr}) == len(fr)
    assert all(1 <= a <= n and 1 <= b <= n and a != b and 1 <= t <= MAXT for a, b, t in calls)
    tests.append(f"{n} {len(fr)} {len(calls)}\n{len(init)} {' '.join(map(str, init))}\n"
                 + "".join(f"{x} {y}\n" for x, y in fr) + "".join(f"{a} {b} {t}\n" for a, b, t in calls))


def shuffled(lst):
    keys = [random.random() for _ in lst]
    order = sorted(range(len(lst)), key=keys.__getitem__)
    return [lst[i] for i in order]


def relabel(n, init, fr, calls):
    p = shuffled(list(range(1, n + 1)))
    p = [0] + p
    fr = [(p[x], p[y]) if (x + y) % 2 else (p[y], p[x]) for x, y in fr]
    fr = shuffled(fr)
    calls = shuffled([(p[a], p[b], t) for a, b, t in calls])
    add(n, sorted(p[s] for s in init), fr, calls)


def tree(n, spread):
    return [(i, ri(max(1, i - spread), i - 1)) for i in range(2, n + 1)]


def extra_edges(n, fr, k):
    seen = {(min(x, y), max(x, y)) for x, y in fr}
    while k > 0:
        x, y = ri(1, n), ri(1, n)
        if x != y and (min(x, y), max(x, y)) not in seen:
            seen.add((min(x, y), max(x, y)))
            fr.append((x, y))
            k -= 1
    return fr


def rnd_calls(n, q, tlo, thi):
    res = []
    while len(res) < q:
        a, b = ri(1, n), ri(1, n)
        if a != b:
            res.append((a, b, ri(tlo, thi)))
    return res


def chain_calls(n, q, slack):
    res = []
    for _ in range(q):
        a = ri(1, n - 1)
        b = ri(a + 1, min(n, a + 3 * slack + 2))
        res.append((a, b, max(1, a + ri(-slack, slack))))
    return res


add(7, [1], [(1, 2), (2, 3), (3, 4), (4, 5)], [(1, 5, 2), (5, 6, 3), (3, 5, 2)])
add(5, [1, 5], [(1, 2), (2, 3)], [(5, 4, 7), (4, 3, 7)])
add(1, [1], [], [])
add(6, [2], [(2, 3), (4, 5)], [(3, 4, 1000000000), (6, 1, 5), (2, 3, 1)])
add(8, [3, 8], [(1, 2), (2, 3), (3, 4), (5, 6), (6, 7)], [(4, 5, 2), (8, 1, 1), (7, 1, 3)])

add(3, [1], [(1, 2)], [(2, 3, 1)])
add(3, [1], [(1, 2)], [(2, 3, 2)])
add(4, [1], [(1, 2), (2, 3), (3, 4)], [(1, 4, 9)])
add(4, [1], [], [(1, 2, 5), (2, 3, 5), (2, 4, 6), (3, 1, 1)])
for n, m, q, t in [(10, 12, 10, 6), (12, 8, 20, 10), (30, 40, 40, 15)]:
    fr = extra_edges(n, [], m)
    relabel(n, random.sample(range(1, n + 1), random.randint(1, 2)), fr, rnd_calls(n, q, 1, t))
n = 300
relabel(n, [1], [(i, i + 1) for i in range(1, n)], chain_calls(n, 300, 3))
n = 3000
relabel(n, [1, 2], tree(n, 30), rnd_calls(n, 3000, 1, 300))

N = MAXN
relabel(N, [1], [(i, i + 1) for i in range(1, N)], chain_calls(N, MAXQ, 5))
relabel(N, [1], [(i, i + 1) for i in range(1, N)], chain_calls(N, MAXQ, 200))
relabel(N, [1], tree(N, 3), rnd_calls(N, MAXQ, 1, 40000))
relabel(N, random.sample(range(1, N + 1), 3), extra_edges(N, tree(N, 50), MAXM - N + 1), rnd_calls(N, MAXQ, 1, 2000))
relabel(N, [1], [], [(i, i + 1, i) for i in range(1, N)])
fr, calls, now = [], [], 0
for i in range(1, N):
    if i % 3 == 1:
        fr.append((i, i + 1))
        now += 1
    else:
        before, now = now, now + 1 + random.choice((0, 0, 3))
        calls.append((i, i + 1, now))
        if i % 3 == 0:
            calls.append((i, i + 1, before))
relabel(N, [1], fr, calls)
calls = [(ri(1, N - 1), ri(1, N), ri(1, MAXT)) for _ in range(MAXQ)]
relabel(N, [1], [(i, i + 1) for i in range(1, N)], [(a, b, t) for a, b, t in calls if a != b])
relabel(N, [1], tree(N, N), rnd_calls(N, MAXQ, 1, 30))
add(N, list(range(1, 11)), extra_edges(N, [], MAXM), rnd_calls(N, MAXQ, 1, 25))
half = N // 2
fr = [(i, i + 1) for i in range(1, half)] + [(i, i + 1) for i in range(half + 1, N)]
relabel(N, [1, half + 1], fr, [(ri(1, half), ri(half + 1, N), ri(1, half))
                               for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
