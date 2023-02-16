SHELL := /bin/bash

VERSION=0.0.1

install-system-dependencies:
	@sudo apt install python3.10-venv

developer-setup: setup-python-venv

setup-python-venv:
	@python3 -m venv .virtualenv; \
	source .virtualenv/bin/activate; \
	pip3 install -r requirements.txt; \
	pip3 install -r requirements-dev.txt; \
	pip3 install -e .

run-tests:
	@python3 -m pytest flask_params/

run-demo:
	@python3 -m demo.app

format:
	@python3 -m black ./flask_params

build:
	@python3 -m build

generate-html-docs:
	@sphinx-build -b html ./docs ./docs/_build
