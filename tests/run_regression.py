#!/usr/bin/env python3
"""
Regression tests for the POSN Practice Judge.

  python3 tests/run_regression.py          run everything (exit code 0 = all passed)

1. Every sample in samples/expected.json is judged and must get its verdict (and score, when given).
   Verdict = CE if it does not compile, else the first non-AC verdict, else AC.
2. The judge's command line is run like a student would (repo layout, --ascii, --list).
3. A student package is built with tools/build_dist.py: the layout (one folder per problem, tools/layout.py) and
   judging from a problem folder, from the topic folder and by file name.
   (1. and 2. also run in a built package, so the big tests that gen.py rebuilds never land in the repo.)
4. Self-update: a local HTTP server serves a modified copy of the repo as v9.9; a package must update itself
   (hashes, backups, restart, create-only code files), and must refuse bad hashes, bad paths and no network.
5. A later release (a fake next version, VERSION + 1 in the last place) over local HTTP: a re-titled, a replaced and a moved problem, a clash,
   files the updater did not ship, a new Mixed set 00_Mixed/M<last + 1> and a re-titled Mixed problem, and a quiet second run.
6. manifest.json is up to date.
"""
import contextlib
import functools
import glob
import hashlib
import http.server
import importlib.util
import socket
import threading
import time
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(REPO, "core")
SAMPLES = os.path.join(REPO, "samples")
JUDGE = os.path.join(CORE, "judge.py")
sys.path.insert(0, CORE)
sys.dont_write_bytecode = True     # no __pycache__ inside core/ (it ships to students)
import judge  # noqa: E402
sys.path.insert(0, os.path.join(REPO, "tools"))
import layout  # noqa: E402     tools/layout.py: the names of the student package
import updater  # noqa: E402    core/updater.py: its path rules must agree with tools/layout.py

FAILED = []
STUDENT_JUDGE = os.path.join(os.pardir, "Judge", "judge.py")     # a package's judge, run from a topic folder
TOPIC3 = "03_Prefix_Sums_and_Two_Pointers"      # topic 3; its problem 1 (3-1) is the sample problem
P31 = os.path.join("01", "03-01.cpp")           # its code file inside the topic folder


def problems_json():
    with open(os.path.join(REPO, "problems", "batch", "problems.json"), encoding="utf-8") as f:
        return json.load(f)
os.environ["JUDGE_NO_UPDATE"] = "1"       # the judge never contacts GitHub during the tests


def check(ok, name, detail=""):
    detail = detail.encode("ascii", "backslashreplace").decode("ascii")    # Windows consoles: cp1252
    print(("  ok    " if ok else "  FAIL  ") + name + ("" if ok else "   " + detail))
    if not ok:
        FAILED.append(name)


# ----------------------------------------------------------------------------- 1. verdicts
def judge_sample(src, problem, full):
    """(verdict, score) of src on problem K-P; full = run every test (needed for the score)."""
    meta = judge.load_meta()
    pdir, num = judge.find_problem(problem, meta)
    if not pdir:
        return "no such problem " + problem, 0
    judge.set_sample_count(meta, num)
    st = judge.Style(color=False, ascii_only=True, tty=False)
    tmp = tempfile.mkdtemp(prefix="judge_")
    try:
        exe, _, _, _ = judge.compile_source(src, tmp)
        if not exe:
            return "CE", 0
        with contextlib.redirect_stdout(io.StringIO()):
            if not judge.ensure_tests(pdir, st):
                return "could not rebuild the big tests", 0
            results, _, total = judge.run_tests(exe, pdir, st, 1.0, 0, not full, quiet=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    bad = [r[1] for r in results if r[1] != "AC"]
    peaks = [r[3] for r in results if r[3] is not None]
    PEAK[0] = max(peaks) / (1024 * 1024) if peaks else None
    return (bad[0] if bad else "AC"), judge.compute_score(results, total)[0]


PEAK = [None]      # peak memory (MB) seen by the last judge_sample call


def test_samples():
    print("Samples")
    with open(os.path.join(SAMPLES, "expected.json"), encoding="utf-8") as f:
        expected = json.load(f)
    for name, want in expected.items():
        full = "score" in want
        verdict, score = judge_sample(os.path.join(SAMPLES, name), want["problem"], full)
        ok = verdict == want["verdict"] and (not full or score == want["score"])
        got = verdict + (f" {score}" if full else "")
        check(ok, f"{name:<28} {want['verdict']}", f"got {got}")
        if name.endswith("_ok.cpp"):      # a small program must be measured as small (not the judge's own image)
            check(PEAK[0] is not None and 0.1 < PEAK[0] < 16, f"peak memory of a small program is measured: {PEAK[0]} MB")


def test_exited_peak():
    """A program that exits before the first memory reading must not get the judge's own size (wait4's ru_maxrss)."""
    if os.name == "nt":
        return
    import resource
    own = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    scale = 1 if sys.platform == "darwin" else 1024
    check(judge.exited_peak(own) is None, "a fast small program's peak is unknown, not the judge's own size",
          f"got {judge.exited_peak(own)}")
    check(judge.exited_peak(3 * own) == 3 * own * scale, "a fast big program's ru_maxrss is still used",
          f"got {judge.exited_peak(3 * own)}")


def test_missed_last_reading():
    """A program that grows after the last memory reading (it exits before the next one) is still MLE: wait4's
    ru_maxrss is used too. On macOS this happened when the exiting program was reaped before its final reading."""
    if os.name == "nt":
        return
    name = "linux_peak_memory" if sys.platform.startswith("linux") else "mac_peak_memory"
    real = getattr(judge, name)
    seen = set()

    def first_only(pid):           # one reading right after each start (the program is still tiny), then none
        if pid in seen:
            return None
        seen.add(pid)
        return 1024 * 1024
    setattr(judge, name, first_only)
    try:
        verdict, _ = judge_sample(os.path.join(SAMPLES, "batch", "grid_mle.cpp"), "3-1", False)
    finally:
        setattr(judge, name, real)
    check(verdict == "MLE", "a 400 MB program is MLE even when the readings miss its growth", f"got {verdict}")

# ----------------------------------------------------------------------------- 2. command line
def run_judge(args, cwd=REPO, judge_path=None):
    """Run judge.py like a student. Returns (exit code, output text, output is plain ASCII)."""
    p = subprocess.run([sys.executable, judge_path or JUDGE] + args, cwd=cwd,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stdout.isascii()


def test_cli():
    print("Command line")
    ok_cpp = os.path.join(SAMPLES, "batch", "grid_ok.cpp")
    wa_cpp = os.path.join(SAMPLES, "batch", "grid_int.cpp")
    code, out, _ = run_judge([ok_cpp, "3-1", "--no-color"])
    check(code == 0 and "ACCEPTED" in out, "judge.py grid_ok.cpp 3-1", f"exit {code}\n{out}")
    code, out, _ = run_judge([os.path.join(SAMPLES, "batch", "grid_throw.cpp"), "3-1", "--no-color", "--stop"])
    check("out_of_range" in out and "stderr" in out, "RE shows the program's stderr (out_of_range)", out)
    code, out, _ = run_judge([os.path.join(SAMPLES, "batch", "grid_warn.cpp"), "3-1", "--no-color", "--stop"])
    check("g++ warning" in out and "unused" in out, "warnings are shown after Compiled", out)
    code, out, _ = run_judge([ok_cpp, "3-1", "--no-color", "--stop"])
    check("warning" not in out and "Memory  peak" in out and "256 MB per test" in out,
          "clean program: no warnings, memory line, limit in header", out)
    mle_cpp = os.path.join(SAMPLES, "batch", "grid_mle.cpp")     # 400 MB: a tiny program is under 1 MB on macOS
    code, out, _ = run_judge([mle_cpp, "3-1", "--no-color", "--stop", "--ml", "100"])
    check("Memory Limit Exceeded" in out and "limit is 100 MB" in out, "--ml 100: a 400 MB program is MLE", out)
    code, out, _ = run_judge([mle_cpp, "3-1", "--no-color", "--stop", "--ml", "512"])
    check(code == 0 and "ACCEPTED" in out, "--ml 512: the same program is accepted", f"exit {code}\n{out}")
    code, out, _ = run_judge(["--ml", "0"])
    check(code == 2 and "--ml must be" in out, "judge.py --ml 0 is rejected", f"exit {code}\n{out}")
    code, out, plain = run_judge([wa_cpp, "3-1", "--ascii", "--no-color"])
    check(code == 0 and "First failure" in out and plain, "judge.py --ascii shows the failure, ASCII only",
          f"exit {code}, ascii={plain}\n{out}")
    code, out, plain = run_judge(["--list", "--ascii"])
    check(code == 0 and "Topic 1" in out and plain, "judge.py --list --ascii", f"exit {code}\n{out}")
    code, out, _ = run_judge(["--tl", "abc"])
    check(code == 2 and "--tl must be" in out, "judge.py --tl abc is rejected", f"exit {code}\n{out}")


# ----------------------------------------------------------------------------- 3. student package
def test_student_package():
    print("Student package (one folder per problem)")
    tmp = tempfile.mkdtemp(prefix="judge_dist_")
    try:
        p = subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", tmp, "--no-zip"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        check(p.returncode == 0, "build_dist.py", p.stdout.decode("utf-8", "replace"))
        if p.returncode != 0:
            return
        root = os.path.join(tmp, "C2_Practice")
        test_layout(root)
        set1 = os.path.join(root, TOPIC3)
        old = os.path.join(root, "old_template.cpp")          # the main() starter of older versions
        with open(old, "w") as f:
            f.write("#include <bits/stdc++.h>\nusing namespace std;\n\nint32_t main() {\n"
                    "    cin.tie(0); ios::sync_with_stdio(0);\n\n    return 0;\n}\n")
        check(judge.is_template(old), "the old main() starter still counts as untouched")
        os.remove(old)
        test_judging(root, tmp)
        test_mixed_sets(root)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_layout(root):
    """The package is laid out as tools/layout.py says, and judge.py names the files the same way."""
    sets, meta = judge.load_sets(), problems_json()
    bad, agree, rules, count = [], True, [], 0
    for s in sets:
        folder = layout.folder(s)                       # 04_Binary_Search, 00_Mixed/M01
        top = os.path.join(root, *folder.split("/"))
        want_top = {"Makefile", "judge.bat", f"Problems_{s['dir']}.pdf"} | {layout.slot(s, i) for i in range(1, len(s["problems"]) + 1)}
        got_top = set(os.listdir(top)) if os.path.isdir(top) else set()
        if got_top != want_top:
            bad.append(f"{folder}: {sorted(got_top ^ want_top)}")
        agree = agree and judge.set_folder(s) == folder
        for rel in (f"{folder}/Makefile", f"{folder}/judge.bat", layout.topic_pdf_path(s)):
            if not updater.managed_path(rel):
                rules.append(rel)
        for i, pid in enumerate(s["problems"], 1):
            count += 1
            agree = agree and judge.code_name(s, i) == layout.code_name(s, i) and judge.slot_name(s, i) == layout.slot(s, i)
            if not updater.set_path(layout.code_path(s, i)) or not updater.managed_path(layout.pdf_path(s, i, meta[str(pid)]["en"])):
                rules.append(layout.code_path(s, i))
            d = os.path.join(top, layout.slot(s, i))
            want = {layout.code_name(s, i), layout.pdf_name(s, i, meta[str(pid)]["en"])}
            got = set(os.listdir(d)) if os.path.isdir(d) else set()
            if got != want:
                bad.append(f"{folder}/{layout.slot(s, i)}: {sorted(got ^ want)}")
            elif os.path.getsize(os.path.join(d, layout.code_name(s, i))) != 0:
                bad.append(f"{folder}/{layout.slot(s, i)}: the code file is not empty")
            else:
                with open(os.path.join(d, layout.pdf_name(s, i, meta[str(pid)]["en"])), "rb") as f:
                    if f.read(5) != b"%PDF-":
                        bad.append(f"{folder}/{layout.slot(s, i)}: not a PDF")
    check(not bad, f"every problem folder ({count}) holds exactly its empty code file and its PDF; "
          "every topic folder its PDF, Makefile, judge.bat and the problem folders", "\n".join(bad[:8]))
    check(agree, "judge.py and tools/layout.py name the topic / set folders, problem folders and code files the same way")
    check(not rules, "updater.py accepts every code file (create-only), PDF, Makefile and judge.bat of tools/layout.py",
          str(rules[:5]))
    mixed = [s for s in sets if judge.is_mixed(s)]
    if mixed:
        old_root = [f"{s['dir']}/3/{s['dir']}-3.cpp" for s in mixed] + [f"{s['dir']}/Makefile" for s in mixed] + [
            f"{s['dir']}/Problems_{s['dir']}.pdf" for s in mixed] + [f"{layout.MIXED_ROOT}/Makefile",
                                                                   f"{layout.MIXED_ROOT}/01/00-01.cpp"]
        check(not any(updater.set_path(r) or updater.managed_path(r) or updater.OLD_FILE.match(r) for r in old_root)
              and updater.managed_path(layout.MIXED_README),
              "updater.py: Mixed paths only under 00_Mixed/ (M01/... at the package root is refused), 00_Mixed/README.txt managed")
        visible = sorted(n for n in os.listdir(root) if not n.startswith("."))
        inner = sorted(os.listdir(os.path.join(root, layout.MIXED_ROOT))) if os.path.isdir(os.path.join(root, layout.MIXED_ROOT)) else []
        check(visible[:1] == [layout.MIXED_ROOT] and not any(re.fullmatch(r"M[0-9]{2}", n) for n in visible)
              and inner == sorted(["README.txt"] + [s["dir"] for s in mixed]),
              "00_Mixed/ is the first folder of the package and holds README.txt and the Mixed sets (none at the top)",
              f"{visible[:4]} {inner}")
    names = [n for _, _, fs in os.walk(root) for n in fs] + [n for _, ds, _ in os.walk(root) for n in ds]
    check(all(n.isascii() and " " not in n for n in names), "every file and folder name is ASCII without spaces")
    pdfs = [layout.pdf_name(s, i, meta[str(pid)]["en"]) for s in sets for i, pid in enumerate(s["problems"], 1)]
    check(all(re.fullmatch(r"[0-9]{1,2}_[A-Za-z0-9_]{1,60}\.pdf", n) for n in pdfs),
          "problem PDF names: <slot>_<EnglishTitle>.pdf, letters, digits and _ only, title at most 60 characters")
    check(layout.title_slug("Mo's  Algo-rithm: 2 (hard)") == "Mos_Algorithm_2_hard" and len(layout.title_slug("x" * 80)) == 60,
          "title -> file name: spaces become _, other characters are dropped, at most 60 characters")
    stray = [os.path.join(dp, n) for dp, _, fs in os.walk(root) for n in fs
             if os.path.basename(os.path.dirname(dp)) != "Judge" and "Judge" not in dp.split(os.sep)
             and (n.endswith((".in", ".out", ".exe", ".o")) or n == "a.out")]
    check(not stray, "no sample files or binaries in the topic and problem folders", str(stray[:5]))


def test_judging(root, tmp):
    """Judging from the problem folder, from the topic folder and by file name; nothing is left in the folders,
    and Judge/.build/ (where the programs are compiled) is empty afterwards."""
    set1 = os.path.join(root, TOPIC3)
    prob = os.path.join(set1, "01")
    ok_cpp = os.path.join(SAMPLES, "batch", "grid_ok.cpp")
    shutil.copy(ok_cpp, os.path.join(set1, P31))
    before = {dp: sorted(fs) for dp, _, fs in os.walk(set1)}
    deep = os.path.join(os.pardir, os.pardir, "Judge", "judge.py")
    code, out, _ = run_judge(["--no-color"], cwd=prob, judge_path=deep)
    check(code == 0 and "ACCEPTED" in out and "03-01.cpp" in out, "inside the problem folder: judge.py (no arguments)",
          f"exit {code}\n{out}")
    code, out, _ = run_judge(["03-01.cpp", "--no-color"], cwd=prob, judge_path=deep)
    check(code == 0 and "ACCEPTED" in out, "inside the problem folder: judge.py 03-01.cpp", f"exit {code}\n{out}")
    for arg in ("1", "01", P31):
        code, out, _ = run_judge([arg, "--no-color"], cwd=set1, judge_path=STUDENT_JUDGE)
        check(code == 0 and "ACCEPTED" in out, f"inside the topic folder: judge.py {arg}", f"exit {code}\n{out}")
    code, out, _ = run_judge(["--no-color"], cwd=set1, judge_path=STUDENT_JUDGE)
    check(code == 0 and "Total" in out and "02/03-02.cpp is still empty - skipped" in out and "Problem 1" in out
          and " 100 / 2000" in out, "inside the topic folder: judge.py (whole topic)", f"exit {code}\n{out}")
    code, out, _ = run_judge(["2", "--no-color"], cwd=set1, judge_path=STUDENT_JUDGE)
    check(code == 0 and "03-02.cpp is empty" in out and "Compil" not in out, "an empty code file: plain message, no compile",
          f"exit {code}\n{out}")
    full = os.path.join(root, "Judge", "judge.py")
    code, out, _ = run_judge([os.path.join(set1, P31), "--no-color"], cwd=tmp, judge_path=full)
    check(code == 0 and "ACCEPTED" in out, "anywhere: judge.py <path>/03-01.cpp (the VS Code task)", f"exit {code}\n{out}")
    away = os.path.join(tmp, "elsewhere")
    os.makedirs(away)
    shutil.copy(ok_cpp, os.path.join(away, "03-01.cpp"))
    code, out, _ = run_judge([os.path.join(away, "03-01.cpp"), "--no-color"], cwd=away, judge_path=full)
    check(code == 0 and "ACCEPTED" in out, "by file name alone: 03-01.cpp in another folder", f"exit {code}\n{out}")
    shutil.copy(ok_cpp, os.path.join(prob, "second_try.cpp"))
    code, out, _ = run_judge(["second_try.cpp", "--no-color"], cwd=prob, judge_path=deep)
    check(code == 0 and "ACCEPTED" in out, "by folder alone: another .cpp inside the problem folder", f"exit {code}\n{out}")
    os.remove(os.path.join(prob, "second_try.cpp"))
    code, out, _ = run_judge([os.path.join(away, "03-01.cpp"), "3-2", "--no-color", "--stop"], cwd=away, judge_path=full)
    check(code == 0 and "ACCEPTED" not in out and "Problem not found" not in out, "an explicit K-P wins over the file name",
          f"exit {code}\n{out}")
    shutil.copy(ok_cpp, os.path.join(away, "mine.cpp"))
    code, out, _ = run_judge([os.path.join(away, "mine.cpp"), "--no-color"], cwd=away, judge_path=full)
    check(code == 1 and "Cannot tell which problem" in out and "04_Binary_Search/05/04-05.cpp" in out,
          "a .cpp with no problem in its name or folders: a clear message", f"exit {code}\n{out}")
    code, out, _ = run_judge(["99", "--no-color"], cwd=set1, judge_path=STUDENT_JUDGE)
    check(code != 0 and "Traceback" not in out, "inside the topic folder: judge.py 99 is refused", f"exit {code}\n{out}")
    if os.name != "nt" and shutil.which("make"):
        env = dict(os.environ, PYTHON=sys.executable, NO_COLOR="1")
        for args, what in ((["1"], "make 1 in the topic folder"), (["01"], "make 01 in the topic folder")):
            r = subprocess.run(["make"] + args, cwd=set1, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = r.stdout.decode("utf-8", "replace")
            check(r.returncode == 0 and "ACCEPTED" in out, what, out[-600:])
        r = subprocess.run(["make"], cwd=set1, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = r.stdout.decode("utf-8", "replace")
        check(r.returncode == 0 and "Total" in out and " 100 / 2000" in out, "make in the topic folder (whole topic)",
              out[-600:])
    with open(os.path.join(set1, "judge.bat"), "rb") as f:
        topic_bat = f.read()
    check(b'"%JUDGE%" %1' in topic_bat and b'set "JUDGE=..\\Judge\\judge.py"' in topic_bat
          and b'"..\\..\\Judge\\judge.py"' in topic_bat and b'cd /d "%~dp0"' in topic_bat
          and topic_bat.count(b"\r\n") == topic_bat.count(b"\n") > 5,
          "judge.bat (topic / Mixed-set folder): finds ..\\Judge or ..\\..\\Judge, quoted, runs from its own folder, passes %1, CRLF")
    with open(os.path.join(root, ".vscode", "tasks.json"), encoding="utf-8") as f:
        tasks = json.load(f)["tasks"]
    check(tasks[0]["args"][-1] == "${file}" and tasks[0]["group"].get("isDefault") and "/.." in tasks[1]["options"]["cwd"],
          "VS Code: Ctrl+Shift+B judges the open file, the second task the whole topic")
    after = {dp: sorted(fs) for dp, _, fs in os.walk(set1)}
    check(after == before, "judging leaves no binary or temporary file in the topic or problem folders",
          str([(k, v) for k, v in after.items() if before.get(k) != v][:3]))
    build = os.path.join(root, "Judge", ".build")
    check(os.path.isdir(build) and os.listdir(build) == [], "programs are compiled in Judge/.build/, which is empty afterwards",
          str(os.listdir(build)) if os.path.isdir(build) else "no Judge/.build")
    os.chmod(build, 0o500)
    try:
        if os.name != "nt" and not os.access(build, os.W_OK):       # (root can always write: skipped then)
            code, out, _ = run_judge(["--no-color"], cwd=prob, judge_path=deep)
            check(code == 0 and "ACCEPTED" in out and os.listdir(build) == [],
                  "Judge/.build/ not writable: the judge compiles in the system temp folder instead", f"exit {code}\n{out}")
    finally:
        os.chmod(build, 0o700)
    code, out, _ = run_judge(["--list", "--no-color"], cwd=root, judge_path=os.path.join("Judge", "judge.py"))
    check(code == 0 and "03-01 " in out and f"{TOPIC3}/01 ... 20" in out, "judge.py --list shows the folders and code names",
          f"exit {code}\n{out[:900]}")


TECHNIQUE_WORDS = ("dp", "dynamic", "greedy", "binary search", "prefix", "two pointers", "graph", "bfs", "dfs",
                   "dijkstra", "shortest", "dsu", "union", "heap", "stack", "queue", "sort", "sweep", "knapsack",
                   "sieve", "number theory", "combinator", "implementation", "tree")


def test_mixed_sets(root):
    """Mixed sets (folders 00_Mixed/M01 ...): judged like a topic, and nothing a student sees names a topic or a
    technique: the folders, the PDF name, 00_Mixed/README.txt, sets.json and the judge's headers say only "Mixed M01"
    (titles are story names). Every way of judging works one folder deeper than in a topic (plans/V4_MIXED_FOLDER.md):
    Ctrl+Shift+B (the tasks.json command line), make / make 3 / judge.py 3 in the set folder, judge.py in a problem
    folder, judge.py FILE from anywhere, by name and by folder; --list shows the Mixed sets first."""
    mixed = [s for s in judge.load_sets() if judge.is_mixed(s)]
    if not mixed:
        return
    check(all(re.fullmatch(r"M[0-9]{2}", s["dir"]) and len(s["problems"]) == 6 for s in mixed)
          and [s["dir"] for s in mixed] == sorted(s["dir"] for s in mixed),
          f"{len(mixed)} Mixed sets M01 ... of 6 problems")
    texts = [s.get("level_en", "") + " " + s.get("group", "") for s in mixed]
    readme = read(os.path.join(root, *layout.MIXED_README.split("/"))) or ""
    check(not any(w in t.lower() for t in texts + [readme] for w in TECHNIQUE_WORDS),
          "sets.json and 00_Mixed/README.txt name no technique for a Mixed set", str(texts))
    check(readme.startswith("ชุดฝึกรวม ไม่บอกหัวข้อ") and f"M01 → {mixed[-1]['dir']}" in readme and len(readme.splitlines()) <= 3,
          "00_Mixed/README.txt: short and neutral (order of the sets, easy to hard)", readme)
    s1 = mixed[0]
    name = s1["dir"]
    m1 = os.path.join(root, *layout.folder(s1).split("/"))          # 00_Mixed/M01
    set_judge = os.path.join(os.pardir, os.pardir, "Judge", "judge.py")
    names = sorted(os.listdir(m1)) if os.path.isdir(m1) else []
    check(names == sorted([str(i) for i in range(1, 7)] + ["Makefile", "judge.bat", f"Problems_{name}.pdf"])
          and os.path.isfile(os.path.join(m1, "3", f"{name}-3.cpp")),
          f"00_Mixed/{name}/ holds the folders 1 ... 6 (with {name}-3.cpp ...), Makefile, judge.bat and Problems_{name}.pdf",
          str(names))
    code, out, _ = run_judge(["--no-color"], cwd=m1, judge_path=set_judge)
    check(code == 0 and f"Mixed {name}" in out and "Topic" not in out and "Problem 6" in out
          and out.count("still empty - skipped") == 6, f"inside 00_Mixed/{name}: ../../Judge/judge.py (whole set), no topic shown",
          f"exit {code}\n{out}")
    src = os.path.join(m1, "3", f"{name}-3.cpp")
    with open(src, "w") as f:
        f.write("int main() { return 0; }\n")
    code, out, _ = run_judge(["3", "--no-color"], cwd=m1, judge_path=set_judge)
    check(code == 0 and f"Mixed {name}" in out and "Topic" not in out and "Problem not found" not in out
          and "Result" in out, f"inside 00_Mixed/{name}: judge.py 3", f"exit {code}\n{out}")
    prob = os.path.join(m1, "3")
    code, out, _ = run_judge(["--no-color"], cwd=prob, judge_path=os.path.join(os.pardir, os.pardir, os.pardir, "Judge", "judge.py"))
    check(code == 0 and f"Mixed {name}" in out and "Topic" not in out and "Result" in out,
          f"inside 00_Mixed/{name}/3: ../../../Judge/judge.py (no arguments)", f"exit {code}\n{out}")
    with open(os.path.join(root, ".vscode", "tasks.json"), encoding="utf-8") as f:
        tasks = json.load(f)["tasks"]

    def task(t, path):          # the command line VS Code runs for a task on the open file `path`
        ws, fdir = root, os.path.dirname(path)
        args = [a.replace("${workspaceFolder}", ws).replace("${file}", path).replace("${fileDirname}", fdir) for a in t["args"]]
        cwd = os.path.normpath(t["options"]["cwd"].replace("${workspaceFolder}", ws).replace("${fileDirname}", fdir))
        return run_judge(args[1:] + ["--no-color"], cwd=cwd, judge_path=args[0])
    code, out, _ = task(tasks[0], src)
    check(code == 0 and f"Mixed {name}" in out and "Result" in out and "Problem not found" not in out,
          f"Ctrl+Shift+B (tasks.json) on 00_Mixed/{name}/3/{name}-3.cpp", f"exit {code}\n{out}")
    code, out, _ = task(tasks[1], src)
    check(code == 0 and f"Mixed {name}" in out and "Problem 6" in out and "Total" in out,
          f"Run Task > Judge whole topic on 00_Mixed/{name}/3/{name}-3.cpp: the whole set", f"exit {code}\n{out}")
    code, out, _ = run_judge([src, f"{name}-3", "--no-color"], cwd=root, judge_path=os.path.join("Judge", "judge.py"))
    check(code == 0 and "Problem not found" not in out, f"judge.py FILE {name}-3", f"exit {code}\n{out}")
    away = os.path.join(os.path.dirname(root), "mixed_elsewhere")
    os.makedirs(away, exist_ok=True)
    shutil.copy(src, os.path.join(away, f"{name}-3.cpp"))
    shutil.copy(src, os.path.join(prob, "try2.cpp"))
    full = os.path.join(root, "Judge", "judge.py")
    code, out, _ = run_judge([os.path.join(away, f"{name}-3.cpp"), "--no-color"], cwd=away, judge_path=full)
    check(code == 0 and f"Mixed {name}" in out and "Result" in out, f"by file name alone: {name}-3.cpp in another folder",
          f"exit {code}\n{out}")
    code, out, _ = run_judge([os.path.join(prob, "try2.cpp"), "--no-color"], cwd=away, judge_path=full)
    check(code == 0 and f"Mixed {name}" in out and "Result" in out, f"by folder alone: another .cpp in 00_Mixed/{name}/3",
          f"exit {code}\n{out}")
    os.remove(os.path.join(prob, "try2.cpp"))
    shutil.rmtree(away, ignore_errors=True)
    if os.name != "nt" and shutil.which("make"):
        env = dict(os.environ, PYTHON=sys.executable, NO_COLOR="1")
        r = subprocess.run(["make", "3"], cwd=m1, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = r.stdout.decode("utf-8", "replace")
        check(r.returncode == 0 and f"Mixed {name}" in out and "Result" in out, f"make 3 in 00_Mixed/{name}", out[-600:])
        r = subprocess.run(["make"], cwd=m1, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = r.stdout.decode("utf-8", "replace")
        check(r.returncode == 0 and "Total" in out and " / 600" in out, f"make in 00_Mixed/{name} (whole set)", out[-600:])
    code, out, _ = run_judge(["--list", "--no-color"], cwd=root, judge_path=os.path.join("Judge", "judge.py"))
    first_topic = out.find("Topic 1 ")
    check(code == 0 and f"Mixed {mixed[-1]['dir']}" in out and f"Topic {mixed[0]['set']}" not in out
          and f"{len(mixed)} mixed sets" in out and f"{name}-3 " in out and f"00_Mixed/{name}/1 ... 6" in out
          and 0 <= out.find(f"Mixed {mixed[-1]['dir']}") < first_topic,
          "judge.py --list shows the Mixed sets by name (00_Mixed/M01/1 ... 6), first, then the topics",
          f"exit {code}\n{out[:900]}")
    open(src, "w").close()


# ----------------------------------------------------------------------------- 4. self-update
def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def serve(folder, log=None):
    """Serve folder over HTTP on a free port of this computer (stands in for raw.githubusercontent.com).
    log: a list that gets the path of every request."""
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            if log is not None:
                log.append(self.path.split("?")[0])
            super().do_GET()

    handler = functools.partial(Handler, directory=folder)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}/"


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def make_repo2(tmp, version, marker):
    """A copy of the repo with a new VERSION, a marker line in judge.py and a changed README, manifest rebuilt."""
    repo2 = os.path.join(tmp, "repo2")
    if os.path.exists(repo2):
        shutil.rmtree(repo2)
    shutil.copytree(REPO, repo2, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
    with open(os.path.join(repo2, "VERSION"), "w") as f:
        f.write(version + "\n")
    with open(os.path.join(repo2, "core", "judge.py"), "a") as f:
        f.write(f"\n# {marker}\n")
    with open(os.path.join(repo2, "core", "README.txt"), "a") as f:
        f.write(f"{marker}\n")
    for name in (("student", "README.txt"), ("student", "set_files", "Makefile"), ("student", "set_files", "Makefile_6"),
                 ("student", *layout.MIXED_README.split("/"))):     # managed package files
        if os.path.exists(os.path.join(repo2, *name)):
            with open(os.path.join(repo2, *name), "a", encoding="utf-8") as f:
                f.write(f"\n# {marker}\n")
    rebuild_manifest(repo2)
    return repo2


def rebuild_manifest(repo2):
    subprocess.run([sys.executable, os.path.join(repo2, "tools", "build_manifest.py")], check=True,
                   stdout=subprocess.DEVNULL)


def edit_manifest(repo2, fn):
    """fn changes manifest.json as updaters read it."""
    p = os.path.join(repo2, "manifest.json")
    with open(p, encoding="utf-8") as f:
        m = json.load(f)
    fn(m)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(m, f)


def run_student(args, cwd, url, judge_path=None):
    """Run the package's judge from a topic folder (../Judge/judge.py, or judge_path) with updates from url."""
    env = dict(os.environ, JUDGE_UPDATE_URL=url)
    env.pop("JUDGE_NO_UPDATE", None)
    t0 = time.time()
    p = subprocess.run([sys.executable, judge_path or os.path.join(os.pardir, "Judge", "judge.py")] + args, cwd=cwd, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    return p.returncode, p.stdout.decode("utf-8", "replace"), time.time() - t0


def test_updater():
    print("Self-update")
    tmp = tempfile.mkdtemp(prefix="judge_upd_")
    try:
        subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", tmp, "--no-zip"],
                       check=True, stdout=subprocess.DEVNULL)
        root = os.path.join(tmp, "C2_Practice")
        judge_dir, set1 = os.path.join(root, "Judge"), os.path.join(root, TOPIC3)
        one, two, new = P31, os.path.join("02", "03-02.cpp"), os.path.join("21", "03-21.cpp")
        shutil.copy(os.path.join(SAMPLES, "batch", "grid_ok.cpp"), os.path.join(set1, one))
        student_hash, old_judge = sha(os.path.join(set1, one)), sha(os.path.join(judge_dir, "judge.py"))
        template = sha(os.path.join(set1, two))

        # a) automatic update during a normal run: new files, backup, restart with the new judge
        repo2 = make_repo2(tmp, "9.9", "marker-v9.9")
        edit_manifest(repo2, lambda m: m["create_only"].update(
            {TOPIC3 + "/21/03-21.cpp": [sha(os.path.join(REPO, "student", "set_files", "template.cpp")), "student/set_files/template.cpp"]}))
        srv, url = serve(repo2)
        code, out, _ = run_student([one, "--no-color"], set1, url)
        check(code == 0 and "restarting" in out and "ACCEPTED" in out and "Judge v9.9" in out,
              "normal run updates to v9.9, restarts, judges", f"exit {code}\n{out}")
        with open(os.path.join(judge_dir, "judge.py"), encoding="utf-8") as f:
            new_judge = f.read()
        check("marker-v9.9" in new_judge and sha(os.path.join(judge_dir, ".backup", "judge.py")) == old_judge,
              "judge.py replaced, old one kept in Judge/.backup/")
        with open(os.path.join(root, "README.txt"), encoding="utf-8") as f:
            readme = f.read()
        with open(os.path.join(set1, "Makefile"), encoding="utf-8") as f:
            makefile = f.read()
        check("marker-v9.9" in readme and "marker-v9.9" in makefile
              and os.path.exists(os.path.join(judge_dir, ".backup", "_package", TOPIC3, "Makefile")),
              "managed files README.txt and the topic Makefile replaced, old copies in Judge/.backup/_package/")
        m1 = layout.folder(next(s for s in judge.load_sets() if judge.is_mixed(s)))
        check("marker-v9.9" in (read(os.path.join(root, *m1.split("/"), "Makefile")) or "")
              and "marker-v9.9" in (read(os.path.join(root, *layout.MIXED_README.split("/"))) or "")
              and os.path.exists(os.path.join(judge_dir, ".backup", "_package", *m1.split("/"), "Makefile")),
              f"managed files {m1}/Makefile and 00_Mixed/README.txt replaced too")
        check(sha(os.path.join(set1, one)) == student_hash and sha(os.path.join(set1, two)) == template,
              "student files untouched")
        check(os.path.exists(os.path.join(set1, new)) and sha(os.path.join(set1, new)) == template,
              "a create-only code file (21/03-21.cpp) is added")
        check(not os.path.exists(os.path.join(judge_dir, ".update_tmp")), "no temp folder left behind")
        code, out, _ = run_student(["--update", "--no-color"], set1, url)
        check(code == 0 and "up to date" in out, "--update: up to date", f"exit {code}\n{out}")

        # b) a newer version appears: normal runs wait 10 minutes, --update takes it now
        repo2 = make_repo2(tmp, "9.11", "marker-v9.11")
        code, out, _ = run_student([one, "--no-color"], set1, url)
        check(code == 0 and "Judge v9.9" in out and "restarting" not in out, "checked recently: no update yet")
        code, out, _ = run_student(["--update", "--no-color"], set1, url)
        check(code == 0 and "updated to v9.11" in out, "--update: updated to v9.11", f"exit {code}\n{out}")

        # c) served file does not match its hash: nothing changes
        edit_manifest(repo2, lambda m: m["files"].update({"README.txt": "1" * 64}) or m.update(version="9.12"))
        before = sha(os.path.join(judge_dir, "README.txt"))
        code, out, _ = run_student(["--update", "--no-color"], set1, url)
        check(code == 1 and "hash mismatch" in out and sha(os.path.join(judge_dir, "README.txt")) == before
              and "9.11" in open(os.path.join(judge_dir, "manifest.json"), encoding="utf-8").read(),
              "bad hash: update refused, files unchanged", f"exit {code}\n{out}")

        # d) manifest with a path outside Judge/: refused
        rebuild_manifest(repo2)
        edit_manifest(repo2, lambda m: m["files"].update({"../evil.txt": "0" * 64}) or m.update(version="9.13"))
        code, out, _ = run_student(["--update", "--no-color"], set1, url)
        check(code == 1 and "bad path" in out and not os.path.exists(os.path.join(root, "evil.txt")),
              "path outside Judge/: refused", f"exit {code}\n{out}")
        rebuild_manifest(repo2)
        edit_manifest(repo2, lambda m: m["managed"].update(
            {TOPIC3 + "/01/03-01.cpp": [sha(os.path.join(repo2, "student", "set_files", "template.cpp")), "student/set_files/template.cpp"]})
            or m.update(version="9.14"))
        code, out, _ = run_student(["--update", "--no-color"], set1, url)
        check(code == 1 and "bad managed entry" in out and sha(os.path.join(set1, one)) == student_hash,
              "a .cpp listed as managed: refused, student file untouched", f"exit {code}\n{out}")
        for n, name in enumerate(("Makefile", "judge.bat")):     # a problem folder holds its code file and its PDF only
            rebuild_manifest(repo2)
            edit_manifest(repo2, lambda m: m["managed"].update(
                {f"{TOPIC3}/01/{name}": [sha(os.path.join(repo2, "student", "set_files", name)), "student/set_files/" + name]})
                or m.update(version=f"9.1{5 + n}"))
            code, out, _ = run_student(["--update", "--no-color"], set1, url)
            check(code == 1 and "bad managed entry" in out and not os.path.exists(os.path.join(set1, "01", name)),
                  f"a managed {name} inside a problem folder ({TOPIC3}/01/{name}) is refused", f"exit {code}\n{out}")
        for n, rel in enumerate((TOPIC3 + "/1.cpp", TOPIC3 + "/01/04-01.cpp", TOPIC3 + "/01/03-02.cpp", "M01/3/M02-3.cpp",
                                 TOPIC3 + "/old/1_X.cpp", "Judge/x.cpp", "M01/3/M01-3.cpp", "00_Mixed/M01/3/M02-3.cpp",
                                 "00_Mixed/01/00-01.cpp")):
            rebuild_manifest(repo2)
            edit_manifest(repo2, lambda m: m["create_only"].update(
                {rel: [sha(os.path.join(repo2, "student", "set_files", "template.cpp")), "student/set_files/template.cpp"]})
                or m.update(version=f"9.2{n}"))
            code, out, _ = run_student(["--update", "--no-color"], set1, url)
            check(code == 1 and "bad create-only entry" in out and not os.path.exists(os.path.join(root, *rel.split("/"))),
                  f"a create-only path that is not <topic>/<slot>/<no.>-<slot>.cpp is refused ({rel})", f"exit {code}\n{out}")
        for n, rel in enumerate(("M01/Makefile", "M01/Problems_M01.pdf", "00_Mixed/Makefile")):    # Mixed: only in 00_Mixed/M01
            rebuild_manifest(repo2)
            edit_manifest(repo2, lambda m: m["managed"].update(
                {rel: [sha(os.path.join(repo2, "student", "set_files", "Makefile")), "student/set_files/Makefile"]})
                or m.update(version=f"9.3{n}"))
            code, out, _ = run_student(["--update", "--no-color"], set1, url)
            check(code == 1 and "bad managed entry" in out and not os.path.exists(os.path.join(root, *rel.split("/"))),
                  f"a managed path outside 00_Mixed/M01 ... ({rel}) is refused", f"exit {code}\n{out}")

        # e) recovery: a damaged file is re-downloaded by python Judge/updater.py
        rebuild_manifest(repo2)
        os.remove(os.path.join(judge_dir, "README.txt"))
        shutil.rmtree(os.path.join(root, ".vscode"))     # lost when the package was copied (hidden folder)
        env = dict(os.environ, JUDGE_UPDATE_URL=url)
        p = subprocess.run([sys.executable, os.path.join(judge_dir, "updater.py")], env=env, cwd=set1,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.stdout.decode("utf-8", "replace")
        check(p.returncode == 0 and os.path.exists(os.path.join(judge_dir, "README.txt")),
              "python Judge/updater.py restores a missing file", f"exit {p.returncode}\n{out}")
        check(os.path.exists(os.path.join(root, ".vscode", "tasks.json")),
              "a missing .vscode/ (Ctrl+Shift+B task) is restored too", f"exit {p.returncode}\n{out}")
        srv.shutdown()

        # f) no network: the judge works as usual, quickly
        os.remove(os.path.join(judge_dir, ".update_check"))
        code, out, dt = run_student([one, "--no-color"], set1, f"http://127.0.0.1:{free_port()}/")
        check(code == 0 and "ACCEPTED" in out and "restarting" not in out and dt < 30,
              f"offline: judge works ({dt:.1f} s)", f"exit {code}\n{out}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_versions():
    """The updater only moves to a strictly newer version. The release served here (9.9) is older-looking content:
    no report.py / config.json, another judge.py and a re-titled problem PDF (what made a newer build go back to 4.0.0,
    retiring its PDFs). Installed newer (9.10) or the same (9.9): nothing changes, even with --update. Older (9.8):
    the normal update."""
    print("Update only to a newer version")
    tmp = tempfile.mkdtemp(prefix="judge_ver_")
    try:
        subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", tmp, "--no-zip"],
                       check=True, stdout=subprocess.DEVNULL)
        root = os.path.join(tmp, "C2_Practice")
        judge_dir, set1 = os.path.join(root, "Judge"), os.path.join(root, TOPIC3)
        repo2 = make_repo2(tmp, "9.9", "marker-v9.9")
        for name in ("report.py", "config.json"):            # files of a newer build (grader-discord)
            if os.path.exists(os.path.join(repo2, "core", name)):
                os.remove(os.path.join(repo2, "core", name))
        rebuild_manifest(repo2)
        pdf = next(k for k in sorted(json.load(open(os.path.join(repo2, "manifest.json"), encoding="utf-8"))["managed"])
                   if re.fullmatch(r".+/[0-9]+/[0-9]+_[A-Za-z0-9_]+\.pdf", k))
        retitled = pdf.rsplit("/", 1)[0] + "/" + pdf.rsplit("/", 1)[1].split("_")[0] + "_Retitled_Problem.pdf"
        edit_manifest(repo2, lambda m: m["managed"].update({retitled: m["managed"].pop(pdf)}))
        srv, url = serve(repo2)

        def mark(version):
            p = os.path.join(judge_dir, "manifest.json")
            with open(p, encoding="utf-8") as f:
                m = json.load(f)
            m["version"] = version
            with open(p, "w", encoding="utf-8") as f:
                json.dump(m, f)

        def snapshot():
            out = {}
            for dp, ds, fs in os.walk(root):
                for f in fs:
                    rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
                    if rel not in ("Judge/.update_check", "Judge/manifest.json"):
                        out[rel] = sha(os.path.join(dp, f))
            return out

        def runs():
            outs = []
            for args in (["--list"], ["--update"]):
                if os.path.exists(os.path.join(judge_dir, ".update_check")):
                    os.remove(os.path.join(judge_dir, ".update_check"))
                outs.append(run_student(args + ["--no-color"], set1, url)[1])
            return outs

        before = snapshot()
        for version, word in (("9.10", "newer than the published v9.9"), ("9.9.0", "up to date")):
            mark(version)
            auto, forced = runs()
            check(snapshot() == before and "restarting" not in auto and word in forced
                  and not os.path.exists(os.path.join(judge_dir, ".backup")),
                  f"installed {version}, release 9.9: nothing changes (no file, no PDF retired), also with --update",
                  forced[-500:])
        header = os.path.join("include", "bits", "stdc++.h")         # the same bytes in the release: put back
        os.remove(os.path.join(judge_dir, header))
        os.remove(os.path.join(judge_dir, "README.txt"))              # other bytes in the release: not touched
        p = subprocess.run([sys.executable, os.path.join(judge_dir, "updater.py")], cwd=set1, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, env=dict(os.environ, JUDGE_UPDATE_URL=url))
        after = snapshot()
        check("repaired 1 files" in p.stdout.decode() and after.get("Judge/include/bits/stdc++.h") == before["Judge/include/bits/stdc++.h"]
              and after.get("Judge/README.txt") is None and after.get("Judge/report.py") == before.get("Judge/report.py"),
              "same version, forced: only a file the release has exactly as installed is put back (README.txt differs: not)",
              p.stdout.decode()[-300:])
        shutil.copy(os.path.join(REPO, "core", "README.txt"), os.path.join(judge_dir, "README.txt"))
        mark("9.8")
        auto, _ = runs()
        check("restarting" in auto and "marker-v9.9" in open(os.path.join(judge_dir, "judge.py"), encoding="utf-8").read()
              and os.path.exists(os.path.join(root, *retitled.split("/"))),
              "installed 9.8, release 9.9: the normal update", auto[-500:])
        srv.shutdown()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_fast_update():
    """A package from a release before the newest topic gets that whole topic in a few requests (a bundle for the
    test data, one template for all the code files, the topic's Makefile and judge.bat, and the PDFs)."""
    print("Fast update")
    tmp = tempfile.mkdtemp(prefix="judge_fast_")
    try:
        subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", tmp, "--no-zip"],
                       check=True, stdout=subprocess.DEVNULL)
        root = os.path.join(tmp, "C2_Practice")
        judge_dir = os.path.join(root, "Judge")
        last = sorted(d for d in os.listdir(root) if d[:2].isdigit() and "_" in d)[-1]
        last_n = len(next(s for s in judge.load_sets() if s["dir"] == last)["problems"])
        # an older package: its manifest does not know the last topic, whose folders are not there yet
        with open(os.path.join(judge_dir, "manifest.json"), encoding="utf-8") as f:
            old = json.load(f)
        old["version"] = "0.9"
        old["files"] = {k: v for k, v in old["files"].items() if not k.startswith("problems/batch/%s/" % last)}
        for key in ("managed", "create_only"):
            old[key] = {k: v for k, v in old.get(key, {}).items() if not k.startswith(last + "/")}
        old.pop("bundles", None)
        with open(os.path.join(judge_dir, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(old, f)
        shutil.rmtree(os.path.join(judge_dir, "problems", "batch", last))
        shutil.rmtree(os.path.join(root, last))
        log = []
        srv, url = serve(REPO, log)
        env = dict(os.environ, JUDGE_UPDATE_URL=url)
        p = subprocess.run([sys.executable, os.path.join(judge_dir, "updater.py")], env=env, cwd=root,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.stdout.decode("utf-8", "replace")
        data = os.path.join(judge_dir, "problems", "batch", last)
        files = [f for _, _, fs in os.walk(data) for f in fs]
        last_set = next(s for s in judge.load_sets() if s["dir"] == last)
        check(p.returncode == 0 and len(files) > 50
              and os.path.exists(os.path.join(root, *layout.code_path(last_set, last_n).split("/")))
              and os.path.exists(os.path.join(root, last, "Problems_" + last + ".pdf"))
              and len(glob.glob(os.path.join(root, last, "*", "*.pdf"))) == last_n and len(log) <= 10 + last_n,
              f"updater installs {last} ({len(files)} files) in {len(log)} requests", f"{log}\n{out}")
        with open(os.path.join(judge_dir, "manifest.json"), encoding="utf-8") as f:
            installed = json.load(f)
        check(installed.get("version") == build_version() and len(installed.get("create_only", {})) > 100,
              "the installed manifest is the new version")
        srv.shutdown()

        # a bundle that does not match its hash: refused, nothing installed
        repo2 = make_repo2(tmp, "9.9", "marker-bundle")
        edit_manifest(repo2, lambda m: m["bundles"]["bundles/%s.zip" % last].update(sha256="0" * 64))
        shutil.rmtree(data)
        srv, url = serve(repo2)
        p = subprocess.run([sys.executable, os.path.join(judge_dir, "updater.py")],
                           env=dict(os.environ, JUDGE_UPDATE_URL=url), cwd=root,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.stdout.decode("utf-8", "replace")
        check(p.returncode == 1 and "hash mismatch" in out and not os.path.exists(data)
              and "marker-bundle" not in open(os.path.join(judge_dir, "judge.py"), encoding="utf-8").read(),
              "bad bundle: update refused, nothing installed", out)
        srv.shutdown()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def build_version():
    with open(os.path.join(REPO, "VERSION"), encoding="utf-8") as f:
        return f.read().strip()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def outside_judge(root):
    """{path: bytes} of every file of a package outside Judge/."""
    out = {}
    for dp, ds, fs in os.walk(root):
        if dp == root and "Judge" in ds:
            ds.remove("Judge")
        for n in fs:
            with open(os.path.join(dp, n), "rb") as f:
                out[os.path.relpath(os.path.join(dp, n), root).replace(os.sep, "/")] = f.read()
    return out


def next_version(v):
    """The version after v (4.1.0 -> 4.1.1, 7.3 -> 7.4): the updater only installs a strictly newer release."""
    parts = v.split(".")
    return ".".join(parts[:-1] + [str(int(parts[-1]) + 1)])


def make_next_release(tmp, version=None):
    """A copy of the repo as a later release that changes topic 3: problems 2 and 9 are re-titled, 3, 6 and 8 are
    replaced by new problems, 4 and 5 swap places, and the old problem 6 moves to a new slot 21. In the Mixed sets
    (plans/V4_MIXED_FOLDER.md): a new set after the last one (now 00_Mixed/M12, a copy of M11's data and PDFs with
    new titles) and problem 4 of the second set re-titled.
    Returns (repo2, the old English titles {slot: title})."""
    version = version or next_version(build_version())
    repo2 = make_repo2(tmp, version, "marker-" + version)
    batch = os.path.join(repo2, "problems", "batch")
    os.makedirs(os.path.join(repo2, "tools", "moves"), exist_ok=True)       # what the teacher saves at release time
    shutil.copy(os.path.join(REPO, "problems", "batch", "problems.json"),
                os.path.join(repo2, "tools", "moves", "problems_4.0.0.json"))
    with open(os.path.join(batch, "problems.json"), encoding="utf-8") as f:
        P = json.load(f)
    with open(os.path.join(batch, "sets.json"), encoding="utf-8") as f:
        S = json.load(f)
    old = {i: P[str(300 + i)]["en"] for i in range(1, 21)}
    renamed = {old[2]: "Renamed Problem Two", old[9]: "Renamed Problem Nine"}
    for i in (2, 9):
        P[str(300 + i)]["en"] = renamed[old[i]]
    a, b = P["304"], P["305"]                                              # 4 <-> 5 (the test data moves too)
    P["304"], P["305"] = dict(b, dir=a["dir"]), dict(a, dir=b["dir"])
    d4, d5 = (os.path.join(batch, TOPIC3, n) for n in ("4", "5"))
    os.rename(d4, d4 + "_x"), os.rename(d5, d4), os.rename(d4 + "_x", d5)
    P["321"] = dict(P["306"], dir=TOPIC3 + "/21")                          # old problem 6 -> a new slot 21
    shutil.copytree(os.path.join(batch, TOPIC3, "6"), os.path.join(batch, TOPIC3, "21"))
    for i, title in ((3, "Brand New Three"), (6, "Brand New Six"), (8, "Brand New Eight")):
        P[str(300 + i)]["en"] = title
    s3 = next(s for s in S if s["set"] == 3)
    s3["problems"].append(321)
    mixed = [s for s in S if s.get("group") == "Mixed"]
    if mixed:                                                              # a new Mixed set and a re-titled Mixed problem
        last, m2 = mixed[-1], mixed[1]
        new = dict(last, set=last["set"] + 1, dir=f"M{int(last['dir'][1:]) + 1:02d}",
                   problems=[100 * (last["set"] + 1) + n for n in range(1, 7)])
        for n, pid in enumerate(new["problems"], 1):
            P[str(pid)] = dict(P[str(last["problems"][n - 1])], en=f"Next Set Problem {n}", dir=f"{new['dir']}/{n}")
            shutil.copytree(os.path.join(batch, last["dir"], str(n)), os.path.join(batch, new["dir"], str(n)))
            d = os.path.join(repo2, "student", *layout.folder(new).split("/"), str(n))
            os.makedirs(d)
            shutil.copy(glob.glob(os.path.join(repo2, "student", *layout.folder(last).split("/"), str(n), "*.pdf"))[0],
                        os.path.join(d, layout.pdf_name(new, n, P[str(pid)]["en"])))
        shutil.copy(os.path.join(repo2, "student", *layout.topic_pdf_path(last).split("/")),
                    os.path.join(repo2, "student", *layout.topic_pdf_path(new).split("/")))
        S.append(new)
        pid4 = str(m2["problems"][3])
        renamed[P[pid4]["en"]] = "Renamed Mixed Four"
        d4m = os.path.join(repo2, "student", *layout.folder(m2).split("/"), "4")
        os.rename(os.path.join(d4m, layout.pdf_name(m2, 4, P[pid4]["en"])),
                  os.path.join(d4m, layout.pdf_name(m2, 4, "Renamed Mixed Four")))
        P[pid4]["en"] = "Renamed Mixed Four"
    with open(os.path.join(batch, "problems.json"), "w", encoding="utf-8") as f:
        json.dump(P, f, ensure_ascii=False, indent=1)
    with open(os.path.join(batch, "sets.json"), "w", encoding="utf-8") as f:
        json.dump(S, f, ensure_ascii=False, indent=1)
    bm = os.path.join(repo2, "tools", "build_manifest.py")
    with open(bm, encoding="utf-8") as f:
        text = f.read()
    assert text.count("\nRENAMED = {") == 1, "tools/build_manifest.py: no RENAMED = {...} line"
    with open(bm, "w", encoding="utf-8") as f:                  # add to the real RENAMED (it may hold entries)
        f.write(text.replace("\nRENAMED = {", "\nRENAMED = {**" + repr(renamed) + ", ", 1))
    files = os.path.join(repo2, "student", "set_files")
    shutil.copy(os.path.join(files, "Makefile"), os.path.join(files, "Makefile_21"))
    for i in range(1, 22):                                                 # the PDFs follow the titles
        d = os.path.join(repo2, "student", TOPIC3, layout.slot(s3, i))
        os.makedirs(d, exist_ok=True)
        want = os.path.join(d, layout.pdf_name(s3, i, P[str(300 + i)]["en"]))
        if not os.path.exists(want):
            have = glob.glob(os.path.join(d, "*.pdf"))
            if have:
                os.rename(have[0], want)
            else:
                shutil.copy(glob.glob(os.path.join(repo2, "student", TOPIC3, "06", "*.pdf"))[0], want)
    rebuild_manifest(repo2)
    return repo2, old


def test_future_update(root=None):
    """From 4.0.0 on, releases replace, re-title and move problems (plans/V4_LAYOUT.md section 3). A package gets a
    fake next version over local HTTP: the student's written files follow their problems, nothing is overwritten or
    deleted, old PDFs are retired only when their bytes are the shipped ones, and the second run is quiet."""
    print("A later release (a fake next version over local HTTP)")
    tmp = tempfile.mkdtemp(prefix="judge_next_")
    try:
        if root is None:
            subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", tmp, "--no-zip"],
                           check=True, stdout=subprocess.DEVNULL)
            root = os.path.join(tmp, "C2_Practice")
        judge_dir, set1 = os.path.join(root, "Judge"), os.path.join(root, TOPIC3)
        s3 = next(s for s in judge.load_sets() if s["set"] == 3)
        repo2, old = make_next_release(tmp)

        def code(i):
            return os.path.join(root, *layout.code_path(dict(s3, problems=list(range(21))), i).split("/"))

        def old_pdf(i):
            return os.path.join(root, *layout.pdf_path(s3, i, old[i]).split("/"))

        # the student's work before the update
        shutil.copy(os.path.join(SAMPLES, "batch", "grid_ok.cpp"), code(1))
        written = {i: f"// my code for problem {i}: {old[i]}\nint main() {{ return 0; }}\n" for i in (2, 3, 4, 5, 6)}
        for i, text in written.items():
            write(code(i), text)
        own = {os.path.join(set1, "01", "notes.txt"): "my notes\n", os.path.join(set1, "mysol.cpp"): "// scratch\n",
               os.path.join(set1, "02", "backup.cpp"): "// an older try\n",
               code(21): "// I made this file myself\nint main() {}\n"}
        for path, text in own.items():
            write(path, text)
        shipped2 = sha(old_pdf(2))
        mixed = [s for s in judge.load_sets() if judge.is_mixed(s)]
        m2 = mixed[1] if mixed else None
        if m2:                                  # the student's Mixed work: the re-titled problem and another one
            meta0 = problems_json()
            mcode = {i: os.path.join(root, *layout.code_path(m2, i).split("/")) for i in (3, 4)}
            mwritten = {i: f"// my Mixed code {i}\nint main() {{ return 0; }}\n" for i in mcode}
            for i in mcode:
                write(mcode[i], mwritten[i])
            m4_old = os.path.join(root, *layout.pdf_path(m2, 4, meta0[str(m2["problems"][3])]["en"]).split("/"))
            m4_shipped = sha(m4_old)
        with open(old_pdf(9), "ab") as f:
            f.write(b"\n% a note the student saved into this PDF\n")
        changed9 = sha(old_pdf(9))

        srv, url = serve(repo2)
        code_, out, _ = run_student([P31, "--no-color"], set1, url)
        check(code_ == 0 and "restarting" in out and f"Judge v{next_version(build_version())}" in out and "ACCEPTED" in out,
              f"a normal run finds {next_version(build_version())}, installs it, restarts and judges", f"exit {code_}\n{out}")
        with open(os.path.join(judge_dir, "problems", "batch", "problems.json"), encoding="utf-8") as f:
            P = {e["dir"]: e["en"] for e in json.load(f).values()}       # the titles after the update
        s21 = dict(s3, problems=list(range(21)))

        def new_pdf(i):
            return os.path.join(root, *layout.pdf_path(s21, i, P[f"{TOPIC3}/{i}"]).split("/"))

        # a re-titled problem: the code stays, the old PDF is retired, the new one appears
        bak2 = os.path.join(judge_dir, ".backup", "_package", *layout.pdf_path(s3, 2, old[2]).split("/"))
        check(read(code(2)) == written[2] and not glob.glob(os.path.join(set1, "old", "2_*")),
              "re-titled problem: the written file stays in its folder")
        check(os.path.isfile(new_pdf(2)) and "Renamed_Problem_Two" in new_pdf(2) and not os.path.exists(old_pdf(2))
              and os.path.isfile(bak2) and sha(bak2) == shipped2,
              "re-titled problem: the new PDF appears, the old one is retired to Judge/.backup/_package/")
        check(os.path.isfile(new_pdf(9)) and os.path.isfile(old_pdf(9)) and sha(old_pdf(9)) == changed9,
              "an old PDF whose bytes are not the shipped ones stays where it is")
        # a replaced problem: the written file goes to <topic>/old/, the slot gets an empty starter
        parked3 = os.path.join(set1, "old", layout.old_name(3, old[3]))
        check(read(parked3) == written[3] and read(code(3)) == "",
              f"replaced problem: the written file goes to {TOPIC3}/old/{layout.old_name(3, old[3])}, the slot is empty again",
              f"{os.listdir(os.path.join(set1, 'old')) if os.path.isdir(os.path.join(set1, 'old')) else None}")
        check(read(code(8)) == "" and not glob.glob(os.path.join(set1, "old", "8_*")),
              "replaced problem with an untouched empty starter: nothing is moved")
        # moved problems follow their titles
        check(read(code(4)) == written[5] and read(code(5)) == written[4],
              "moved problems (4 <-> 5): each written file follows its problem")
        # a clash: the destination already holds written code
        parked6 = os.path.join(set1, "old", "03-06_moved.cpp")
        check(read(code(21)) == own[code(21)] and read(parked6) == written[6] and read(code(6)) == ""
              and "already held your code" in out,
              "clash (6 -> 21, where the student has code): nothing overwritten, the incoming file goes to old/, reported",
              out)
        check(all(read(path) == text for path, text in own.items()), "files the updater did not ship are untouched")
        lines = [ln for ln in out.splitlines() if " -> " in ln]
        check(len(lines) == 4 and "moved with their problems" in out, "every move is printed once", "\n".join(lines))
        folder8 = sorted(os.listdir(os.path.join(set1, "08")))
        check(folder8 == ["03-08.cpp", "08_Brand_New_Eight.pdf"],
              "a replaced problem's folder holds exactly its code file and the new PDF (the old shipped one is retired)",
              str(folder8))
        folder21 = sorted(os.listdir(os.path.join(set1, "21")))
        check(folder21 == ["03-21.cpp", os.path.basename(new_pdf(21))],
              "a new problem folder (21) holds exactly the code file and its PDF", str(folder21))
        if m2:                                  # Mixed sets in 00_Mixed/ (plans/V4_MIXED_FOLDER.md)
            sets_after = json.load(open(os.path.join(judge_dir, "problems", "batch", "sets.json"), encoding="utf-8"))
            meta1 = json.load(open(os.path.join(judge_dir, "problems", "batch", "problems.json"), encoding="utf-8"))
            m9 = next((s for s in sets_after if s["set"] == mixed[-1]["set"] + 1), None)
            bad = ["no new set in sets.json"] if m9 is None else []
            if m9 is not None:
                top = os.path.join(root, *layout.folder(m9).split("/"))
                want = sorted([str(n) for n in range(1, 7)] + ["Makefile", "judge.bat", f"Problems_{m9['dir']}.pdf"])
                if not os.path.isdir(top) or sorted(os.listdir(top)) != want:
                    bad.append(f"{layout.folder(m9)}: {sorted(os.listdir(top)) if os.path.isdir(top) else None}")
                for n, pid in enumerate(m9["problems"], 1):
                    d = os.path.join(top, str(n))
                    w = sorted([layout.code_name(m9, n), layout.pdf_name(m9, n, meta1[str(pid)]["en"])])
                    if not os.path.isdir(d) or sorted(os.listdir(d)) != w or read(os.path.join(d, layout.code_name(m9, n))) != "":
                        bad.append(f"{layout.folder(m9)}/{n}")
            check(not bad and m9["dir"] == f"M{int(mixed[-1]['dir'][1:]) + 1:02d}" and not os.path.exists(os.path.join(root, m9["dir"])),
                  "a new Mixed set appears as 00_Mixed/M<last + 1>/ (Makefile, judge.bat, Problems_M<last + 1>.pdf, 1 ... 6 with an "
                  "empty code file and its PDF each), nothing at the package root", str(bad))
            m4_new = os.path.join(root, *layout.pdf_path(m2, 4, "Renamed Mixed Four").split("/"))
            bak4 = os.path.join(judge_dir, ".backup", "_package", *os.path.relpath(m4_old, root).split(os.sep))
            check(os.path.isfile(m4_new) and not os.path.exists(m4_old) and os.path.isfile(bak4) and sha(bak4) == m4_shipped
                  and sorted(os.listdir(os.path.dirname(m4_new))) == sorted([layout.code_name(m2, 4), os.path.basename(m4_new)]),
                  f"a re-titled Mixed problem ({layout.folder(m2)}/4): the new PDF appears, the old-title PDF is retired "
                  "to Judge/.backup/_package/", str(os.listdir(os.path.dirname(m4_new))))
            check(all(read(mcode[i]) == mwritten[i] for i in mcode)
                  and not os.path.exists(os.path.join(root, *layout.folder(m2).split("/"), "old")),
                  "the student's Mixed .cpp files are untouched (nothing moved to old/)")
            code_, outm, _ = run_student(["--no-color"], os.path.join(root, *layout.folder(m9).split("/")) if m9 else root,
                                         url, judge_path=os.path.join(os.pardir, os.pardir, "Judge", "judge.py"))
            check(code_ == 0 and f"Mixed {m9['dir'] if m9 else ''}" in outm and outm.count("still empty - skipped") == 6
                  and "moved" not in outm and "restarting" not in outm,
                  "the new set is judged in 00_Mixed/M<last + 1> (whole set); this second run is quiet", outm)
        # the second run is quiet and changes nothing
        snap = outside_judge(root)
        code_, out2, _ = run_student([P31, "--no-color"], set1, url)
        check(code_ == 0 and "ACCEPTED" in out2 and "moved" not in out2 and "restarting" not in out2
              and outside_judge(root) == snap, "the second run is quiet and changes nothing", out2)
        code_, out3, _ = run_student(["--update", "--no-color"], set1, url)
        check(code_ == 0 and "up to date" in out3 and outside_judge(root) == snap, "--update afterwards: up to date",
              out3)
        srv.shutdown()
        with open(os.path.join(REPO, "manifest.json"), encoding="utf-8") as f:
            real = json.load(f)
        check(set(real) == {"version", "sources", "files", "managed", "create_only", "bundles", "moves"},
              "the manifest is one plain view (no bootstrap view, no retired list)", str(sorted(real)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_crlf_generator():
    """On Windows gen.py (text mode) writes CRLF; the sha256 in manifest.json is of the LF file."""
    tmp = tempfile.mkdtemp(prefix="judge_gen_test_")
    try:
        data = b"3 1 0 10\n2 1\n7 2\n12 1\n"
        with open(os.path.join(tmp, "gen.py"), "w") as f:
            f.write("import os\nos.makedirs('tests', exist_ok=True)\n"
                    f"open('tests/01.in', 'w', newline='\\r\\n').write({data.decode()!r})\n")
        test = {"name": "01", "in": hashlib.sha256(data).hexdigest(), "out": "", "in_file": False, "out_file": True}
        with open(os.path.join(tmp, "manifest.json"), "w") as f:
            json.dump({"version": 1, "tests": [test]}, f)
        with contextlib.redirect_stdout(io.StringIO()):
            ok = judge.ensure_tests(tmp, judge.Style(color=False, ascii_only=True, tty=False))
        got = b""
        if os.path.isfile(os.path.join(tmp, "01.in")):
            with open(os.path.join(tmp, "01.in"), "rb") as f:
                got = f.read()
        check(ok and got == data, "gen.py writing CRLF (Windows) is accepted and stored with LF", repr(got))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_generated_tests():
    """In a fresh student package, gen.py rebuilds every big test that is not shipped, with the right sha256."""
    print("Generated tests")
    tmp = tempfile.mkdtemp(prefix="judge_gen_all_")
    try:
        subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", tmp, "--no-zip"],
                       check=True, stdout=subprocess.DEVNULL)
        batch = os.path.join(tmp, "C2_Practice", "Judge", "problems", "batch")
        st = judge.Style(color=False, ascii_only=True, tty=False)
        bad, rebuilt = [], 0
        for m in sorted(glob.glob(os.path.join(batch, "[0-9][0-9]_*", "*", "manifest.json"))):
            pdir = os.path.dirname(m)
            with open(m, encoding="utf-8") as f:
                tests = json.load(f)["tests"]
            missing = [t for t in tests if not t["in_file"]]
            if not missing:
                continue
            if any(os.path.exists(os.path.join(pdir, t["name"] + ".in")) for t in missing):
                bad.append(os.path.relpath(pdir, batch) + " ships a big test")
            with contextlib.redirect_stdout(io.StringIO()):
                ok = judge.ensure_tests(pdir, st)
            if not ok:
                bad.append(os.path.relpath(pdir, batch))
            rebuilt += len(missing)
        check(not bad and rebuilt > 0, f"gen.py rebuilds all {rebuilt} big tests (sha256 checked)", ", ".join(bad[:5]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stale_tests():
    """An update that changes a problem's tests leaves the old files of its big tests behind (the updater never
    deletes): a big input whose sha256 differs is rebuilt, and an old .out of a hash-only test is ignored."""
    print("Stale tests")
    tmp = tempfile.mkdtemp(prefix="judge_stale_")
    try:
        subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", tmp, "--no-zip"],
                       check=True, stdout=subprocess.DEVNULL)
        batch = os.path.join(tmp, "C2_Practice", "Judge", "problems", "batch")
        pdir = t = None
        for m in sorted(glob.glob(os.path.join(batch, "[0-9][0-9]_*", "*", "manifest.json"))):
            with open(m, encoding="utf-8") as f:
                big = [x for x in json.load(f)["tests"] if not x["in_file"] and not x["out_file"]]
            if big:
                pdir, t = os.path.dirname(m), big[0]
                break
        fin = os.path.join(pdir, t["name"] + ".in")
        for path in (fin, fin[:-3] + ".out"):          # what an older version of the problem left behind
            with open(path, "wb") as f:
                f.write(b"stale\n")
        st = judge.Style(color=False, ascii_only=True, tty=False)
        with contextlib.redirect_stdout(io.StringIO()):
            rebuilt = judge.ensure_tests(pdir, st) and sha(fin) == t["in"]
        src = os.path.join(tmp, "stale.cpp")            # prints exactly the old .out
        with open(src, "w") as f:
            f.write('#include <cstdio>\nint main() { std::puts("stale"); }\n')
        exe, _, _, _ = judge.compile_source(src, tmp)
        with contextlib.redirect_stdout(io.StringIO()):
            results, _, _ = judge.run_tests(exe, pdir, st, 1.0, 0, False, quiet=True)
        verdict = {r[0]: r[1] for r in results}.get(t["name"])
        check(rebuilt and verdict == "WA", "old test files left by an update: big input rebuilt, old .out ignored",
              f"rebuilt {rebuilt}, {verdict}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_data():
    """Every test input has its expected output (the judge silently skips an .in without .out)."""
    print("Test data")
    orphans = []
    for m in glob.glob(os.path.join(REPO, "problems", "batch", "[0-9][0-9]_*", "*", "manifest.json")):
        with open(m, encoding="utf-8") as f:
            shipped_out = {t["name"] for t in json.load(f)["tests"] if t["out_file"]}
        orphans += [f for f in glob.glob(os.path.join(os.path.dirname(m), "*.in"))
                    if os.path.basename(f)[:-3] in shipped_out and not os.path.exists(f[:-3] + ".out")]
    check(not orphans, "every shipped .out exists", ", ".join(os.path.relpath(f, REPO) for f in orphans[:5]))
    p = subprocess.run([sys.executable, os.path.join(REPO, "tools", "update_problem_manifest.py"), "--check", "--all"],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    check(p.returncode == 0, "problem manifests (test hashes) are up to date", p.stdout.decode("utf-8", "replace"))


def test_manifest():
    print("Manifest")
    p = subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_manifest.py"), "--check"],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    check(p.returncode == 0, "manifest.json is up to date", p.stdout.decode("utf-8", "replace"))


def main():
    if not shutil.which("g++"):
        print("g++ not found: the regression tests need a C++ compiler in PATH.")
        return 1
    # samples and command line run in a built package: problem 3-1's big tests are rebuilt there by gen.py,
    # never inside the repo
    global judge, JUDGE
    repo_judge = judge
    pkg = tempfile.mkdtemp(prefix="judge_pkg_")
    try:
        subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", pkg, "--no-zip"],
                       check=True, stdout=subprocess.DEVNULL)
        JUDGE = os.path.join(pkg, "C2_Practice", "Judge", "judge.py")
        spec = importlib.util.spec_from_file_location("judge", JUDGE)
        judge = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(judge)
        test_samples()
        test_exited_peak()
        test_missed_last_reading()
        test_cli()
    finally:
        judge, JUDGE = repo_judge, os.path.join(CORE, "judge.py")
        shutil.rmtree(pkg, ignore_errors=True)
    test_student_package()
    test_updater()
    test_versions()
    test_fast_update()
    test_future_update()
    test_crlf_generator()
    test_generated_tests()
    test_stale_tests()
    test_data()
    test_manifest()
    print()
    if FAILED:
        print(f"{len(FAILED)} FAILED: " + ", ".join(FAILED))
        return 1
    print("All regression tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
