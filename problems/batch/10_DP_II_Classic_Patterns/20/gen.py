# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(10019)
MAXN, MAXV = 200000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    assert 1 <= len(a) <= MAXN and 1 <= min(a) and max(a) <= MAXV
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo=1, hi=MAXV):
    return [ri(lo, hi) for _ in range(n)]


def chain(n, k, width):
    out = []
    per = max(1, n // k)
    for t in range(k):
        size = 1 if random.random() < 0.3 else ri(1, per)
        base = (t + 1) * width
        out += sorted((base + ri(0, width - 1) for _ in range(size)), reverse=True)
    noise = n - len(out)
    for _ in range(max(0, noise)):
        out.insert(ri(0, len(out)), ri(1, MAXV))
    return out[:n]


add([2, 5, 3, 7, 4, 8])
add([1, 3, 2, 4])
add([5, 4, 3])
add([4, 4, 5])
add([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])

add([7])
add([1, 2])
add(rnd(10, 1, 4))
add(rnd(15, 1, 10))
add(chain(18, 6, 10))
add(rnd(18, 1, 100))
add(rnd(400, 1, 300))
add(chain(3000, 60, 1000))

N = MAXN
add(rnd(N))
add(rnd(N, 1, 1000))
add(chain(N, 400, 10**6))
add(chain(N, 3000, 10**5))
add(list(range(1, N + 1)))
add(list(range(N, 0, -1)))
add([MAXV] * N)
add([i // 2 + 1 for i in range(N)])
add([(i * 7919) % 200003 + 1 for i in range(N)])
add([ri(1, 50) + (i // 500) * 50 for i in range(N)])
add(chain(N, 50000, 10**4))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
