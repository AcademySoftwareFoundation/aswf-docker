# ASWF Python Utilities

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![pytest coverage](https://img.shields.io/azure-devops/coverage/academysoftwarefoundation/Academy%20Software%20Foundation/2/master)

The `aswfdocker` command line tool is available to help with package and
image builds.

## Installation

### For users

Clone this repository and run the setup:

```bash
git clone https://github.com/AcademySoftwareFoundation/aswf-docker
cd aswf-docker
python3 setup.py install
```

### For developers

Install [pipenv](https://github.com/pypa/pipenv) for Python 3 first:

```bash
pip3 install pipenv
```

Then clone this repository, start the pipenv shell and install the
dev dependencies:

```bash
git clone https://github.com/AcademySoftwareFoundation/aswf-docker
cd aswf-docker
pipenv shell
pipenv install --dev
```

You should now be in a Python `virtualenv` shell where the `aswfdocker`
command is available.

### Finally

You should check the command is working:

```bash
aswfdocker --help
```

## Usage

### List packages and images

List all known packages:

```bash
aswfdocker packages
```

List all known images:

```bash
aswfdocker images
```

## Development

### Process

Once in the `pipenv shell` you should first install the
[pre-commit](https://pre-commit.com/) hooks by running `pre-commit install`.

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

### Adding new pip dependencies

* Run `pipenv install xyz`
* Run `pipenv-setup sync` to update `setup.py` with added dependency
  (`pipenv-setup` is a "dev" dependency already declared in `Pipfile`)
