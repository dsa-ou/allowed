# Changelog

This file documents notable changes to this project.
Changes to the documentation are not listed.
The format is based on [Keep a Changelog](https://keepachangelog.com),
with an additional 'Development' section for changes that don't affect users.
This project does *not* adhere to [Semantic Versioning](https://semver.org).

<!-- Per release: Added / Changed / Deprecated / Removed / Fixed / Security -->

## [Unreleased](https://github.com/dsa-ou/allowed/compare/v1.3.0...HEAD)
These changes are in the GitHub repository but not on [PyPI](https://pypi.org/project/allowed).

### Added
- option `-v`/ `--verbose`: display additional info about the checking process
- option `--file-unit`: regular expression to extract unit number from file name

### Changed
- `-f` option: only warn that other constructs may exist if any were reported
- `-c` option: add `.json` extension if user does not type it
- moved regular expression from the configuration file to the command line

### Fixed
- report syntax errors in notebooks in the same way as in Python files

### Development
- update tests and contribution guide

## [1.3.0](https://github.com/dsa-ou/allowed/compare/v1.2.1...v1.3.0) - 2024-02-13
### Added
- option `-V` / `--version`: display the version number and exit
- option `-f` / `--first`: for each file, only report the first of each construct

### Changed
- run under Python > 3.10
- improve error and warning messages

### Fixed
- locale encoding on Windows can't read UTF-8: use UTF-8; replace characters that lead to errors
- annotated assignment is unknown construct: ignore type annotation
- processing of folders
- reduced the likelihood of crashing when the configuration is invalid

### Development
- improve tests: check processing folders, using `-f`, not using pytype/ipython, etc.
- move ipython and pytype to development dependencies

## [1.2.1](https://github.com/dsa-ou/allowed/compare/v1.2b1...v1.2.1) - 2024-02-10
The 1.2 version on PyPI doesn't include a fix to the usage message.

Neither 1.2 and 1.2.1 can process folders, i.e. `allowed path/to/folder` won't work.

### Changed
- make `allowed` publishable on PyPI
- make `allowed` executable as `allowed ...` or `python -m allowed ...`

### Fixed
- usage message: show `allowed` instead of `__main__.py` when called as `python -m allowed ...`

### Security
- use `jinja2` 3.1.3

### Development
- fixed various code style violations

## [1.2 beta 1](https://github.com/dsa-ou/allowed/compare/v1.1.0...v1.2b1) - 2024-01-11

### Added
- configuration for our introductory Computing course TM112
- feature: skip lines ending with `# allowed`

### Changed
- reporting of disallowed constructs, to be clearer
- M269 configuration: allow augmented assignments

### Fixed
- check of import configuration: display units affected
- crash on Unicode error: report and skip file
- M269 configuration: disallow string/tuple methods
- double reporting of try-except: report only first line (with `try`)

### Development
- use `poetry` and `pyproject.toml` to ease future PyPI publishing
- improve `sample.py` test file: cover more constructs

## [1.1.0](https://github.com/dsa-ou/allowed/compare/22J-final...v1.1.0) - 2023-10-19

### Changed
- M269 configuration: update for 2023/24 academic year
- documentation theme: reduce size of banner; page title is always project name

## [22J final](https://github.com/dsa-ou/allowed/compare/22J-initial...22J-final) - 2023-08-29

### Added
- option `-m` to check method calls
- option `-c` to indicate which configuration to use
- process notebooks directly, without needing `nbqa`
- GitHub Pages site with documentation

### Development
- add regression tests

## [22J initial](https://github.com/dsa-ou/allowed/releases/tag/22J-initial) - 2023-02-13

This is the initial version, given to the 2022/23 students of M269.
It provides the core functionality:
- check one or more Python files, or all Python files in a subtree
- check against the M269 configuration (included in `allowed.py`)
- check method calls if `pytype` is installed
- check against a unit, given with `-u` or extracted from the file name
- check notebooks, using [`nbqa`](https://nbqa.readthedocs.io/en/latest/readme.html)
