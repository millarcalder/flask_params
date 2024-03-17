SHELL := /bin/bash

PY_VERSION=3.12
PYTHON=.virtualenv-$(PY_VERSION)/bin/python
PIP=.virtualenv-$(PY_VERSION)/bin/pip

setup-python-venv:
	pyenv install $(PY_VERSION) --skip-existing
	pyenv global $(PY_VERSION)
	python -m venv .virtualenv-$(PY_VERSION)

developer-setup: setup-python-venv
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

run-tests:
	$(PYTHON) -m pytest flask_parameters

run-demo:
	$(PYTHON) -m demo.app

format:
	$(PYTHON) -m black ./flask_parameters

build:
	$(PYTHON) -m build

generate-html-docs:
	$(PYTHON) -m sphinx-build -b html ./docs ./docs/_build

release-testing: build
	$(PYTHON) -m twine upload --repository testpypi dist/*

release-production: build
	$(PYTHON) -m twine upload dist/*
