# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(500002)
MAXN = 100000
MAXK = 100000
MAXA = 10 ** 9
MAXR = 10 ** 9
tests = []


def add(n, k, r, h, a):
    assert 1 <= n <= MAXN and 1 <= k <= MAXK and 1 <= r <= MAXR
    assert len(a) == k + n - 1 and 1 <= h <= k + n - 1
    assert all(1 <= x <= MAXA for x in a) and len(set(a)) == len(a)
    tests.append(f"{n} {k} {r} {h}\n{' '.join(map(str, a))}\n")


def strengths(cnt, lo=1, hi=MAXA):
    if cnt <= 1000:
        return random.sample(range(lo, hi + 1), cnt)
    step = (hi - lo + 1) // cnt
    a = [lo + i * step + random.randrange(step) for i in range(cnt)]
    random.shuffle(a)
    return a


def with_rank(n, k, hero, rank):
    cnt = k + n - 1
    step = MAXA // cnt
    a = [MAXA - i * step - random.randrange(step) for i in range(cnt)]
    v = a[rank - 1]
    del a[rank - 1]
    random.shuffle(a)
    a.insert(hero - 1, v)
    return a


add(5, 2, 1, 5, [7, 1, 8, 6, 9, 4])
add(4, 3, 3, 3, [4, 1, 2, 7, 9, 8])
add(7, 2, 2, 7, [5, 6, 8, 2, 3, 7, 9, 1])
add(7, 3, 3, 9, [4, 6, 7, 8, 2, 3, 5, 9, 1])
add(1, 1, 1000000000, 1, [1000000000])


for n, k, r in [(6, 2, 1), (8, 3, 2), (10, 4, 3), (12, 1, 2), (12, 5, 4)]:
    tot = k + n - 1
    add(n, k, r, random.randint(1, tot), strengths(tot, 1, 50))
def top_first(n, k, hero, rank, r):
    a = with_rank(n, k, hero, rank)
    order = sorted(range(k + n - 1), key=lambda i: -a[i])
    top = [i for i in order[:rank] if i != hero - 1]
    topset = set(top)
    slots = [i for i in range(k) if i != hero - 1 and i not in topset]
    for i in top:
        if i >= k:
            j = slots.pop()
            a[i], a[j] = a[j], a[i]
    add(n, k, r, hero, a)


add(3000, 2000, 7, 1500, with_rank(3000, 2000, 1500, 8))
add(4000, 3000, 900, 3500, with_rank(4000, 3000, 3500, 600))
add(2500, 2500, 2400, 2600, with_rank(2500, 2500, 2600, 2300))
top_first(3000, 3000, 10, 3, 2)
top_first(2000, 4000, 4000, 2, 1)


N, K = MAXN, MAXK


top_first(N, K, 5, 2, 1)
top_first(N, K, 6, 3, 2)
top_first(N, K, 7, 4, 3)
add(N, K, MAXR, 77777, with_rank(N, K, 77777, 90000))
add(N, K, 60000, 123, with_rank(N, K, 123, 59000))
add(N, K, 30000, 321, with_rank(N, K, 321, 59000))
add(N, K, 20000, K + 90000, with_rank(N, K, K + 90000, 25002))
add(N, K, 35000, K + 70000, with_rank(N, K, K + 70000, 50000))
add(N, K, 20000, K + 90000, with_rank(N, K, K + 90000, 19990))
add(N, K, 40000, K + 99990, with_rank(N, K, K + 99990, 39995))
add(N, K, 30000, K + 60000, with_rank(N, K, K + 60000, 29800))
add(N, K, 3, 2, with_rank(N, K, 2, K + N - 1))
a = sorted(strengths(K + N - 1))
add(N, K, 2, K - 1, a)
add(N, 1, 40000, 60000, with_rank(N, 1, 60000, 39000))
add(N, 1, 2, 70000, with_rank(N, 1, 70000, 3))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
