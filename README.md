# Chaos Toolkit Extension for Honeycomb

[![Version](https://img.shields.io/pypi/v/chaostoolkit-honeycomb.svg)](https://img.shields.io/pypi/v/chaostoolkit-honeycomb.svg)
[![License](https://img.shields.io/pypi/l/chaostoolkit-honeycomb.svg)](https://img.shields.io/pypi/l/chaostoolkit-honeycomb.svg)

[![Build, Test, and Lint](https://github.com/chaostoolkit/chaostoolkit-extension-template/actions/workflows/build.yaml/badge.svg)](https://github.com/chaostoolkit/chaostoolkit-extension-template/actions/workflows/build.yaml)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-honeycomb.svg)](https://www.python.org/)

This project contains Chaos Toolkit activities for the
[Honeycomb](https://www.honeycomb.io/) platform.

## Install

This package requires Python 3.7+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install chaostoolkit-honeycomb
```

## Usage

```json
{
    "title": "SLO should not be impacted",
    "description": "n/a",
    "secrets": {
        "honeycomb": {
            "api_key": {
                "type": "env",
                "key": "HONEYCOMB_API_KEY"
            }
        }
    },
    "steady-state-hypothesis": {
        "title": "Use SLO as Steady-State Hypothesis verification",
        "probes": [
            {
                "name": "slo has enough budget left",
                "type": "probe",
                "tolerance": true,
                "provider": {
                    "type": "python",
                    "secrets": ["honeycomb"],
                    "module": "chaoshoneycomb.slo.probes",
                    "func": "slo_has_enough_remaining_budget",
                    "arguments": {
                        "dataset_slug": "ds",
                        "slo_id": "slo1",
                        "min_budget": 7.5
                    }
                }
            }
        ]
    }
}
```

That's it!

Please explore the code to see existing probes and actions.

## Configuration

Specify the Honeycomb API key either via the `secrets` block or via
the `HONEYCOMB_API_KEY` environment variable. In that later case, you
can in fact skip the declaration on the `secrets` block as the
extension will look for it anyway.

## Test

To run the tests for the project execute the following:

```
$ pdm run test
```

### Formatting and Linting

We use a combination of [`black`][black], [`ruff`][ruff], and [`isort`][isort]
to both lint and format this repositories code.

[black]: https://github.com/psf/black
[ruff]: https://github.com/astral-sh/ruff
[isort]: https://github.com/PyCQA/isort

Before raising a Pull Request, we recommend you run formatting against your
code with:

```console
$ pdm run format
```

This will automatically format any code that doesn't adhere to the formatting
standards.

As some things are not picked up by the formatting, we also recommend you run:

```console
$ pdm run lint
```

To ensure that any unused import statements/strings that are too long, etc.
are also picked up.

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [black][blackstyle] code style, sprinkling with tests and submit a PR for
review.

[blackstyle]: https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html

To contribute to this project, you will also need to install [pdm][].

[pdm]: https://pdm.fming.dev/latest/
