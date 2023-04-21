if [ $# -eq 0 ]; then
    echo "Usage: ./tests.sh [run|create]"
elif [ $1 = "run" ]; then
    echo "sample.py\n---"
    python allowed.py sample.py | diff -w - tests/sample-py.txt
    echo "\nsample.py -m\n---"
    python allowed.py sample.py -m | diff -w - tests/sample-py-m.txt
    echo "\nsample.ipynb\n---"
    python allowed.py sample.ipynb | diff -w - tests/sample-nb.txt
    echo "\nsample.ipynb -m\n---"
    python allowed.py sample.ipynb -m | diff -w - tests/sample-nb-m.txt
elif [ $1 = "create" ]; then
    python allowed.py sample.py > tests/sample-py.txt
    python allowed.py sample.py -m > tests/sample-py-m.txt
    python allowed.py sample.ipynb > tests/sample-nb.txt
    python allowed.py sample.ipynb -m > tests/sample-nb-m.txt
else
    echo "Usage: ./tests.sh [run|create]"
fi