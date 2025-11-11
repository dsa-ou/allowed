install:
	poetry install

update:
	poetry update

format:
	poetry run ruff format allowed/

lint:
	poetry run bandit allowed/
	poetry run mypy --ignore-missing-imports allowed/
	poetry run ruff check allowed/

run_tests:
	@echo "Tests in poetry environment, WITH ipython installed"
	-@poetry run tests/tests.sh run
	@echo "Tests in global environment, WITHOUT ipython installed"
	@echo; echo "sample.py (3.10 no ipython)"; echo "---"
	-@python3.10 -m allowed.allowed tests/sample.py | diff -w - tests/sample-py.txt | diff -w - tests/sample-py-none-10.txt
	@echo; echo "sample.ipynb (3.10 no ipython)"; echo "---"
	-@python3.10 -m allowed.allowed tests/sample.ipynb | diff -w - tests/sample-nb.txt | diff -w - tests/sample-nb-none-10.txt
	@echo; echo "sample.py (3.11 no ipython)"; echo "---"
	-@python3.11 -m allowed.allowed tests/sample.py | diff -w - tests/sample-py.txt | diff -w - tests/sample-py-none-11.txt
	@echo; echo "sample.ipynb (3.11 no ipython)"; echo "---"
	-@python3.11 -m allowed.allowed tests/sample.ipynb | diff -w - tests/sample-nb.txt | diff -w - tests/sample-nb-none-11.txt
	@echo; echo "sample.py (3.12 no ipython)"; echo "---"
	-@python3.12 -m allowed.allowed tests/sample.py | diff -w - tests/sample-py.txt | diff -w - tests/sample-py-none-12.txt
	@echo; echo "sample.ipynb (3.12 no ipython)"; echo "---"
	-@python3.12 -m allowed.allowed tests/sample.ipynb | diff -w - tests/sample-nb.txt | diff -w - tests/sample-nb-none-12.txt

create_tests:
	poetry run tests/tests.sh create
	-python3.10 -m allowed.allowed tests/sample.py | diff -w - tests/sample-py.txt > tests/sample-py-none-10.txt
	-python3.10 -m allowed.allowed tests/sample.ipynb | diff -w - tests/sample-nb.txt > tests/sample-nb-none-10.txt
	-python3.11 -m allowed.allowed tests/sample.py | diff -w - tests/sample-py.txt > tests/sample-py-none-11.txt
	-python3.11 -m allowed.allowed tests/sample.ipynb | diff -w - tests/sample-nb.txt > tests/sample-nb-none-11.txt
	-python3.12 -m allowed.allowed tests/sample.py | diff -w - tests/sample-py.txt > tests/sample-py-none-12.txt
	-python3.12 -m allowed.allowed tests/sample.ipynb | diff -w - tests/sample-nb.txt > tests/sample-nb-none-12.txt

run_m269_tests:
	-@poetry run tests/m269_tests.sh run

create_m269_tests:
	-@poetry run tests/m269_tests.sh create
