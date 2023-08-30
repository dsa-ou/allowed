## Usage

Open a terminal. Change to the folder where you have put `allowed.py` and `m269.json`.
You can check code files and Jupyter notebook files by typing
```bash
python allowed.py path/to/file.py path/to/notebook.ipynb ...
```
This will list all disallowed constructs in the given files.
If a Python file (or code cell) has a syntax error, it can't be parsed and hence it's not checked.

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
`allowed` needs to know the type of `variable`. For that purpose, it uses
the `pytype` type checker, if it's installed and the Python version is 3.10.

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
Option `-u N` or `--unit N` will check code against
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

`allowed` does check Jupyter notebooks and reports the cells and lines with
disallowed constructs. For example, `path/to/notebook.ipynb:cell_13:5: ...`
means that the problem is in line 5 of the 13th code cell.

If a code cell has invalid Python, `allowed` reports a syntax error and
skips the cell. Using IPython magics such as `%timeit` and `%run`
triggers a syntax error if IPython isn't installed. If it is,
the magics are transformed into Python code and the cell is checked,
if it hasn't other syntax errors.
The transformed magics use function calls and attributes, so
the cell will only pass the check if those constructs are allowed.

⇦ [Installation](installation.md) | ⇧ [Start](../README.md) | [Configuration](configuration.md) ⇨