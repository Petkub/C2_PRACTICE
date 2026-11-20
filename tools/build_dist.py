#!/usr/bin/env python3
"""
Build the student package.

  python3 tools/build_dist.py                  writes dist/C2_Practice/ and dist/C2_Practice.zip
  python3 tools/build_dist.py --out DIR        writes DIR/C2_Practice/ (and DIR/C2_Practice.zip)
  python3 tools/build_dist.py --no-zip         folder only

Layout produced (one folder per problem, tools/layout.py):
  C2_Practice/README.txt, Guide.pdf, .vscode/    from student/
  C2_Practice/Judge/                             exactly the files listed in manifest.json (core/ + problems/),
                                               plus manifest.json itself (the installed version for updater.py)
  C2_Practice/<NN_Name>/Problems_<NN_Name>.pdf from student/<NN_Name>/ (the whole topic; a Mixed set: M01/Problems_M01.pdf)
  C2_Practice/<NN_Name>/Makefile, judge.bat     from student/set_files/ (Makefile_<n> for a topic of n != 20)
  C2_Practice/<NN_Name>/05/04-05.cpp            the student's code file: empty (student/set_files/template.cpp)
  C2_Practice/<NN_Name>/05/05_<Title>.pdf       the problem's own PDF, from student/<NN_Name>/05/
                                               (a problem folder holds exactly these two files)
The zip holds the contents of C2_Practice/ without the folder itself (see make_zip).
The manifest is rebuilt first, so the zip and manifest.json always agree.
"""
import os
import shutil
import sys
import zipfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_manifest  # noqa: E402

REPO = build_manifest.REPO
STUDENT = os.path.join(REPO, "student")
NAME = "C2_Practice"
MARKER = ".built_by_build_dist"     # only a folder with this file may be replaced by a new build


def prepare(out):
    """Create out/C2_Practice, replacing an earlier build but never a folder this script did not make."""
    root = os.path.join(out, NAME)
    if os.path.exists(root):
        if not os.path.exists(os.path.join(root, MARKER)):
            sys.exit(f"Refusing to replace {root}: it was not made by build_dist.py (it may hold student code).")
        shutil.rmtree(root)
    os.makedirs(root)
    with open(os.path.join(root, MARKER), "w") as f:
        f.write("Made by tools/build_dist.py; not part of the zip.\n")
    return root


def copy_file(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)


def copy_judge(root, manifest):
    judge = os.path.join(root, "Judge")
    for rel, src in build_manifest.judge_files():
        copy_file(os.path.join(REPO, src), os.path.join(judge, *rel.split("/")))
    with open(os.path.join(judge, "manifest.json"), "w", encoding="utf-8") as f:
        f.write(build_manifest.dumps(build_manifest.installed(manifest)))     # as the updater leaves it


def copy_package_files(root):
    """Everything outside Judge/: the managed files and the create-only templates, as the manifest lists them."""
    pairs = build_manifest.managed_files() + build_manifest.set_files()
    for rel, src in pairs:
        copy_file(os.path.join(REPO, src), os.path.join(root, *rel.split("/")))
    tops = {rel.split("/")[0] for rel, _ in pairs}
    return (len([d for d in tops if d[:2].isdigit()]),
            len([d for d in tops if len(d) == 3 and d[0] == "M" and d[1:].isdigit()]))


def make_zip(root):
    """No top-level folder in the zip: Windows "Extract All" already makes C2_Practice/, and a top-level folder gave
    C2_Practice/C2_Practice/, where VS Code opened on the outer folder finds no .vscode/tasks.json (no Ctrl+Shift+B)."""
    path = root + ".zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames.sort()
            for name in sorted(filenames):
                if name == MARKER:
                    continue
                full = os.path.join(dirpath, name)
                z.write(full, os.path.relpath(full, root).replace(os.sep, "/"))
    return path


def main():
    argv = sys.argv[1:]
    out = os.path.join(REPO, "dist")
    if "--out" in argv:
        i = argv.index("--out")
        if i + 1 >= len(argv):
            sys.exit("--out needs a folder")
        out = os.path.abspath(argv[i + 1])
    manifest = build_manifest.build()
    with open(build_manifest.MANIFEST, "w", encoding="utf-8") as f:
        f.write(build_manifest.dumps(manifest))
    root = prepare(out)
    copy_judge(root, manifest)
    n = copy_package_files(root)
    print(f"Built {root} (v{build_manifest.installed(manifest)['version']}, {n[0]} topics, {n[1]} Mixed sets)")
    if "--no-zip" not in argv:
        path = make_zip(root)
        print(f"Built {path} ({os.path.getsize(path) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
