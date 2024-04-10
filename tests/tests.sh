#!/bin/bash

# this script is meant to be executed from the project's root directory
cmd='python allowed/allowed.py'
if [ $# -eq 0 ]; then
    echo "Usage: ./tests.sh [run|create]"
elif [ $1 = "run" ]; then
    # test that there are no warnings if no file is processed
    echo "foobar -fm"; echo "---"
    $cmd foobar -fm | diff -w - tests/foobar-fm.txt
    # -h trumps other flags
    echo; echo "foobar -hfm"; echo "---"
    $cmd foobar -hfm | diff -w - tests/foobar-hfm.txt
    # check with invalid notebook (not JSON)
    echo; echo "invalid.ipynb"; echo "---"
    $cmd tests/invalid.ipynb | diff -w - tests/invalid-nb.txt
    # check with configuration file that isn't JSON
    echo; echo "-c sample.py"; echo "---"
    $cmd -c tests/sample.py foobar | diff -w - tests/sample-c.txt
    # check with incomplete configuration file
    echo; echo "-c invalid.json"; echo "---"
    $cmd -c tests/invalid.json foobar | diff -w - tests/invalid-c.txt
    # check with invalid Python code
    echo; echo "-v -u 3 invalid.py"; echo "---"
    $cmd -v -u 3 tests/invalid.py | diff -w - tests/invalid-py.txt
    # check the example code and notebook
    echo; echo "sample.py"; echo "---"
    $cmd tests/sample.py | diff -w - tests/sample-py.txt
    echo ; echo "sample.py -m"; echo "---"
    $cmd tests/sample.py -m | diff -w - tests/sample-py-m.txt
    echo; echo "sample.ipynb"; echo "---"
    $cmd tests/sample.ipynb | diff -w - tests/sample-nb.txt
    echo; echo "sample.ipynb -m"; echo "---"
    $cmd tests/sample.ipynb -m | diff -w - tests/sample-nb-m.txt
    echo; echo "-vf sample.ipynb allowed/"; echo "---"
    $cmd -vf tests/sample.ipynb allowed | diff -w - tests/folder-first.txt
elif [ $1 = "create" ]; then
    $cmd foobar -fm > tests/foobar-fm.txt
    $cmd foobar -hfm > tests/foobar-hfm.txt
    $cmd tests/invalid.ipynb > tests/invalid-nb.txt
    $cmd -c tests/sample.py foobar > tests/sample-c.txt
    $cmd -c tests/invalid.json foobar > tests/invalid-c.txt
    $cmd -v -u 3 tests/invalid.py > tests/invalid-py.txt
    $cmd tests/sample.py > tests/sample-py.txt
    $cmd tests/sample.py -m > tests/sample-py-m.txt
    $cmd tests/sample.ipynb > tests/sample-nb.txt
    $cmd tests/sample.ipynb -m > tests/sample-nb-m.txt
    $cmd -vf tests/sample.ipynb allowed > tests/folder-first.txt
else
    echo "Usage: ./tests.sh [run|create]"
fi