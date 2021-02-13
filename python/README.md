# ASWF Python Utilities
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![pytest coverage](https://img.shields.io/azure-devops/coverage/academysoftwarefoundation/Academy%20Software%20Foundation/2/master)

The `aswfdocker` command line tool is available to help with package and image builds.

## Installation

### For users:
```bash
git clone https://github.com/AcademySoftwareFoundation/aswf-docker
cd aswf-docker
python3 setup.py install
```

### For developers:
First install [pipenv](https://github.com/pypa/pipenv) for Python 3: `pip3 install pipenv`.
Then:
```bash
git clone https://github.com/AcademySoftwareFoundation/aswf-docker
cd aswf-docker
pipenv shell
pipenv install --dev
```
You should now be in a python `virtualenv` shell where the `aswfdocker` command is available.

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
Once in the `pipenv shell` you should first install the [pre-commit](https://pre-commit.com/) hooks by running `pre-commit install`
The pre-commit hooks will run the following commands, which can be run individually as well:
* run `black` on the code to ensure formatting is OK: `black python`
* run the tests to ensure everything is OK: `pytest python/aswfdocker`
* run [mypy](http://mypy-lang.org/) to ensure static types are OK: `mypy python/aswfdocker`
* run `prospector` on the code to ensure linting is OK: `prospector -P aswfdocker -F python/aswfdocker`

To run them all manually use `pre-commit run --all-files`.

### Adding new pip dependencies
* Run `pipenv install xyz`
* Run `pipenv-setup sync` to update `setup.py` with added dependency (`pipenv-setup` is a "dev" dependency already declared in `PipFile`)
