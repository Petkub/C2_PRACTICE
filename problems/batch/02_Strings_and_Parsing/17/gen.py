# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(151701)
MAXN = 1_000_000
tests = []
LOWER = set("abcdefghijklmnopqrstuvwxyz")


def add(a, b):
    n = len(a)
    assert 1 <= n <= MAXN and len(b) == n
    assert set(a) <= LOWER and set(b) <= LOWER
    t = f"{n}\n{a}\n{b}\n"
    assert all(32 <= ord(c) <= 126 or c == "\n" for c in set(t))
    tests.append(t)


def rs(n, alpha):
    return "".join(random.choices(alpha, k=n))


def pal(n, alpha):
    h = rs(n // 2, alpha)
    return h + (random.choice(alpha) if n % 2 else "") + h[::-1]


def change(s, pos, alpha):

    c = random.choice([x for x in sorted(set(alpha + "b")) if x != s[pos]])
    return s[:pos] + c + s[pos + 1:]


def perturbed(n, alpha, k_a, k_b, where):

    p = pal(n, alpha)
    a, b = p, p
    for _ in range(k_a):
        a = change(a, where(n), alpha)
    for _ in range(k_b):
        b = change(b, where(n), alpha)
    return a, b


def near_mid(n):
    return max(0, min(n - 1, n // 2 + random.randint(-n // 50 - 1, n // 50 + 1)))


def near_end(n):
    x = random.randint(0, n // 50 + 1)
    return min(n - 1, x) if random.random() < 0.5 else max(0, n - 1 - x)


def anywhere(n):
    return random.randint(0, n - 1)


def bounded(n, p, qa, qb, alpha="ab"):

    b = list(pal(n, alpha))
    if qb > 0:
        b[qb - 1] = "a" if b[n - qb] != "a" else "b"
    a = list(pal(n, alpha))
    if qa > 0:
        a[qa - 1] = "a" if a[n - qa] != "a" else "b"

    for k in range(1, p + 1):
        if k != qa and n + 1 - k != qa:
            a[k - 1] = b[n - k]
    return "".join(a), "".join(b)


add("abcab", "cxyba")
add("ab", "ab")
add("z", "q")
add("aaaa", "aaaa")
add("abcd", "dcba")
add("xaaab", "baaay")

add("a", "a")
for n in [3, 7, 10]:
    add(rs(n, "ab"), rs(n, "ab"))
add(*perturbed(11, "ab", 1, 0, anywhere))
add(*perturbed(12, "abc", 0, 1, anywhere))
add(*bounded(20, 10, 0, 10))
add(*bounded(21, 10, 10, 0))
add(*perturbed(3000, "ab", 1, 1, near_mid))
add(*perturbed(5000, "a", 1, 0, near_end))
s = rs(4000, "abc")
add(s, s[::-1])

N = MAXN
add("a" * N, "a" * N)
p = pal(N, "ab")
add(p, p)
s = rs(N, "ab")
add(s, s[::-1])
add(*perturbed(N, "ab", 1, 0, near_mid))
add(*perturbed(N, "ab", 0, 1, near_end))
add(*perturbed(N - 1, "a", 1, 1, anywhere))
add(*perturbed(N, "abc", 2, 1, near_mid))
add(*bounded(N, N // 2, 0, N // 2))
add(*bounded(N - 1, (N - 1) // 2, (N - 1) // 2, 0))
add(*bounded(N, N // 3, N // 4, N // 5))
add(*perturbed(N - 1, "ab", 0, 0, anywhere))
add(rs(N, "abcdefghijklmnopqrstuvwxyz"), rs(N, "abcdefghijklmnopqrstuvwxyz"))
add(*perturbed(N, "a", 1, 0, near_mid))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
