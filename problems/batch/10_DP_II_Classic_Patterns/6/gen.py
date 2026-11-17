# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(10006)
MAXN = 10**6
tests = []


def add(s):
    n = len(s)
    assert 1 <= n <= MAXN
    assert set(s) <= set(".#o") and "oo" not in s
    tests.append(f"{n}\n{s}\n")


def rnd(n, p_broken, p_taken, end=""):
    """random row; a taken seat is never placed next to another one"""
    n -= len(end)
    out = []
    for i in range(n):
        r = random.random()
        if r < p_broken:
            out.append("#")
        elif r < p_broken + p_taken and (not out or out[-1] != "o"):
            out.append("o")
        else:
            out.append(".")
    s = "".join(out) + end
    return s.replace("oo", "o.")


# samples
add("..#...o")
add("o.#.o")
add(".....#")
add("#.#.#.#")
add("..o.....#...o......#")
add("................................o")
# hidden: small (brute.cpp tries every set of free seats)
add(".")
add("o")
add("..")
add("#.")
add("." * 20)
add("o" + "." * 18 + "o")
add(rnd(18, 0.2, 0.1, ".."))
add(rnd(20, 0.3, 0.05, ".."))
add(rnd(19, 0.1, 0.15, "#."))
add("#" * 7 + "." + "#" * 7 + ".." + "#" * 3)
# hidden: big
add(rnd(400000, 0.1, 0.03, ".."))
N = MAXN
add("." * N)
add("." * (N - 1))
add(rnd(N, 0.15, 0.0, ".."))
add(rnd(N, 0.05, 0.05, ".."))
add(("..#" * (N // 3 + 1))[:N - 1] + "#")
add(("o...." * (N // 5 + 1))[:N])
add("".join("#" * random.randint(1, 30) + "." * random.randint(1, 6) for _ in range(N // 15))[:N - 2] + "..")
add(rnd(N, 0.08, 0.08, "o"))
add("." * 3 + "o" + "." * (N - 8) + "o" + "...")

for t in tests:
    assert t.endswith("\n") and " " not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
