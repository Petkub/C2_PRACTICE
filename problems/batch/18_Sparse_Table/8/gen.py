# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180008)
MAXN, B = 200_000, 30
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, a):
    n = len(a)
    assert 1 <= n <= MAXN and 0 <= k <= B
    assert all(0 <= v < 2**B for v in a)
    t = f"{n} {k}\n" + " ".join(map(str, a)) + "\n"
    assert len(t) <= 3_100_000
    tests.append(t)


def mask_from(bits, cnt):
    """a mask with cnt bits chosen from the list bits"""
    m = 0
    for b in random.sample(bits, min(cnt, len(bits))):
        m |= 1 << b
    return m


def songs(n, bits, lo, hi):
    return [mask_from(bits, ri(lo, hi)) for _ in range(n)]


# samples
add(2, [1, 2, 4, 3, 1])
add(0, [0, 0, 5, 0])
add(30, [2**30 - 1])
add(3, [8, 8, 1, 6, 0, 16, 8])
add(1, [3, 1, 1, 2, 2, 2, 4])
# hidden: small
add(2, songs(10, list(range(5)), 0, 2))
add(4, songs(200, list(range(8)), 0, 2))
add(10, songs(1000, list(range(30)), 0, 3))
add(0, [0 if random.random() < 0.8 else 1 << ri(0, 29) for _ in range(2000)])
add(30, songs(2000, list(range(30)), 0, 30))                               # everything allowed
add(5, songs(3000, list(range(12)), 1, 1))
# hidden: maximum size (most runs long, so the extend-and-break way is slow)
N = MAXN


def drift(n, step, width, noise_every=0):
    """song i uses some of the instruments (i // step + t) mod 30, t < width: the set changes slowly"""
    a = []
    for i in range(n):
        base = i // step
        m = 0
        for t in range(width):
            if random.random() < 0.6:
                m |= 1 << ((base + t) % B)
        if noise_every and i % noise_every == noise_every - 1:
            m = mask_from(list(range(B)), ri(1, 4))
        a.append(m)
    return a


add(30, songs(N, list(range(30)), 1, 30))                                  # all N(N+1)/2 runs
add(6, songs(N, [0, 3, 7, 11, 19, 29], 0, 3))                              # only 6 instruments in total
add(29, [2**29 - 1] * (N // 2) + [2**30 - 1] * (N // 2))
add(10, drift(N, 8000, 3))
add(29, drift(N, 1500, 2))
add(3, [1 << ((i // 20_000) % 30) for i in range(N)])                        # one instrument at a time
add(15, drift(N, 5000, 4, 20_000))
a = [0] * N
for i in range(59_999, N, 60_000):
    a[i] = 1 << ri(0, 29)
add(0, a)                                                                  # long silent stretches
a = songs(N, list(range(10)), 0, 2)
for i in range(0, N, 5000):
    a[i] = 2**30 - 1                                                       # rare songs with everything
add(10, a)
add(25, songs(N, list(range(30)), 1, 2))                                   # short runs

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
