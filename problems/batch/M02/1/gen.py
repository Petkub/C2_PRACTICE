# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4801)
MAXN, MAXA, MAXP, MAXD = 200000, 10**9, 10**9, 10**15
tests = []


def add(k, p, d, a):
    n = len(a)
    assert 1 <= k <= n <= MAXN
    assert 1 <= p <= MAXP and 0 <= d <= MAXD
    assert all(1 <= x <= MAXA for x in a)
    tests.append(f"{n} {k} {p} {d}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


add(2, 10, 20, [17, 13, 19, 2, 16])
add(2, 9, 19, [14, 3, 3, 5, 7, 5])
add(2, 5, 4, [20, 30, 40])
add(6, 7, 0, [7, 3, 5, 1, 6, 2])
add(1, 8, 40, [8, 8, 15, 10, 1, 14])

add(1, 1, 0, [1])
add(1, 1, 0, [2])
add(1, MAXP, 0, [MAXA])
a = rnd(10, 1, 30)
add(3, 12, 46, a)
a = rnd(12, 1, 50)
add(5, 40, 18, a)
a = rnd(15, 20, 100)
add(4, 15, 176, a)
a = rnd(18, 1, 10**9)
add(6, 5 * 10**8, 1145580333, a)
a = [3, 3, 3, 3, 50, 60, 70, 80, 90, 100, 1000, 1000]
add(3, 45, 57, a)
a = [1, 2, 3, 4, 5, 6, 30, 31, 32, 33]
add(4, 30, 11, a)

a = rnd(3000, 1, 10**6)
add(700, 300000, 533285644, a)
a = rnd(5000, 1, 10**9)
add(4000, 10**9, 24072444112, a)

N = MAXN
add(N, MAXP, 0, [MAXA] * N)
add(1, 1, MAXD, [MAXA] * N)
a = [MAXA] * N
add(N // 2, 10**8, 189999000000005, a)
a = rnd(N, 1, MAXA)
add(N // 2, 5 * 10**8, 47014093883009, a)
a = rnd(N, 1, 10**6)
add(N // 3, 900000, 41869380811, a)
a = rnd(N, 1, MAXA)
add(1000, MAXP // 2, 80318508873970, a)
a = rnd(N - 2000, 1, 10**7) + [MAXA] * 2000
add(30000, 10**7, 707438158232, a)
a = rnd(N, 1, 10**5) + []
add(N - 1, 50000, 2497398622, a)
a = sorted(rnd(N, 1, MAXA), reverse=True)
add(60000, 7 * 10**8, 16056738605793, a)
a = rnd(N, MAXA - 10**6, MAXA)
add(N // 4, 10**9 - 10**6, 149943174660181, a)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
