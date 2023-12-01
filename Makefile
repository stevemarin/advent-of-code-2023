
.PHONY: ruff black isort

all: black ruff isort

black:
	black .

ruff:
	ruff . --fix

isort:
	isort ./advent-of-code-2023

day01:
	python ./advent-of-code-2023/day01.py