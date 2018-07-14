.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

install: ## install dependencies
	pip install -r requirements.txt

install-dev: install ## install dev dependencies
	pip install -r requirements.txt
	pip install -r test-requirements.txt

clean: clean-build clean-pyc clean-cache

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-cache: ## remove .cache and .pytest_cache
	rm -rf .cache
	rm -rf .pytest_cache

lint: ## check style with flake8
	flake8

test: ## run tests
	pytest tests/

coverage: ## check code coverage quickly with the default Python
	coverage erase
	coverage run -m pytest
	coverage report -m
	coverage html

docs: ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

serve: ## run flask server in development mode
	SETTINGS_PATH=settings.conf FLASK_ENV=development FLASK_APP=app.py flask run --port 3000