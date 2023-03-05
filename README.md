This program checks if your Python code only uses certain constructs,
which you can configure.

Like all static analysis tools, `allowed` isn't perfect and will never be.
There will be false positives (code reported to be a violation, but isn't)
and false negatives (code that uses disallowed constructs but isn't reported).

This program requires Python 3.10 or later and that your code compiles.

## Installation

Click on the green 'Code' button and select the 'download zip' option.
Unzip the downloaded file if your web browser hasn't done so.
This creates an `allowed-main` folder within your downloads folder.

The only files you need within that folder are `allowed.py` and `m269.json`,
which you may move to anywhere, e.g. to the folder with the code you want to check.
The files `sample.py` and `sample.ipynb` are example files with code to check.

## Usage

Open a terminal. Change to the folder where you have put `allowed.py`.
You can check code files and Jupyter notebook files by typing
```bash
python allowed.py path/to/file.py path/to/notebook.ipynb ...
```
This will list all disallowed constructs in the given files.
If the file has a syntax error, it can't be parsed and hence it's not checked.

For example, you can check the sample file and `allowed`'s code with:
```bash
python allowed.py sample.py allowed.py
```
or with
```bash
python allowed.py sample.ipynb allowed.py
```
If you expect a long list of disallowed constructs, it may be better to
check one file at a time and store the report in a text file, e.g.
```bash
python allowed.py allowed.py > disallowed.txt
```
To check all `.py` and `.ipynb` files in a folder and its subfolders, type:
```bash
python allowed.py path/to/folder
```

### Extra checks

To check if the attribute access `variable.method` is allowed,
the program needs to know the type of `variable`. For that purpose, it uses
the `pytype` type checker, which only works with Python versions 3.7 to 3.10.

For installation instructions, see [its website](https://google.github.io/pytype).
On Windows, you must first install [WSL](https://learn.microsoft.com/en-us/windows/wsl/).

By default, `allowed` skips method call checks because they slow down the process.
You can enable these checks with option `-m` or `--methods`, for example
```bash
python allowed.py -m sample.py
```
will print one further violation: method `list.count()` is used in line 52.

The methods call option can appear anywhere after `allowed.py` and in either form.
For example, the following two commands are equivalent:
```bash
python allowed.py -m file1.py file2.py
python allowed.py file1.py --methods file2.py
```

### Organising by units

`allowed` assumes that your course or textbook is organised in 'units'
(lessons, weeks, chapters, whatever you want) and that they are cumulative:
a Python construct introduced in a unit can be used in any subsequent unit.

By default, `allowed` uses all units, i.e. checks against all the material introduced.
Option `-u N` or `--unit N` will check the file(s) against
the Python constructs introduced up to unit `N` (inclusive).
For example, checking a submission to an assessment that covers units 1 to 5
can be done with:
```bash
python allowed.py -u 5 submission.py
```
To see the weekly difference in the allowed constructs, type for example:
```bash
python allowed.py -u 2 sample.py
python allowed.py -u 4 sample.py
```
The second command will report fewer violations because units 3 and 4 of
the default configuration introduce Booleans, lists, strings and tuples.

If the file name starts with the unit number and there's no unit option,
the file is checked against that unit. For example,
```bash
python allowed.py 05_submission.py
```
also checks the submission against the constructs introduced in units 1–5.
However, if the file name starts with a number that isn't the intended unit,
you must provide it,
e.g. if the file name starts with the number of the assignment, not of the unit:
```bash
python allowed.py 01_submission.py -u 5
```
Like the methods call option, the unit option can appear
anywhere after `allowed.py` and in either form.

### Checking notebooks

While the program can check Jupyter notebooks, it has two limitations.
First, if any code cell has a syntax error or non-Python code, like
`%run`, `%timeit` and other IPython commands, then the whole notebook isn't checked.
Second, the reported line numbers are relative to the whole notebook.
So, if line 45 has a disallowed construct, to fix the problem
it's easier to search for the reported construct in the notebook than
to count 45 code lines from the start of the notebook.

A more robust way to check notebooks is to first install
[nbqa](https://http://nbqa.readthedocs.io) and then type one of the following.
```bash
nbqa allowed path/to/notebook1.ipynb path/to/notebook2.ipynb ...
nbqa allowed path/to/folder
```
The latter checks all notebooks (but no `.py` files!)
in that folder and its subfolders.

Using `nbqa` overcomes the two limitations mentioned.
First, an error in one cell doesn't prevent `allowed` from checking the other cells.
Thus, with `nbqa` you will find more disallowed constructs than without,
but see [this issue](https://github.com/dsa-ou/allowed/issues/15).

Second, `nbqa` reports the cell and line which uses a disallowed construct.
For example, `path/to/notebook1.ipynb:cell_13:5: ...` means that the problem
is in line 5 of the 13th code cell.

You can use options with `nbqa`, but they must be given at the end.
For example, if you're an M269 student or tutor, you can check the
second assignment (on chapters 1–20) before you submit or mark it with
```bash
nbqa allowed path/to/TMA02.ipynb -u 20
```

## Configuration

The program is already configured for our course,
[M269](https://www.open.ac.uk/courses/modules/m269),
but you can create your own configuration by creating a JSON file of the form
```json
{
   "FILE_UNIT": "...",
   "LANGUAGE": { ... },
   "IMPORTS": { ... },
   "METHODS": { ... }
}
```
File [`m269.json`](m269.json) is the default configuration.
You can copy, rename and edit it to configure `allowed` for your course.

You can have multiple configuration files and select one with
option `-c` or `--config`, e.g.
```bash
python allowed.py assignment.py -c cs101.json
```

### FILE_UNIT
This entry in the JSON file is
a [regular expression](https://docs.python.org/3/howto/regex.html)
that extracts the unit from the file name.
If there's a match, the unit number must be in the first group of the regular expression.
If there's no match, the unit given with option `-u` will be used.

Note that in JSON you have to double each backspace used in the regular expression.
For example, `"^(\\d+)"` extracts the unit number from the start of the file,
while `"(\\d+).(py|ipynb)$"` extracts it from the end of the file.
If the names of your files don't include a unit number,
remove the `"FILE_UNIT"` entry or set it to the empty string.

### LANGUAGE
This entry is a dictionary that maps each unit number to
a list of strings describing the syntax and built-in functions introduced in that unit. For example,
```json
"LANGUAGE": {
   "2": ["name", "+", "help"]
}
```
means that unit 2 introduces names (identifiers), the plus operator and the builtin `help` function.

For the possible syntactical elements, see dictionary `SYNTAX` in `allowed.py`.
For the possible built-in functions, see set `BUILTINS` in `allowed.py`.

The various uses of a construct can't be individually allowed or disallowed.
For example, you can't allow integer addition
and disallow string concatenation (or vice versa): you either allow
the `+` operator (and all its uses) or you don't.

Adding `"for"` and `"while"` to `"LANGUAGE"` only allows the 'normal' loops.
To also allow the `else` clause in loops, add `"for else"` and `"while else"`.

### IMPORTS
This entry is a dictionary that maps units to dictionaries of
the modules and the list of exported objects introduced in those units. For example,
```json
"IMPORTS": {
   "10": {"math": ["sqrt", "inf"]},
   "11": {"math": ["abs"], "fractions": ["Fraction"]}
}
```
allows function `math.sqrt(x)` and constant `math.inf` from unit 10 onwards, and
allows function `math.abs(x)` and class `fractions.Fraction` from unit 11 on.

Entry `"METHODS"` has the same structure as `"IMPORTS"`, but instead of listing
which objects of which modules can be imported,
it lists which methods of which classes can be called.

## Contributing

Any help to improve `allowed` is welcome and appreciated.

If you spot an error in the code or documentation, please check if it
[has been reported](https://github.com/dsa-ou/allowed/issues),
before creating a new issue.

If you have an idea for a new feature, post it in the
[ideas discussion forum](https://github.com/dsa-ou/allowed/discussions/categories/ideas).
If you have a query about using `allowed`, post it in the
[Q & A discussion forum](https://github.com/dsa-ou/allowed/discussions/categories/q-a).

If you are an M269 student or tutor, you can alternatively report errors,
make suggestions and ask questions in the M269 technical forum.

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

## Licences

The code and text in this repository are
Copyright © 2023 by The Open University, UK.
The code is licensed under a [BSD-3-clause licence](LICENCE.MD).
The text is licensed under a
[Creative Commons Attribution 4.0 International Licence](http://creativecommons.org/licenses/by/4.0).
