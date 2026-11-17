# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(250012)
MAXN, MAXQ, MAXV = 200_000, 200_000, (1 << 20) - 1
tests = []


def add(a, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= x <= MAXV for x in a)
    for op in ops:
        assert (op[0] in (1, 2) and len(op) == 2 and 0 <= op[1] <= MAXV) or op == (3,)
    assert any(op == (3,) for op in ops)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(" ".join(map(str, op)) + "\n" for op in ops))


def mix(q, p_ins, p_xor, xlo, xhi, ylo, yhi):
    ops = []
    for _ in range(q):
        r = random.random()
        if r < p_ins:
            ops.append((1, random.randint(xlo, xhi)))
        elif r < p_ins + p_xor:
            ops.append((2, random.randint(ylo, yhi)))
        else:
            ops.append((3,))
    if (3,) not in ops:
        ops.append((3,))
    return ops


def trap(b, n_other, q, p_query=0.4, p_hit=0.25, p_ins=0.1, fill_end=0.05):
    """the set holds 0 .. 2^b - 1 and nothing in 2^b .. 2^(b+1) - 1, so the mex is 2^b while the XOR tag T stays
    below 2^b; the values whose top b bits (bits 19, 18, ...) equal T are only one, for T = P (queries asked
    often there); near the end some values of 2^b .. 2^(b+1) - 1 are added"""
    low, bsz = 1 << b, 1 << (20 - b)
    P = random.randint(max(1, 1 << max(0, 2 * b - 19)), low - 1)
    r0, r1 = P * bsz, (P + 1) * bsz
    assert r0 >= 2 * low
    others = set()
    while len(others) < n_other:
        x = random.randint(2 * low, MAXV)
        if not r0 <= x < r1:
            others.add(x)
    vals = list(range(low)) + sorted(others) + [random.randrange(r0, r1)]
    random.shuffle(vals)
    a, ops = vals[:MAXN], [(1, x) for x in vals[MAXN:]]                     # tag 0: stored = real
    T = 0
    q_end = q - int(q * fill_end)
    while len(ops) < q_end - 1:
        r = random.random()
        if r < p_query:
            ops.append((3,))
        elif r < p_query + p_hit:
            ops.append((2, T ^ P)); T = P
            ops.append((3,))
        elif r < p_query + p_hit + p_ins:
            if random.random() < 0.5:
                ops.append((1, random.randrange(low)))                       # already in the set
            else:
                x = random.choice(vals)
                if 2 * low <= x and not r0 <= x < r1:
                    ops.append((1, x ^ T))                                   # stored x again
        else:
            y = random.randrange(low)
            ops.append((2, y)); T ^= y
    while len(ops) < q - 1:                                                  # fill part of 2^b .. 2^(b+1) - 1
        ops.append((1, random.randrange(low, 2 * low)) if random.random() < 0.5 else (3,))
    ops.append((3,))
    return a, ops


# samples
add([0, 1, 3], [(3,), (2, 1), (3,), (1, 3), (3,), (2, 4), (3,)])
add([5], [(3,), (2, 5), (3,), (1, 0), (3,)])
add([2, 2, 7], [(3,), (1, 0), (1, 1), (3,), (2, 2), (3,)])
add([4, 5, 6, 7, 0], [(3,), (2, 4), (3,), (2, 1), (3,), (1, 2), (3,), (2, 7), (3,)])
add([1], [(2, 1), (3,), (1, 2), (1, 3), (3,), (2, 3), (3,)])
# hidden: small
add([0], [(3,)])
add([random.randint(0, 7) for _ in range(5)], mix(30, 0.3, 0.3, 0, 7, 0, 7))
add([random.randint(0, 31) for _ in range(20)], mix(200, 0.3, 0.3, 0, 31, 0, 31))
add(list(range(64)), mix(300, 0.2, 0.4, 0, 127, 0, 127))
add([random.randint(0, 1023) for _ in range(1000)], mix(2000, 0.3, 0.3, 0, 1023, 0, 1023))
add(random.sample(range(4096), 3000), mix(3000, 0.2, 0.4, 0, 4095, 0, 4095))
add([0] * 3000, mix(3000, 0.2, 0.4, 0, 3, 0, 3))                                   # tiny set, repeats ignored
add(random.sample(range(MAXV + 1), 5000), mix(5000, 0.45, 0.1, 0, MAXV, 0, MAXV))
# the lower half full and the upper half empty, and no value has the top bits that the tag points to
add([0, 1, 1 << 19], [(3,), (2, 1), (3,), (1, 2), (3,), (2, 3), (3,), (2, 2), (3,)])
add(*trap(3, 40, 300))
add(*trap(10, 3000, 5000))
# hidden: maximum size (the mex is large at most queries)
N, Q = MAXN, MAXQ
K = 1 << 17
add(list(range(K)) + [random.randint(0, MAXV) for _ in range(N - K)], mix(Q, 0.1, 0.45, 0, MAXV, 0, K - 1))   # mex stays >= 2^17
a = list(range(190_000))
random.shuffle(a)
add(a, mix(Q, 0.2, 0.4, 0, (1 << 18) - 1, 0, K - 1))                              # a full block of 2^17 stays
a = list(range(K)) + [K + i for i in range(N - K)]
add(a, [(2, random.randint(0, (1 << 18) - 1)) if i % 2 else (3,) for i in range(Q)])   # XORs move the block
ops = []
for i in range(Q):                                                                 # fill the gaps one by one
    r = i % 4
    ops.append((1, random.randint(K, K + 80_000)) if r < 2 else ((2, random.randint(0, K - 1)) if r == 2 else (3,)))
add(list(range(K)), ops)
add(list(range(N)), [(3,)] * Q)                                                     # mex = N every time
a = [x for x in range(1 << 18) if x != 77_777][:N]
add(a, [(2, random.randint(0, (1 << 18) - 1)) if i % 2 else (3,) for i in range(Q)])
# the lower half full and the upper half empty at a high bit (see trap)
add(*trap(17, N - K - 1, Q))
add(*trap(16, N - (1 << 16) - 1, Q))
add(*trap(17, 30_000, Q, p_query=0.3, p_hit=0.4))
add(*trap(18, 20_000, Q))
add(*trap(16, 60_000, Q, p_query=0.5, p_hit=0.15, fill_end=0.2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
