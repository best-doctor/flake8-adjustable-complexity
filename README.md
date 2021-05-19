# flake8-adjustable-complexity

[![Build Status](https://github.com/best-doctor/flake8-adjustable-complexity/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/best-doctor/flake8-adjustable-complexity/actions/workflows/build.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/544649e16b4cf6645ad3/maintainability)](https://codeclimate.com/github/best-doctor/flake8-adjustable-complexity/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/544649e16b4cf6645ad3/test_coverage)](https://codeclimate.com/github/best-doctor/flake8-adjustable-complexity/test_coverage)

An extension for flake8 to report on too complex functions with bad variables names.

Sometimes you want to use too generic variable name inside some function.
It this case you want to be sure that the function is more simple that
others, so a reader doesn't have to remember meaning of a variable
together with other logic for a long time.

This plugin calculates max allowed cyclomatic complexity for each function
separately. Default is 7, and it is decreased by 2 for each variable from
blacklist inside the function. If actual complexity overcomes max calculated
complexity, the plugin reports an error.

Currently, the following errors are reported:

| Code    | Description |
| ------- | ----------- |
| **CAC001** | `func` is too complex (`complexity` > `max allowed complexity`) |
| **CAC002** | `func` is too complex (`complexity`). Bad variable names penalty is too high (`penalty`) |

## Installation

```terminal
pip install flake8-adjustable-complexity
```

## Configuration

The plugin has the following configuration options:

* `--max-mccabe-complexity` (or `--max-adjustable-complexity`) - Max allowed cyclomatic complexity.
* `--per-path-max-adjustable-complexity` - Per-path complexity settings.
  The value of the option must be a comma-separated list of `<path>:<complexity>` pairs.
* `--var-names-extra-blacklist` - Comma-separated list of bad variable names to blacklist.
  Each variable will affect the max allowed complexity.
* `--var-names-whitelist` - Comma-separated list of bad variable names to whitelist.

All options also can be specified via `[flake8]` section of `setup.cfg`.

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
test.py:1:1: CAC001 foo is too complex (4 > 1)
```

## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have.
   Wait for approve from maintainer.
1. Create a pull request. Make sure all checks are green.
1. Fix review comments if any.
1. Be awesome.

Here are useful tips:

* You can run all checks and tests with `make check`. Please do it before TravisCI does.
* We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
* We respect [Django CoC](https://www.djangoproject.com/conduct/). Make soft, not bullshit.
