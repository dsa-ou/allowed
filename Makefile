install:
	poetry install

update:
	poetry update

format:
	poetry run ruff format allowed.py

lint:
	poetry run bandit allowed.py
	poetry run mypy --ignore-missing-imports allowed.py
	poetry run ruff check allowed.py

test:
	poetry run ./tests.sh run