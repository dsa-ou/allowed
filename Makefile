install:
	poetry install --extras "all"

update:
	poetry update

format:
	poetry run ruff format allowed/allowed.py

lint:
	poetry run bandit allowed/allowed.py
	poetry run mypy --ignore-missing-imports allowed/allowed.py
	poetry run ruff check allowed/allowed.py

run_tests:
	poetry run tests/tests.sh run

create_tests:
	poetry run tests/tests.sh create
