# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(150901)
MAXT = 200_000
MAXQ = 100_000
tests = []


def add(t, words):
    assert 1 <= len(t) <= MAXT and 1 <= len(words) <= MAXQ
    assert t.isascii() and t.isalpha() and t.islower()
    for w in words:
        assert 1 <= len(w) <= 10 and w.isascii() and w.isalpha() and w.islower()
    tests.append(f"{t}\n{len(words)}\n" + "".join(w + "\n" for w in words))


def rs(n, alpha):
    return "".join(random.choice(alpha) for _ in range(n))


def periodic(n, unit):
    return (unit * (n // len(unit) + 1))[:n]


def words_from(t, q, lo=1, hi=10, p_rand=0.2, alpha="ab"):
    out = []
    for _ in range(q):
        L = random.randint(lo, hi)
        if random.random() < p_rand or L > len(t):
            out.append(rs(L, alpha))
        else:
            i = random.randint(0, len(t) - L)
            out.append(t[i:i + L])
    return out


add("abababa", ["aba", "ab", "bab", "c", "abababab"])
add("aaaa", ["aa", "a", "aaaaa", "aa"])
add("mississippi", ["ssi", "issi", "s", "pi", "ippi", "sip"])
add("z", ["z", "zz", "a"])
add("hellohello", ["hello", "lohe", "l", "ohell", "hellohello", "lo"])

t = rs(50, "ab")
add(t, words_from(t, 50))
t = rs(500, "abc")
add(t, words_from(t, 500, alpha="abc"))
t = periodic(1000, "abcab")
add(t, words_from(t, 1000, alpha="abc"))
t = "a" * 2000
add(t, ["a" * random.randint(1, 10) for _ in range(2000)])
t = rs(3000, "abcdefghijklmnopqrstuvwxyz")
add(t, words_from(t, 3000, alpha="abcdefghijklmnopqrstuvwxyz"))
add("q" * 9, ["q" * 10, "q" * 9, "q", "qq"])
t = rs(MAXT, "ab")
add(t, words_from(t, 300))

t = rs(MAXT, "abcd")
add(t, words_from(t, MAXQ, 7, 10, alpha="abcd"))
t = rs(MAXT, "abc")
add(t, words_from(t, MAXQ, 1, 10, alpha="abc"))
t = rs(MAXT, "ab")
add(t, words_from(t, MAXQ, 8, 10))
t = "a" * MAXT
add(t, ["a" * random.randint(1, 10) for _ in range(MAXQ)])
t = periodic(MAXT, "abcab")
add(t, words_from(t, MAXQ, 5, 10, alpha="abc"))
t = rs(MAXT, "abcdefghijklmnopqrstuvwxyz")
add(t, words_from(t, MAXQ, 1, 10, p_rand=0.5, alpha="abcdefghijklmnopqrstuvwxyz"))
t = rs(MAXT, "abcdefgh")
add(t, words_from(t, MAXQ, 9, 10, p_rand=0.05, alpha="abcdefgh"))
t = "".join(random.choice(["a", "b", "ab", "ba"]) * random.randint(1, 6) for _ in range(MAXT))[:MAXT]
add(t, words_from(t, MAXQ, 6, 10))
t = rs(MAXT, "xy")
add(t, ["z" * 10] * MAXQ)
t = rs(MAXT, "abcd")
add(t, [rs(10, "abcd") for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and " " not in t
    assert t.encode().translate(None, bytes(range(32, 127)) + b"\n") == b""
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
