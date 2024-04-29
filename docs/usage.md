## Usage

`allowed` is a command-line tool, to be used in a Linux/macOS terminal,
a Windows Command Prompt or a Windows Powershell.

For a summary of the command line options, type `allowed -h` or `allowed --help`.

### Checking code
You can check Python code in `.py` and `.ipynb` (Jupyter notebook) files by typing
```bash
allowed path/to/file.py path/to/notebook.ipynb ...
```
To check all `.py` and `.ipynb` files in a folder and its subfolders, type:
```bash
allowed path/to/folder
```
If you expect a long list of disallowed constructs, it may be better to
check one file at a time and store the report in a text file, e.g.
```bash
allowed path/to/file.py > disallowed.txt
```
Another way to shorten the list of reported constructs is to report only
the first occurrence in each file, using option `-f` or `--first`:
```bash
allowed -f path/to/file.py path/to/notebook.ipynb
```
If this option is used, a warning will remind you that other occurrences of
the reported constructs may exist in the given files.

As `allowed` checks the files, it reports the line (and for notebooks the cell)
where each disallowed construct occurs, like so:
```
file.py:3: break
notebook.ipynb:cell_2:4: type()
```
The message doesn't show the code line but rather
the statement, operator, function or method that isn't allowed.
For example, if the line of code is `from random import choice`,
then the message may be:
- `from import`: the `from ... import ...` statement isn't allowed
- `random`: importing the `random` module isn't allowed
- `choice`: importing the `random.choice()` function isn't allowed.

If the same disallowed construct occurs more than once in a line,
it is reported only once.

For some constructs, `allowed` reports the type of the construct instead of
the actual occurrence in the code line. For example:
- `attribute`: dot notation, as in `a_list.sort()`, isn't allowed
- `constant`: immutable values like `None`, `True`, `(1, 2, 3)` and `"Hi!"` aren't allowed
- `if expression`: expressions of the form `... if ... else ...` aren't allowed
- `for-else` and `while-else`: the `else` branch of a for- or while-loop isn't allowed
- `name`: variable, function and other names aren't allowed.

It's unlikely for `constant` and `name` to be flagged, as all Python programs need them.

By default, the allowed constructs are those taught in our algorithms and data structures course,
but you can change that, as explained in the [Configuration](configuration.md) section.

If a message contains the string `ERROR`, then the indicated file or cell
was _not_ checked, for these reasons:
- `CONFIGURATION ERROR`: the configuration file hasn't the [expected format](configuration.md)
- `FORMAT ERROR`: the internal notebook format has been corrupted
- `OS ERROR`: an operating system error, e.g. the file doesn't exist or can't be read
- `PYTYPE ERROR`: an error that blocked the type checker, usually a syntax error
- `SYNTAX ERROR`: the file has invalid Python
- `UNICODE ERROR`: the file has some strange characters and couldn't be read
- `VALUE ERROR`: some other cause; please report it to us.

When the command line option `-v` or `--verbose` is given,
the tool outputs additional information, including
the total number of files processed and of unknown constructs found, and
the total number of files not processed due to syntax, format or other errors.

### Extra checks

To check method calls of the form `variable.method(...)`,
we must know the type of `variable`. For that purpose, `allowed` uses
the `pytype` type checker, if it's installed and the Python version is 3.10.

By default, `allowed` does _not_ check method calls because it slows down the process.
You can enable these checks with option `-m` or `--methods`:
```bash
allowed -m file1.py notebook.ipynb
```

### Ignoring specific lines

If a code line ends with the comment `# allowed`, then no violations are flagged for that line.
This is useful for assessment or examples that exceptionally use constructs not taught.
This feature should of course be used sparingly, as it bypasses the checks by `allowed`.

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
allowed -u 5 submission.py
```
If the file name includes the unit it corresponds to, then you can provide
option `--file-unit` followed by
a [regular expression](https://docs.python.org/3/howto/regex.html)
that extracts the unit from the file name.
If there's a match, the unit number must be in the first group of the regular expression.
If there's no match, all units or the unit given with option `-u` or `--unit` will be used.

For example, to use the first two digits in the names of files as the unit number, type
```bash
allowed --file-unit '(\d\d)' path/to/file_or_folder
```
If the file's name doesn't have two consecutive digits, then the file will be checked against all units,
because option `-u` is not given. So, if you have a folder `cs101/` with files
named `weekDD_exerciseDD.py`, where D is a digit, then
```bash
allowed --file-unit '(\d\d)' cs101
```
will check each file against the corresponding units:
`week01_exercise03.py` against unit 1, `week10_exercise02.py` against units 1 to 10, etc.
You can use option `-v` (verbose output) to see the units each file is checked against.

As a further example, if your files are named `cs101-week-DD-exercise-DD.ipynb`
then using regular expression `'(\d\d)'` would check all files against units 1 to 10,
as those are the first two digits in the name. The regular expression should be `'-(\d\d)'`
so that only the first two digits after a hyphen are used for the unit.

The part of the regular expression that indicates the unit must always be within brackets
because `allowed` will use the first group of the regular expression as the unit number.

### Checking notebooks

As mentioned earlier, `allowed` does check Jupyter notebooks and
reports the cells and lines with unknown constructs: `notebook.ipynb:cell_13:5: ...`
means that line 5 of the 13th code cell uses a construct that wasn't taught.

If a code cell has invalid Python, `allowed` reports a syntax error and
skips the cell, but continues checking the rest of the notebook.
Using IPython commands such as `%timeit` and `%run`
triggers a syntax error if IPython isn't installed. If it is,
the commands are transformed into Python code and the cell is checked,
if it hasn't other syntax errors.
The transformed commands use function calls and attributes, so
the cell will only pass the check if those Python constructs are allowed.

In the verbose output (option `-v` / `--verbose`), syntax errors do not count
towards the unknown constructs total.

⇦ [Installation](installation.md) | ⇧ [Start](../README.md) | [Configuration](configuration.md) ⇨