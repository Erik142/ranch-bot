##
# Ranch bot
#
# @file
# @version 0.1

.PHONY: test
test:
	PYTHONPATH=./src/ranchbot pytest --cov --cov-branch --cov-report term-missing

# end
