## Configuration

Students and instructors often study and teach multiple courses at the same time.
You can have multiple configuration files and select one with
option `-c` or `--config`, e.g.
```bash
allowed path/to/file.py -c path/to/configuration.json
```
The program comes with two configuration files,
one for our algorithms and data structures course M269,
and one for our introductory Computing course TM112.
If no configuration file is given, `allowed` will use the one for M269.

For example, `allowed program.py` will check the given program against the constructs
taught in M269, while `allowed program.py -c tm112.json` will check it against those
taught in TM112.

You can create your own configuration by writing a JSON file of the form
```json
{
   "FILE_UNIT": "...",
   "LANGUAGE": { ... },
   "IMPORTS": { ... },
   "METHODS": { ... }
}
```
The easiest approach is to download and rename
[`m269.json`](https://raw.githubusercontent.com/dsa-ou/allowed/main/allowed/m269.json) or
[`tm112.json`](https://raw.githubusercontent.com/dsa-ou/allowed/main/allowed/tm112.json)
and edit it to suit your course.

The rest of this document explains the various parts of the JSON file.

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

For the possible syntactical elements, see dictionary `SYNTAX` in
[`allowed.py`](https://github.com/dsa-ou/allowed/blob/main/allowed/allowed.py).
For the possible built-in functions, see set `BUILTINS` in the same file.

The various uses of a construct can't be individually allowed or disallowed.
For example, you can't allow integer addition
and disallow string concatenation (or vice versa): you either allow
the `+` operator (and all its uses) or you don't.

Adding `"for"` and `"while"` to `"LANGUAGE"` only allows the 'normal' loops.
To also allow the `else` clause in loops, add `"for else"` and `"while else"`.

To allow _all_ possible augmented assignments (`+=`, `*=`, `//=`, etc.), add `"+="` to `"LANGUAGE"`.

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
allows function `math.abs(x)` and class `fractions.Fraction` from unit 11 onwards.

### METHODS
This entry has the same structure as `"IMPORTS"`, but instead of listing
which objects of which modules can be imported,
it lists which methods of which classes can be called.

Note that some of the built-in classes are written in lowercase and
others in uppercase (see `m269.json`, the default configuration).

If a unit introduces literals of some type (e.g. lists) in the `"LANGUAGE"` section,
then there should be an entry for the same unit and type in the `"METHODS"` section.
If no methods are allowed, this must be explicitly indicated with an empty list.

In the following example, unit 2 allows any immutable value
(numbers, Booleans, `None`, strings, tuples), so it must also state
which methods are allowed for strings (none in the example) and tuples (only `index`).
```
{
   "FILE_UNIT": "...",
   "LANGUAGE": {
      "2": [ "constant", ...],
      ...
   },
   "IMPORTS": { ... },
   "METHODS": {
      "2": {"Tuple": ["index"], "str": []},
      ...
   }
}
```

⇦ [Usage](usage.md) | ⇧ [Start](../README.md)