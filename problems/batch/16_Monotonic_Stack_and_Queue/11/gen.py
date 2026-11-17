# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(160112)
MAXN, MAXH, MAXV = 200_000, 10**9, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def best(h, v, equal_blocks=True):
    st, dp = [], []
    for j in range(len(h)):
        b = None
        while st and (h[st[-1]] < h[j] or (not equal_blocks and h[st[-1]] == h[j])):
            b = dp[st[-1]] if b is None else max(b, dp[st[-1]])
            st.pop()
        if st:
            b = dp[st[-1]] if b is None else max(b, dp[st[-1]])
            if equal_blocks and h[st[-1]] == h[j]:
                st.pop()
        dp.append(v[j] + (0 if j == 0 else b))
        st.append(j)
    return dp[-1]


def add(h, v, sample=False):
    n = len(h)
    assert 1 <= n <= MAXN and len(v) == n
    assert all(1 <= x <= MAXH for x in h) and all(-MAXV <= x <= MAXV for x in v)
    if sample:
        assert best(h, v) == best(h, v, False)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n" + " ".join(map(str, v)) + "\n")
    assert len(tests[-1]) <= 3_100_000


def rv(n, lo=-MAXV, hi=MAXV):
    return [ri(lo, hi) for _ in range(n)]


def vee(n, top=MAXH, step=5000, noise=0, rep=1):
    half = (n + 1) // 2
    left = [max(1, top - step * (i // rep) - ri(0, noise)) for i in range(half)]
    right = [max(1, top - step * ((n - 1 - i) // rep) - ri(0, noise)) for i in range(half, n)]
    return left + right


add([4, 2, 3, 1, 5, 2, 4], [3, -5, 2, -10, 4, -1, 2], True)
add([6, 5, 5, 6], [2, -3, -4, 1], True)
add([7], [-5], True)
add([3, 3], [1, -2], True)
add([4, 2, 4, 8, 6, 9, 6, 9], [-1, 5, -6, 9, 2, 0, -8, 4], True)

add([5, 5, 5], [1, -100, 1])
add([6, 5, 5, 6], [2, -3, 10, 1])
add([1, 2, 3, 4, 5], [-1, -1, -1, -1, -1])
add([5, 4, 3, 2, 1], [MAXV, -MAXV, MAXV, -MAXV, MAXV])
for n in (8, 12, 20):
    add([ri(1, 4) for _ in range(n)], rv(n, -9, 9))
add([ri(1, 6) for _ in range(300)], rv(300, -50, 50))
add([ri(1, 1000) for _ in range(2000)], rv(2000))
add([7] * 3000, rv(3000))
add(vee(5000, step=3, rep=2), rv(5000))
add([ri(1, 30) for _ in range(20000)], rv(20000))
add(vee(150_000, top=MAXH, step=6000), rv(150_000))


N = MAXN
T = 10**6 - 1
add(vee(N, top=T, step=9), rv(N, -99_999, MAXV))
add(vee(N, top=T, step=9, rep=2), rv(N, -99_999, 99_999))
add(vee(N, top=T, step=9, noise=20), rv(N, -99_999, MAXV))
add(vee(N, top=T, step=9), [MAXV] * N)
add(vee(N, top=T, step=9, rep=2), [-99_999] * N)
add([1 + 4 * i for i in range(N)], rv(N, -99_999, 99_999))
add([1 + 9 * (i // 2) for i in range(N)], rv(N, -99_999, MAXV))
h = vee(N // 2, top=T, step=9) + vee(N - N // 2, top=T, step=9)
add(h, rv(N, -99_999, 99_999))
h = vee(N, top=T, step=9, rep=2)
add(h, [99_999 if i % 2 == 0 else -99_999 for i in range(N)])
add(vee(N, top=T, step=9, noise=8, rep=2), rv(N, -10, 10))
h = vee(N, top=T, step=9)
mid = N // 2
for i in range(mid - 1000, mid + 1000):
    h[i] = h[mid - 1000]
add(h, rv(N, -99_999, MAXV))
h = [1 + 9 * (i // 2) + ri(0, 8) for i in range(N)]
add(h, rv(N, -99_999, 99_999))
for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
