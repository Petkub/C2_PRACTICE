# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random, string

random.seed(150101)
MAXN = 10 ** 5
MAXLEN = 10 ** 6
MAXTOT = 2 * 10 ** 6
LOW = string.ascii_lowercase
UP = string.ascii_uppercase
MARKS = ",.;:!?"
OTHER = "0123456789()-'\"/+*=#@&%$[]{}<>_~^`|\\"
OK_BYTES = bytes(range(32, 127)) + b"\n"
tests = []


def add(lines):
    assert 1 <= len(lines) <= MAXN
    assert sum(len(l) for l in lines) <= MAXTOT
    for l in lines:
        assert 1 <= len(l) <= MAXLEN
        assert l[-1] != " " and l.strip(" ") != ""
    t = f"{len(lines)}\n" + "".join(l + "\n" for l in lines)
    assert not t.encode().translate(None, OK_BYTES)          # only ASCII 32-126 and newlines
    tests.append(t)


def word(k=None):
    k = k or random.randint(1, 8)
    w = "".join(random.choices(LOW, k=k))
    r = random.random()
    if r < 0.15:
        w = w.upper()
    elif r < 0.35:
        w = w[0].upper() + w[1:]
    return w


def spaces(lo=0, hi=3):
    return " " * random.randint(lo, hi)


POOL_W = [word() for _ in range(500)]
POOL_M = [c * k for c in MARKS for k in (1, 1, 1, 2, 3)]
POOL_O = ["".join(random.choices(OTHER, k=random.randint(1, 4))) for _ in range(50)]


def prose(length, sp=(0, 3), pmark=0.3, pother=0.1, lead=(0, 3)):
    # words, marks and other symbols with runs of spaces of random lengths (pieces drawn from small pools)
    pool_w, pool_m, pool_o = POOL_W, POOL_M, POOL_O
    pool_s = [" " * k for k in range(sp[0], sp[1] + 1)]
    lead_s = " " * random.randint(*lead)
    parts = [lead_s]
    size = len(lead_s)
    while size < length:
        r = random.random()
        pool = pool_m if r < pmark else pool_o if r < pmark + pother else pool_w
        piece = pool[int(random.random() * len(pool))] + pool_s[int(random.random() * len(pool_s))]
        parts.append(piece)
        size += len(piece)
    s = "".join(parts)[:length].rstrip(" ")
    if s.strip(" ") == "":
        s = s + "a"
    return s


def prose_lines(count, lo, hi, **kw):
    # many short lines cut from one long text
    text = prose(count * hi, **kw)
    lines, p = [], 0
    for _ in range(count):
        k = random.randint(lo, hi)
        l = text[p:p + k].rstrip(" ")
        p += k
        lines.append(l if l.strip(" ") else "q")
    return lines


def chars(length, alpha):
    s = "".join(random.choices(alpha, k=length)).rstrip(" ")
    return s if s.strip(" ") else "x"


# samples
add(["   hello ,   world  !how are you?", "wait...what?!no"])
add(["it is 3.5 kg.ok", "  a : b;c"])
add(["x", "  ?  !", "e.g. , mr. x"])
add(["hELLO.wORLD", "    5 apples ;  2 pears !"])
add(["(see p.12) - ok ?yes"])
add(["  hi!!!   bye ."])
# hidden: small (brute checks these)
add(["a"])
add(["?"])
add([" " * 9 + "z"])
add([chars(random.randint(1, 12), "aB .,!?1 ") for _ in range(400)])
add([prose(random.randint(1, 60)) for _ in range(300)])
add([chars(random.randint(1, 40), LOW + UP + MARKS + OTHER + "     ") for _ in range(300)])
add([prose(random.randint(1, 30), sp=(0, 1), pmark=0.6, pother=0.0) for _ in range(500)])
add([prose(2000, sp=(0, 6)) for _ in range(20)])
# hidden: large
add(["  ".join(random.choices(LOW, k=MAXLEN // 3 + 1))])          # runs of two spaces
add(["".join(a + b for a, b in zip(random.choices(LOW, k=MAXLEN // 2), random.choices(MARKS, k=MAXLEN // 2)))
     for _ in range(2)])                                                                # a mark before every letter
add(["a" + " ,b" * ((MAXLEN - 1) // 3)])                                                # a space before every mark
add([" " * (MAXLEN - 5) + "end.", " " * (MAXLEN - 5) + "?!?."])                         # long leading runs
add(["a" + " " * (MAXLEN - 2) + "b", chars(MAXLEN, "a .")])                             # one huge run
add(prose_lines(MAXN, 1, 30))                                # many short lines
add(prose_lines(2000, 900, 1000, sp=(0, 4), pmark=0.4))
add([chars(MAXLEN, " .!?ab"), chars(MAXLEN, " ,;:aZ1")])
add([prose(MAXLEN, sp=(1, 3), pmark=0.5, pother=0.0), prose(MAXLEN, sp=(0, 2), pmark=0.2)])
add([chars(MAXLEN, "   ,.?aB"), chars(MAXLEN, "  !:x")])
add(["x" + "  ." * ((MAXLEN - 1) // 3), "y" + "  ,  z" * ((MAXLEN - 1) // 6)])     # long runs right before marks
add([prose(MAXLEN, sp=(2, 4), pmark=0.5, pother=0.0), prose(MAXLEN, sp=(2, 5), pmark=0.3)])

for t in tests:
    assert t.endswith("\n") and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
