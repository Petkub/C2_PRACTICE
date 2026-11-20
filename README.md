# C2_PRACTICE — POSN Camp 2 Topic Practice (teacher's guide)

This repo is the source of the judge and test data that students run on their own computers for Camp 2 topic
practice. **Version 4** has 567 problems: 519 in 33 topics, each topic ordered from easy to hard (★ easy, ★★ medium,
★★★ challenging; in the Advanced group ★ reads "เริ่มต้น", starting level), in three groups, plus 48 in 8 Mixed sets:

- **Core** (01-14): the main content of Camp 2, 20 problems per topic.
- **Intermediate** (15-25): the extended content, 12 problems per topic (15 Trees has 20, 17 Fenwick and Segment
  Tree has 15).
- **Advanced (TOI)** (26-33): beyond Camp 2, 12 problems per topic.
- **Mixed** (folders `00_Mixed/M01` ... `00_Mixed/M08`, set numbers 41-48 in the judge): 8 sets of 6 problems from different Camp 2
  topics, for practising which technique a problem needs. **Nothing a student sees names the topic or the
  technique** (folders, `00_Mixed/README.txt`, PDF `Problems_M01.pdf`, cover "ชุดฝึกรวม · 6 ข้อ", titles, `--list`); there is no level, time
  limit or target score. The techniques are only in the teacher's solution book and in
  `C2_PRACTICE_SRC/plans/V4_MIXED_STATUS.md`. Used after the vjudge MUST list and before the timed mock exams.

| topic | folder | group | problems |
|---|---|---|---|
| 1 | `01_Brute_Force_and_Implementation` | Core | 20 |
| 2 | `02_Strings_and_Parsing` | Core | 20 |
| 3 | `03_Prefix_Sums_and_Two_Pointers` | Core | 20 |
| 4 | `04_Binary_Search` | Core | 20 |
| 5 | `05_Greedy` | Core | 20 |
| 6 | `06_Sorting_and_Sweep_Line` | Core | 20 |
| 7 | `07_Number_Theory_and_Counting` | Core | 20 |
| 8 | `08_Divide_and_Conquer` | Core | 20 |
| 9 | `09_DP_I_Foundations` | Core | 20 |
| 10 | `10_DP_II_Classic_Patterns` | Core | 20 |
| 11 | `11_DP_III_Faster_Transitions` | Core | 20 |
| 12 | `12_Graph_Traversal` | Core | 20 |
| 13 | `13_Shortest_Paths` | Core | 20 |
| 14 | `14_DSU_and_MST` | Core | 20 |
| 15 | `15_Trees` | Intermediate | 20 |
| 16 | `16_Monotonic_Stack_and_Queue` | Intermediate | 12 |
| 17 | `17_Fenwick_and_Segment_Tree` | Intermediate | 15 |
| 18 | `18_Sparse_Table` | Intermediate | 12 |
| 19 | `19_Lazy_Segment_Tree` | Intermediate | 12 |
| 20 | `20_Tree_DP` | Intermediate | 12 |
| 21 | `21_Rerooting` | Intermediate | 12 |
| 22 | `22_Euler_Tour` | Intermediate | 12 |
| 23 | `23_LCA_and_Binary_Lifting` | Intermediate | 12 |
| 24 | `24_SCC_Bridges_and_Articulation_Points` | Intermediate | 12 |
| 25 | `25_Trie` | Intermediate | 12 |
| 26 | `26_Bitmask_and_Digit_DP` | Advanced (TOI) | 12 |
| 27 | `27_DSU_on_Tree` | Advanced (TOI) | 12 |
| 28 | `28_Heavy_Light_Decomposition` | Advanced (TOI) | 12 |
| 29 | `29_Centroid_Decomposition` | Advanced (TOI) | 12 |
| 30 | `30_Persistent_Segment_Tree` | Advanced (TOI) | 12 |
| 31 | `31_Convex_Hull` | Advanced (TOI) | 12 |
| 32 | `32_Convex_Hull_Trick_and_DP_Optimization` | Advanced (TOI) | 12 |
| 33 | `33_Mo_Algorithm` | Advanced (TOI) | 12 |
| 41-48 | `00_Mixed/M01` ... `00_Mixed/M08` | Mixed | 6 each |

Students never clone this repo: they download `C2_Practice.zip` once from
[Releases](https://github.com/Petkub/C2_PRACTICE/releases/latest), and from then on their judge **updates itself
from this repo** every time you push to `main`.

**4.0.0 is the first release students get.** No student has an older package, so nothing in the code or in this
guide handles older layouts.

**The student package: one folder per problem.** (The names are written down once, in `tools/layout.py`.)

```
C2_Practice/
  00_Mixed/                                all Mixed sets, on top (00_ sorts first); names no topic
    README.txt                             one neutral line: the order of the sets, easy to hard inside a set
    M01/                                   a Mixed set: laid out like a topic folder, slot folders have one digit (1 ... 6)
      Problems_M01.pdf
      Makefile, judge.bat                  find Judge/ two levels up (../../Judge)
      3/
        M01-3.cpp
        3_Free_Coins_Only.pdf
    ...
    M08/
  04_Binary_Search/                        a topic folder
    Problems_04_Binary_Search.pdf          the whole topic: a cover with the problem list, then every problem
    Makefile, judge.bat                    judge the whole topic, or one problem (make 5 / judge 5)
    01/
    ...
    05/                                    problem 5: two digits in a topic (01 ... 20)
      04-05.cpp                            the student's code: empty at first, created once, never replaced
      05_Cutting_Ropes.pdf                 this problem's own PDF (the same pages as in the topic PDF, no cover)
    ...
    20/
    old/                                   only after an update that replaced a problem the student had written (below)
  Judge/                                   the judge and the test data (= core/ + problems/ + manifest.json)
  README.txt, Guide.pdf, .vscode/
```

- A problem folder holds **exactly its code file and its PDF**. `Makefile` and `judge.bat` exist in the topic and
  Mixed-set folders only (`make 5` / `judge 5` there judges one problem); the updater refuses them in a problem folder.

- A folder name and a code file name never change, also when a problem is replaced or re-titled. The code file
  names are unique in the whole package (`04-05.cpp`, `27-12.cpp`, `M01-3.cpp`), so editor tabs are never ambiguous.
- The problem PDF's name follows the English title: ASCII letters, digits and `_` only (spaces become `_`, other
  characters are dropped), at most 60 characters.
- Students must not rename the folders or the `.cpp` files: the judge finds the problem from the file name
  (`04-05.cpp`) or from its folder (`04_Binary_Search/05/`). `student/README.txt` tells them so.
- In the repo the PDFs are `student/<folder>/Problems_<folder>.pdf` and `student/<folder>/<slot>/<slot>_<Title>.pdf`
  (`<folder>` = `04_Binary_Search` or `00_Mixed/M01`; both written by `C2_PRACTICE_SRC` `build.py all`, which also
  writes `student/00_Mixed/README.txt`). The test data of a Mixed set stays in `problems/batch/M01/` (sets.json
  `"dir": "M01"`); only the package folder is `00_Mixed/M01` (`layout.folder`).

**How students judge** (binaries are compiled in `Judge/.build/<new folder>`, removed after the run, like C2_MOCK;
in the system temp folder when `Judge/` cannot be written; never in a topic or problem folder):

| where | command |
|---|---|
| VS Code, the `C2_Practice` folder open | `Ctrl+Shift+B` on the open `.cpp` judges that problem; *Run Task > Judge whole topic* |
| a problem folder (`04_Binary_Search/05`) | `python3 ../../Judge/judge.py` (no `make` / `judge` here: the folder has no Makefile or judge.bat); in a Mixed set (`00_Mixed/M03/2`) `python3 ../../../Judge/judge.py` |
| a topic folder (`04_Binary_Search`) | `make 5` or `make 05` (one problem), `make` (whole topic) · Windows `judge 5`, `judge` · `python3 ../Judge/judge.py`, `python3 ../Judge/judge.py 5` |
| a Mixed set folder (`00_Mixed/M03`) | `make 2`, `make` · Windows `judge 2`, `judge` (Makefile and judge.bat find `../../Judge`) · `python3 ../../Judge/judge.py`, `python3 ../../Judge/judge.py 2` |
| anywhere | `python3 <path>/Judge/judge.py FILE.cpp` (the problem comes from the file's name or folder), or `FILE.cpp K-P` to name the problem (`4-5`, `M01-3`) |

`python3 ../Judge/judge.py --list` shows the Mixed sets first (as on disk), then every topic, with their folders and
code file names (Mixed sets without any topic name).

**What the updater does when a later release changes problems** (from 4.0.0 on; details in section 5): a
student's written file follows its problem, a replaced problem's file goes to `<topic>/old/`, nothing is
overwritten or deleted. `core/CHANGELOG.txt` and `student/README.txt` tell students the same.

The Camp 2 mock exams live in [C2_MOCK](https://github.com/Petkub/C2_MOCK) and the Camp 1 practice in
[C1_PRACTICE](https://github.com/Petkub/C1_PRACTICE); all of them share this judge (C2_MOCK's README lists the
differences). `CLAUDE.md` has the rules for working on the code with Claude Code.

**Solutions are not in this repo** (it is public). Statements (Typst), official solutions, brute-force checkers,
generators and the solution book are in the teacher-only folder `C2_PRACTICE_SRC/` (its `CATALOG.md` lists every
problem, `WHATS_NEW_v4.md` the new ones): `/usr/bin/python3 build.py check 4/5` rebuilds one problem's tests and
checks sol against brute; `/usr/bin/python3 build.py all` exports all test data, `problems.json`, `sets.json` and
the topic PDFs into this repo and writes `build/C2_Practice_Solutions.pdf`. Never type an expected output by hand.

---

## 1. What is where

```
core/                  what students get inside Judge/   (judge.py, updater.py, include/, README.txt, CHANGELOG.txt)
problems/batch/        test data: <NN_Name>/N/01.in, 01.out, ..., manifest.json (hashes), gen.py (rebuilds tests
                       > 64 KB on the student's computer)   + problems.json (problem bank) + sets.json (topics)
student/               the rest of the student package: README.txt, .vscode/,
                       <NN_Name>/Problems_<NN_Name>.pdf (the whole topic) and <NN_Name>/<slot>/<slot>_<Title>.pdf (one
                       problem), the same for a Mixed set under 00_Mixed/M01/, and 00_Mixed/README.txt, all written by
                       C2_PRACTICE_SRC build.py all,
                       set_files/: Makefile (Makefile_<n> for a topic of n != 20 problems) and judge.bat for a topic
                       folder (none for a problem folder), template.cpp (empty) -> every
                       <NN_Name>/<slot>/<no.>-<slot>.cpp
samples/               known-verdict programs used by the tests (expected.json says which verdict each must get)
tests/run_regression.py   the test suite: run before every push
tools/layout.py           the names of the student package (folders, code files, PDFs): the one place for them
tools/build_manifest.py   writes manifest.json (hashes of everything students get) and bundles/
tools/build_dist.py       builds dist/C2_Practice.zip for new students (dist/ is not committed)
tools/moves/              problems_<version>.json of earlier releases (from 4.0.0 on; none yet): how students' files
                          find their problems after a release that moves them (section 4f)
tools/replaced.json       titles of problems that were replaced by new ones (their files go to <topic>/old/);
                          written by C2_PRACTICE_SRC build.py all
VERSION                   the version students see ("Judge v4.0.0")
manifest.json             generated, served to students by GitHub; never edit by hand
bundles/                  generated zips of each topic's test data (fast updates); commit them with manifest.json
```

What a student has: `C2_Practice/Judge/` (= `core/` + `problems/` + `manifest.json`) and
`C2_Practice/<NN_Name>/<slot>/<no.>-<slot>.cpp` (their code, which the updater never overwrites) next to that
problem's PDF, with `Problems_<NN_Name>.pdf` in the topic folder (the tree at the top of this file).

## 2. One-time setup on a new computer

```bash
git clone https://github.com/Petkub/C2_PRACTICE.git
cd C2_PRACTICE
python3 tests/run_regression.py        # needs python3 and g++; ~20 min; must end with "All regression tests passed."
```
Optional: `gh auth login` (GitHub CLI) if you want to publish releases from the terminal.

## 3. The release routine (every change students should get)

```bash
cd ~/stupidGrader/C2_PRACTICE            # or wherever your clone is
# ... make the change (see section 4) ...
python3 tests/run_regression.py       # 1. tests pass
cat VERSION                           # 2. bump the version: one higher than this
echo 4.0.1 > VERSION
python3 tools/build_manifest.py       # 3. rebuild manifest.json (ALWAYS after the change, never before)
git add -A
git commit -m "04/5: add test 17"        # 4. commit ...
git push                              #    ... and push
```
Then check that CI is green: <https://github.com/Petkub/C2_PRACTICE/actions> (it runs the tests on Windows, macOS,
Linux and Python 3.7, and fails if `manifest.json` is stale).

Students receive it automatically: their judge checks GitHub at most every 10 minutes, GitHub caches files for
up to 5 minutes, so everyone who is judging gets the new version within ~15 minutes; a student who opens the judge
later gets it on that first run. To see it immediately on any installed copy:
`python3 ../Judge/judge.py --update` (inside a topic folder).

Add one line to `core/CHANGELOG.txt` for each version; students can read it.

## 4. Common changes

### 4a. Fix or extend a problem (tests, statement)
Work in `C2_PRACTICE_SRC/topics/<NN_Name>/<N>/` (statement.typ, gen.py, sol.cpp, brute.cpp), then
`/usr/bin/python3 build.py check <NN>/<N>` (until `ok`) and `/usr/bin/python3 build.py all`, and release (section 3).
Add new tests at the end of gen.py so existing test numbers keep their content (the updater never deletes a test
that students already have). Outputs always come from sol.cpp.

### 4b. Fix a bug in the judge
1. Edit `core/judge.py` (or `core/updater.py`).
2. Add a sample program that shows the bug under `samples/batch/` and its expected verdict in
   `samples/expected.json`, so the bug cannot come back.
3. Run the tests, release. If it cannot be tested on Linux (a Windows-only problem), rely on CI's Windows job.

### 4c. Add a new topic (e.g. topic 27)
1. Add it to `C2_PRACTICE_SRC/topics.json` and write `topics/27_Name/1..n/`; check each problem.
2. `/usr/bin/python3 build.py all` writes `problems/batch/27_Name/`, the new entries of `problems.json` /
   `sets.json`, `student/27_Name/Problems_27_Name.pdf` and every `student/27_Name/<slot>/<slot>_<Title>.pdf`.
3. Release. Existing students get the test data, the PDFs, the topic's `Makefile` and `judge.bat`, and the updater
   **creates** `27_Name/01/27-01.cpp ...` (code files are only ever created, never overwritten).

### 4d. Change something students see outside Judge/ (README, Makefile, judge.bat, template)
Edit it under `student/` and release. These are *managed* files: the updater replaces them on every student's
computer when they change (the old copy goes to `Judge/.backup/_package/`), because students do not edit them.
The only files that are never replaced are the code files `<NN_Name>/<slot>/<no.>-<slot>.cpp` (created once, empty,
then the student's own) and `Judge/progress.json`.

### 4e. A new zip for new students
```bash
python3 tools/build_dist.py                              # -> dist/C2_Practice.zip
gh release create v4.0.0 dist/C2_Practice.zip --title "C2_Practice v4.0.0"
```
The link <https://github.com/Petkub/C2_PRACTICE/releases/latest/download/C2_Practice.zip> always gives the newest
release. You only need a new release for new students (or new sets); existing students update themselves.

### 4f. Move, replace or re-title problems (any release after 4.0.0)
The updater matches a problem of the installed release with a problem of the new one **by English title**, so it
needs the `problems.json` students have now. Before you export the new problems:

1. Save the released `problems/batch/problems.json` (exact bytes, e.g. `git show v4.0.0:problems/batch/problems.json`)
   as `tools/moves/problems_<released version>.json`, e.g. `tools/moves/problems_4.0.0.json`. Keep the files of
   earlier releases there: a student may update from any of them.
2. If a problem only gets a new title, add it to `RENAMED` in `tools/build_manifest.py` (old title -> new title).
   Without this line a re-titled problem counts as a replaced one, and written code goes to `old/`.
3. Make the change in `C2_PRACTICE_SRC` and run `build.py all` (it also writes `tools/replaced.json` from its
   `bank/`), then release as in section 3 (`tools/build_manifest.py` writes the `moves` into `manifest.json`).

What students then see is in section 5. `tests/run_regression.py` ("A later release (fake 4.0.1 over local HTTP)")
checks all of it on a fake release.

## 5. How the self-update works (so you can trust it)

- `Judge/updater.py` fetches `manifest.json` from `raw.githubusercontent.com/Petkub/C2_PRACTICE/main/`, compares the
  SHA-256 of every file in `Judge/`, downloads the changed ones to a temp folder, verifies each hash, compiles
  the new `.py` files and test-runs the new `judge.py --help`, and only then swaps them in. The old file is kept
  in `Judge/.backup/`.
- Outside `Judge/` it only replaces the managed files above (PDFs, a topic or Mixed-set folder's `Makefile` and
  `judge.bat`, `README.txt`, `00_Mixed/README.txt`, `Guide.pdf`, `.vscode/`) and creates missing code files
  `<NN_Name>/<slot>/<no.>-<slot>.cpp` (`00_Mixed/M01/<slot>/M01-<slot>.cpp`); Mixed paths are accepted only under
  `00_Mixed/` (a root-level `M01/...` is refused); it never deletes
  anything and never overwrites an existing code file. Files it did not ship are never touched.
- When a release moves, replaces or re-titles problems (section 4f), on the first run after the update:
  - a **moved** problem: the student's written file follows it (same English title) to
    `<topic>/<slot>/<no.>-<slot>.cpp`, and the place it left gets an empty code file again;
  - a **replaced** problem: the written file goes to `<topic>/old/<n>_<OldTitle>.cpp`, never under the new problem;
  - **nothing is overwritten**: if the new place already holds written code, the incoming file goes to
    `<topic>/old/<name>_moved.cpp` and the judge says so;
  - an empty (unwritten) code file is not moved;
  - a problem PDF whose title changed: the new PDF is installed, and the old one is moved to
    `Judge/.backup/_package/` only when its bytes are exactly the ones the updater installed. This needs no list:
    the updater compares the installed `Judge/manifest.json` with the new one;
  - the judge prints every move once; the second run is quiet.
- No network, a slow network (> 2 s), a bad hash, a strange path: it keeps the current version and says nothing.
  A failed update never stops a student from judging.
- `manifest.json` is one plain view: `version`, `sources`, `files`, `managed`, `create_only`, `bundles`, `moves`.

## 6. Checking a student's problem report

- "The judge says I have the old version": ask them to run `python3 ../Judge/judge.py --update`. Its message says
  why it cannot update (e.g. a school firewall, or a macOS Python without certificates:
  `CERTIFICATE_VERIFY_FAILED` → run "Install Certificates.command" from the Python folder).
- "My correct code gets Runtime Error / Wrong Answer": ask for the problem, the test number and the lines printed
  under *First failure* (e.g. `your program crashed (signal 11 SIGSEGV: invalid memory access)` and the program's
  own stderr below it, such as `terminate called after throwing ... out_of_range`), plus any g++ warnings printed
  after "Compiled". Then run their
  file here: `python3 core/judge.py their.cpp K-N`. The judge compiles with `-O2`, which exposes uninitialised
  variables and out-of-bounds reads that pass on the student's own compile.
- To check the judge itself, run every official solution: they must all score 100
  (`python3 core/judge.py solution.cpp K-N`).

## 7. Things that go wrong, and the fix

| Symptom | Fix |
|---|---|
| CI red: "manifest.json is stale" | `python3 tools/build_manifest.py`, commit, push. |
| CI red: "every .in has an .out" | you added `NN.in` without `NN.out` (section 4a). |
| A pushed version is broken | `git revert HEAD`, bump `VERSION`, rebuild the manifest, push. Students roll forward to the fixed version; their `Judge/.backup/` also still has the previous files. |
| `build_dist.py` refuses to overwrite | it only replaces a `dist/C2_Practice` folder it made itself, so a student folder is never wiped; delete `dist/` by hand if you are sure. |
| Students on Windows see `?` boxes | they can use `--ascii`; the judge output must stay ASCII-safe. |

## 8. Never

- Edit `manifest.json` by hand, or commit without rebuilding it.
- Delete or rename a test that students already have (the updater never deletes; add a new one instead).
- Type an expected output by hand.
- Change the judge's exit codes, the manifest format or the updater's safety rules without updating the tests.
