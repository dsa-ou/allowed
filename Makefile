install:
	poetry install

update:
	poetry update

fmt:
	poetry run autoflake \
		--in-place \
		--remove-all-unused-imports \
		-r \
		allowed.py
	poetry run isort --profile black allowed.py
	poetry run black allowed.py

lint:
	poetry run mypy --ignore-missing-imports allowed.py
	poetry run flake8 allowed.py
	poetry run bandit -q -r allowed.py

test:
	poetry run ./tests.sh run