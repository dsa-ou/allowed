## Installation

Download the [latest release](https://github.com/dsa-ou/allowed/releases/latest)
of `allowed`. You may download the archive in zip or compressed tar format.
Expand the downloaded archive, if your web browser hasn't done so.
This creates a subfolder named `allowed-...` within your downloads folder.

The only files you need from the `allowed-...` folder are:
`allowed.py`, `m269.json`, `sample.py` and `sample.ipynb`.
Move those four files to anywhere, e.g. to the folder with the code you want to check.
You can then remove the downloaded archive and subfolder, as they're no longer needed.

`allowed` can check Python files and notebooks 'out of the box',
but more checks are possible with extra software:

- If you want to check method calls (as explained in the next section), you must
use Python 3.10 and install the [pytype](https://google.github.io/pytype) type checker.
On Windows, you must install [WSL](https://learn.microsoft.com/en-us/windows/wsl) before `pytype`.

- If you want to check notebook cells that have IPython commands like `%timeit`,
you must install [IPython](https://ipython.readthedocs.io/en/latest/install/index.html).
If you have installed the Jupyter software, you already have IPython.

⇧ [Start](../README.md) | [Usage](usage.md) ⇨