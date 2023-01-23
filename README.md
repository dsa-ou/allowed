This program checks if your Python code only uses certain constructs,
which you can configure.
The check is purely syntactic and therefore assumes that your code compiles.

The various uses of a construct can't be individually allowed or disallowed.
For example, you can't allow integer addition
and disallow string concatenation (or vice versa): either you allow
the `+` operator (and all its uses) or not.

Like all static analysis tools, `allowed` isn't perfect and will never be.
There will be false positives (code reported to be a violation, but isn't)
and false negatives (code that uses disallowed constructs but isn't reported).

## Usage
Download the files in this repository and type in a terminal:
```bash
python allowed.py path/to/file1.py path/to/file2.py ...
```
This will list all disallowed constructs in the given files.
If the file has a syntax error, it can't be parsed and hence it's not checked.

For example, you can check the sample file and `allowed`'s code with:
```bash
python allowed.py sample.py allowed.py
```
The latter has many violations because the program uses many advanced
Python features and modules not allowed by the basic default configuration.
If you expect a long list of disallowed constructs, it's better to
check one Python file at a time and store the reports in a text file, e.g.
```bash
python allowed.py sample.py > sample_errors.txt
```
If you want to check all Python files in a folder and its subfolders, type:
```bash
python allowed.py path/to/folder
```

### Extra checks

To check if the attribute access `variable.method` is allowed,
the program needs to know the type of `variable`. For that purpose, it uses
the [`pytype`](https://google.github.io/pytype) type checker,
which only works with Python versions 3.7 to 3.10.
If you don't have such a version or have not installed `pytype`,
`allowed` skips those checks (which by the way slow down the process substantially).

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
The second command will report far fewer violations because units 3 and 4 of
the default configuration introduce Booleans, lists, strings and tuples.

The unit option can appear anywhere after `allowed.py` and in either form.
For example, the following two commands are equivalent:
```bash
python allowed.py -u 2 file1.py file2.py
python allowed.py file1.py --unit 2 file2.py
```

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

### Checking notebooks
There are two ways of checking Python code in a Jupyter notebook.

The first is to save the notebook as a Python file
(e.g with menu File -> Download as -> Python in the web interface) and check that file.
When `allowed` reports a violation as `notebook1.py:line: construct`,
that line number relates to the Python file but is meaningless for the notebook.
To find the issue, search for the reported construct in the notebook.
Every time you change the notebook, you must convert it again to Python
or use [`jupytext`](https://jupytext.readthedocs.io) to do it automatically.

The second way is much simpler but requires extra software:
install [nbqa](https://http://nbqa.readthedocs.io) and type one of the following.
```bash
nbqa allowed path/to/notebook1.ipynb path/to/notebook2.ipynb ...
nbqa allowed path/to/folder
```
The latter will check all notebooks in that folder and its subfolder.
With `nbqa`, reports state which line of which code cell uses a disallowed construct,
like `path/to/notebook1.ipynb:cell_13:5: ...`, which helps find the issue more quickly.

You can of course still use option `-u` or `--unit`.

## Configuration
The program is already configured for our course,
[M269](https://www.open.ac.uk/courses/modules/m269), but you can change that.

You can define which language elements, modules, built-in functions and methods
are introduced in which units by setting the constants
`LANGUAGE`, `IMPORTS`, `FUNCTIONS` and `METHODS` in `allowed.py`.
See the file for details.

You can also decide whether to allow the `else` clause in for- and while-loops
by setting the Boolean constants `FOR_ELSE` and `WHILE_ELSE` in `allowed.py`.

You can set constant `FILE_UNIT` to the
[regular expression](https://docs.python.org/3/howto/regex.html)
that extracts the unit number from the file name. See the file for details.

## Contributing
If you spot an error, please check if it
[has been reported](https://github.com/dsa-ou/allowed/issues)
before creating a new issue.

For anything else, like an idea for a feature or
a query on how to use and configure `allowed`, please use the
[discussion forum](https://github.com/dsa-ou/allowed/discussion).

Please only submit pull requests for open issues.

## Licences

The code and text in this repository are
Copyright © 2023 by The Open University, UK.
The code is licensed under a [BSD-3-clause licence](LICENCE.MD).
The text is licensed under a
[Creative Commons Attribution 4.0 International Licence](http://creativecommons.org/licenses/by/4.0).
