## Quick Guide for M269

First, make sure you have Python 3.10 or 3.11.
If you intend to later install further software in order to check the method calls of your code,
you need 3.10 rather than 3.11.

1. Open a terminal and type `python3 -V`.
2. If your Python version is 3.9 or lower,
   install 3.10 or 3.11 from [https://python.org](https://www.python.org/downloads/).
   (You don't need to uninstall your current Python.)

Next, install the `allowed` tool:

3. Click on one of the download buttons above.
4. Go to your downloads folder and extract the files from the downloaded archive.
   (Your web browser may have done it automatically.)
5. Move the files `allowed.py` and `m269.json` from the `allowed-main` folder
   to the folder with your M269 materials.

To use the tool:

6. Open a terminal and go to the folder where you put both files.

- To check the first TMA, type `python allowed.py -u 10 path/to/TMA01.ipynb`,
  e.g. `python allowed.py -u 10 TMA01/22J-TMA01-STUDENT.ipynb` or similar.
  (On Windows, use backslashes.)
- To check the second TMA, type `python allowed.py -u 20 path/to/TMA02.ipynb`.
- To check the third TMA,  type `python allowed.py path/to/TMA03.ipynb`.

These checks won't detect if you're calling methods that haven't been taught,
like `count()` on lists.
To check methods calls you need Python 3.10 and do the following:

7. If you're on Windows, install [WSL](https://learn.microsoft.com/en-us/windows/wsl).
8. In a terminal, type `pip install pytype` to install the necessary type checker.
9. Add `-m` when checking a TMA, e.g. `python allowed.py -m -u 10 path/to/TMA01.ipynb`.