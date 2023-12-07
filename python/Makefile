
.PHONY: ruff black isort

default: black ruff isort

black:
	black .

ruff:
	ruff . --fix

isort:
	isort ./aoc2023

day01:
	python ./aoc2023/day01.py

day02:
	python ./aoc2023/day02.py

day03:
	python ./aoc2023/day03.py

all:
	find ./aoc2023 -name "day*.py" -exec python {} \;