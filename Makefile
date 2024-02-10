install:
	poetry install

update:
	poetry update

format:
	poetry run ruff format allowed/allowed.py

lint:
	poetry run bandit allowed/allowed.py
	poetry run mypy --ignore-missing-imports allowed/allowed.py
	poetry run ruff check allowed/allowed.py

test:
	poetry run ./tests.sh run