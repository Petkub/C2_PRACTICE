# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(40111)
MAXN, MAXT = 150_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, films):
    n = len(films)
    assert 1 <= n <= MAXN and 1 <= k <= MAXN
    assert all(0 <= s < e <= MAXT for (s, e) in films)
    tests.append(f"{n} {k}\n" + "".join(f"{s} {e}\n" for (s, e) in films))


def rnd_films(n, lo, hi, maxlen):
    res = []
    for _ in range(n):
        s = ri(lo, hi - 1)
        res.append((s, min(hi, s + ri(1, maxlen))))
    return res


# samples
add(2, [(1, 4), (2, 5), (4, 7), (5, 8), (3, 9)])
add(2, [(0, 1), (0, 3), (3, 6), (1, 7)])
add(5, [(0, 100), (0, 100), (50, 60)])
add(3, [(10, 20)] * 5)
add(1, [(1, 3), (2, 5), (4, 7), (6, 9), (3, 4)])
add(2, [(0, 5), (1, 2), (2, 3), (3, 4), (0, 10), (4, 6), (5, 8)])
# hidden: small (checked by trying every subset)
add(1, [(0, 1)])
for (n, k, hi, ml) in [(8, 2, 10, 4), (10, 3, 15, 8), (12, 2, 20, 6), (14, 3, 30, 12), (15, 4, 20, 10),
                       (16, 2, 40, 10), (18, 5, 30, 15), (18, 3, 1000, 300), (20, 4, 50, 20), (20, 7, 25, 25)]:
    add(k, rnd_films(n, 0, hi, ml))
add(50, rnd_films(5000, 0, 10**6, 10**4))
add(3, rnd_films(5000, 0, 10**5, 1000))
# hidden: maximum size (K is set relative to the largest number of films running at one moment)
N = MAXN


def depth(films):
    ev = sorted([(s, 1) for (s, e) in films] + [(e, -1) for (s, e) in films])
    cur = best = 0
    for (_, d) in ev:
        cur += d
        best = max(best, cur)
    return best


def addf(frac, films):
    add(max(1, int(depth(films) * frac)), films)


addf(0.6, rnd_films(N, 0, MAXT, MAXT // 2))                     # many friends: scanning all friends is slow
addf(0.9, rnd_films(N, 0, MAXT, MAXT))
addf(0.4, rnd_films(N, 0, MAXT, MAXT // 2))
addf(1.0, rnd_films(N, 0, MAXT, MAXT // 4))                     # exactly enough friends: answer N
add(N - 1, [(0, MAXT)] * N)                                      # all the same film
add(1, rnd_films(N, 0, MAXT, 10**5))                             # one friend
addf(0.5, rnd_films(N, 0, MAXT, 10**7))
add(N // 2, [(i, MAXT - i) for i in range(N)])                   # nested
add(N // 4, [(i, i + N // 2) for i in range(N)])                 # sliding window of overlaps
addf(0.7, rnd_films(N, 0, 1000, 1000))                           # many equal times
f = []
for i in range(N):                                               # chains that touch: s = previous e
    t = (i % 990) * 10**6
    f.append((t, t + 10**6) if i % 3 else (t, t + 3 * 10**6))
addf(0.8, f)
addf(0.95, rnd_films(N, 0, MAXT, MAXT // 3))
f = rnd_films(N // 2, 0, MAXT, MAXT) + rnd_films(N // 2, 0, MAXT, 10**6)   # long and short films mixed
random.shuffle(f)
addf(0.5, f)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
