Courses often use a restricted subset of a programming language and its library,
for various reasons: reduce cognitive load, focus on concepts, simplify marking, etc.

This program checks if your Python files and notebooks only use certain constructs,
which you can configure.

Like all static analysis tools, `allowed` isn't perfect and will never be.
There may be false positives (code reported to be a violation, but isn't)
and false negatives (code that uses disallowed constructs but isn't reported).

To refer to `allowed` in a publication, please cite
> Michel Wermelinger.
> [_Checking Conformance to a Subset of the Python Language_](https://oro.open.ac.uk/88862).
> Proceedings of the Conference on Innovation and Technology in
> Computer Science Education (ITiCSE), vol. 2, pp. 573–574. ACM, 2023.

## Instructions

If you're an M269 student or tutor, follow the
[M269 software](https://dsa-ou.github.io/m269-installer) installation instructions,
and use the M269 technical forum or the tutor forum to report issues and ask questions.

For everyone else:

- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Configuration](docs/configuration.md)

If you need help in installing, configuring or using `allowed`, post your query in the
[Q & A discussion forum](https://github.com/dsa-ou/allowed/discussions/categories/q-a).

## Contributing

Any help to improve `allowed` is welcome and appreciated.

- If you use `allowed`, please share your experience and tips in the
  [show & tell forum](https://github.com/dsa-ou/allowed/discussions/categories/show-and-tell).
- If you require a new feature, please suggest it in the
  [ideas discussion forum](https://github.com/dsa-ou/allowed/discussions/categories/ideas).
- If you spot an error in the code or documentation, please check if it
  [has been reported](https://github.com/dsa-ou/allowed/issues), before creating a new issue.

## Licences

The code and text in this repository are
Copyright © 2023 by The Open University, UK.
The code is licensed under a [BSD-3-clause licence](LICENCE.MD).
The text is licensed under a
[Creative Commons Attribution 4.0 International Licence](http://creativecommons.org/licenses/by/4.0).
