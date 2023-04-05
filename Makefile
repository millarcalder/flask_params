SHELL := /bin/bash

VERSION=0.0.2

developer-setup: setup-python-venv

setup-python-venv:
	@python3 -m venv .virtualenv; \
	source .virtualenv/bin/activate; \
	pip install -r requirements.txt; \
	pip install -r requirements-dev.txt; \
	pip install -e .

run-tests:
	@source .virtualenv/bin/activate; \
	python -m pytest flask_parameters/

run-demo:
	@source .virtualenv/bin/activate; \
	python -m demo.app

format:
	@source .virtualenv/bin/activate; \
	python -m black ./flask_parameters

build:
	@source .virtualenv/bin/activate; \
	python -m build

generate-html-docs:
	@source .virtualenv/bin/activate; \
	sphinx-build -b html ./docs ./docs/_build

release-testing: build
	@source .virtualenv/bin/activate; \
	python -m twine upload --repository testpypi dist/*

release-production: build
	@source .virtualenv/bin/activate; \
	python -m twine upload dist/*
