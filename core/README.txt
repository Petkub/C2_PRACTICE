POSN Camp 2 - Topic Practice Judge
==================================
Requirements: Python 3.7+ and g++ in PATH (Linux / macOS / Windows; on Windows type python, not python3).
macOS: g++ is Apple clang without <bits/stdc++.h>; the judge adds include/ (a fallback header) automatically.

Inside a topic folder (e.g. Topic_3):
  python3 ../Judge/judge.py               judge the whole topic (1.cpp ... 20.cpp)
  python3 ../Judge/judge.py 5.cpp         judge problem 5 of this topic
  python3 ../Judge/judge.py 5             the same (just the problem number)

From the Judge folder (or use ../Judge/judge.py from a topic folder):
  python3 judge.py --list                 list all 11 topics and their problems
  python3 judge.py --set 3                show topic 3
  python3 judge.py --set 3 FOLDER         judge a whole topic (files 1.cpp ... 20.cpp in FOLDER)
  python3 judge.py my.cpp 3-5             judge one solution: topic 3, problem 5

Options: --tl SECONDS  --ml MB (default 256)  --diff N  --stop  --ascii  --no-color
Test data: problems/batch/Topic_K/P/*.in|out (the first 5 or 6 tests are the samples shown in the statement).
Windows: VS Code's Ctrl+Shift+B runs judge.cmd (uses the py launcher if installed, else python).
Updates: the judge updates itself from GitHub when online (checked at most once every 10 minutes; your .cpp files
are never touched). Force a check: python3 ../Judge/judge.py --update   (version shown in the header box)
