#!/bin/bash

# this script is meant to be executed from the project's root directory
folder="$HOME/GitHub/M269-NE/book-24j"
cmd="python allowed/allowed.py -f --file-unit (\d\d) -c m269-24j"

if [ "$1" = "run" ]; then
    echo "NOTEBOOKS"; echo
    $cmd $folder/notebooks | diff -w - tests/m269-nb.txt
    echo; echo "NOTEBOOKS -M"; echo
    $cmd -m $folder/notebooks | diff -w - tests/m269-nb-m.txt
    echo; echo "PYTHON"; echo
    $cmd $folder/python | diff -w - tests/m269-py.txt
    echo; echo "PYTHON -M"; echo
    $cmd -m $folder/python | diff -w - tests/m269-py-m.txt
elif [ "$1" = "create" ]; then
    $cmd $folder/notebooks > tests/m269-nb.txt
    $cmd -m $folder/notebooks > tests/m269-nb-m.txt
    $cmd $folder/python > tests/m269-py.txt
    $cmd -m $folder/python > tests/m269-py-m.txt
else
    echo "Usage: $0 [run|create]"
fi