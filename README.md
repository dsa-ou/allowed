This program allows you to check if a Python program only uses certain constructs.
The check is purely syntactic and therefore assumes the program compiles.
The various uses of a construct can't be individually allowed or disallowed.
For example, you can't allow integer addition
and disallow string concatenation (or vice versa): either you allow
the `+` operator (and all its uses) or not.

Like all static analysis tools, `allowed` isn't perfect and will never be.
There will be false positives (code reported as a violation, but isn't)
and false negatives (code is a violation but isn't reported).

## Usage
Download the files in this repository and type in a terminal:
```bash
python allowed.py path/to/folder_or_file
```
For example, you can check `allowed` itself and the sample file with:
```bash
python allowed.py allowed.py
python allowed.py sample.py
```
If you want to check all Python files in a folder and its subfolders, type:
```bash
python allowed.py /home/my_project
```
or whatever the path to the folder is.

To check code in a Jupyter notebook, save it as a Python file and check that file.
In the classic web interface, use menu File -> Download as -> Python.

`allowed` assumes that your course or textbook is organised in 'units'
(lessons, weeks, chapters, whatever you want) and that they are cumulative:
a Python construct introduced in a unit can be used in any subsequent unit.

Typing a unit number after the file or folder path will check the file(s)
only against the Python constructs introduced up to that unit (inclusive).
Checking a submission to an assessment that covers units 1 to 5 can be done with:
```bash
python allowed.py submission.py 5
```
To see the weekly difference in the allowed constructs, type for example:
```bash
python allowed.py sample.py 2
python allowed.py sample.py 4
```

The earlier examples, without a unit number, correspond to considering all units,
i.e. checking against _all_ allowed Python constructs.

If the file name starts with the unit number, you can leave the number out, e.g.
```bash
python allowed.py 05_submission.py
```
also allows only constructs introduced in units 1–5. However, if the filename
starts with a number that isn't the intended unit, you must provide it:
```bash
python allowed.py 01_submission.py 5
```

## Configuration
The program is already configured for our course,
[M269](https://www.open.ac.uk/courses/modules/m269), but you can change that.

You can define which constructs, modules and built-in functions
are introduced in which units by setting the constants
`CONSTRUCTS`, `IMPORTS` and `FUNCTIONS` in `allowed.py`.
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

Please _don't_ submit pull requests: this project isn't stable yet.