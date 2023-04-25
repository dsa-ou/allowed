Courses often use a restricted subset of a programming language and its library,
for various reasons: reduce cognitive load, focus on concepts, simplify marking, etc.

This program checks if your Python files and notebooks only use certain constructs,
which you can configure.

Like all static analysis tools, `allowed` isn't perfect and will never be.
There may be false positives (code reported to be a violation, but isn't)
and false negatives (code that uses disallowed constructs but isn't reported).

If you're an M269 student or tutor, read the [quick guide](docs/m269_guide.md);
otherwise go through the full manual:

- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Configuration](docs/configuration.md)
- [Contributing](docs/contribution.md)

## Licences

The code and text in this repository are
Copyright © 2023 by The Open University, UK.
The code is licensed under a [BSD-3-clause licence](LICENCE.MD).
The text is licensed under a
[Creative Commons Attribution 4.0 International Licence](http://creativecommons.org/licenses/by/4.0).
