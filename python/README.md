# ASWF Python Utilities
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![pytest coverage](https://img.shields.io/azure-devops/coverage/academysoftwarefoundation/Academy%20Software%20Foundation/2/master)

The `aswfdocker` command line tool is available to help with package and image builds.

## Installation

### For users:
```bash
git clone https://github.com/AcademySoftwareFoundation/aswf-docker
cd aswf-docker/python
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

### Build
`aswfdocker build` builds ci packages and ci images.
Example use: just build a single package for testing:
```bash
# Build and push USD package to aswftesting
aswfdocker --verbose build -t PACKAGE --group-name vfx --group-version 2019 --target usd --push
# Build and push ci-vfxall image to aswftesting
aswfdocker --verbose build -t IMAGE --group-name vfx --group-version 2019 --target vfxall --push
```

### Migrate
`aswfdocker migrate` can migrate packages between docker organisations.
Example use: migrate a single package from `aswftesting` to `aswf` dockerhub organisation.
```bash
aswfdocker --verbose migrate --from aswftesting --to aswf --package usd
```

### Development

Once in the `pipenv shell` you should first install the [pre-commit](https://pre-commit.com/) hooks by running `pre-commit install`
The pre-commit hooks will run the following commands, which can be run individually as well:
* run `black` on the code to ensure formatting is OK: `black python`
* run the tests to ensure everything is OK: `pytest python/aswfdocker`
* run [mypy](http://mypy-lang.org/) to ensure static types are OK: `mypy python/aswfdocker`
* run `prospector` on the code to ensure linting is OK: `prospector -F python/aswfdocker`

To run them all manually use `pre-commit run --all-files`.
