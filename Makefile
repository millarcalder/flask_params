SHELL := /bin/bash

VERSION=0.0.1

developer-setup: setup-python-venv

setup-python-venv:
	@python3 -m venv .virtualenv; \
	source .virtualenv/bin/activate; \
	pip3 install -r requirements.txt; \
	pip3 install -r requirements-dev.txt; \
	pip3 install -e .

run-tests:
	@source .virtualenv/bin/activate; \
	python3 -m pytest flask_parameters/

run-demo:
	@source .virtualenv/bin/activate; \
	python3 -m demo.app

format:
	@source .virtualenv/bin/activate; \
	python3 -m black ./flask_parameters

build:
	@source .virtualenv/bin/activate; \
	python3 -m build

generate-html-docs:
	@source .virtualenv/bin/activate; \
	sphinx-build -b html ./docs ./docs/_build
