## Installation

If your IT administrator or instructor has created an environment for your course,
with `allowed` installed, then you may skip this section.

### Preparation
1. Open a Linux/macOS terminal or Windows PowerShell,
   in order to enter the commands given in these instructions.
2. Enter `python -V` to check the version you have installed.
3. If it's 3.9 or earlier, [download and install](https://www.python.org/downloads)
   the latest version.
   However, to use `pytype` (see below) you must install Python 3.10 or 3.11.

### Virtual environments
Like any other Python package, `allowed` can be installed in your default global environment,
but should preferably be installed in a new or existing virtual environment,
e.g. the one for the course you are studying or teaching.
A virtual environment is a folder with the software you need for one or more projects.
This helps ensuring that you always use the right versions of the right packages for
each project.

1. To create a virtual environment, enter `python -m venv path/to/folder`.

The folder you indicate will be created if it doesn't exist.
For example, if you want to keep all virtual environments in subfolders of `~/environments`,
you would create a new virtual environment for course CS101 with
`python -m venv ~/environments/cs101`.

Virtual environments need to be activated in order install software in them.

2. To activate a virtual environment enter
   - `source path/to/folder/bin/activate` in Linux/macOS
   - `path/to/folder/scripts/Activate` in Windows.

For our example, it would be `source ~/environments/cs101/bin/activate` or
`~/environments/cs101/scripts/Activate`.
After activating, the command prompt becomes `(folder)`, e.g. `(cs101)`,
to show which environment is active.

You must activate a virtual environment every time you want to
install further software into it or use the software that is installed in it.

3. Once you're done using a virtual environment,
   close the terminal/PowerShell or type `deactivate`.

For more details on why one should use virtual environments and how to use them,
we recommend reading the first two sections of
[Real Python's tutorial](https://realpython.com/python-virtual-environments-a-primer/).

### Installing
The following instructions will install `allowed` and optional additional software
in your current environment, whether it's the global environment or an active virtual environment.

1. Enter `pip install allowed`.

`allowed` can check Python code in `.py` files and in `.ipynb` files (Jupyter notebooks).
If you want to check Jupyter notebooks that have IPython commands
like `%timeit` and `%run`, then you need IPython.

2. Enter `pip show ipython` to check if your current environment has IPython installed.
3. If you get a message that there's no such package, then enter `pip install ipython`.

To check method calls of the form `variable.method(...)`, `allowed` needs
the `pytype` package, to know the type of `variable`.
`pytype` is only available for Linux and macOS.

4. Enter `pip show pytype` to see if `pytype` is already installed.
5. If it isn't, enter `pip install pytype`.

⇧ [Start](../README.md) | [Usage](usage.md) ⇨