
.PHONY: ruff black isort all_days day

default: black ruff isort

black:
	black .

ruff:
	ruff . --fix

isort:
	isort ./aoc2023

all_days:
	find ./aoc2023 -name "day*.py" -exec python {} \;
	
day:
	python ./aoc2023/day${day}.py

