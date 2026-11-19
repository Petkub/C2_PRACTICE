POSN Camp 2 - Topic Practice Judge
==================================
Requirements: Python 3.7+ and g++ in PATH (Linux / macOS / Windows; on Windows type python, not python3).
macOS: g++ is Apple clang without <bits/stdc++.h>; the judge adds include/ (a fallback header) automatically.

One folder per problem: 04_Binary_Search/05/04-05.cpp (your code) and 05_<Title>.pdf (the statement); a Mixed set:
M01/3/M01-3.cpp. Do not rename the folders or the .cpp files: the judge finds the problem from them.

Inside a problem folder (e.g. 04_Binary_Search/05):
  python3 ../../Judge/judge.py            judge this problem                 (also: make, or judge on Windows)
Inside a topic folder (e.g. 04_Binary_Search):
  python3 ../Judge/judge.py               judge the whole topic              (also: make, judge)
  python3 ../Judge/judge.py 5             judge problem 5 (05 works too)     (also: make 5, judge 5)
Anywhere:
  python3 <path>/Judge/judge.py FILE.cpp  the problem comes from the file's name (04-05.cpp) or its folder (.../05/)
  python3 <path>/Judge/judge.py my.cpp 4-5    judge any file as topic 4, problem 5 (Mixed sets: M01-3)

From the Judge folder (or use ../Judge/judge.py from a topic folder):
  python3 judge.py --list                 list all topics and problems, with their folders and code file names
  python3 judge.py --set 3                show topic 3
  python3 judge.py --set 3 FOLDER         judge a whole topic (FOLDER laid out like a topic folder)

Options: --tl SECONDS  --ml MB (default 256)  --diff N  --stop  --ascii  --no-color
Test data: problems/batch/<topic folder>/P/*.in|out (the first 5 or 6 tests are the samples shown in the statement).
Windows: VS Code's Ctrl+Shift+B runs judge.cmd (uses the py launcher if installed, else python).
Programs are compiled in a temporary folder, never in the problem folder.
Updates: the judge updates itself from GitHub when online (checked at most once every 10 minutes; your .cpp files
are never changed or deleted). When an update moves a problem, your written file moves with it; when it replaces a
problem, your file goes to <topic>/old/<n>_<OldTitle>.cpp; the judge prints every move.
Force a check: python3 ../Judge/judge.py --update   (version shown in the header box)
