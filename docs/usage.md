## Usage

Open a terminal or a PowerShell console. Use the `cd` command to go to the folder
where you have put `allowed.py` and the other three files.
You can check code files and Jupyter notebook files by typing
```bash
python allowed.py path/to/file.py path/to/notebook.ipynb ...
```
For example, you can check the two sample files with:
```bash
python allowed.py sample.py sample.ipynb
```
This will list the lines with disallowed constructs, which are by default
those not taught in our algorithms and data structures course,
but you can change that, as explained in the [Configuration](configuration.md) section.
If a Python file (or a code cell) has a syntax error,
then it can't be parsed and hence it's not checked.

If you expect a long list of disallowed constructs, it may be better to
check one file at a time and store the report in a text file, e.g.
```bash
python allowed.py sample.py > disallowed.txt
```
To check all `.py` and `.ipynb` files in a folder and its subfolders, type:
```bash
python allowed.py path/to/folder
```

### Extra checks

To check method calls of the form `variable.method(...)`,
we must know the type of `variable`. For that purpose, `allowed` uses
the `pytype` type checker, if it's installed and the Python version is 3.10.

By default, `allowed` does _not_ check method calls because it slows down the process.
You can enable these checks with option `-m` or `--methods`. For example,
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
Note that the second command also checks the method calls in _both_ files,
not just in the second file.

### Organising by units

`allowed` assumes that your course is organised in 'units'
(lessons, weeks, textbook chapters, whatever you want) and that they are cumulative:
a Python construct taught in a unit can be used in any subsequent unit.

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
The second command reports fewer violations because units 3 and 4 of
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
python allowed.py 01_submission.py --unit 5
```
As the previous example shows, the unit option can appear
anywhere after `allowed.py` and in either form.

### Checking notebooks

`allowed` does check Jupyter notebooks and reports the cells and lines with
disallowed constructs. For example, `path/to/notebook.ipynb:cell_13:5: ...`
means that line 5 of the 13th code cell uses a construct that wasn't taught.

If a code cell has invalid Python, `allowed` reports a syntax error and
skips the cell. Using IPython magics such as `%timeit` and `%run`
triggers a syntax error if IPython isn't installed. If it is,
the magics are transformed into Python code and the cell is checked,
if it hasn't other syntax errors.
The transformed magics use function calls and attributes, so
the cell will only pass the check if those constructs are allowed.

⇦ [Installation](installation.md) | ⇧ [Start](../README.md) | [Configuration](configuration.md) ⇨