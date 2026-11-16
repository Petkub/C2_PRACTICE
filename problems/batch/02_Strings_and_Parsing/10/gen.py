# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, datetime

random.seed(151001)
MAXN = 150_000
MAXW = 10 ** 9
DAY = 86400
START = datetime.date(2000, 1, 1)
DATES = [(START + datetime.timedelta(days=k)).isoformat() for k in range(36525)]
assert DATES[-1] == "2099-12-31"
DAY_OF = {d: k for k, d in enumerate(DATES)}
CLOCKS = [f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}" for s in range(DAY)]
CLOCK_OF = {c: s for s, c in enumerate(CLOCKS)}
TEND = len(DATES) * DAY - 1            # 2099-12-31 23:59:59
LEVELS = ("INFO", "WARN", "ERROR")
MSG_CHARS = [chr(c) for c in range(32, 127)]
tests = []


def stamp(sec):
    return DATES[sec // DAY] + " " + CLOCKS[sec % DAY]


def seconds(line):
    return DAY_OF[line[:10]] * DAY + CLOCK_OF[line[11:19]]


def add(w, lines):
    assert 1 <= len(lines) <= MAXN and 1 <= w <= MAXW
    prev = -1
    for ln in lines:
        assert ln[10] == " " and ln[19] == " "
        t = seconds(ln)                 # KeyError if the date or the clock is not valid
        assert t >= prev
        prev = t
        rest = ln[20:]
        lv, sp, msg = rest.partition(" ")
        assert lv in LEVELS
        if sp:
            assert 1 <= len(msg) <= 100 and msg[0] != " " and msg[-1] != " "
    tests.append(f"{len(lines)} {w}\n" + "".join(ln + "\n" for ln in lines))


def message():
    r = random.random()
    if r < 0.3:
        return random.choice(["ERROR", "INFO", "WARN", "ERROR ERROR", "disk ERROR", "x", "retry in 5 s",
                              "user=bob; code=500", "a  b", "2024-02-29 00:00:00 ERROR"])
    k = random.randint(1, 40)
    s = "".join(random.choice(MSG_CHARS) for _ in range(k))
    return s.strip() or "ok"


def line(sec, level, p_msg=0.5):
    s = stamp(sec) + " " + level
    if random.random() < p_msg:
        s += " " + message()
    return s


def from_times(times, p_err=0.6, p_msg=0.5):
    times = sorted(times)
    return [line(t, "ERROR" if random.random() < p_err else random.choice(LEVELS[:2]), p_msg) for t in times]


def at(text):
    """seconds of a 'YYYY-MM-DD HH:MM:SS' text"""
    return DAY_OF[text[:10]] * DAY + CLOCK_OF[text[11:]]


# samples
add(60, ["2024-02-28 23:59:30 ERROR disk full",
         "2024-02-29 00:00:20 ERROR",
         "2024-02-29 00:00:29 INFO ERROR x",
         "2024-02-29 00:01:20 ERROR again"])
add(1000, ["2030-01-01 00:00:00 WARN ERROR"])
add(172800, ["2000-02-28 12:00:00 ERROR a",
             "2000-03-01 12:00:00 ERROR b"])
add(1, ["2099-12-31 23:59:59 ERROR",
        "2099-12-31 23:59:59 ERROR"])
add(1000000000, ["2001-05-05 05:05:05 ERROR",
                 "2033-01-11 06:51:45 ERROR"])
# hidden: small
add(1, ["2000-01-01 00:00:00 ERROR"])
add(2 * DAY, [line(at(f"{y}-{md}"), "ERROR") for y in (2000, 2001)
              for md in ("02-28 12:00:00", "03-01 11:59:59", "03-01 12:00:00")])            # 2000 is a leap year
add(365 * DAY + 1, [line(at(f"{y}-03-01 00:00:00"), "ERROR") for y in range(2003, 2011)])   # so is 2004
add(random.randint(1, 10 ** 6), from_times([random.randint(0, TEND) for _ in range(500)]))
add(3600, from_times([at("2059-12-31 23:00:00") + random.randint(0, 7200) for _ in range(800)], p_err=0.3))
add(500, from_times([random.randint(0, 2000) for _ in range(2000)], p_err=0.9))
# a few equally good windows: the earliest one is the answer
base = at("2077-07-07 07:07:07")
add(100, from_times([base + k * 1000 + j for k in range(5) for j in range(0, 100, 10)], p_err=1.0))


def big(times, w, p_err=0.97, p_msg=0.05):
    assert len(times) == MAXN
    add(w, from_times(times, p_err, p_msg))


# hidden: large
big([random.randint(0, 31 * 365 * DAY) for _ in range(MAXN)], MAXW, p_err=1.0)
big([random.randint(TEND - 30 * 365 * DAY, TEND) for _ in range(MAXN)], MAXW)
big([random.randint(0, TEND) for _ in range(MAXN)], 900_000_000)
big([at("2099-06-01 00:00:00") + random.randint(0, 10 ** 6) for _ in range(MAXN)], 600_000)
big([random.randint(0, TEND) for _ in range(MAXN)], 20 * DAY * 365)
big([at("2096-02-27 00:00:00") + random.randint(0, 4 * DAY) for _ in range(MAXN)], 2 * DAY)
big([at("2048-01-01 00:00:00") + (k // 50) * 7 for k in range(MAXN)], 7 * 1000, p_err=1.0)
big([random.randint(0, TEND) for _ in range(MAXN)], 1, p_err=0.6)
# 2^31 seconds after the start is 2068-01-19 03:14:08; and 2000-02-29 exists
add(60, [line(at("2068-01-19 03:14:00"), "ERROR"), line(at("2068-01-19 03:14:10"), "ERROR")])
WRAP = 2 ** 31
add(3600, from_times([WRAP + random.randint(-20000, 20000) for _ in range(20000)], p_err=0.8))
add(DAY, from_times([at("2000-02-25 00:00:00") + random.randint(0, 10 * DAY) for _ in range(20000)], p_err=0.8))

for t in tests:
    assert t.endswith("\n") and " \n" not in t
    assert t.encode().translate(None, bytes(range(32, 127)) + b"\n") == b""
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
