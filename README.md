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

Like all static analysis tools, `allowed` isn't perfect, nor will it ever be.
It will likely let pass some violations of the subset of Python you intend to enforce.

## Configuration
The program is already configured for our course,
[M269](https://www.open.ac.uk/courses/modules/m269), but you can change that.

You can define which statements are allowed by setting the constant `STATEMENTS`
in `allowed.py`. See the file for details.

You can also decide whether to allow the `else` clause in for- and while-loops
by setting the Boolean constants `FOR_ELSE` and `WHILE_ELSE` in `allowed.py`.

## Contributing
If you spot an error, please check if it
[has been reported](https://github.com/dsa-ou/allowed/issues)
before creating a new issue.

For anything else, like an idea for a feature or
a query on how to use and configure `allowed`, please use the
[discussion forum](https://github.com/dsa-ou/allowed/discussion).

Please do _not_ submit pull requests. This project is not yet stable.