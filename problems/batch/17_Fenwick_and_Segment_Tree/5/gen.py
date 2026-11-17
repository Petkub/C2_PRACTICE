# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(110005)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(init, ops):
    n, q = len(init), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXV for v in init)
    cnt = {}
    for v in init:
        cnt[v] = cnt.get(v, 0) + 1
    size = n
    for t, x in ops:
        if t == 1:
            assert 1 <= x <= MAXV
            cnt[x] = cnt.get(x, 0) + 1
            size += 1
        elif t == 2:
            assert cnt.get(x, 0) > 0
            cnt[x] -= 1
            size -= 1
        else:
            assert t == 3 and 1 <= x <= size
    assert any(t == 3 for t, _ in ops)
    tests.append(f"{n} {q}\n" + " ".join(map(str, init)) + "\n" + "".join(f"{t} {x}\n" for t, x in ops))


def rnd_ops(init, q, p_ins, p_del, new_val, k_kind="any"):
    pool = list(init)
    random.shuffle(pool)
    pool_extra = []
    size = len(init)
    ops = []
    for _ in range(q):
        r = random.random()
        if r < p_ins:
            v = new_val()
            ops.append((1, v))
            pool_extra.append(v)
            size += 1
        elif r < p_ins + p_del and size > 1:
            if pool_extra:
                v = pool_extra.pop(ri(0, len(pool_extra) - 1))
            else:
                v = pool.pop()
            ops.append((2, v))
            size -= 1
        else:
            if k_kind == "high":
                k = ri(max(1, size - 99), size)
            elif k_kind == "mid":
                k = ri(size // 3, size)
                k = max(k, 1)
            else:
                k = ri(1, size)
            ops.append((3, k))
    if all(t != 3 for t, _ in ops):
        ops[-1] = (3, 1)
    return ops


add([5, 1, 4, 1, 3], [(3, 2), (1, 2), (3, 3), (2, 1), (3, 1)])
add([7, 7, 7], [(2, 7), (3, 2), (1, 9), (3, 3)])
add([MAXV], [(2, MAXV), (1, 1), (3, 1)])
add([6, 2, 9, 2, 5], [(3, 5), (2, 9), (1, 2), (3, 4)])
add([10, 20, 30], [(1, 15), (2, 10), (3, 1), (3, 3)])

add([1], [(1, 1), (3, 2), (2, 1), (3, 1)])
for n, q, vmax in ((5, 10, 5), (10, 40, 3), (50, 100, 100), (300, 600, MAXV), (2000, 3000, 10), (6000, 6000, MAXV)):
    init = [ri(1, vmax) for _ in range(n)]
    add(init, rnd_ops(init, q, 0.35, 0.3, lambda: ri(1, vmax)))
init = [ri(1, MAXV) for _ in range(20_000)]
add(init, rnd_ops(init, 20_000, 0.4, 0.4, lambda: ri(1, 50), "high"))

N, Q = MAXN, MAXQ
init = [ri(1, MAXV) for _ in range(N)]
add(init, rnd_ops(init, Q, 0.45, 0.45, lambda: ri(1, 99), "high"))
init = [ri(1, MAXV) for _ in range(N)]
add(init, rnd_ops(init, Q, 0.48, 0.47, lambda: ri(1, 9), "mid"))
init = [ri(1, MAXV) for _ in range(N)]
add(init, rnd_ops(init, Q, 0.7, 0.25, lambda: ri(1, 99), "high"))
init = [ri(MAXV - 999, MAXV) for _ in range(N)]
add(init, rnd_ops(init, Q, 0.5, 0.4, lambda: ri(1, 999), "high"))
init = [ri(1, MAXV) for _ in range(N)]
add(init, rnd_ops(init, Q, 0.3, 0.3, lambda: ri(1, MAXV)))
init = [MAXV] * N
add(init, rnd_ops(init, Q, 0.45, 0.45, lambda: random.choice((1, 1, 1, MAXV)), "mid"))
init = list(range(MAXV - N + 1, MAXV + 1))
random.shuffle(init)
add(init, [(1, 1) if k % 2 == 0 else (3, N + k // 2 + 1) for k in range(Q)])
init = [ri(1, 3) for _ in range(N)]
add(init, rnd_ops(init, Q, 0.4, 0.4, lambda: ri(1, 3)))
init = [1]
add(init, rnd_ops(init, Q, 0.6, 0.1, lambda: ri(1, MAXV)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
