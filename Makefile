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

run_tests:
	-@poetry run tests/tests.sh run
	@echo; echo "sample.py (no ipython or pytype)"; echo "---"
	-@python3.10 allowed/allowed.py tests/sample.py | diff -w - tests/sample-py.txt | diff -w - tests/sample-py-none.txt
	@echo; echo "sample.ipynb (no ipython or pytype)"; echo "---"
	-@python3.10 allowed/allowed.py tests/sample.ipynb | diff -w - tests/sample-nb.txt | diff -w - tests/sample-nb-none.txt

create_tests:
	poetry run tests/tests.sh create
	-python3.10 allowed/allowed.py tests/sample.py | diff -w - tests/sample-py.txt > tests/sample-py-none.txt
	-python3.10 allowed/allowed.py tests/sample.ipynb | diff -w - tests/sample-nb.txt > tests/sample-nb-none.txt
