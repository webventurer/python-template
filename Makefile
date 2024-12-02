.PHONY: install install-local uninstall-local compile sync update default lint format types test

install:
	pip install --upgrade pip
	@pip install \
	-r requirements.txt \
	-r requirements-dev.txt

install-local:
	pip install --root-user-action=ignore --use-pep517 thirdparty/app

uninstall-local:
	rm -rf thirdparty/app/*.egg-info
	pip uninstall --root-user-action=ignore -y app

compile:
	@rm -f requirements*.txt
	@pip-compile requirements.in
	@pip-compile requirements-dev.in

sync:
	@pip-sync requirements*.txt

update:
	pip install --upgrade pip
	make compile && make sync

check: lint format types

lint:
	ruff check --output-format=grouped .

format:
	ruff format --check .

types:
	pyright .

test:
	sh -c 'pytest tests || ([ $$? = 5 ] && exit 0 || exit $$?)'
