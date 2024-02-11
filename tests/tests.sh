#!/bin/bash

# this script is meant to be executed from the project's root directory
cmd='python allowed/allowed.py'
if [ $# -eq 0 ]; then
    echo "Usage: ./tests.sh [run|create]"
elif [ $1 = "run" ]; then
    echo "sample.py"; echo "---"
    $cmd tests/sample.py | diff -w - tests/sample-py.txt
    echo ; echo "sample.py -m"; echo "---"
    $cmd tests/sample.py -m | diff -w - tests/sample-py-m.txt
    echo; echo "sample.ipynb"; echo "---"
    $cmd tests/sample.ipynb | diff -w - tests/sample-nb.txt
    echo; echo "sample.ipynb -m"; echo "---"
    $cmd tests/sample.ipynb -m | diff -w - tests/sample-nb-m.txt
    echo; echo "-f ."; echo "---"
    $cmd -f . | diff -w - tests/folder-first.txt
elif [ $1 = "create" ]; then
    $cmd tests/sample.py > tests/sample-py.txt
    $cmd tests/sample.py -m > tests/sample-py-m.txt
    $cmd tests/sample.ipynb > tests/sample-nb.txt
    $cmd tests/sample.ipynb -m > tests/sample-nb-m.txt
    $cmd -f . > tests/folder-first.txt
else
    echo "Usage: ./tests.sh [run|create]"
fi