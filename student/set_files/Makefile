# Linux / macOS, inside this Topic folder:
#   make      judge the whole set (1.cpp ... 20.cpp)
#   make 5    judge problem 5 only
PYTHON ?= python3
JUDGE  := $(PYTHON) ../Judge/judge.py

all:
	@$(JUDGE)

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20:
	@$(JUDGE) $@.cpp

.PHONY: all 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
