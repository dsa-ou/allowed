This program allows you to check if a Python program only uses certain statements.

## Usage
Download the `allowed.py` file and type in a terminal or Command Prompt
```bash
python allowed.py path/to/folder_or_file
```
For example, if you also download the `sample.py` file, you can check it with
```bash
python allowed.py sample.py
```
If you want to check all Python files in a folder and its subfolders, type:
```bash
python allowed.py /home/my_project
```
or whatever the path to the folder is.

To check code in a Jupyter notebook, save it as a Python file and check that file.
In the classic web interface, use menu File -> Download as -> Python.

## Configuration
The program is already configured for our course,
[M269](https://www.open.ac.uk/courses/modules/m269), but you can change that.

You can define which statements are allowed by setting the constant `STATEMENTS`
in `allowed.py`. See the file for details.

You can also decide whether to allow the `else` clause in for- and while-loops
by setting the Boolean constants `FOR_ELSE` and `WHILE_ELSE` in `allowed.py`.
