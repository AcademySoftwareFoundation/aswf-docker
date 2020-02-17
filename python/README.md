# ASWF Python Utilities
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

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
cd aswf-docker/python
pipenv install -d -e .
pipenv shell
```
You should now be in a python `virtualenv` shell where the `aswfdocker` command is available.

### Finally
You should check the command is working:
```bash
aswfdocker --help
```

## Usage
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
Once in the `pipenv shell` you should:

* run the tests to ensure everything is OK: `pytest`
* run [mypy](http://mypy-lang.org/) to ensure static types are OK: `mypy aswfdocker`
* run `black` on the code to ensure formatting is OK: `black .`
