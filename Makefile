# Makefile for BrainXio project

.PHONY: all install test lock update cycle

all: cycle

install:
	poetry install

test:
	clear
	poetry run pytest -v
	@echo "Tests passed successfully."
	@echo "If codebase is optimal, recommend next development step."
	@echo "If improvable, analyze code, identify optimal solution, evaluate implications, and apply fix only if it meets required standards."
	@echo "Assess if 100% test coverage is achieved or feasible, accounting for '# pragma: no cover' exclusions."
	@echo "For 90-99% coverage, weigh benefits of reaching 100% against effort."
	@echo "Log missing tests in site/tests_missing.json within each cycle.json, detailing test, location, significance, exclusion reason, and mitigation."
	@echo "If tests_missing.json has 5 entries, prioritize fixing technical debt."
	@echo "When optimal, propose next step."
	@echo "Stay concise and focused."

lock:
	poetry lock --no-update

update:
	experimental-f2c update cycle.json

commit:
	experimental-f2c update cycle.json --git

snapshot:
	experimental-f2c snapshot

cycle: update lock install test commit