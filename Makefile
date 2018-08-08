.PHONY: clean docs help test
.DEFAULT_GOAL := help

APP=app.py
SETTINGS_DEV=settings.yml
SETTINGS_TEST=settings_test.yml
ENV_DEV=development
ENV_TEST=testing

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

install: ## install required dependencies
	pip install -r requirements.txt

install-dev: install ## install required dependencies with test-requirements
	pip install -r requirements.txt
	pip install -r test-requirements.txt

clean: clean-build clean-pyc clean-cache clean-session ## clean all artifacts and cache

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

clean-session: ## remove flask_session files
	rm -rf flask_session/

lint: ## check code style and formatting with flake8
	flake8

test: ## run tests
	SETTINGS_PATH=$(SETTINGS_TEST) FLASK_ENV=$(ENV_TEST) FLASK_APP=$(APP) TESTING=1 pytest

coverage: clean-cache ## create code coverage report
	coverage erase
	SETTINGS_PATH=$(SETTINGS_TEST) FLASK_ENV=$(ENV_TEST) FLASK_APP=$(APP) TESTING=1 coverage run -m pytest
	coverage report -m
	coverage html

docs: ## generate Sphinx HTML documentation
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

serve: ## run Flask server in development mode
	SETTINGS_PATH=$(SETTINGS_DEV) FLASK_ENV=$(ENV_DEV) FLASK_APP=$(APP) flask run --port 3000

dev-run: ## run vagrant box with Zuul and Gerrit
	vagrant up

dev-stop: ## stop vagrant box
	vagrant halt

dev-reload: ## remove vagrant box and run again
	vagrant destroy -f
	vagrant up
