# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4802)
MAXN, MAXQ, MAXV = 200000, 100000, 10**9
tests = []


def add(a, ds):
    n, q = len(a), len(ds)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= x <= MAXV for x in a)
    assert all(0 <= d <= MAXV for d in ds)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{d}\n" for d in ds))


def queries(a, q, hi=MAXV, share=0.5):
    s = sorted(a)
    own = [s[i + 1] - s[i] for i in range(len(s) - 1)] or [0]
    out = []
    for _ in range(q):
        if random.random() < share:
            out.append(random.choice(own))
        else:
            out.append(random.randint(0, hi))
    return out


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def mid_first(a):
    s = sorted(a)
    m = s[len(s) // 2]
    a = a[:]
    i = a.index(m)
    a[0], a[i] = a[i], a[0]
    return a


add([40, 3, 8, 10, 15, 22], [4, 10, 0])
add([5, 9, 5, 5], [3, 100])
add([7], [0, MAXV])
add([0, MAXV, 500000000], [MAXV, 7])
add([1, 13, 6, 30, 2, 21, 9], [2, 6, 10, 1000])

add([10, 20], [0, 5, 10, 15, 20])
add([8, 2, 5], [3, 6, 2, 1])
a = rnd(8, 0, 50)
add(mid_first(a), queries(a, 10, 60))
a = rnd(10, 0, 1000)
add(mid_first(a), queries(a, 12, 1000))
a = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
add(mid_first(a), [0, 1, 3, 8, 100, 512, 1024, 2048, 5000])
a = rnd(12, 0, MAXV)
add(mid_first(a), queries(a, 15))
a = [5] * 6 + [100] * 6
add(a, [0, 1, 94, 95, 96, MAXV])

a = rnd(2000, 0, 10**6)
add(mid_first(a), queries(a, 2000, 3000))
a = rnd(5000, 0, MAXV)
add(mid_first(a), queries(a, 5000))

N, Q = MAXN, MAXQ
a = rnd(N, 0, MAXV)
add(mid_first(a), queries(a, Q))
a = [i * 5000 for i in range(N)]
random.shuffle(a)
add(mid_first(a), [random.choice([4999, 5000, 5001, random.randint(0, 10**4)]) for _ in range(Q)])
add([MAXV] * N, rnd(Q, 0, MAXV))
a = rnd(N // 2, 0, 10**5) + rnd(N // 2, MAXV - 10**5, MAXV)
random.shuffle(a)
add(mid_first(a), queries(a, Q, MAXV, 0.3))
a = rnd(N, 0, 10**6)
add(mid_first(a), queries(a, Q, 60, 0.6))
x, a = 0, []
for i in range(N):
    x += random.choice([0, 1, 7, 100, 3000, random.randint(0, 9000)])
    a.append(x)
assert a[-1] <= MAXV
random.shuffle(a)
add(mid_first(a), queries(a, Q, 10**4))
a = sorted(rnd(N, 0, MAXV))
add(a[N // 3:] + a[:N // 3], queries(a, Q))
a = [random.choice([0, 1, 2, 10**8, 5 * 10**8, MAXV]) for _ in range(N)]
add(mid_first(a), queries(a, Q, MAXV, 0.8))
a = rnd(N, 0, MAXV)
add(mid_first(a), [MAXV - i % 7 for i in range(Q)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
