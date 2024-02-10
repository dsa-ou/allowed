#!/bin/bash

cmd='python allowed/allowed.py'
if [ $# -eq 0 ]; then
    echo "Usage: ./tests.sh [run|create]"
elif [ $1 = "run" ]; then
    echo "sample.py"; echo "---"
    $cmd sample.py | diff -w - tests/sample-py.txt
    echo ; echo "sample.py -m"; echo "---"
    $cmd sample.py -m | diff -w - tests/sample-py-m.txt
    echo; echo "sample.ipynb"; echo "---"
    $cmd sample.ipynb | diff -w - tests/sample-nb.txt
    echo; echo "sample.ipynb -m"; echo "---"
    $cmd sample.ipynb -m | diff -w - tests/sample-nb-m.txt
elif [ $1 = "create" ]; then
    $cmd sample.py > tests/sample-py.txt
    $cmd sample.py -m > tests/sample-py-m.txt
    $cmd sample.ipynb > tests/sample-nb.txt
    $cmd sample.ipynb -m > tests/sample-nb-m.txt
else
    echo "Usage: ./tests.sh [run|create]"
fi