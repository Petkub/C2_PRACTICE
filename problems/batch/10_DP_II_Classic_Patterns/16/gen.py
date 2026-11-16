# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(10016)
MAXN, MAXW, MAXLETTERS = 100000, 100, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(w, words):
    n = len(words)
    assert 1 <= n <= MAXN and 1 <= w <= MAXW
    assert all(1 <= len(s) <= w and s.isalpha() and s.islower() for s in words)
    assert sum(map(len, words)) <= MAXLETTERS
    tests.append(f"{n} {w}\n" + " ".join(words) + "\n")


LET = "abcdefghijklmnopqrstuvwxyz"


def word(k):
    return "".join(random.choices(LET, k=k))


def words(n, lo, hi):
    return [word(ri(lo, hi)) for _ in range(n)]


# Word lengths (one digit per word) of paragraphs on which a DP from the front with "the latest parent on a
# tie" breaks the tie rule (found by search against brute.cpp): T10 when the last line is chosen with the
# longest last line, T11 with the shortest last line.
T10_W21 = "11321123223122121313121312231333121113122"
T11_W11 = "322133322231313111112113331233321113321312331"
T11_W13 = ("2211112121112222222222222121121122221111121122221121111222222121122121122211121112212211221211"
           "11221121")
T11_W15 = ("2132433214312113411212243124112321414432114321414132213131121422143342342442312334231242111123"
           "32313431121322211322224314414222231123222214431241124132233231212322333223313")
T10_W25 = ("4232342313434244432344123132122413124142443213112322111123242432313421432322421144433114424342"
           "1214322321141114142123131112333233441322323432332233443221432443424214212323134213223211434244"
           "3331433233421212214122212142134312311341242322431233342143343123241333314421144333224123222123"
           "3112424234441133213441124331331211243243134413231244131214313314142112343311232211411423214434"
           "334213212231213433243234123241212242331441231112314211341144132232221")


def from_lengths(code):
    return [word(int(ch)) for ch in code]


def tie_trap(w, n, code, hi):
    """n words: tie-heavy random words, one word of length w (alone on its line, cost 0), then a trap paragraph"""
    tail = from_lengths(code)
    return words(n - len(tail) - 1, 1, hi) + [word(w)] + tail


# samples
add(6, ["sun", "a", "go", "rain"])
add(5, ["aa", "bb", "cc", "dd", "e", "ffff"])
add(5, ["hello"])
add(12, ["this", "is", "a", "test", "of", "a", "neat", "paragraph"])
add(4, ["x", "y", "z", "w", "v", "u", "t"])
# hidden: small (brute.cpp tries every set of line breaks)
add(1, ["q"])
add(3, ["a", "b", "c", "d", "e", "f", "g", "h", "i"])
add(8, words(14, 1, 4))
add(10, words(16, 1, 6))
add(7, ["aa"] * 18)
add(20, words(18, 1, 9))
add(15, words(20, 1, 15))
add(21, from_lengths(T10_W21))
add(11, from_lengths(T11_W11))
# hidden: maximum size
N = MAXN
add(100, words(N, 1, 10))
add(100, words(N, 1, 17))
add(50, words(N, 1, 8))
add(30, words(N, 2, 4))                    # many equal-cost layouts
add(11, ["ab"] * N)                       # even more ties
add(100, words(N - 10000, 5, 15))
add(100, [word(ri(90, 100)) if k % 13 == 0 else word(ri(1, 3)) for k in range(N)])
add(64, words(N, 2, 3))
add(99, words(N, 1, 17))
add(10, words(N, 1, 10))
add(97, words(N, 3, 6))
add(100, words(N, 8, 11))
add(25, tie_trap(25, N, T10_W25, 4))
add(13, tie_trap(13, N, T11_W13, 2))
add(15, tie_trap(15, N, T11_W15, 4))
add(11, tie_trap(11, N, T11_W11, 3))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
