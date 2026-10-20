# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(11016)
MAXN, MAXQ, MAXS, MAXK = 200_000, 200_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(seats, ops):
    n, q = len(seats), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= s <= MAXS for s in seats)
    lines = []
    for j, op in enumerate(ops, 1):
        if op[0] == 'B':
            a, b, k = op[1:]
            assert 0 <= a < b <= n and 1 <= k <= MAXK
            lines.append(f"B {a} {b} {k}")
        else:
            assert 1 <= op[1] < j
            lines.append(f"C {op[1]}")
    tests.append(f"{n} {q}\n" + " ".join(map(str, seats)) + "\n" + "\n".join(lines) + "\n")


def ops_of(n, q, trip, seats_k, cancel=0.0, recent=0):
    """trip() -> (a, b); seats_k() -> k; a share `cancel` of the operations cancel an earlier booking
    (a recent one when recent > 0, so that it is likely still active)"""
    ops, books = [], []
    for j in range(1, q + 1):
        if books and random.random() < cancel:
            if recent:
                ops.append(('C', books[max(0, len(books) - ri(1, recent))]))
            else:
                ops.append(('C', random.choice(books)))
        else:
            a, b = trip()
            ops.append(('B', a, b, seats_k()))
            books.append(j)
    return ops


def long_trip(n, slack):
    def f():
        a = ri(0, slack)
        b = ri(max(a + 1, n - slack), n)
        return a, b
    return f


def any_trip(n):
    def f():
        a = ri(0, n - 1)
        return a, ri(a + 1, n)
    return f


def short_trip(n, d):
    def f():
        a = ri(0, n - 1)
        return a, min(n, a + ri(1, d))
    return f


def steady(n, q, lo, hi, edge, cancel, kmax):
    """segments 1..edge and n-edge+1..n have MAXS seats, the middle has lo..hi; every trip covers the whole
    middle, so the free seats of every trip are min(middle) - (seats of the active bookings): the generator
    follows them exactly and asks for exactly the free seats, one more, small and large numbers"""
    mid = [ri(lo, hi) for _ in range(n - 2 * edge)]
    seats = [MAXS] * edge + mid + [MAXS] * edge
    free, ops, active = min(mid), [], {}
    for j in range(1, q + 1):
        if active and random.random() < cancel:
            if random.random() < 0.9:
                x = random.choice(sorted(active)) if len(active) < 50 else max(active) - ri(0, 20)
                while x not in active:
                    x -= 1
                free += active.pop(x)
            else:
                x = ri(1, j - 1)                            # often refused or already cancelled
                if x in active:
                    free += active.pop(x)
            ops.append(('C', x))
            continue
        a, b = ri(0, edge - 1), ri(n - edge + 1, n)
        r = random.random()
        if free > 0 and r < 0.3:
            k = free                                        # exactly fits
        elif r < 0.5:
            k = free + 1                                    # one too many
        elif r < 0.6:
            k = ri(free + 1, max(free + 1, kmax))
        else:
            k = ri(1, max(1, min(kmax, free // 8 + 1)))
        k = max(1, min(k, MAXK))
        ops.append(('B', a, b, k))
        if k <= free:
            free -= k
            active[j] = k
    return seats, ops


# samples
add([3, 5, 2, 4, 4], [('B', 0, 2, 3), ('B', 1, 4, 2), ('B', 3, 5, 3), ('C', 2), ('B', 3, 5, 3), ('B', 0, 1, 1)])
add([1, 1, 1], [('B', 0, 1, 1), ('B', 1, 3, 1), ('B', 0, 3, 1), ('C', 3), ('C', 1), ('B', 0, 1, 2)])
add([2, 2, 2], [('B', 0, 3, 2), ('C', 1), ('C', 1), ('B', 1, 3, 3)])
add([MAXS, 7], [('B', 0, 1, MAXK), ('B', 0, 2, 1), ('B', 1, 2, 8)])
add([0], [('B', 0, 1, 1), ('C', 1)])
# hidden: small
for n, q, smax, kmax, c in ((1, 6, 3, 3, 0.3), (5, 20, 5, 3, 0.3), (10, 40, 10, 6, 0.25),
                            (30, 200, 40, 15, 0.3), (200, 2000, 1000, 300, 0.3)):
    s = [ri(0, smax) for _ in range(n)]
    add(s, ops_of(n, q, any_trip(n), lambda: ri(1, kmax), c, 5))
n = 3000
s = [ri(0, 10**6) for _ in range(n)]
add(s, ops_of(n, 3000, any_trip(n), lambda: ri(1, 3000), 0.3, 8))
s = [MAXS] * n
add(s, ops_of(n, 3000, short_trip(n, 20), lambda: ri(MAXK // 2, MAXK), 0.4, 3))
# hidden: maximum size (inputs kept near 3 MB: either N or Q at the maximum)
N, Q = MAXN, MAXQ
mostly_small = lambda big: (lambda: big if random.random() < 0.1 else ri(1, 9))
s = [10**6] * N                                             # every booking is accepted
add(s, ops_of(N, Q // 2, long_trip(N, 50), lambda: ri(1, 9), 0.2))
s = [ri(10**6 - 100, 10**6) for _ in range(N)]              # refused only when k is huge
add(s, ops_of(N, Q // 2, long_trip(N, 99), mostly_small(10**6), 0.1))
add(*steady(N, Q // 2, 10**4, 99_999, 50, 0.3, 10**4))       # a steady mix of OK and refusals
s = [ri(0, MAXS) for _ in range(N // 2)]
add(s, ops_of(N // 2, Q // 2, any_trip(N // 2), lambda: ri(1, MAXK // 1000), 0.3, 50))
s = [10**5 + abs(i - N // 2) for i in range(N)]             # one narrowest segment in the middle
add(s, ops_of(N, Q // 2, long_trip(N, N // 4), lambda: ri(1, 3), 0.2, 20))
s = [99_999] * N
s[N // 2] = 5000                                            # trips that end or start right at the bottleneck
trip = lambda: random.choice(((ri(0, 20), N // 2), (N // 2 + 1, ri(N - 20, N)), (ri(0, 20), ri(N - 20, N))))
add(s, ops_of(N, Q // 2, trip, lambda: ri(1, 9), 0.4, 3))
s = [ri(0, 9) for _ in range(N)]
s[ri(0, N - 1)] = 0                                         # nothing can ever be sold
add(s, ops_of(N, Q // 2 + 30000, long_trip(N, 9), lambda: 1, 0.1))
add(*steady(N // 2, Q // 2, 5 * 10**8, MAXS, 9, 0.35, MAXK))
s = [ri(0, 10**4) for _ in range(N)]
add(s, ops_of(N, Q // 2, short_trip(N, 50), lambda: ri(1, 200), 0.3, 10))
add(*steady(120_000, 150_000, 5000, 5000, 1, 0.35, 5000))     # the whole line every time
add(*steady(N, Q // 2, 1, 999, 30, 0.4, 999))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
