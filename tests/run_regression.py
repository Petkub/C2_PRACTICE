#!/usr/bin/env python3
"""
Regression tests for the POSN Practice Judge.

  python3 tests/run_regression.py          run everything (exit code 0 = all passed)

1. Every sample in samples/expected.json is judged and must get its verdict (and score, when given).
   Verdict = CE if it does not compile, else the first non-AC verdict, else AC.
2. The judge's command line is run like a student would (repo layout, --ascii, --list).
3. A student package is built with tools/build_dist.py and judged from inside 03_Prefix_Sums_and_Two_Pointers.
   (1. and 2. also run in a built package, so the big tests that gen.py rebuilds never land in the repo.)
4. Self-update: a local HTTP server serves a modified copy of the repo as v9.9; a package must update itself
   (hashes, backups, restart, create-only set files), and must refuse bad hashes, bad paths and no network.
5. manifest.json is up to date.
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

FAILED = []
STUDENT_JUDGE = os.path.join(os.pardir, "Judge", "judge.py")     # a package's judge, run from a topic folder
TOPIC3 = "03_Prefix_Sums_and_Two_Pointers"      # topic 3; its problem 1 (3-1) is the sample problem
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
    print("Student package")
    tmp = tempfile.mkdtemp(prefix="judge_dist_")
    try:
        p = subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", tmp, "--no-zip"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        check(p.returncode == 0, "build_dist.py", p.stdout.decode("utf-8", "replace"))
        if p.returncode != 0:
            return
        root = os.path.join(tmp, "C2_Practice")
        set1 = os.path.join(root, TOPIC3)
        count = len(next(s for s in judge.load_sets() if s["set"] == 3)["problems"])
        templates = [os.path.join(set1, f"{i}.cpp") for i in range(1, count + 1)]
        check(all(judge.is_template(t) for t in templates), f"{TOPIC3}/1.cpp ... {count}.cpp are empty templates")
        check(all(os.path.getsize(t) == 0 for t in templates), "the starter .cpp files are empty files")
        old = os.path.join(root, "old_template.cpp")          # the main() starter of older versions
        with open(old, "w") as f:
            f.write("#include <bits/stdc++.h>\nusing namespace std;\n\nint32_t main() {\n"
                    "    cin.tie(0); ios::sync_with_stdio(0);\n\n    return 0;\n}\n")
        check(judge.is_template(old), "the old main() starter still counts as untouched")
        os.remove(old)
        shutil.copy(os.path.join(SAMPLES, "batch", "grid_ok.cpp"), os.path.join(set1, "1.cpp"))
        student_judge = os.path.join(os.pardir, "Judge", "judge.py")
        code, out, _ = run_judge(["1", "--no-color"], cwd=set1, judge_path=student_judge)
        check(code == 0 and "ACCEPTED" in out, "inside " + TOPIC3 + ": judge.py 1", f"exit {code}\n{out}")
        code, out, _ = run_judge(["--no-color"], cwd=set1, judge_path=student_judge)
        check(code == 0 and "Total" in out and "still empty - skipped" in out and "Problem 1" in out, "inside " + TOPIC3 + ": judge.py (whole set)",
              f"exit {code}\n{out}")
        code, out, _ = run_judge(["2.cpp", "--no-color"], cwd=set1, judge_path=student_judge)
        check(code == 0 and "2.cpp is empty" in out and "Compil" not in out, "an empty .cpp: plain message, no compile",
              f"exit {code}\n{out}")
        test_mixed_sets(root, student_judge)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


TECHNIQUE_WORDS = ("dp", "dynamic", "greedy", "binary search", "prefix", "two pointers", "graph", "bfs", "dfs",
                   "dijkstra", "shortest", "dsu", "union", "heap", "stack", "queue", "sort", "sweep", "knapsack",
                   "sieve", "number theory", "combinator", "implementation", "tree")


def test_mixed_sets(root, student_judge):
    """Mixed sets (folders M01 ...): judged like a topic, and nothing a student sees names a topic or a technique:
    the folder, the PDF name, sets.json and the judge's headers say only "Mixed M01" (titles are story names)."""
    mixed = [s for s in judge.load_sets() if judge.is_mixed(s)]
    if not mixed:
        return
    check(all(re.fullmatch(r"M[0-9]{2}", s["dir"]) and len(s["problems"]) == 6 for s in mixed)
          and [s["dir"] for s in mixed] == sorted(s["dir"] for s in mixed),
          f"{len(mixed)} Mixed sets M01 ... of 6 problems")
    texts = [s.get("level_en", "") + " " + s.get("group", "") for s in mixed]
    check(not any(w in t.lower() for t in texts for w in TECHNIQUE_WORDS), "sets.json names no technique for a Mixed set",
          str(texts))
    m1 = os.path.join(root, mixed[0]["dir"])
    names = sorted(os.listdir(m1)) if os.path.isdir(m1) else []
    check(names == sorted([f"{i}.cpp" for i in range(1, 7)] + ["Makefile", "judge.bat", f"Problems_{mixed[0]['dir']}.pdf"]),
          f"{mixed[0]['dir']}/ holds 1.cpp ... 6.cpp, Makefile, judge.bat and Problems_{mixed[0]['dir']}.pdf", str(names))
    code, out, _ = run_judge(["--no-color"], cwd=m1, judge_path=student_judge)
    check(code == 0 and f"Mixed {mixed[0]['dir']}" in out and "Topic" not in out and "Problem 6" in out
          and out.count("still empty - skipped") == 6, f"inside {mixed[0]['dir']}: judge.py (whole set), no topic shown",
          f"exit {code}\n{out}")
    with open(os.path.join(m1, "3.cpp"), "w") as f:
        f.write("int main() { return 0; }\n")
    code, out, _ = run_judge(["3", "--no-color"], cwd=m1, judge_path=student_judge)
    check(code == 0 and f"Mixed {mixed[0]['dir']}" in out and "Topic" not in out and "Problem not found" not in out,
          f"inside {mixed[0]['dir']}: judge.py 3", f"exit {code}\n{out}")
    code, out, _ = run_judge([os.path.join(m1, "3.cpp"), f"{mixed[0]['dir']}-3", "--no-color"], cwd=root,
                             judge_path=os.path.join("Judge", "judge.py"))
    check(code == 0 and "Problem not found" not in out, f"judge.py FILE {mixed[0]['dir']}-3", f"exit {code}\n{out}")
    code, out, _ = run_judge(["--list", "--no-color"], cwd=root, judge_path=os.path.join("Judge", "judge.py"))
    check(code == 0 and f"Mixed {mixed[-1]['dir']}" in out and f"Topic {mixed[0]['set']}" not in out
          and f"{len(mixed)} mixed sets" in out, "judge.py --list shows the Mixed sets by name", f"exit {code}\n{out[-600:]}")
    os.remove(os.path.join(m1, "3.cpp"))
    open(os.path.join(m1, "3.cpp"), "w").close()


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
    for name in (("student", "README.txt"), ("student", "set_files", "Makefile")):     # managed package files
        with open(os.path.join(repo2, *name), "a", encoding="utf-8") as f:
            f.write(f"\n# {marker}\n")
    rebuild_manifest(repo2)
    return repo2


def rebuild_manifest(repo2):
    subprocess.run([sys.executable, os.path.join(repo2, "tools", "build_manifest.py")], check=True,
                   stdout=subprocess.DEVNULL)


def edit_manifest(repo2, fn):
    """fn changes the parts of manifest.json that updaters install ("full_v4" and the bootstrap "full", format 3)."""
    p = os.path.join(repo2, "manifest.json")
    with open(p, encoding="utf-8") as f:
        m = json.load(f)
    parts = [m[k] for k in ("full_v4", "full") if isinstance(m.get(k), dict)] or [m]
    for part in parts:
        fn(part)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(m, f)


def run_student(args, cwd, url):
    env = dict(os.environ, JUDGE_UPDATE_URL=url)
    env.pop("JUDGE_NO_UPDATE", None)
    t0 = time.time()
    p = subprocess.run([sys.executable, os.path.join(os.pardir, "Judge", "judge.py")] + args, cwd=cwd, env=env,
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
        shutil.copy(os.path.join(SAMPLES, "batch", "grid_ok.cpp"), os.path.join(set1, "1.cpp"))
        student_hash, old_judge = sha(os.path.join(set1, "1.cpp")), sha(os.path.join(judge_dir, "judge.py"))
        template = sha(os.path.join(set1, "2.cpp"))

        # a) automatic update during a normal run: new files, backup, restart with the new judge
        repo2 = make_repo2(tmp, "9.9", "marker-v9.9")
        edit_manifest(repo2, lambda m: m["create_only"].update(
            {TOPIC3 + "/9.cpp": [sha(os.path.join(REPO, "student", "set_files", "template.cpp")), "student/set_files/template.cpp"]}))
        srv, url = serve(repo2)
        code, out, _ = run_student(["1.cpp", "--no-color"], set1, url)
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
        check(sha(os.path.join(set1, "1.cpp")) == student_hash and sha(os.path.join(set1, "2.cpp")) == template,
              "student files untouched")
        check(os.path.exists(os.path.join(set1, "9.cpp")) and sha(os.path.join(set1, "9.cpp")) == template,
              "create-only 9.cpp added to the topic folder")
        check(not os.path.exists(os.path.join(judge_dir, ".update_tmp")), "no temp folder left behind")
        code, out, _ = run_student(["--update", "--no-color"], set1, url)
        check(code == 0 and "up to date" in out, "--update: up to date", f"exit {code}\n{out}")

        # b) a newer version appears: normal runs wait 10 minutes, --update takes it now
        repo2 = make_repo2(tmp, "9.11", "marker-v9.11")
        code, out, _ = run_student(["1.cpp", "--no-color"], set1, url)
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
            {TOPIC3 + "/1.cpp": [sha(os.path.join(repo2, "student", "set_files", "template.cpp")), "student/set_files/template.cpp"]})
            or m.update(version="9.14"))
        code, out, _ = run_student(["--update", "--no-color"], set1, url)
        check(code == 1 and "bad managed entry" in out and sha(os.path.join(set1, "1.cpp")) == student_hash,
              "a .cpp listed as managed: refused, student file untouched", f"exit {code}\n{out}")

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
        code, out, dt = run_student(["1.cpp", "--no-color"], set1, f"http://127.0.0.1:{free_port()}/")
        check(code == 0 and "ACCEPTED" in out and "restarting" not in out and dt < 30,
              f"offline: judge works ({dt:.1f} s)", f"exit {code}\n{out}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_fast_update():
    """A package from a release before the newest topic gets that whole topic in a few requests (a bundle for the
    test data, one template for all N.cpp)."""
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
        check(p.returncode == 0 and len(files) > 50 and os.path.exists(os.path.join(root, last, "%d.cpp" % last_n))
              and os.path.exists(os.path.join(root, last, "Problems_" + last + ".pdf")) and len(log) <= 12,
              f"updater installs {last} ({len(files)} files) in {len(log)} requests", f"{log}\n{out}")
        with open(os.path.join(judge_dir, "manifest.json"), encoding="utf-8") as f:
            installed = json.load(f)
        check("full" not in installed and installed.get("version") == build_version(),
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


def test_retired_pdf():
    """The topic PDF was renamed <topic>/<topic>.pdf -> <topic>/Problems_<topic>.pdf: an old-name file whose bytes are a
    version we shipped ("retired" in the manifest) goes to Judge/.backup/_package/; any other file there stays."""
    print("Retired topic PDF")
    tmp = tempfile.mkdtemp(prefix="judge_retired_")
    try:
        subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", tmp, "--no-zip"],
                       check=True, stdout=subprocess.DEVNULL)
        root = os.path.join(tmp, "C2_Practice")
        judge_dir = os.path.join(root, "Judge")
        a, b = [s["dir"] for s in judge.load_sets()][:2]
        with open(os.path.join(REPO, "manifest.json"), encoding="utf-8") as f:
            real = json.load(f)["full_v4"]
        check(len(real.get("retired", {})) == len([s for s in judge.load_sets() if not judge.is_mixed(s)])
              and all(k in real["retired"] for k in (f"{a}/{a}.pdf", f"{b}/{b}.pdf"))
              and all(os.path.exists(os.path.join(root, d, f"Problems_{d}.pdf"))
                      and not os.path.exists(os.path.join(root, d, f"{d}.pdf")) for d in (a, b)),
              "the package has Problems_<topic>.pdf and the manifest retires every old name")
        shipped, own = b"%PDF old name, as shipped", b"%PDF a file the student saved under the old name"
        write(os.path.join(root, a, f"{a}.pdf"), shipped.decode())
        write(os.path.join(root, b, f"{b}.pdf"), own.decode())
        repo2 = make_repo2(tmp, "9.9", "marker-retired")
        edit_manifest(repo2, lambda m: m.update(retired={f"{a}/{a}.pdf": [hashlib.sha256(shipped).hexdigest()],
                                                         f"{b}/{b}.pdf": ["0" * 64]}))
        srv, url = serve(repo2)
        p = subprocess.run([sys.executable, os.path.join(judge_dir, "updater.py")],
                           env=dict(os.environ, JUDGE_UPDATE_URL=url), cwd=root,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.stdout.decode("utf-8", "replace")
        srv.shutdown()
        check(p.returncode == 0 and not os.path.exists(os.path.join(root, a, f"{a}.pdf"))
              and read(os.path.join(judge_dir, ".backup", "_package", a, f"{a}.pdf")) == shipped.decode()
              and os.path.exists(os.path.join(root, a, f"Problems_{a}.pdf")),
              "a shipped old-name PDF moves to Judge/.backup/_package/", out)
        check(read(os.path.join(root, b, f"{b}.pdf")) == own.decode(), "an old-name file with other bytes stays", out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def build_version():
    with open(os.path.join(REPO, "VERSION"), encoding="utf-8") as f:
        return f.read().strip()


def test_bootstrap_view():
    """Updaters before 4.0 reject the new topic folder paths: they read "full", which must only hold entries they accept."""
    print("Bootstrap view")
    import re as _re
    old_set = _re.compile(r"^Topic_[0-9]+/[0-9]+\.cpp$")
    old_managed = _re.compile(r"^(Topic_[0-9]+/(Makefile|judge\.bat|Topic_[0-9]+\.pdf)|Guide\.pdf|README\.txt"
                              r"|Progress\.md|\.vscode/(tasks|settings)\.json)$")
    with open(os.path.join(REPO, "manifest.json"), encoding="utf-8") as f:
        m = json.load(f)
    full, v7 = m.get("full", {}), m.get("full_v4", {})
    check(bool(v7) and full.get("bootstrap") is True, "manifest has full_v4 and a bootstrap \"full\"")
    check(all(old_managed.match(k) for k in full.get("managed", {})) and
          all(old_set.match(k) for k in full.get("create_only", {})), "the bootstrap view only holds old-style paths")
    check(full.get("files") == v7.get("files"), "the bootstrap view installs every Judge/ file (incl. the new updater)")


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


def test_moves(root, tmp, release="2.1"):
    """After an update from an older release (2.1, 3.0.1, ...) the student's files follow their problems to the v4
    topic folders, once, never over written code; an old folder with nothing of the student's left is removed, one
    with something left gets README_MOVED.txt."""
    print(f"Moves ({release} -> now)")
    base = os.path.join(tmp, "moves_pkg_" + release)
    shutil.copytree(root, base)
    jd = os.path.join(base, "Judge")
    with open(os.path.join(jd, "manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    for rel in manifest.get("create_only", {}):                  # a fresh install: every starter empty
        write(os.path.join(base, *rel.split("/")), "")
    old = os.path.join(REPO, "tools", "moves", f"problems_{release}.json")
    pairs = manifest.get("moves", {}).get(sha(old))
    check(bool(pairs), f"the manifest lists moves for a {release} install", str(list(manifest.get("moves", {}))))
    if not pairs:
        return
    os.makedirs(os.path.join(jd, ".backup", "problems", "batch"), exist_ok=True)     # what the old updater kept
    shutil.copy(old, os.path.join(jd, ".backup", "problems", "batch", "problems.json"))
    written = {src: f"// student code for {src}\nint main(){{}}\n" for src, _ in pairs}
    first = pairs[0][0]
    for src, text in written.items():
        if src != first:
            write(os.path.join(base, *src.split("/")), text)
    write(os.path.join(base, *first.split("/")), "")             # an untouched (empty) starter is not moved
    keep_dir = pairs[-1][0].split("/")[0]                        # a folder that keeps something of the student's
    write(os.path.join(base, keep_dir, "notes.txt"), "// stays\n")
    gone_dir = first.split("/")[0]                               # holds only starters / managed files after the moves
    for name in ("Makefile", "judge.bat"):
        write(os.path.join(base, gone_dir, name), "managed\n")
    run_dir = os.path.join(base, os.path.dirname(next(iter(manifest["create_only"]))))   # a v4 topic folder
    sources = {src for src, _ in pairs}
    clash = next((dst for src, dst in pairs[1:] if dst.split("/")[1] != "old" and dst not in sources), None)
    if clash:                                                    # written code already at a destination
        write(os.path.join(base, *clash.split("/")), "// written before the update\n")
    probe = next(((s, d) for s, d in reversed(pairs) if d != clash and s.split("/")[0] == keep_dir), None)
    if probe:                                                    # judging a file that moves in this very run
        code, out, _ = run_judge([probe[0].split("/")[1], "--no-color"], os.path.join(base, keep_dir), STUDENT_JUDGE)
        check(code == 1 and "moved with their problems" in out and f"moved with its problem to {probe[1]}" in out,
              "the judge says the files moved, and where the file it was asked to judge went", out[:800])
    else:
        code, out, _ = run_judge(["--list", "--no-color"], run_dir, STUDENT_JUDGE)
        check(code == 0 and "moved with their problems" in out, "the judge says the files moved", out[:800])
    bad = []
    for src, dst in pairs[1:]:
        if dst == clash:
            continue
        if read(os.path.join(base, *dst.split("/"))) != written[src]:
            bad.append(f"{src} -> {dst}")
    check(not bad, "every written file is at its problem's new place (or in Topic_K/old/)", ", ".join(bad[:5]))
    replaced_file = os.path.join(REPO, "tools", "replaced.json")
    if os.path.exists(replaced_file):        # problems replaced by new ones (C2_PRACTICE_SRC bank/): their files
        with open(replaced_file, encoding="utf-8") as f:     # go to the new topic's old/, never into the slot
            replaced = json.load(f)
        with open(old, encoding="utf-8") as f:
            old_dirs = {e["en"]: e["dir"] for e in json.load(f).values()}
        wrong = []
        for title, slot in replaced.items():
            if title in old_dirs:
                dst = dict(pairs).get(old_dirs[title] + ".cpp")
                folder, n = slot.split("/")
                if not dst or not dst.startswith(folder + "/old/" + n + "_") or dst == slot + ".cpp":
                    wrong.append(f"{title}: {dst}")
        check(not wrong, "a replaced problem's file goes to its new topic's old/, not to the new problem's slot",
              ", ".join(wrong[:5]))
    if clash:
        src = next(s for s, d in pairs if d == clash)
        kept = read(os.path.join(base, *clash.split("/"))) == "// written before the update\n"
        parked = glob.glob(os.path.join(base, clash.split("/")[0], "old", "*_moved*.cpp"))
        check(kept and any(read(p) == written[src] for p in parked), "a clash never overwrites: the moved file goes to old/",
              f"{clash}: kept={kept}, parked={parked}")
    vacated = [src for src, _ in pairs[1:] if not any(d == src for _, d in pairs)]
    check(all(read(os.path.join(base, *v.split("/"))) in (None, "") for v in vacated), "no written file is left behind")
    check(not glob.glob(os.path.join(base, first.split("/")[0], first.split("/")[1])) or
          read(os.path.join(base, *first.split("/"))) == "", "an untouched starter is not moved")
    check(read(os.path.join(base, keep_dir, "notes.txt")) == "// stays\n" and
          os.path.exists(os.path.join(base, keep_dir, "README_MOVED.txt")),
          "an old folder with something of the student's stays, with README_MOVED.txt")
    gone_left = os.listdir(os.path.join(base, gone_dir)) if os.path.isdir(os.path.join(base, gone_dir)) else []
    check(not os.path.isdir(os.path.join(base, gone_dir)) or "README_MOVED.txt" in gone_left,
          f"an old folder with only starters / managed files is removed ({gone_dir})", str(gone_left))
    snapshot = {p: read(p) for p in glob.glob(os.path.join(base, "*", "**", "*.cpp"), recursive=True) if "Judge" not in p}
    code, out, _ = run_judge(["--list", "--no-color"], run_dir, STUDENT_JUDGE)
    again = {p: read(p) for p in glob.glob(os.path.join(base, "*", "**", "*.cpp"), recursive=True) if "Judge" not in p}
    check("moved" not in out and again == snapshot, "the moves happen once")


def test_all_moves():
    """test_moves for every older release in tools/moves (each on a fresh copy of a built package)."""
    tmp = tempfile.mkdtemp(prefix="judge_moves_")
    try:
        subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_dist.py"), "--out", tmp, "--no-zip"],
                       check=True, stdout=subprocess.DEVNULL)
        root = os.path.join(tmp, "C2_Practice")
        for name in sorted(os.listdir(os.path.join(REPO, "tools", "moves"))):
            test_moves(root, tmp, name[len("problems_"):-len(".json")])
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
    test_bootstrap_view()
    test_all_moves()
    test_updater()
    test_fast_update()
    test_retired_pdf()
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
