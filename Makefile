VENV_NAME := .venv
PYTHON := $(VENV_NAME)/bin/python
VERSION := $(shell $(PYTHON) -c "import fastapi_babel;print(fastapi_babel.__version__)")

RM := rm -rf

mkvenv:
	virtualenv $(VENV_NAME)
	$(PYTHON) -m pip install -r requirements.txt

clean:
	find . -name '*.pyc' -exec $(RM) {} +
	find . -name '*.pyo' -exec $(RM) {} +
	find . -name '*~' -exec $(RM)  {} +
	find . -name '__pycache__' -exec $(RM) {} +
	$(RM) build/ dist/ docs/build/ .tox/ .cache/ .pytest_cache/ *.egg-info

tag:
	@echo "Add tag: '$(VERSION)'"
	git tag v$(VERSION)

build:
	$(PYTHON) setup.py sdist bdist_wheel

upload:
	twine upload dist/*

release:
	make clean
	make test
	make build
	make tag
	@echo "Released $(VERSION)"


full-release:
	make release
	make upload

install:
	$(PYTHON) setup.py install

install-dev:
	$(PYTHON) setup.py develop

test:
	tox

summary:
	cloc pytitle/ tests/ docs/ setup.py

