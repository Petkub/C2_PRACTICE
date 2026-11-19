# C2_PRACTICE: POSN Camp 2 Topic Practice Judge

A terminal judge that students run on their own machines to practice for the POSN Computer Olympiad Camp 2,
organised by topic. **4.0.0 is the first release students get** (no student has an older package, so there is no
code for older layouts; plans `C2_PRACTICE_SRC/plans/V4_RESTRUCTURE.md` and `V4_LAYOUT.md`): English numbered topic
folders in study order (`01_Brute_Force_and_Implementation` ... `33_Mo_Algorithm`), in three groups (Core 01-14 with
20 problems, Intermediate 15-25 with 12 (15 has 20, 17 has 15), Advanced (TOI) 26-33 with 12), plus the
group **Mixed**: 8 sets of 6 problems with no topic label (student folders `M01` ... `M08`, set numbers 41-48,
`sets.json` "group": "Mixed", tier 0 = no level shown; nothing a student sees may name a topic or technique:
`is_mixed`, `set_label`, `MIXED_DIR` in `judge.py`; regression `test_mixed_sets`). Problem id =
100 * topic + n. `sets.json` gives each topic's `set` number, `dir`, `group` and problem ids; the judge looks a topic
up by its number and recognises a topic folder by its two-digit prefix. In the judge, the data files and options keep
the mock-exam names (`sets.json`, `--set K`): a "set" here is a topic.
The student package has **one folder per problem**: `04_Binary_Search/05/04-05.cpp` (the student's code) and
`04_Binary_Search/05/05_<English_Title>.pdf` (that problem's PDF); a Mixed set: `M01/3/M01-3.cpp`, `M01/3/3_<Title>.pdf`
(slot folders: two digits `01` ... `20` in a topic, one digit `1` ... `6` in a Mixed set). Folder and code-file names
never change; the PDF's name follows the English title (letters, digits and `_` only, at most 60 characters).
**`tools/layout.py` is the one place for these names** (build tools); `core/judge.py` and `core/updater.py` hold the
same rules for the students' side, and the regression test (`test_layout`) compares them. Change a name in all three.
Sibling repos `C1_MOCK`, `C1_PRACTICE` (Camp 1) and `C2_MOCK` (Camp 2 mock exams) share the same judge; fix shared bugs in all four.
Default memory limit 256 MB (Camp 2), not C1's 64 MB.

**Solutions never go in this repo** (it is public: GitHub raw serves the updates). Problem sources, official
solutions, generators and the solution book live in the teacher-only folder `C2_PRACTICE_SRC/` next to this repo
(`/usr/bin/python3 build.py check 4/5`, `/usr/bin/python3 build.py all` exports test data, problems.json, sets.json and PDFs here).
Today it judges batch problems (`judge.py`). We are adding interactive and communication problems,
and it updates itself from this GitHub repo so bugs can be fixed without re-sending zip files.

## Hard constraints (never break these)

1. **Python 3.7+ standard library only.** No pip packages. Students have Python and g++, nothing else.
2. **Student machines run Windows, macOS and Linux.** Every change must work on all three.
   Use `os.name == "nt"` guards like `judge.py` does. Never assume `/tmp`, `fork`, `resource`, or bash.
3. **Never touch student code.** The updater writes only files listed in `manifest.json`: inside `Judge/`,
   plus the managed package files students do not edit (PDFs, Makefile, judge.bat, READMEs, `.vscode/`) and
   missing code files `<topic>/<slot>/<no.>-<slot>.cpp` (empty, create-only). It must never read, move, delete or
   overwrite an existing student `.cpp` or `progress.json`, and never touch a file it did not ship. One exception,
   asked for by the teacher (plans/V4_LAYOUT.md section 3): when a release after 4.0.0 moves or replaces problems,
   the manifest's `moves` let a student's written file follow its problem once (`follow_moves` in `updater.py`): by
   English title to `<topic>/<slot>/<no.>-<slot>.cpp`; a replaced problem's file to `<topic>/old/<n>_<OldTitle>.cpp`;
   never over written code (on a clash the incoming file goes to `<topic>/old/<name>_moved.cpp` and the judge
   prints it); empty starters stay; nothing deleted; every move printed once (`show_moves` in `judge.py`), the
   second run is quiet.
4. **Never delete files the updater does not own.** No "wipe and reinstall" step, ever.
5. **Fail safe.** If the network is down, slow (>2 s), or a hash does not match, keep the current
   version and continue silently. A broken update must never stop a student from judging.
6. **Do not change the existing look.** New commands reuse `Style`, `box`, `rule`, `bar`, `compile_source`
   and the scoring functions from `judge.py` so everything feels the same (verdict table, score bar).
7. **Output is English, ASCII-safe.** Keep the `--ascii` and `--no-color` fallbacks working.

## Repo layout

```
C2_PRACTICE/
  CLAUDE.md
  core/                         # what students get inside Judge/
    judge.py                    # batch judge (existing, keep working)
    interactive_judge.py        # interactive problems (prototype exists)
    communication_judge.py      # TODO: IOI-style manager + stub
    updater.py                  # self-update from GitHub (manifest + SHA-256), see below
    include/bits/stdc++.h       # macOS fallback header
  problems/
    batch/<NN_Name>/N/*.in|out, gen.py, manifest.json   # see "Compact test data" below
    batch/problems.json         # problem bank: id -> title, tier, dir (<NN_Name>/N), samples, optional ml (MB)
    batch/sets.json             # topic K -> dir, group, problem ids (id = 100*K + N)
    interactive/<name>/{problem.json, interactor.cpp, tests/NN.in}
    communication/<name>/{problem.json, manager.cpp, stub/, tests/}
  student/                      # student-side files outside Judge/ (copied by build_dist.py)
    README.txt, .vscode/
    <NN_Name>/Problems_<NN_Name>.pdf, M01/Problems_M01.pdf        # the whole topic / Mixed set
    <NN_Name>/<slot>/<slot>_<Title>.pdf, M01/3/3_<Title>.pdf      # one problem; all PDFs are written by
                                                                  # C2_PRACTICE_SRC build.py all
    set_files/{Makefile, Makefile_<n>, judge.bat}                 # in every topic folder (Makefile_<n> for n != 20
                                                                  # problems): whole topic, `make 5` / `judge 5`
    set_files/{Makefile_problem, judge_problem.bat}               # in every problem folder, as Makefile / judge.bat
    set_files/template.cpp                                        # (empty) -> <NN_Name>/<slot>/<no.>-<slot>.cpp
  samples/                      # known-verdict programs used as regression tests
    batch/grid_ok.cpp, grid_int.cpp, grid_loop.cpp, grid_crash.cpp, grid_syntax.cpp      # problem 3-1
    interactive/guess_ok.cpp, guess_noflush.cpp, guess_linear.cpp, guess_crash.cpp
    expected.json               # {"batch/grid_ok.cpp": {"problem": "3-1", "verdict": "AC", "score": 100}, ...}
                                # verdict: AC/WA/TLE/RE/MLE/CE (first failing test); "score" optional (runs all tests)
  tools/
    layout.py                   # the names of the student package (slot, code_path, pdf_path, old_name): the one place
    build_manifest.py           # writes manifest.json (VERSION + SHA-256 of every file in Judge/); --check for CI
    moves/problems_<v>.json     # problems.json of release <v> (from 4.0.0 on; none yet), see "Self-update"
    replaced.json               # old English title -> "NN_Name/n" of replaced problems (written by build.py all)
    update_problem_manifest.py  # refreshes problems/batch/<NN_Name>/N/manifest.json after adding tests; --check --all in CI
    build_dist.py               # builds the student zip (C2_Practice/ layout with Judge/ and one folder per problem)
  tests/
    run_regression.py           # runs every sample, compares verdicts with expected.json
  .github/workflows/ci.yml      # matrix: windows-latest, macos-latest, ubuntu-latest
  VERSION                       # e.g. 1.0; bump it with every change students should get
  manifest.json                 # generated by build_manifest.py, committed, served by GitHub raw; do not edit by hand
```

Student-side layout (what `build_dist.py` produces): `C2_Practice/Judge/` = `core/` + `problems/`,
and `C2_Practice/<NN_Name>/<slot>/` = one problem: the student's `<no.>-<slot>.cpp` (empty at first), `<slot>_<Title>.pdf`,
`Makefile`, `judge.bat`; the topic folder also holds `Problems_<NN_Name>.pdf`, `Makefile`, `judge.bat` (and `old/`
after an update that replaced a problem the student had written). The repo layout is **not** the student layout.
The judge finds the problem from the code file's name (`04-05.cpp`, `M01-3.cpp`: `problem_of_name`) or from its
folder (`04_Binary_Search/05/`: `problem_of_folder`); both must keep working. Binaries are compiled in a temporary
folder (`tempfile.mkdtemp`), never in the problem folder (`test_judging` checks that nothing is left behind).
`judge.py` finds batch data in the first existing of `Judge/problems/batch/` (student package),
`../problems/batch/` (repo, run from `core/`) and `Judge/tests/` (older zips, JSON files next to judge.py).

## Compact test data (same mechanism as C2_MOCK)

- Each problem folder has a per-problem `manifest.json` (not the updater's `manifest.json`) listing every test with
  the SHA-256 of its input and of its normalized output, and `gen.py` when some tests are not shipped.
  Tests bigger than 64 KB are not shipped (`"in_file": false`): `judge.py` rebuilds them with `gen.py` the first time
  the problem is judged and checks their SHA-256. Outputs bigger than 64 KB (`"out_file": false`) are compared by hash.
  `C2_PRACTICE_SRC/build.py all` writes all of this; gen.py must stay Python 3.7 compatible and deterministic.
- Judging in the repo (`python3 core/judge.py ...`) can write those big inputs into `problems/batch/`. Never commit
  them; `build_dist.py` and `build_manifest.py` leave them out. The regression test rebuilds every big test in a
  temporary package and checks the hashes.

## Judging rules (batch)

- Compile: `g++ -O2 -std=c++17 -Wall -Wno-sign-compare -Wno-char-subscripts` (Windows: `-static`, 256 MB stack).
  Warnings are shown after "Compiled" (a count in set mode); they do not change the verdict.
- Limits: time `--tl` (default 1 s, hard kill at 2x+0.5 s), memory `--ml` (default 256 MB, the statements;
  `"ml"` in `problems.json` per problem). Memory = the program's peak resident size, read every millisecond while
  it runs (`/proc/<pid>/status VmHWM` on Linux, `proc_pid_rusage` on macOS, `GetProcessMemoryInfo` after exit on
  Windows); `ru_maxrss` of the child (`exited_peak`) only as a last check after the exit, because it includes the
  judge's own Python image before exec: used when it is clearly above the judge's own peak and above the readings
  (a program can grow after the last reading). On macOS the reading is `max(ri_phys_footprint,
  ri_lifetime_max_phys_footprint)`; never compare it with `ri_resident_size`, which counts shared pages too (that
  check threw away nearly every reading and made a 200 MB program AC now and then on CI).
  Verdicts in order: MLE, TLE (killed), WA (output over 64 MB), RE (exit code != 0), TLE (slow), AC/WA.
- The last 8 KB of the program's stderr are kept; after an RE the last 5 lines are shown (exception text, assert).
- Samples for the regression suite: `*_mle.cpp`, `*_throw.cpp`, `*_warn.cpp` next to the AC/WA/TLE/RE/CE ones.

## Interactive protocol (already implemented, keep compatible)

- Interactor is called as `interactor <input-file> <output-file>` and talks to the student on stdin/stdout.
- Exit code: `0` OK, `1` Wrong Answer, `2` Presentation Error (treated as WA), `3` judge failure.
  One line on stderr is the message shown to the student. This matches testlib.
- The judge relays the pipes and records the conversation, so failures show a `you` / `judge` transcript.
- A student program that hangs while the judge waits gets a flush hint
  (`cin.tie(0); ios::sync_with_stdio(0);` disables the automatic flush; the course template has it).
- Times are wall-clock on the student's machine: fine for practice, not for ranking.

## Communication problems (next, design before coding)

Manager process + one or more student processes linked by pipes, with a stub/grader header the
student includes. Reuse the pipe relay and transcript code from `interactive_judge.py`.
Propose the design and wait for approval before writing it.

## Self-update (implemented: `core/updater.py`, hooks in `judge.py`)

- Hosting is GitHub raw: `https://raw.githubusercontent.com/Petkub/C2_PRACTICE/main/` is the one
  constant (`BASE_URL` in `updater.py`; `REPO` differs between C2_PRACTICE and C2_MOCK). HTTPS only; the env var
  `JUDGE_UPDATE_URL` may point at `http://127.0.0.1:PORT/` for tests. `JUDGE_NO_UPDATE=1` disables checks
  (set by the regression tests and by the judge when it restarts after an update).
- `judge.py` is the entry point students already have (Makefile, judge.bat, VS Code tasks), so there is no
  separate launcher: `judge.py` imports `updater.py`, calls `updater.check()` at start-up (at most once every 10 minutes,
  stamp file `Judge/.update_check`), and after an update re-runs itself with the same arguments.
- `check()`: fetch `manifest.json` (2 s timeout) -> compare hashes (files whose hash equals the installed
  `Judge/manifest.json` entry are trusted without re-reading; `--update` re-hashes everything) -> download the
  changed files into `Judge/.update_tmp/` -> verify every SHA-256, `compile()` every `.py`, run the new
  `judge.py --help` -> only then `os.replace` them in (data first, `judge.py` last), old files to `Judge/.backup/`
  -> write the new `Judge/manifest.json`. Any failure: remove the temp folder, keep the current version, silent.
- Paths: only `Judge/`-relative, no absolute, no `..`, no `\`, no leading `.`, never `manifest.json` /
  `progress.json`. Outside `Judge/` only two kinds, each matched by a strict regex in `updater.py`:
  *managed* files students do not edit (`<NN_Name>/Problems_<NN_Name>.pdf`, `<NN_Name>/<slot>/<slot>_<Title>.pdf`,
  `Makefile` and `judge.bat` of a topic folder and of a problem folder, `README.txt`, `Guide.pdf`, `Progress.md`,
  `.vscode/*.json`) are replaced when their hash changes (old copy in `Judge/.backup/_package/`);
  *create-only* files (`<NN_Name>/<slot>/<no.>-<slot>.cpp`, `M01/3/M01-3.cpp`: the numbers in the name must agree
  with the folders, `SET_FILE`) are added only when missing. A `.cpp` can never be managed. Nothing is ever deleted.
- Retired PDFs: a problem PDF is named after its English title, so a re-titled problem gets a new PDF name and
  the new manifest no longer lists the old one. The updater moves the old PDF to `Judge/.backup/_package/` only when
  its bytes are exactly what it installed (the hash in the installed `Judge/manifest.json`) and the new manifest
  manages another PDF in the same problem folder (`plan_retired`, `retire`). No list of old names is needed; a file
  with other bytes stays.
- Only an installed package updates (`Judge/judge.py` and `Judge/manifest.json` exist); `core/` in the repo never.
- `--update` forces a check and prints the result; `--no-update` skips it; the header box shows `Judge vX.Y`
  (from `Judge/manifest.json`). Recovery when `judge.py` itself is broken: `python3 ../Judge/updater.py`.
- Manifest format (version in `tools/build_manifest.py`): `version`, `sources` (Judge/ prefix -> repo folder),
  `files` (Judge/ path -> sha256), `managed` and `create_only` (package path -> [sha256, repo path]), `bundles`,
  `moves`. It is one plain view: no bootstrap or per-version views (every installed updater reads it as it is).
- Speed: GitHub raw answers one file in about 0.3 s, so an updater that fetches files one
  by one needs minutes for a new set of problems (v3.0 of C1_PRACTICE: ~1,950 files, ~11 minutes, and one slow
  request aborted all of it). The updater therefore downloads in parallel (`WORKERS`), retries each file (`TRIES`),
  fetches one `bundles/<folder>.zip` per problem folder when it needs many of its files (every member is still
  checked against its own sha256 in `files`), and prints "Downloading ..." for big updates.
  `build_manifest.py` writes the bundles (deterministic zips, rewritten only when their content changes) and
  `manifest.json` lists them under `bundles`. Commit `bundles/` with the manifest.
- Format 2 (a legacy view for updaters that fetch one file at a time) exists in the older repos only (C1_MOCK, C1_PRACTICE, C2_MOCK): this repo
  started after the fast updater, so it has no `tools/legacy_manifest.json`. Never add a legacy manifest here.
- Moves (releases after 4.0.0 move, replace and re-title problems): `moves` is {sha256 of an earlier release's
  `problems.json`: [[from, to], ...]}, built by `build_manifest.py` from `tools/moves/problems_<v>.json` (exact bytes of
  release `<v>`; none exist yet). The same English title = the same problem (`RENAMED` in `build_manifest.py` maps an
  old title to a new one; without it a re-title counts as a replacement); a replaced problem (`tools/replaced.json`)
  goes to `<topic>/old/<n>_<OldTitle>.cpp`. After an update, `follow_moves` finds the hash of the `problems.json` it
  replaced (in `Judge/.backup/`), applies the pairs once (`Judge/.moves_done`) under the rules of hard constraint 3,
  and puts an empty starter back where a file moved away. Regression: `test_future_update` (a fake 4.0.1 over local
  HTTP: re-titled, replaced and moved problems, a clash, files the updater did not ship, a quiet second run).

## Releasing a change to students

1. Make the change, add a sample/test, run `python3 tests/run_regression.py`.
2. If the release moves, replaces or re-titles problems: first save the released `problems.json` (exact bytes) as
   `tools/moves/problems_<released version>.json`, and put re-titled problems in `RENAMED` in `tools/build_manifest.py`.
3. Bump `VERSION`, run `python3 tools/build_manifest.py`, commit both with the change, push.
   CI fails if `manifest.json` is stale. Students get the new files on their next judge run (GitHub raw caches
   for up to 5 minutes; a forced `--update` adds `?t=<time>` to every URL to skip that cache).
4. For new students: `python3 tools/build_dist.py` and publish `dist/C2_Practice.zip` (GitHub Release).

## Commands

```
python3 tests/run_regression.py          # must pass before every commit
python3 tools/build_manifest.py          # after changing anything under core/, problems/ or student/ (and bump VERSION)
python3 tools/build_manifest.py --check  # CI: fails if manifest.json is stale
python3 tools/build_dist.py              # build dist/C2_Practice/ + dist/C2_Practice.zip (--out DIR, --no-zip)
python3 core/judge.py samples/batch/grid_ok.cpp 3-1       # judge one file from the repo (topic 3, problem 1)
python3 core/interactive_judge.py guess samples/interactive/guess_ok.cpp
```
In a student package (`dist/C2_Practice/`):
```
python3 ../../Judge/judge.py             # in a problem folder (04_Binary_Search/05): that problem; also `make`, `judge`
python3 ../Judge/judge.py                # in a topic folder: the whole topic; also `make`, `judge`
python3 ../Judge/judge.py 5              # in a topic folder: problem 5 (05 too); also `make 5`, `make 05`, `judge 5`
python3 <path>/Judge/judge.py FILE.cpp   # anywhere: the problem from the file's name or folder (Ctrl+Shift+B does this)
python3 <path>/Judge/judge.py FILE.cpp K-P   # name the problem yourself (4-5, M01-3)
python3 ../Judge/judge.py --list         # topics and Mixed sets with their folders and code names
```

## Working rules for Claude Code

- Before changing `judge.py`, run the regression tests; after changing it, run them again.
- Add a sample program + expected verdict for every new behaviour or bug fix.
- Keep functions small and readable, in the same style as `judge.py`. No new dependencies.
- If a change cannot be verified on Windows locally, say so and rely on the CI matrix.
- Ask before: changing the manifest format, the exit-code protocol, or the safety rules of the updater.
