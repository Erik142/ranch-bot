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

.PHONY: poetry
poetry:
	python3 -m pip install --user poetry

.PHONY: environment
environment: poetry deps

.PHONY: devversion
devversion:
	./bump_version.sh dev

.PHONY: patchversion
patchversion:
	./bump_version.sh patch

staging:
	./build_publish_staging.sh
# end
