clean:
	rm -rf .venv day-summary *.checkpoint .pytest_cache .coverage

init: clean
	pip install poetry
	poetry install
	pre-commit install

test:
	python3 -m pytest

ci-setup:
	pip install poetry
	poetry install

ci-test:
	poetry run python -m pytest