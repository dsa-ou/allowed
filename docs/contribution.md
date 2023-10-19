## Contributing

_The following is out of date:_

If you want to contribute code to address an open issue:

1. Install and activate the `dsa-ou` [virtual environment](https://github.com/dsa-ou/virtual-env).
2. Fork this repository to your GitHub account and then clone it to your disk.
3. Run `python allowed.py sample.py > sample.txt`
   (optionally with option `-m` if you installed `pytype`).
4. Run `python allowed.py path/to/M269/book/python > book.txt`.
5. Choose an [open issue](https://github.com/dsa-ou/allowed/issues) and assign it to yourself.
6. Create a branch in your repository to work on the issue.
7. Run the `black` and `isort` formatter on your modified `allowed.py` before testing it.
8. Check that your changes didn't modify `allowed`'s behaviour:
   1. run `python allowed.py sample.py | diff -w - sample.txt`
   2. run `python allowed.py path/to/M269/book/python | diff -w - book.txt`
   3. neither run should show any differences
9.  Do any tests specific to the issue you're addressing.
10. Make a pull request.

⇦ [Configuration](configuration.md)