# Makefile for BrainXio project

.PHONY: all install test lock update cycle

all: cycle

install:
	poetry install

test:
	poetry run pytest -v

lock:
	poetry lock --no-update

update:
	experimental-f2c update cycle.json --git

cycle: update lock install test
	clear
