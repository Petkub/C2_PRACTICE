# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(150701)
MAXN = 1_000_000
OPEN, CLOSE = "([{<", ")]}>"
tests = []


def add(s):
    assert 1 <= len(s) <= MAXN
    assert all(c in "()[]{}<>" for c in s)
    tests.append(s + "\n")


def balanced(n, deep=0.5):
    out, st = [], []
    rnd = random.random
    for i in range(n):
        left = n - i
        if st and (len(st) == left or rnd() >= deep):
            out.append(CLOSE[st.pop()])
        else:
            k = int(rnd() * 4)
            st.append(k)
            out.append(OPEN[k])
    assert not st
    return "".join(out)


def noisy(n, p):
    parts, size = [], 0
    while size < n:
        if random.random() < p:
            parts.append(random.choice("()[]{}<>"))
        else:
            parts.append(balanced(2 * random.randint(1, 30), random.choice([0.3, 0.5, 0.7])))
        size += len(parts[-1])
    return "".join(parts)[:n]


add("(())[]")
add("([)]<>{}")
add(")(")
add("{<>}()<{}>(")
add("()()()()")

add("(")
add("([]){}[(])<>")
add("".join(random.choice("()[]{}<>") for _ in range(200)))
add(noisy(1000, 0.05))
add(balanced(3000, 0.6))
add("(" * 1000 + ")" * 1000)

add("()" * (MAXN // 2))
add("<>" * (MAXN // 2 - 1) + "<")
add("(" * (MAXN // 2) + ")" * (MAXN // 2))
add(balanced(MAXN, 0.5))
add(balanced(MAXN, 0.3))
add(balanced(MAXN, 0.7))
add("".join(balanced(2 * random.randint(1, 3), 0.5) for _ in range(MAXN // 4))[:MAXN - 1] + "]")
add(noisy(MAXN, 0.0005))
add("".join(random.choice("()[]{}<>") for _ in range(MAXN)))
add("([" * (MAXN // 4) + ")]" * (MAXN // 4))
add("(" * MAXN)


def corrupt(s, k):
    s = list(s)
    closers = [i for i, c in enumerate(s) if c in CLOSE]
    for i in random.sample(closers, k):
        s[i] = random.choice([c for c in CLOSE if c != s[i]])
    return "".join(s)


add("((])" + "<[(>)]" + "{()}")
add(corrupt(balanced(2000, 0.6), 5))
add(corrupt(balanced(MAXN, 0.5), 20))
add(corrupt(balanced(MAXN, 0.7), 40))
add(corrupt("".join(balanced(2 * random.randint(1, 3000), 0.6) for _ in range(1000))[:MAXN], 10))
A = (MAXN - 5) // 4
add("((" + "()" * A + "]" + "<>" * A + "))")
add("(" * 3 + corrupt("()" * (MAXN // 2 - 3), 3) + ")" * 3)
add("[" * 4 + corrupt("{}" * (MAXN // 2 - 4), 1) + "]" * 4)

for t in tests:
    assert t.endswith("\n") and t.count("\n") == 1
    assert t.encode().translate(None, bytes(range(32, 127)) + b"\n") == b""
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
