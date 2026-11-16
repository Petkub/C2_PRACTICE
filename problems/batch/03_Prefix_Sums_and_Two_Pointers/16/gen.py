# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(11602)
MAXN = 200_000
AL = "abcdefghijklmnopqrstuvwxyz"
tests = []


def add(s):
    n = len(s)
    assert 1 <= n <= MAXN
    assert all(ch in AL for ch in s)
    tests.append(f"{n}\n{s}\n")


def rnd(n, letters=AL):
    return "".join(random.choices(letters, k=n))


# samples
add("abba")
add("abc")
add("aaaaa")
add("racecar")
add("abcabcab")
add("z")
# hidden (small)
add("ab")
add(AL)
add(AL + AL[::-1])
add(rnd(40, "ab"))
add(rnd(300, "abc"))
add(rnd(2000, "abcde"))
add(rnd(3000))
add("ab" * 1500)
add(("abcdefghij" * 300)[:2999] + "z")
# large
add("a" * MAXN)                               # every substring, answer about 2*10^10
add("ab" * (MAXN // 2))
add(rnd(MAXN, "ab"))
add(rnd(MAXN, "abc"))
add(rnd(MAXN, "abcdefgh"))
add(rnd(MAXN))
add((AL * (MAXN // 26 + 1))[:MAXN])           # the 26 letters cycled
s = "".join(random.choice(AL) * random.randint(1, 4) for _ in range(MAXN))[:MAXN]
add(s)
half = rnd(MAXN // 2, "abcdefghijklm")
add(half + half[::-1])
s = list(rnd(MAXN, "a"))
for i in random.sample(range(MAXN), 300):
    s[i] = random.choice(AL[1:])
add("".join(s))                               # almost all equal letters
add("".join(random.choice(AL) + random.choice(AL) * 2 for _ in range(MAXN // 3)) + "zz")

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
