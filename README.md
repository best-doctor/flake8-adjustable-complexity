# flake8-adjustable-complexity

[![Build Status](https://travis-ci.org/best-doctor/flake8-adjustable-complexity.svg?branch=master)](https://travis-ci.org/best-doctor/flake8-adjustable-complexity)
[![Maintainability](https://api.codeclimate.com/v1/badges/544649e16b4cf6645ad3/maintainability)](https://codeclimate.com/github/best-doctor/flake8-adjustable-complexity/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/544649e16b4cf6645ad3/test_coverage)](https://codeclimate.com/github/best-doctor/flake8-adjustable-complexity/test_coverage)

An extension for flake8 to report on too complex functions with bad variables names.

Sometimes you want to use too generic variable name inside some function.
It this case you want to be sure that the function is more simple that
others, so a reader doesn't have to remember meaning of a variable
together with other logic for a long time.

This plugin calculates max allowed cyclomatic complexity for each function
separately. Default is 7 and it is decreased by 2 for each variable from
blacklist inside the function. If actual complexity overcomes max calculated
complexity, the plugin reports an error.

Max allowed cyclomatic complexity can be configured via
`--max-mccabe-complexity` (or `--max-adjustable-complexity`) option. The plugin
also accepts `--per-path-max-adjustable-complexity` to define a simple per-path
complexity settings. The value of the option must be a comma-delimited list
of `<path>:<complexity>` pairs.

Both options also can be specified via `[flake8]` section of `setup.cfg`.

## Installation

```terminal
pip install flake8-adjustable-complexity
```

## Example

Sample file:

```python
# test.py

def foo():
    for vars in range(5):
        for info in range(5):
            for obj in range(5):
                pass
```

Usage:

```terminal
$ flake8 test.py
test.py:1:1: CAC001 is too complex (4 > 1)
```

## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have.
   Wait for approve from maintainer.
1. Create a pull request. Make sure all checks are green.
1. Fix review comments if any.
1. Be awesome.

Here are useful tips:

- You can run all checks and tests with `make check`.
  Please do it before TravisCI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.
