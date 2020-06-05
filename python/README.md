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

### Manually push new packages
When rebuilding all packages from the CI is overkill, and if you have access to the right dockerhub organisations, it is possible
to manually build and push packages and images by overriding the automatic discovery of current repo and branch.
E.g. to build and push a new `ninja` package these commands can be run to push to `aswf` and `aswftesting` organisations:

```bash
# push to aswftesting
aswfdocker --verbose --repo-uri https://github.com/AcademySoftwareFoundation/aswf-docker --source-branch refs/heads/testing build -t PACKAGE --group-name common --group-version 1 --target ninja --push
# push to aswf
aswfdocker --verbose --repo-uri https://github.com/AcademySoftwareFoundation/aswf-docker --source-branch refs/heads/master build -t PACKAGE --group-name common --group-version 1 --target ninja --push
```

## New Image Release

### Manual GitHub release creation
* Create a new release in [GitHub New Release](https://github.com/AcademySoftwareFoundation/aswf-docker/releases/new)
    * Use the following tag format: `ci-NAME:X.Y` (e.g. `ci-common:1.4`)
    * Use the following release name format: `aswf/ci-NAME:X.Y` (e.g. `aswf/ci-common:1.4`)
    * Enter the release notes for that particular image
    * Click Create
* Run a manual build in Azure on the specific tagged commit created before

### Automatic GitHub release creation
* 
* Generate a GitHub token to allow `aswfdocker release` to create GitHub releases: [GitHub Settings](https://github.com/settings/tokens) with **"repo"** permissions.
* Configure the token in the `aswfdocker` settings by running:
    `aswfdocker settings --github-access-token MYTOKEN`.
* 