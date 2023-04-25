## Installation

Unzip the downloaded file if your web browser hasn't done so.
This creates an `allowed-main` folder within your downloads folder.

The only files you need within that folder are `allowed.py` and `m269.json`,
which you may move to anywhere, e.g. to the folder with the code you want to check.
The example files with code to check (`sample.py` and `sample.ipynb`)
can be removed after going through the following explanations.

`allowed` can check Python files and notebooks 'out of the box',
but more checks are possible with extra software.

If you want to check method calls (see below), you must use Python 3.10
and install the [pytype](https://google.github.io/pytype) type checker.
On Windows, you must first install [WSL](https://learn.microsoft.com/en-us/windows/wsl).

If you want to check notebook cells that have IPython commands like `%timeit` (see below),
you must install [IPython](https://ipython.readthedocs.io/en/latest/install/index.html).
If you have installed the Jupyter software, you already have IPython.

⇦ [Start](../README.md) | [Usage](usage.md) ⇨