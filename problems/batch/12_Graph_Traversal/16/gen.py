# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(81010)
MAXN, MAXS = 100000, 10**9
tests = []


def add(tr):
    n = len(tr)
    assert 1 <= n <= MAXN
    assert all(len(t) == 3 and min(t) >= 1 and max(t) <= MAXS for t in tr)
    tests.append(f"{n}\n" + "\n".join(map("%d %d %d".__mod__, tr)) + "\n")


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]
    return a


def triples(s):
    return [(s[i], s[i + 1], s[i + 2]) for i in range(len(s) - 2)]


def route(n, stops):
    k = len(stops)
    rnd = random.random
    return [stops[int(rnd() * k)] for _ in range(n + 2)]


def log(s):
    return shuffle(triples(s))


add([(2, 3, 2), (1, 2, 3), (2, 3, 1), (3, 2, 3)])
add([(9, 5, 7), (7, 5, 9), (5, 9, 5), (5, 7, 5)])
add([(1, 2, 1), (3, 4, 3), (2, 1, 2), (4, 3, 4)])
add([(7, 7, 7)])
add([(1, 1, 2), (1, 1, 1), (2, 1, 1), (1, 2, 1), (1, 1, 1)])
add([(3, 1000000000, 3), (1000000000, 3, 5), (1000000000, 3, 1000000000)])

add([(1, 2, 3), (3, 4, 5)])
add([(MAXS, MAXS, MAXS)] * 6)
add(log(route(7, [1, 2])))
add(shuffle(triples([1, 2, 2, 1, 2, 1]) + [(1, 3, 1), (3, 1, 3)]))
add([(3, 3, 3), (1, 1, 1), (2, 2, 2)])

add(log(route(300, [1, 2, 3])))
s = route(400, list(range(1, 21)))
add(log(s + s[:2]))
add(log(route(200, [10, 20])) + [(20, 20, 20)])
add(log(route(150, [1, 2])) + log([3, 4] * 80))
add(shuffle(triples(route(500, list(range(1, 21)))) + [(21, 21, 21), (22, 22, 22)]))
c = route(98, [6, 7])
add(shuffle(triples(route(500, [1, 2, 3, 4, 5])) + triples(c + c[:2])))

N = MAXN
add(log(route(N, [1, 2, 3])))
add(log(route(N, list(range(1, 11)))))
add(log(route(N, list(range(MAXS - 299, MAXS + 1)))))
add(log(route(N, random.sample(range(1, MAXS + 1), 50000))))
add([(MAXS, MAXS, MAXS)] * (N - 10000))
s = route(N - 2, [7, 8, 9])
add(log(s + s[:2]))
s = [random.choice([1, 2]) for _ in range(30)]
s = (s * (N // 30 + 3))[13:13 + N + 2]
add(log(s))
add(log(list(range(MAXS, MAXS - N - 2, -1))))
add(log(route(N, [1, MAXS])))
s = route(N - 1000, [1, 2])
add(shuffle(triples(s) + triples([1, 3] * 501)))
a = route(N // 2 - 2, [1, 2, 3])
b = route(N // 2 - 2, [4, 5, 6])
add(shuffle(triples(a + a[:2]) + triples(b + b[:2])))
c = route(998, [8, 9])
add(shuffle(triples(route(N - 1000, [1, 2, 3, 4])) + triples(c + c[:2])))
add(shuffle([(x, x, x) for x in random.sample(range(1, MAXS + 1), N)]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
