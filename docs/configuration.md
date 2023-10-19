## Configuration

The program is already configured for our course,
[M269](https://www.open.ac.uk/courses/modules/m269),
but you can create your own configuration by creating a JSON file of the form
```json
{
   "FILE_UNIT": "...",
   "LANGUAGE": { ... },
   "IMPORTS": { ... },
   "METHODS": { ... }
}
```
File [`m269.json`](m269.json) is the default configuration.
You can copy, rename and edit it to configure `allowed` for your course.

Students and instructors often study and teach multiple courses at the same time.
You can have multiple configuration files and select one with
option `-c` or `--config`, e.g.
```bash
python allowed.py sample.py -c cs101.json
```
While you can test your configuration with our `sample.py` and `sample.ipynb` files,
as shown in the example,
you will probably want to use Python and notebook files from your course.
You may thus wish to delete the two `sample` files, as they're no longer needed.

### FILE_UNIT
This entry in the JSON file is
a [regular expression](https://docs.python.org/3/howto/regex.html)
that extracts the unit from the file name.
If there's a match, the unit number must be in the first group of the regular expression.
If there's no match, the unit given with option `-u` or `--unit` will be used.

Note that in JSON you have to double each backspace used in the regular expression.
For example, `"^(\\d+)"` extracts the unit number from the start of the file name,
while `"(\\d+).(py|ipynb)$"` extracts it from the end of the file name.
If the names of your files don't include a unit number,
remove the `"FILE_UNIT"` entry or set it to the empty string.

### LANGUAGE
This entry is a dictionary that maps each unit number to
a list of strings describing the syntax and built-in functions introduced in that unit. For example,
```json
"LANGUAGE": {
   "2": ["name", "+", "help"]
}
```
means that unit 2 introduces names (identifiers), the plus operator and the builtin `help` function.

For the possible syntactical elements, see dictionary `SYNTAX` in `allowed.py`.
For the possible built-in functions, see set `BUILTINS` in `allowed.py`.

The various uses of a construct can't be individually allowed or disallowed.
For example, you can't allow integer addition
and disallow string concatenation (or vice versa): you either allow
the `+` operator (and all its uses) or you don't.

Adding `"for"` and `"while"` to `"LANGUAGE"` only allows the 'normal' loops.
To also allow the `else` clause in loops, add `"for else"` and `"while else"`.

### IMPORTS
This entry is a dictionary that maps units to dictionaries of
the modules and the list of exported objects introduced in those units. For example,
```json
"IMPORTS": {
   "10": {"math": ["sqrt", "inf"]},
   "11": {"math": ["abs"], "fractions": ["Fraction"]}
}
```
allows function `math.sqrt(x)` and constant `math.inf` from unit 10 onwards, and
allows function `math.abs(x)` and class `fractions.Fraction` from unit 11 on.

### METHODS
This entry has the same structure as `"IMPORTS"`, but instead of listing
which objects of which modules can be imported,
it lists which methods of which classes can be called.

⇦ [Usage](usage.md) | ⇧ [Start](../README.md)