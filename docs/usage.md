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
To check all `.py` and `.ipynb` files in a folder and its subfolders, type:
```bash
python allowed.py path/to/folder
```
If you expect a long list of disallowed constructs, it may be better to
check one file at a time and store the report in a text file, e.g.
```bash
python allowed.py sample.py > disallowed.txt
```

As `allowed` checks the files, it shows the line (and for notebooks the cell)
where each disallowed construct occurs, like so:
```
file.py:3: break
notebook.ipynb:cell_2:4: type()
```
The message only shows the statement, operator, function, method that isn't allowed.
For example, if the line of code is `from random import choice`,
then the possible flagged constructs are:
- `from import`: the `from ... import ...` statement isn't allowed
- `random`: importing the `random` module isn't allowed
- `choice`: importing the `random.choice()` function isn't allowed.

For some constructs, `allowed` reports the type of the construct instead of
the actual occurrence in the code line. For example:
- `attribute`: dot notation, as in `a_list.sort()`, isn't allowed
- `constant`: immutable values like `None`, `True`, `(1, 2, 3)` and `"Hi!"` aren't allowed
- `if expression`: expressions of the form `... if ... else ...` aren't allowed
- `for-else` and `while-else`: the `else` branch of a for- or while-loop isn't allowed
- `name`: variable, function and other names aren't allowed.

It's unlikely for `constant` and `name` to be flagged, as Python programs need them.

By default, the allowed constructs are those taught in our algorithms and data structures course,
but you can change that, as explained in the [Configuration](configuration.md) section.

If a message contains the string `ERROR`, then the indicated file or cell
was _not_ checked, for these reasons:
- `CONFIGURATION ERROR`: the allowed constructs are not well defined in the JSON configuration file
- `FORMAT ERROR`: the internal notebook format has been corrupted
- `OS ERROR`: an operating system error, e.g. the file doesn't exist or can't be read
- `PYTYPE ERROR`: an error that blocked the type checker, usually a syntax error
- `SYNTAX ERROR`: the file has invalid Python
- `UNICODE ERROR`: the file has some strange characters and couldn't be read
- `VALUE ERROR`: some other cause; please report it to us.

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

As mentioned earlier, `allowed` does check Jupyter notebooks and
reports the cells and lines with disallowed constructs: `notebook.ipynb:cell_13:5: ...`
means that line 5 of the 13th code cell uses a construct that wasn't taught.

If a code cell has invalid Python, `allowed` reports a syntax error and
skips the cell, but continues checking the rest of the notebook.
Using IPython magics such as `%timeit` and `%run`
triggers a syntax error if IPython isn't installed. If it is,
the magics are transformed into Python code and the cell is checked,
if it hasn't other syntax errors.
The transformed magics use function calls and attributes, so
the cell will only pass the check if those constructs are allowed.

⇦ [Installation](installation.md) | ⇧ [Start](../README.md) | [Configuration](configuration.md) ⇨