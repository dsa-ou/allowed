## Quick Guide for M269

The following explains how to install and use `allowed`, a tool that checks if
your TMA code only uses the Python constructs mentioned in Chapters 10, 20 and 28.
The tool is merely a convenience compared to visually inspecting your code.

1. Open a terminal. Enter `python -V` to obtain your Python version.

If it is 3.9 or lower, then you can't use `allowed`, sorry.
While you can have multiple Python versions on your system,
it's not worth the hassle and potential problems at this point in M269.

Next, if you have Python 3.10 or later, install the `allowed` tool:

2. Click the 'Download .zip' button above.
3. Go to your downloads folder and extract the files from the downloaded archive.
   (Your web browser may have done it automatically.)
4. Move the files `allowed.py` and `m269.json` from the
   `dsa-ou-allowed-main-24ac36b` folder (the last 7 characters may vary)
   to the folder with your M269 materials.

To use the tool, open a terminal and go to the folder where you put both files:

5. To check the first TMA, type `python allowed.py -u 10 path/to/TMA01.ipynb`,
  e.g. `python allowed.py -u 10 TMA01/22J-TMA01-STUDENT.ipynb` or similar.
  (On Windows, use backslashes.)
6. To check the second TMA, type `python allowed.py -u 20 path/to/TMA02.ipynb`.
7. To check the third TMA,  type `python allowed.py path/to/TMA03.ipynb`.

These checks won't detect if you're calling methods that haven't been taught,
like `count()` on lists.
It's possible for `allowed` to check method calls,
but it would require installing Linux on Windows. Again, not worth the trouble.