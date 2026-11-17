# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(402613)
MAXN, MAXK, MAXC = 200_000, 10**9, 10**18
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def check(lines):
    assert 1 <= len(lines) <= MAXN
    st = [[1, 0, True]]
    coef = {}
    for ln in lines:
        p = ln.split()
        if p[0] == "END":
            assert len(p) == 1 and len(st) > 1
            assert st[-1][2], "a loop without an OP"
            st.pop()
            continue
        assert len(p) == 2 and p[0] in ("LOOP", "OP")
        mult, e, _ = st[-1]
        if p[1] == "n":
            assert p[0] == "LOOP"
            st.append([mult, e + 1, False])
            continue
        k = int(p[1])
        assert 1 <= k <= MAXK and str(k) == p[1]
        if p[0] == "OP":
            coef[e] = coef.get(e, 0) + k * mult
            for s in reversed(st):
                if s[2]:
                    break
                s[2] = True
        else:
            st.append([mult * k, e, False])
    assert len(st) == 1
    assert all(v <= MAXC for v in coef.values())
    return coef


def add(lines):
    check(lines)
    tests.append(f"{len(lines)}\n" + "".join(l + "\n" for l in lines))


def program(n, p_open, p_n, p_close, kconst=(1, 3), kop=(1, 9), big=0.0):
    lines, st = [], []
    coef = {}
    mult, e = 1, 0
    has = []
    empty = [0]

    def room():
        return (MAXC - coef.get(e, 0)) // mult

    def op(k):
        lines.append(f"OP {k}")
        coef[e] = coef.get(e, 0) + k * mult
        for i in range(len(has) - 1, -1, -1):
            if has[i]:
                break
            has[i] = True
            empty[0] -= 1

    while len(lines) + len(st) + empty[0] + 3 < n:
        r = random.random()
        if r < p_open:
            if random.random() < p_n:
                st.append((mult, e))
                has.append(False)
                empty[0] += 1
                e += 1
                lines.append("LOOP n")
            else:
                hi = min(MAXK, room() // 4)
                if hi < 1:
                    continue
                k = ri(1, hi) if random.random() < big else min(hi, ri(*kconst))
                st.append((mult, e))
                has.append(False)
                empty[0] += 1
                mult *= k
                lines.append(f"LOOP {k}")
        elif st and r < p_open + p_close and has[-1]:
            mult, e = st.pop()
            has.pop()
            lines.append("END")
        else:
            hi = min(MAXK, room() // 4)
            if hi < 1:
                continue
            op(ri(1, hi) if random.random() < big else min(hi, ri(*kop)))
    while st:
        if not has[-1]:
            op(1)
        mult, e = st.pop()
        has.pop()
        lines.append("END")
    return lines


def chain(depth, every=False, kop=(1, 9)):
    lines = []
    for _ in range(depth):
        lines.append("LOOP n")
        if every:
            lines.append(f"OP {ri(*kop)}")
    lines.append(f"OP {ri(*kop)}")
    lines += ["END"] * depth
    return lines


add(["OP 5", "LOOP n", "OP 4", "LOOP 3", "OP 2", "END", "END"])
add(["LOOP n", "LOOP n", "OP 1", "END", "OP 2", "END", "LOOP 2", "OP 3", "END"])
add(["OP 7"])
add(["LOOP n", "LOOP n", "LOOP n", "OP 1", "END", "END", "END", "OP 1"])
add(["LOOP 2", "LOOP n", "OP 3", "LOOP 2", "LOOP n", "OP 1", "END", "END", "END", "END"])

add(["LOOP 1000000000", "OP 1000000000", "END"])
add(["LOOP 1", "LOOP n", "LOOP 1", "OP 1", "END", "END", "END",
     "LOOP 1000", "LOOP 1000", "LOOP n", "OP 999", "END", "END", "END"])
add(program(40, 0.3, 0.5, 0.3))
add(program(200, 0.35, 0.4, 0.3, big=0.1))
add(program(2000, 0.4, 0.7, 0.35))
add(chain(3000, True))
add(program(20000, 0.45, 0.6, 0.4, big=0.02))

N = MAXN
add(chain((N - 1) // 2))
add(chain((N - 1) // 3, True, (1, MAXK)))
add(program(N, 0.5, 0.95, 0.02))
add(program(N, 0.48, 0.8, 0.03, big=0.01))
add(program(N, 0.45, 0.9, 0.05, kconst=(1, 1), kop=(1, MAXK)))
add(program(N, 0.5, 0.97, 0.01, big=0.2))
d = (N - 40) // 2
add(["LOOP 1000000", "LOOP 999999"] + ["LOOP n"] * d + ["OP 999999"] + ["END"] * d
    + ["END", "OP 1000000000", "END", "OP 1"])
add(chain(70_000) + ["LOOP n"] * 20 + ["OP 1000000000"] + ["END"] * 20
    + program(N - 140_100, 0.4, 0.6, 0.3, big=0.05))
add(program(N, 0.5, 0.99, 0.005, kop=(MAXK // 2, MAXK)))
add(program(N, 0.47, 0.85, 0.04, kconst=(1, 2), big=0.03))
add(program(N, 0.5, 0.92, 0.02, big=0.5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
