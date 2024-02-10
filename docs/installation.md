## Installation

`allowed` requires Python 3.10. Type `python3.10 -V` in a terminal to check if you have it.
If you haven't it, [install it](https://www.python.org/downloads/release/python-31011/).

Like any other Python package, `allowed` can be installed in your default global environment,
but should preferably be installed in a new or existing
[virtual environment](https://realpython.com/python-virtual-environments-a-primer/)
created with Python 3.10.
Once the virtual environment is activated, type _one_ of the following:
1. `pip install allowed` if you only need to
   check Python files and Jupyter notebooks with Python code
2. `pip install 'allowed[pytype]'` if you also want to
   check method calls (as explained in the next section)
3. `pip install 'allowed[ipython]'` if you want to
   check notebook cells that have IPython commands like `%timeit`
4. `pip install 'allowed[all]'` if you want to
   check method calls and notebook cells with IPython commands

If you're using Jupyter notebooks, then you will likely already have IPython installed.
Type `pip show ipython` to check if you have it.

On Windows, you must install [WSL](https://learn.microsoft.com/en-us/windows/wsl)
in order to be able to choose option 2 or 4, as the
[pytype](https://google.github.io/pytype) type checker isn't available for Windows.

⇧ [Start](../README.md) | [Usage](usage.md) ⇨