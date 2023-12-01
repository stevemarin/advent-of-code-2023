
all: black ruff isort

.PHONY: ruff black

black:
	black .

ruff:
	ruff . --fix

isort:
	isort ./advent-of-code-2023

day01:
	python ./advent-of-code-2023/day01.py