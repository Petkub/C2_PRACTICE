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


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def mixed(q, small, big=MAXV, share=0.5):
    return [random.randint(0, small if random.random() < share else big) for _ in range(q)]


add([40, 3, 8, 10, 15, 22], [4, 10, 0])
add([5, 9, 5, 5], [3, 100])
add([7], [0, MAXV])
add([0, MAXV, 500000000], [MAXV, 7])
add([1, 13, 6, 30, 2, 21, 9], [2, 6, 10, 1000])

add([10, 20], [0, 5, 10, 15, 20])
add([8, 2, 5], [3, 6, 2, 1])
add([28, 39, 11, 1, 44, 28, 12, 36], [60, 1, 10, 16, 31, 5, 59, 51, 16, 10])
add([598, 403, 666, 812, 110, 617, 914, 192, 231, 138], [954, 892, 504, 620, 146, 49, 54, 158, 792, 39, 899, 507])
add([64, 2, 4, 8, 16, 32, 1, 128, 256, 512, 1024, 2048], [0, 1, 3, 8, 100, 512, 1024, 2048, 5000])
add([696831685, 946970824, 191142626, 986844296, 252925111, 59584338, 166794482, 309086891, 916341115, 87391148,
     699557555, 774287385],
    [2725870, 79498008, 74729830, 61782485, 39873472, 873237318, 422430531, 24348144, 39873472, 74729830,
     395026011, 387744794, 56161780, 694550443, 930363721])
add([5] * 6 + [100] * 6, [0, 1, 94, 95, 96, MAXV])

add([500000] + rnd(1999, 0, 10**6), mixed(2000, 3000, 10**6, 0.9))
add([MAXV // 2] + rnd(4999, 0, MAXV), mixed(5000, 10**6))

N, Q = MAXN, MAXQ
add(rnd(N, 0, MAXV), mixed(Q, 20000))
a = [i * 5000 for i in range(N)]
random.shuffle(a)
add(a, [random.choice([4999, 5000, 5001, random.randint(0, 10**4)]) for _ in range(Q)])
add([123456789] * N, rnd(Q, 0, MAXV))
a = rnd(N // 2, 0, 10**5) + rnd(N // 2, MAXV - 10**5, MAXV)
random.shuffle(a)
add(a, mixed(Q, 12, MAXV, 0.7))
add([400000] + rnd(N - 1, 0, 10**6), mixed(Q, 60, 10**6, 0.9))
x, a = 0, []
for i in range(N):
    x += random.choice([0, 1, 7, 100, 3000, random.randint(0, 9000)])
    a.append(x)
assert a[-1] <= MAXV
random.shuffle(a)
add(a, mixed(Q, 120, 10**4))
add([25000] + rnd(N - 1, 0, 50000), mixed(Q, 5, 50000, 0.8))
a = [random.choice([0, 1, 2, 10**8, 5 * 10**8, MAXV]) for _ in range(N)]
add([10**8] + a[1:], [random.choice([0, 1, 2, 3, 10**8, 4 * 10**8, 5 * 10**8, MAXV, random.randint(0, MAXV)])
                      for _ in range(Q)])
add([MAXV // 3] + rnd(N - 1, 0, MAXV), [MAXV - i % 7 for i in range(Q)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
