# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160112)
MAXN, MAXH, MAXV = 200_000, 10**9, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def best(h, v, equal_blocks=True):
    """the official stack DP; equal_blocks=False is the tempting version that pops equal roofs too"""
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
    if sample:                                    # the tempting tie rule gives the right answer on samples
        assert best(h, v) == best(h, v, False)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n" + " ".join(map(str, v)) + "\n")
    assert len(tests[-1]) <= 3_100_000


def rv(n, lo=-MAXV, hi=MAXV):
    return [ri(lo, hi) for _ in range(n)]


def vee(n, top=MAXH, step=5000, noise=0, rep=1):
    """heights fall from the left end to the middle, then rise again; each height repeated rep times"""
    half = (n + 1) // 2
    left = [max(1, top - step * (i // rep) - ri(0, noise)) for i in range(half)]
    right = [max(1, top - step * ((n - 1 - i) // rep) - ri(0, noise)) for i in range(half, n)]
    return left + right


# samples
add([4, 2, 3, 1, 5, 2, 4], [3, -5, 2, -10, 4, -1, 2], True)
add([6, 5, 5, 6], [2, -3, -4, 1], True)
add([7], [-5], True)
add([3, 3], [1, -2], True)
add([4, 2, 4, 8, 6, 9, 6, 9], [-1, 5, -6, 9, 2, 0, -8, 4], True)
# hidden: small
add([5, 5, 5], [1, -100, 1])                                   # equal roofs block: must step on the middle
add([6, 5, 5, 6], [2, -3, 10, 1])                              # 1 -> 3 is not allowed
add([1, 2, 3, 4, 5], [-1, -1, -1, -1, -1])
add([5, 4, 3, 2, 1], [MAXV, -MAXV, MAXV, -MAXV, MAXV])
for n in (8, 12, 20):
    add([ri(1, 4) for _ in range(n)], rv(n, -9, 9))
add([ri(1, 6) for _ in range(300)], rv(300, -50, 50))
add([ri(1, 1000) for _ in range(2000)], rv(2000))
add([7] * 3000, rv(3000))                                      # all equal: only neighbours
add(vee(5000, step=3, rep=2), rv(5000))
add([ri(1, 30) for _ in range(20000)], rv(20000))
add(vee(150_000, top=MAXH, step=6000), rv(150_000))              # tall roofs (not the largest N)
# hidden: maximum size (V and rising shapes: going back from every roof is slow); heights below 10^6
# keep the inputs under 3 MB
N = MAXN
T = 10**6 - 1
add(vee(N, top=T, step=9), rv(N, -99_999, MAXV))                 # strict V
add(vee(N, top=T, step=9, rep=2), rv(N, -99_999, 99_999))        # V of equal pairs
add(vee(N, top=T, step=9, noise=20), rv(N, -99_999, MAXV))       # rough V
add(vee(N, top=T, step=9), [MAXV] * N)                           # every roof, largest total
add(vee(N, top=T, step=9, rep=2), [-99_999] * N)                 # every roof costs
add([1 + 4 * i for i in range(N)], rv(N, -99_999, 99_999))       # rising: only neighbours
add([1 + 9 * (i // 2) for i in range(N)], rv(N, -99_999, MAXV))  # rising pairs
h = vee(N // 2, top=T, step=9) + vee(N - N // 2, top=T, step=9)  # two valleys
add(h, rv(N, -99_999, 99_999))
h = vee(N, top=T, step=9, rep=2)
add(h, [99_999 if i % 2 == 0 else -99_999 for i in range(N)])    # the second roof of each pair pays
add(vee(N, top=T, step=9, noise=8, rep=2), rv(N, -10, 10))
h = vee(N, top=T, step=9)
mid = N // 2
for i in range(mid - 1000, mid + 1000):                          # a wide flat valley floor
    h[i] = h[mid - 1000]
add(h, rv(N, -99_999, MAXV))
h = [1 + 9 * (i // 2) + ri(0, 8) for i in range(N)]              # rough rise
add(h, rv(N, -99_999, 99_999))
for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
