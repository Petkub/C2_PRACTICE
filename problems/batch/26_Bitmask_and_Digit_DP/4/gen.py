# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(26007)
MAXB, MAXN, MAXQ = 20, 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(b, boxes, jobs):
    assert 1 <= b <= MAXB and 1 <= len(boxes) <= MAXN and 1 <= len(jobs) <= MAXQ
    assert all(0 <= m < (1 << b) for m in boxes) and all(0 <= m < (1 << b) for m in jobs)
    tests.append(f"{b} {len(boxes)} {len(jobs)}\n" + " ".join(map(str, boxes)) + "\n"
                 + " ".join(map(str, jobs)) + "\n")


BY_POP = {}


def by_pop(b, k):
    if (b, k) not in BY_POP:
        for kk in range(b + 1):
            BY_POP[(b, kk)] = []
        for m in range(1 << b):
            BY_POP[(b, bin(m).count("1"))].append(m)
    return BY_POP[(b, k)]


def bits_list(b, cnt, lo, hi):
    out = []
    for _ in range(cnt):
        g = by_pop(b, ri(lo, hi))
        out.append(g[int(random.random() * len(g))])
    return out


def mask_p(b, level):
    top = (1 << b) - 1
    m = ri(0, top)
    for _ in range(abs(level) - 1):
        x = ri(0, top)
        m = m & x if level < 0 else m | x
    return m


add(4, [13, 6, 7, 15, 4], [4, 5, 8, 10, 0])
add(3, [1, 2, 3], [4, 3, 0, 1])
add(1, [0], [0, 1])
add(5, [31, 30, 0, 17], [17, 16, 31, 2, 0])
add(6, [5, 12, 40, 63, 33, 9, 44], [1, 8, 12, 36, 48, 63])

add(1, [1, 1, 0], [0, 1])
add(2, [0, 1, 2, 3, 3, 2], [0, 1, 2, 3])
add(8, [ri(0, 255) for _ in range(300)], [ri(0, 255) for _ in range(300)])
add(10, bits_list(10, 500, 6, 10), bits_list(10, 500, 0, 3))
add(12, [mask_p(12, 2) for _ in range(2000)], [mask_p(12, -2) for _ in range(2000)])
add(MAXB, [(1 << MAXB) - 1] * 5 + [0], [0, (1 << MAXB) - 1, 1 << 19, 12345])
add(16, [mask_p(16, 1) for _ in range(5000)], [mask_p(16, 1) for _ in range(5000)])

add(MAXB, bits_list(MAXB, 20_000, 10, 20), bits_list(MAXB, 20_000, 0, 6))
add(17, [ri(0, (1 << 17) - 1) for _ in range(50_000)], [ri(0, (1 << 17) - 1) for _ in range(50_000)])

add(MAXB, bits_list(MAXB, MAXN, 14, 20), bits_list(MAXB, MAXQ, 0, 3))
add(MAXB, bits_list(MAXB, MAXN, 16, 20), bits_list(MAXB, MAXQ, 0, 2))
add(MAXB, [mask_p(MAXB, 1) for _ in range(MAXN)], [mask_p(MAXB, 1) for _ in range(MAXQ)])
add(MAXB, [mask_p(MAXB, 2) for _ in range(MAXN)], [mask_p(MAXB, -2) for _ in range(MAXQ)])
add(MAXB, [mask_p(MAXB, -2) for _ in range(MAXN)], [mask_p(MAXB, 2) for _ in range(MAXQ)])
add(MAXB, [(1 << MAXB) - 1 - (1 << ri(0, 19)) for _ in range(MAXN)], [0] * (MAXQ // 2) + bits_list(MAXB, MAXQ // 2, 1, 2))
add(MAXB, [ri(0, 1023) << 10 for _ in range(MAXN)], [ri(0, 1023) << 10 for _ in range(MAXQ)])
add(MAXB, [ri(0, (1 << MAXB) - 1) for _ in range(MAXN)], [ri(0, (1 << MAXB) - 1) for _ in range(MAXQ)])
add(18, [mask_p(18, 2) for _ in range(MAXN)], [mask_p(18, -3) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_400_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
