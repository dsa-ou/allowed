Courses often use a restricted subset of a programming language and its library,
to reduce cognitive load, focus on concepts, simplify marking, etc.

`allowed` is a program that checks if your code files and Jupyter notebooks only
use the Python constructs that were taught.

`allowed` enables instructors to check in advance their examples, exercises and assessment
for inadvertent use of constructs that weren't taught. It also allows students
and instructors to check submitted code against the taught constructs.
To do its job, `allowed` requires a short file that lists which constructs were
introduced in which 'unit' of the course. That file can be used as a reference
document to onboard new tutors and to discuss the design of the course, e.g.
to check if important constructs are missing or if some units are overloaded.

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

Otherwise, follow the [instructions](https://dsa-ou.github.io/allowed/docs/installation.html)
on how to install, use and configure `allowed`.
If you need help, post your query in the
[Q & A discussion forum](https://github.com/dsa-ou/allowed/discussions/categories/q-a).

## Contributing

Any help to improve `allowed` is welcome and appreciated.

- If you use `allowed`, please share your experience and tips in the
  [show & tell forum](https://github.com/dsa-ou/allowed/discussions/categories/show-and-tell).
- If you require a new feature, please suggest it in the
  [ideas discussion forum](https://github.com/dsa-ou/allowed/discussions/categories/ideas).
- If you spot an error in the code or documentation, please check if it
  [has been reported](https://github.com/dsa-ou/allowed/issues), before creating a new issue.
- If you want to contribute code or documentation that addresses
  an [open issue](https://github.com/dsa-ou/allowed/issues),
  please read first our [code contribution guide](https://dsa-ou.github.io/allowed/docs/contribution.html).
  Your contribution will become available under the terms below.

## Licences

The code and text in this repository are
Copyright © 2023 by The Open University, UK.
The code is licensed under a [BSD 3-clause licence](https://github.com/dsa-ou/allowed/blob/main/LICENCE.MD).
The text is licensed under a
[Creative Commons Attribution 4.0 International Licence](http://creativecommons.org/licenses/by/4.0).
