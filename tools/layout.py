#!/usr/bin/env python3
"""
Names of the student package (v4.0: one folder per problem). The one place the layout is written down for the
build tools; Judge/judge.py and Judge/updater.py hold the same rules for the students' side (the regression test
compares them).

  00_Mixed/                              all Mixed sets, first in the package (README.txt: neutral, no topic)
    M01/                                 a Mixed set (sets.json "dir": M01; package folder 00_Mixed/M01)
  04_Binary_Search/                      topic folder (sets.json "dir")
    Problems_04_Binary_Search.pdf        the whole topic
    Makefile, judge.bat                  the whole topic, or one problem: make 5 / judge 5
    05/                                  problem 5: two digits in a topic (01 ... 20), one digit in a Mixed set (1 ... 6)
      04-05.cpp                          the student's code (create-only: empty at first, never replaced)
      05_Cutting_Ropes.pdf               the statement of this problem alone (managed: replaced when it changes)

A problem folder holds exactly these two files (no Makefile, no judge.bat).
A folder name never changes when a problem is replaced or re-titled; the PDF's name follows the English title.
"""
import re

TITLE_MAX = 60          # characters of the title kept in a PDF's file name
MIXED_ROOT = "00_Mixed"  # the folder that holds every Mixed set (00_ sorts it first); it names no topic
MIXED_README = MIXED_ROOT + "/README.txt"     # short and neutral (written by C2_PRACTICE_SRC build.py all)


def mixed(s):
    """s: an entry of sets.json. A Mixed set has "group": "Mixed" and folder M01 ... (no topic shown)."""
    return s.get("group") == "Mixed"


def folder(s):
    """Package path of a topic / Mixed-set folder: 04_Binary_Search, 00_Mixed/M01 (sets.json "dir" is M01)."""
    return f"{MIXED_ROOT}/{s['dir']}" if mixed(s) else s["dir"]


def topic_pdf_path(s):
    """Package path of the whole topic's / set's PDF: 04_Binary_Search/Problems_04_Binary_Search.pdf,
    00_Mixed/M01/Problems_M01.pdf."""
    return f"{folder(s)}/Problems_{s['dir']}.pdf"


def prefix(s):
    """First part of a code file's name: "04" for topic 4, "M01" for a Mixed set."""
    return s["dir"] if mixed(s) else f"{s['set']:02d}"


def slot(s, i):
    """Folder of problem i (1-based) inside its topic folder."""
    return str(i) if mixed(s) else f"{i:02d}"


def code_name(s, i):
    return f"{prefix(s)}-{slot(s, i)}.cpp"


def code_path(s, i):
    """Package path of problem i's code file: 04_Binary_Search/05/04-05.cpp, 00_Mixed/M01/3/M01-3.cpp."""
    return f"{folder(s)}/{slot(s, i)}/{code_name(s, i)}"


def title_slug(title):
    """An English title as part of a file name: ASCII letters, digits and "_" only; spaces become "_", every
    other character is dropped; at most TITLE_MAX characters."""
    out = re.sub(r"[^A-Za-z0-9_]", "", re.sub(r"\s+", "_", title.strip()))
    out = re.sub(r"_+", "_", out).strip("_")[:TITLE_MAX].rstrip("_")
    if not out:
        raise ValueError(f"title gives an empty file name: {title!r}")
    return out


def pdf_name(s, i, title):
    """File name of problem i's own PDF: 05_Cutting_Ropes.pdf."""
    return f"{slot(s, i)}_{title_slug(title)}.pdf"


def pdf_path(s, i, title):
    return f"{folder(s)}/{slot(s, i)}/{pdf_name(s, i, title)}"


def old_name(i, title):
    """Where the written file of a replaced problem goes inside <topic>/old/: 5_CuttingRopes.cpp."""
    words = "".join(c if c.isalnum() and c.isascii() else " " for c in title).split()
    return f"{i}_{''.join(w[:1].upper() + w[1:] for w in words)}.cpp"


def dir_folder(d):
    """Package folder of a sets.json "dir" (also the first part of a problems.json "dir"): M01 -> 00_Mixed/M01."""
    return f"{MIXED_ROOT}/{d}" if re.match(r"^M[0-9]{2}$", d) else d


def entry_set(pid, e):
    """The sets.json-like view of a problems.json entry (id = 100 * set + n, "dir": "<topic folder>/<n>", a Mixed
    set's "M01/<n>": the test data stays in problems/batch/M01/<n>; only the package folder is 00_Mixed/M01)."""
    d = e["dir"].split("/")[0]
    return {"set": int(pid) // 100, "dir": d, "group": "Mixed" if re.match(r"^M[0-9]{2}$", d) else ""}


def entry_code_path(pid, e):
    """Package path of the code file of a problems.json entry (also of an earlier release's problems.json)."""
    return code_path(entry_set(pid, e), int(e["dir"].split("/")[1]))
