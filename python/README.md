# ASWF Python Utilities

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![pytest coverage](https://img.shields.io/azure-devops/coverage/academysoftwarefoundation/Academy%20Software%20Foundation/2/master)

The `aswfdocker` command line tool is available to help with package and
image builds.

## Installation

### For users and developers

Install [uv](https://docs.astral.sh/uv/) (Python 3.9+ required):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then clone this repository and install the project and its dependencies:

```bash
git clone https://github.com/AcademySoftwareFoundation/aswf-docker
cd aswf-docker
```

For users, install the dependencies for `aswfdocker`:

```bash
uv sync
```

For developers, install the `aswfdocker` dependencies and additional tools:

```bash
uv sync --all-extras
```

Run the `aswfdocker` command via `uv run`:

```bash
uv run aswfdocker --help
```

### Finally

Check that the command works:

```bash
uv run aswfdocker --help
```

## Usage

### Activating the venv created by `uv`

`uv` creates a venv which you can explicitly activate to avoid having to prefix
every invocation of `aswfdocker` with `uv run`:

```bash
source .venv/bin/activate
aswfdocker --version
```

### List packages and images

List all known packages:

```bash
uv run aswfdocker packages
```

List all known images:

```bash
uv run aswfdocker images
```

## Development

### Process

First install the [pre-commit](https://pre-commit.com/) hooks by running
`uv run pre-commit install`.

The pre-commit hooks will run the following commands, which can be run
individually as well:
* Run [Black](https://github.com/psf/black) on the code to ensure formatting
  is okay: `black python`
* Run the tests to ensure everything is okay: `pytest python/aswfdocker`
* Run [mypy](http://mypy-lang.org/) to ensure static types are okay:
  `mypy python/aswfdocker`
* Run [PyLint](https://docs.pylint.org/) on the code to ensure
  linting is okay: `pylint python/aswfdocker`

To run them all manually use `pre-commit run --all-files`.

### Adding new dependencies

* Add a runtime dependency: `uv add <package>`
* Add a dev dependency: `uv add --dev <package>`
* Dependencies are declared in `pyproject.toml`; run `uv lock` after editing.
