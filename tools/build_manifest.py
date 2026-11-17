#!/usr/bin/env python3
"""
Write manifest.json: the version (file VERSION) and the SHA-256 of every file the student package gets inside
Judge/, the managed package files outside Judge/ (<topic>.pdf, Makefile, judge.bat, README.txt, Guide.pdf,
Progress.md, .vscode/: replaced on the students' computers when they change) and the create-only files
(<topic folder>/N.cpp templates: added only when missing, never replaced).
Judge/updater.py on the students' computers compares this file with what they have.

  python3 tools/build_manifest.py            write manifest.json (run after changing core/, problems/, student/)
  python3 tools/build_manifest.py --check    exit 1 if manifest.json or a bundle is stale (used by CI)

It also writes bundles/<folder>.zip: every shipped file of one topic folder (problems/batch/<folder>/), so the
updater fetches a new topic in a few requests. A bundle is rewritten only when its content changes.

Format 1 (the real manifest):
  {"version": "4.0.0",
   "sources": {"problems/": "problems/", "": "core/"},        Judge/ path prefix -> repo folder
   "files": {"judge.py": "<sha256>", "problems/batch/04_Binary_Search/1/01.in": "<sha256>", ...},
   "managed": {"04_Binary_Search/04_Binary_Search.pdf": ["<sha256>", "student/04_Binary_Search/04_Binary_Search.pdf"], ...},
   "create_only": {"04_Binary_Search/1.cpp": ["<sha256>", "student/set_files/template.cpp"], ...},
   "bundles": {"bundles/04_Binary_Search.zip": {"sha256": "<sha256>", "prefix": "problems/batch/04_Binary_Search/"}, ...},
   "moves": {"<sha256 of an older release's problems.json>": [["Topic_3/5.cpp", "04_Binary_Search/5.cpp"], ...]}}
Format 3 (v4.0; the same scheme as C2_MOCK v7.0): updaters before 4.0 reject the new folder names in managed and
create-only paths, so the top level holds only the version, "full" is a bootstrap view for them ("bootstrap": true:
every Judge/ file, only the package files their path rules accept) and "full_v4" is the real manifest. An old judge
installs the bootstrap (so it gets the new updater), restarts, and the new judge.py installs "full_v4" at once.

"moves": tools/moves/problems_<v>.json are the problems.json of earlier releases (exact bytes); a problem is the same
problem when its English title is the same, so its student file goes from its old folder to the new one; a problem
replaced by a new problem (tools/replaced.json, written by C2_PRACTICE_SRC build.py all from its bank/) goes to
<the slot's new topic folder>/old/N_<Title>.cpp; any other problem no longer in a topic goes to
<old folder>/old/N_<Title>.cpp. Judge/updater.py follow_moves() applies them once.
"""
import hashlib
import json
import re
import os
import sys
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO, "manifest.json")
SOURCES = {"problems/": "problems/", "": "core/"}
SKIP_NAMES = {"__pycache__", ".DS_Store", "progress.json", "progress.json.tmp", ".update_check"}
SKIP_SUFFIXES = (".pyc",)
BUNDLES = "bundles"
BOOTSTRAP = ("judge.py", "updater.py")      # what an old updater must take so that this updater does the rest
STALE = []                                  # bundles that --check found out of date


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def version():
    with open(os.path.join(REPO, "VERSION"), encoding="utf-8") as f:
        return f.read().strip()


def shipped(dirpath, names):
    """Names in dirpath that go into the package: not the big tests gen.py rebuilds on the student's computer
    (manifest.json of the problem: in_file / out_file false), which judging in the repo may have created."""
    skip = set()
    p = os.path.join(dirpath, "manifest.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for t in json.load(f)["tests"]:
                if not t["in_file"]:
                    skip.add(t["name"] + ".in")
                if not t["out_file"]:
                    skip.add(t["name"] + ".out")
    return [n for n in names if n not in SKIP_NAMES and n not in skip and not n.endswith(SKIP_SUFFIXES)
            and not n.startswith(".")]


def judge_files():
    """Every file of Judge/ as (Judge-relative path, repo-relative path), both with '/' separators."""
    out = []
    for prefix, repo_dir in SOURCES.items():
        top = os.path.join(REPO, repo_dir)
        for dirpath, dirnames, filenames in os.walk(top):
            dirnames[:] = sorted(shipped(dirpath, dirnames))
            for name in sorted(shipped(dirpath, filenames)):
                rel = os.path.relpath(os.path.join(dirpath, name), top).replace(os.sep, "/")
                out.append((prefix + rel, repo_dir + rel))
    return sorted(out)


def load_sets():
    with open(os.path.join(REPO, "problems", "batch", "sets.json"), encoding="utf-8") as f:
        return json.load(f)


def set_files():
    """Create-only files (the N.cpp templates of every topic) as (package path, repo-relative source path)."""
    return [(f"{s['dir']}/{i}.cpp", "student/set_files/template.cpp")
            for s in load_sets() for i in range(1, len(s["problems"]) + 1)]


def managed_files():
    """Managed package files outside Judge/ as (package path, repo-relative source path)."""
    out = []
    for name in ("README.txt", "Guide.pdf", "Progress.md", ".vscode/tasks.json", ".vscode/settings.json"):
        if os.path.exists(os.path.join(REPO, "student", *name.split("/"))):
            out.append((name, "student/" + name))
    for s in load_sets():
        d = s["dir"]
        n = len(s["problems"])
        out.append((f"{d}/Makefile", "student/set_files/Makefile" + ("" if n == 20 else f"_{n}")))
        out.append((f"{d}/judge.bat", "student/set_files/judge.bat"))
        if os.path.exists(os.path.join(REPO, "student", d, f"{d}.pdf")):
            out.append((f"{d}/{d}.pdf", f"student/{d}/{d}.pdf"))
    return out


def with_hashes(pairs):
    return {rel: [sha256_file(os.path.join(REPO, src)), src] for rel, src in pairs}


def zip_members(path):
    """{member name: sha256} of a zip, or None when it is missing or broken."""
    try:
        with zipfile.ZipFile(path) as z:
            return {i.filename: hashlib.sha256(z.read(i)).hexdigest() for i in z.infolist()}
    except (OSError, zipfile.BadZipFile):
        return None


def write_zip(path, members):
    """Deterministic zip of (Judge/ path, repo path) pairs: fixed dates and modes, sorted names."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel, src in sorted(members):
            info = zipfile.ZipInfo(rel, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(REPO, src), "rb") as f:
                z.writestr(info, f.read())
    os.replace(tmp, path)


def bundles(pairs, files, write):
    """One bundle per problem folder problems/batch/<folder>/, rewritten only when its content changed."""
    groups = {}
    for rel, src in pairs:
        parts = rel.split("/")
        if len(parts) >= 4 and parts[0] == "problems" and parts[1] == "batch":
            groups.setdefault(parts[2], []).append((rel, src))
    out = {}
    for folder, members in sorted(groups.items()):
        name = f"{BUNDLES}/{folder}.zip"
        path = os.path.join(REPO, BUNDLES, folder + ".zip")
        if zip_members(path) != {rel: files[rel] for rel, _ in members}:
            if not write:
                STALE.append(name)
                continue
            write_zip(path, members)
        out[name] = {"sha256": sha256_file(path), "prefix": f"problems/batch/{folder}/"}
    return out


MOVES = os.path.join(REPO, "tools", "moves")
RENAMED = {}                        # old English title -> new title, if a problem is renamed between releases
REPLACED_FILE = os.path.join(REPO, "tools", "replaced.json")   # old English title -> "NN_Name/n" (C2_PRACTICE_SRC bank/)


def slug(title):
    return "".join(w[:1].upper() + w[1:] for w in "".join(c if c.isalnum() else " " for c in title).split())


def moves():
    """{sha256 of an old problems.json: [[from, to], ...]} for every file in tools/moves/."""
    with open(os.path.join(REPO, "problems", "batch", "problems.json"), encoding="utf-8") as f:
        now = {e["en"]: e["dir"] for e in json.load(f).values()}
    replaced = {}
    if os.path.exists(REPLACED_FILE):
        with open(REPLACED_FILE, encoding="utf-8") as f:
            replaced = json.load(f)
    out = {}
    for name in sorted(os.listdir(MOVES)) if os.path.isdir(MOVES) else []:
        path = os.path.join(MOVES, name)
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
        pairs = []
        for e in sorted(old.values(), key=lambda e: e["dir"]):
            src, title = e["dir"] + ".cpp", RENAMED.get(e["en"], e["en"])
            if title in now:
                if now[title] != e["dir"]:
                    pairs.append([src, now[title] + ".cpp"])
            elif title in replaced:                 # its slot holds a new problem: park it in that topic's old/
                k, n = replaced[title].split("/")
                pairs.append([src, f"{k}/old/{n}_{slug(e['en'])}.cpp"])
            else:
                k, n = e["dir"].split("/")
                pairs.append([src, f"{k}/old/{n}_{slug(e['en'])}.cpp"])
        out[sha256_file(path)] = pairs
    return out


# path rules of the updaters before 4.0: they reject a whole manifest with another topic folder name
OLD_SET_FILE = re.compile(r"^Topic_[0-9]+/[0-9]+\.cpp$")
OLD_MANAGED_FILE = re.compile(r"^(Topic_[0-9]+/(Makefile|judge\.bat|Topic_[0-9]+\.pdf)|Guide\.pdf|README\.txt"
                              r"|Progress\.md|\.vscode/(tasks|settings)\.json)$")


def bootstrap_view(full):
    """What updaters before 4.0 read ("full"): every Judge/ file (so they install the 4.0 updater and judge), only the
    package files their path rules accept, and "bootstrap": true so the new updater adds the rest at once."""
    view = dict(full)
    view["managed"] = {k: v for k, v in full["managed"].items() if OLD_MANAGED_FILE.match(k)}
    view["create_only"] = {k: v for k, v in full["create_only"].items() if OLD_SET_FILE.match(k)}
    view["bootstrap"] = True
    return view


def build(write=True):
    pairs = judge_files()
    files = {rel: sha256_file(os.path.join(REPO, src)) for rel, src in pairs}
    full = {"version": version(), "sources": SOURCES, "files": files, "managed": with_hashes(managed_files()),
            "create_only": with_hashes(set_files()), "bundles": bundles(pairs, files, write), "moves": moves()}
    return {"version": full["version"], "full": bootstrap_view(full), "full_v4": full}


def installed(manifest):
    """The part of a manifest that the updater installs (and writes as Judge/manifest.json)."""
    return manifest.get("full_v4", manifest.get("full", manifest))


def dumps(manifest):
    return json.dumps(manifest, indent=0, sort_keys=True) + "\n"


def main():
    check = "--check" in sys.argv[1:]
    manifest = build(write=not check)
    text = dumps(manifest)
    if check:
        if STALE:
            print("bundles are stale (" + ", ".join(STALE[:3]) + "): run  python3 tools/build_manifest.py  and commit.")
            return 1
        try:
            with open(MANIFEST, encoding="utf-8") as f:
                current = f.read()
        except OSError:
            current = ""
        if current != text:
            print("manifest.json is stale: run  python3 tools/build_manifest.py  and commit it.")
            return 1
        full = installed(manifest)
        print(f"manifest.json is up to date (v{full['version']}, {len(full['files'])} files).")
        return 0
    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write(text)
    full = installed(manifest)
    print(f"Wrote manifest.json: v{full['version']}, {len(full['files'])} files in Judge/, "
          f"{len(full['managed'])} managed and {len(full['create_only'])} create-only package files, "
          f"{len(full['bundles'])} bundles, moves from {len(full['moves'])} older releases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
