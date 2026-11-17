# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random, itertools

random.seed(160101)
MAXT, MAXSUM = 100_000, 300_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def need(a):
    st, nxt, best = [], 1, 0
    for x in a:
        while nxt <= x:
            st.append(nxt)
            nxt += 1
            best = max(best, len(st))
        if st[-1] != x:
            return -1
        st.pop()
    return best


def triple(a):
    return any(a[i + 1] < a[i + 2] < a[i] for i in range(len(a) - 2))


def add(trains):
    t = len(trains)
    assert 1 <= t <= MAXT and sum(len(a) for a in trains) <= MAXSUM
    for a in trains:
        assert len(a) >= 1 and sorted(a) == list(range(1, len(a) + 1))
    tests.append(f"{t}\n" + "".join(f"{len(a)}\n" + " ".join(map(str, a)) + "\n" for a in trains))
    assert len(tests[-1]) <= 3_000_000


def valid(n, p_push=0.5):
    out, st, nxt = [], [], 1
    while len(out) < n:
        if nxt <= n and (not st or random.random() < p_push):
            st.append(nxt)
            nxt += 1
        else:
            out.append(st.pop())
    return out


def broken_tail(m, tail):
    return valid(m) + [m + x for x in tail]


add([[3, 2, 5, 4, 1], [3, 1, 2, 4, 5]])
add([[1, 2, 3, 4], [4, 3, 2, 1]])
add([[1]])
add([[2, 1, 4, 3, 6, 5], [3, 4, 2, 6, 5, 1], [1, 5, 3, 4, 2, 6]])
add([[4, 5, 3, 6, 2, 7, 1], [2, 3, 1]])

add([list(p) for k in range(1, 5) for p in itertools.permutations(range(1, k + 1))])
add([list(p) for p in itertools.permutations(range(1, 7))])
trains = []
for _ in range(3000):
    n = ri(5, 10)
    a = list(range(1, n + 1))
    random.shuffle(a)
    trains.append(a if random.random() < 0.6 else valid(n, random.random()))
add(trains)
trains = []
for _ in range(400):
    n = ri(10, 120)
    a = valid(n, random.choice([0.3, 0.5, 0.8]))
    if random.random() < 0.4:
        i, j = random.sample(range(n), 2)
        a[i], a[j] = a[j], a[i]
    trains.append(a)
add(trains)
trains = []
for _ in range(60):
    n = ri(500, 1500)
    a = valid(n, random.random())
    if random.random() < 0.5:
        a = broken_tail(n - 4, [3, 1, 4, 2]) if random.random() < 0.5 else a[::-1]
    trains.append(a)
add(trains)

N = MAXSUM
add([list(range(1, N + 1))])
add([list(range(N, 0, -1))])
add([valid(N, 0.5)])
add([valid(N, 0.62)])
B = 1000
add([[x for s in range(0, N, B) for x in range(s + B, s, -1)]])
add([list(range(N // 2, 0, -1)) + list(range(N // 2 + 1, N + 1))])
a = broken_tail(N - 4, [3, 1, 4, 2])
assert not triple(a)
add([a])
a = broken_tail(N - 6, [4, 2, 5, 1, 6, 3])
assert not triple(a)
add([a])


def stuck_then(m, l, n2):
    first = [m] + list(range(m - 1, l, -1)) + [m + 3, m + 1, m + 4, m + 2] + list(range(l, 0, -1))
    return [first, list(range(1, n2 + 1))]


add(stuck_then(140_000, 40_000, 150_000 - 4))
tr = stuck_then(90_000, 30_000, 100_000 - 4)
add(tr + [valid(100_000, 0.55)])
big = valid(200_000, 0.5)
small = [[2, 1], [1, 2], [3, 1, 2], [2, 3, 1]] * 10_000
add([big] + small)
for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t


exp = [[3, -1], [1, 4], [1], [2, 3, -1], [4, 2]]
for k, e in enumerate(exp):
    lines = tests[k].split("\n")
    trains = [list(map(int, lines[2 + 2 * j].split())) for j in range(int(lines[0]))]
    assert [need(a) for a in trains] == e
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
