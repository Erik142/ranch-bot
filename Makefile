##
# Ranch bot
#
# @file
# @version 0.1

.PHONY: test
test:
	PYTHONPATH=./src poetry run pytest ./tests/ --cov=ranchbot --cov-branch --cov-report term-missing

.PHONY: deps
deps:
	python3 -m poetry install
	python3 -m poetry run pip install -e ./src/dpytest

.PHONY: poetry
poetry:
	python3 -m pip install --user poetry

.PHONY: environment
environment: poetry deps

# end
