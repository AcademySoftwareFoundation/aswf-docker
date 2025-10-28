# Contributing to aswf-docker

Thank you for your interest in contributing to aswf-docker. This document
explains our contribution process and procedures:

* [Getting Information](#Getting-Information)
* [Legal Requirements](#Legal-Requirements)
* [Development Workflow](#Development-Workflow)
* [Versioning Policy](#Versioning-Policy)
* [Creating a Release](#Creating-a-Release)

## Getting Information

There are three primary ways to connect with the aswf-docker project:

* The [TAC mailing list](https://lists.aswf.io/g/tac):
  This is a general mailing list which can be used to discuss CI issues, please
  use the `#ci-working` tag.

* The [ASWF Slack workspace](http://slack.aswf.io/):
  The CI working group has a channel `#wg-ci` for discussions.

* [GitHub Issues](https://github.com/AcademySoftwareFoundation/aswf-docker/issues): GitHub
  Issues are used both to track bugs and to discuss feature requests.

### How to Report a Bug

aswf-docker use GitHub's issue tracking system for bugs and enhancements:
https://github.com/AcademySoftwareFoundation/aswf-docker/issues

If you are submitting a bug report, please be sure to note which
Docker image you are using. Please give a specific account of

* what you tried
* what happened
* what you expected to happen instead

with enough detail that others can reproduce the problem.

### How to Request a Change

Open a GitHub issue: https://github.com/AcademySoftwareFoundation/aswf-docker/issues .

Describe the situation and the objective in as much detail as
possible. Feature requests will almost certainly spawn a discussion
among the project community.

### How to Contribute a Bug Fix or Change

To contribute code to the project, you will need:

* A good knowledge of git.

* A fork of the GitHub repo.

* An understanding of the project's development workflow.

* Legal authorization, that is, you need to have signed a Contributor
  License Agreement. See below for details.

## Legal Requirements

aswf-docker is a project of the Academy Software Foundation and follows the
open source software best practice policies of the Linux Foundation.

### License

aswf-docker is licensed under the [Apache-2.0](LICENSE.md)
license. Contributions to the project should abide by that standard
license.

### Commit Sign-Off

Every commit must be signed off.  That is, every commit log message
must include a "`Signed-off-by`" line (generated, for example, with
"`git commit --signoff`"), indicating that the committer wrote the
code and has the right to release it under the [Apache-2.0](LICENSE.md)
license. See [Contribution Sign-Off](https://github.com/AcademySoftwareFoundation/tac/blob/main/process/contributing.md#contribution-sign-off)
for more information on this requirement.

## Development Workflow

### Git Basics

Working with aswf-docker requires understanding a significant amount of
Git and GitHub based terminology. If you're unfamiliar with these
tools or their lingo, please look at the [GitHub
Glossary](https://help.github.com/articles/github-glossary/) or browse
[GitHub Help](https://help.github.com/).

To contribute, you need a GitHub account. This is needed in order to
push changes to the upstream repository, via a pull request.

You will also need Git installed on your local development machine. If
you need setup assistance, please see the official [Git
Documentation](https://git-scm.com/doc).

### Docker Basics

You will also need to understand how Docker images are built and how
to test them. The `aswfdocker` Python utility wraps many of the complexities
of the Docker build process and must be installed locally before starting.
Please read the Python [README.md](python/README.md) file for further instructions.

### Repository Structure and Commit Policy

The aswf-docker repository uses a simple branching and merging strategy.

All development work is done directly on the main branch. The main
branch represents the bleeding-edge of the project and most
contributions should be done on top of it.

After sufficient work is done on the main branch and the aswf-docker
leadership determines that a release is due, we will bump the relevant
internal versioning and tag a commit with the corresponding version
number, e.g. v2.0.1. Each Minor version also has its own "Release
Branch", e.g. RB-1.1. This marks a branch of code dedicated to that
Major.Minor version, which allows upstream bug fixes to be
cherry-picked to a given version while still allowing the main
branch to continue forward onto higher versions. This basic repository
structure keeps maintenance low, while remaining simple to understand.

To reiterate, the main branch represents the latest development
version, so beware that it may include untested features and is not
generally stable enough for release.  To retrieve a stable version of
the source code, use one of the release branches.

### The Git Workflow

This development workflow is sometimes referred to as
[OneFlow](https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow). It
leads to a simple, clean, linear edit history in the repo.

The aswf-docker GitHub repo allows rebase merging and disallows merge
commits and squash merging. This ensures that the repo edit history
remains linear, avoiding the "bubbles" characteristic of the
[GitFlow](https://www.endoflineblog.com/gitflow-considered-harmful)
workflow.

### Use the Fork, Luke.

In a typical workflow, you should **fork** the aswf-docker repository to
your account. This creates a copy of the repository under your user
namespace and serves as the "home base" for your development branches,
from which you will submit **pull requests** to the upstream
repository to be merged.

Once your Git environment is operational, the next step is to locally
**clone** your forked aswf-docker repository, and add a **remote**
pointing to the upstream aswf-docker repository. These topics are
covered in the GitHub documentation [Cloning a
repository](https://help.github.com/articles/cloning-a-repository/)
and [Configuring a remote for a
fork](https://help.github.com/articles/configuring-a-remote-for-a-fork/),
but again, if you need assistance feel free to reach out on the
aswf-docker-dev@lists.aswf.io mail list.

### Pull Requests

Contributions should be submitted as GitHub pull requests. See
[Creating a pull request](https://help.github.com/articles/creating-a-pull-request/)
if you're unfamiliar with this concept.

The development cycle for a code change should follow this protocol:

1. Create a topic branch in your local repository, following the naming format
"feature/<your-feature>" or "bugfix/<your-fix>".

2. Make changes, compile, and test thoroughly. Code style should match existing
style and conventions, and changes should be focused on the topic the pull
request will be addressing. Make unrelated changes in a separate topic branch
with a separate pull request.

3. Push commits to your fork.

4. Create a GitHub pull request from your topic branch.

5. Pull requests will be reviewed by project Committers and Contributors,
who may discuss, offer constructive feedback, request changes, or approve
the work.

6. Upon receiving the required number of Committer approvals (as
outlined in [Required Approvals](#required-approvals)), a Committer
other than the PR contributor may merge changes into the main
branch.

### Code Review and Required Approvals

Modifications of the contents of the aswf-docker repository are made on a
collaborative basis. Anyone with a GitHub account may propose a
modification via pull request and it will be considered by the project
Committers.

Pull requests must meet a minimum number of Committer approvals prior
to being merged. Rather than having a hard rule for all PRs, the
requirement is based on the complexity and risk of the proposed
changes, factoring in the length of time the PR has been open to
discussion. The following guidelines outline the project's established
approval rules for merging:

* Core design decisions, large new features, or anything that might be
perceived as changing the overall direction of the project should be
discussed at length in the mail list before any PR is submitted, in
order to: solicit feedback, try to get as much consensus as possible,
and alert all the stakeholders to be on the lookout for the eventual
PR when it appears.

* Small changes (bug fixes, docs, tests, cleanups) can be approved and
merged by a single Committer.

* Big changes that can alter behavior, add major features, or present
a high degree of risk should be signed off by TWO Committers, ideally
one of whom should be the "owner" for that section of the codebase (if
a specific owner has been designated). If the person submitting the PR
is him/herself the "owner" of that section of the codebase, then only
one additional Committer approval is sufficient. But in either case, a
48 hour minimum is helpful to give everybody a chance to see it,
unless it's a critical emergency fix (which would probably put it in
the previous "small fix" category, rather than a "big feature").

* Escape valve: big changes can nonetheless be merged by a single
Committer if the PR has been open for over two weeks without any
unaddressed objections from other Committers. At some point, we have
to assume that the people who know and care are monitoring the PRs and
that an extended period without objections is really assent.

Approval must be from Committers who are not authors of the change. If
one or more Committers oppose a proposed change, then the change
cannot be accepted unless:

* Discussions and/or additional changes result in no Committers
objecting to the change. Previously-objecting Committers do not
necessarily have to sign-off on the change, but they should not be
opposed to it.

### Test Policy

All functionality in the aswfdocker Python library must be covered by an automated
test.

* Any new functionality should be accompanied by a test that validates
  its behavior.

* Any change to existing functionality should have tests added if they
  don't already exist.

Pre-commit hooks need to be installed by running `pre-commit install`, and
tests can be run manually by running `pre-commit run --all-files`.

## Coding Style

#### Formatting

[Black](https://black.readthedocs.io/en/stable/) is the automatic formatter of choice
for aswf-docker and is required to be run before any commit.

#### Naming Conventions

We follow PEP-8 naming convention which is also checked before any commit by the
[PyLint](https://docs.pylint.org/) linter.

#### Copyright Notices

All new source files should begin with a copyright and license stating:

    # Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
    # SPDX-License-Identifier: Apache-2.0

## Versioning Policy

Any non-trivial change to the Docker images should be followed by incrementing
the corresponding image version. We use MAJOR.MINOR versioning for all images.
Versioning is further explained in the [README](README.md#version) file.

## Building Conan Packages

This repository contains 2 ways of building packages, Docker packages (`aswf/ci-package-*` images) and Conan packages.

The Docker packages are being phased out as Conan offers a lot more flexibility when building options and variants of packages, with great cross-platform support.

The [Conan](https://conan.io) [Reference Documentation](https://docs.conan.io/en/latest/reference.html) is a great way to discover and learn all about the Conan package manager.

The AcademySoftwareFoundation has an [Artifactory](https://linuxfoundation.jfrog.io/ui/packages) server which hosts all `aswf` Conan packages.
Credentials of the artifactory server are maintained by the Linux Foundation and are not known by the ASWF crew, new packages get uploaded via GitHub organisation secrets.

### Getting started

Use the existing recipes as an example, and borrow from the MIT-licensed
[Conan Center Index](https://github.com/conan-io/conan-center-index/tree/master/recipes).

Follow the great instructions there:
[Conan Center Index - How to add Packages](https://github.com/conan-io/conan-center-index/blob/master/docs/how_to_add_packages.md),
but ignore the `config.yml` instructions as the aswfdocker `versions.yaml` already
takes care of listing all the maintained package versions. If required `config.yml` can still be used when completely different recipes are require for
major package versions, see the `onetbb` package for an example.

Then ensure the ASWF-specific settings are added in the `conanfile.py` such as `cpython`. This project attempts to minimize local changes to the recipes which originate in the Conan Center Index. Local changes may be marked with a `# ASWF` comment. For simple recipes, the required changes may be as minimal as:

- adding a [SPDX license header](https://spdx.dev/learn/handling-license-info/) where the `From:` URL can be obtained by using the `y` hotkey in the GitHub web UI to obtain a permalink to the version of the Conan recipe file
you are basing hyour local copy on.
```
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/opencolorio/all/conanfile.py
```

- adding a `self.name` level to the `copy()` in the `package()` method: when Conan packages are "installed" in the CI build images, they are all flattened together into `/usr/local/` and without this change the license files for all the packages end up in the same directory and can overwrite each other:
```
    def package(self):
        # ASWF: separate licenses from multiple package installs
        copy(self, "LICENSE.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses", self.name))
```

- comment out the call that removes the `cmake` directory: we want to be able to use
these Conan packages outside the context of Conan, and thus want to retain the
generated `.cmake` files:
```
        # ASWF: keep cmake files, delete pkgconfig files
        # rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
```

To help minimize changes to the standard Conan recipes, Conan `profiles` are used to
override specific package versions in the recipes. For instance in
[packages/conan/settings/profiles_aswf/vfx2025](https://github.com/AcademySoftwareFoundation/aswf-docker/blob/main/packages/conan/settings/profiles_aswf/vfx2025):

```
include(ci_common5)

[settings]
[options]
# Build everything as shared libs by default
*:shared=True
[tool_requires]
[replace_requires]
b2/*: b2/5.2.1@aswf/vfx2025
boost/*: boost/1.85.0@aswf/vfx2025
brotli/*: brotli/system@aswf/vfx2025
bzip2/*: bzip2/1.0.8@aswf/vfx2025
dbus/*: dbus/system@aswf/vfx2025
...
```

Unfortunately there is duplication between the version information in
 [`versions.yaml`](https://github.com/AcademySoftwareFoundation/aswf-docker/blob/main/python/aswfdocker/data/versions.yaml) and the Conan profiles: a future update
 will auto generate the Conan profiles from `versions.yaml` which should be the
 source of truth.

When a sufficiently recent package is provided by the underlying OS distribution, packages labeled as version `system` are created which are thin wrappers around system installed components, and the Conan profile is used to remap `requires()`
call to specific versions to these wrapper packages. Confusingly some will have an actual version number since some dependent packages check for acceptable version ranges. A better versioning scheme would be desirable for these wrapper packages.

To test locally, use the `aswfdocker build` command with the `--use-conan` argument.
The `--keep-source` and `--keep-build` can help when iterating on the build recipe to
avoid re-downloading the source, and even keep the previous build artifact.
All regular aswfdocker commands and options work the same with conan or docker packages.

You can use the `aswfdocker conandiff` command to view updates in the upstream Conan Center Index recipes since the last time the local copy was updated. This requires the `From: https://...` header comment to be updated correctly.

```
$ aswfdocker conandiff
Checking conanfile.py files...

Found outdated conanfile.py:
aswf-docker/packages/conan/recipes/minizip-ng/conanfile.py:
  Package: minizip-ng
  Current SHA: 156d3592a823c0d3d297d8c365eee01f27532a49
  Found 1 newer commits:
    Commit: 7e056a381694e0fd0b791b9fd06d87d391f461c0
    Diff URL: https://github.com/conan-io/conan-center-index/commit/7e056a381694e0fd0b791b9fd06d87d391f461c0
    Timestamp: 2024-12-31 14:55:30+00:00
    Message:
      minizip-ng: add version 4.0.7 (#26112)

      * minizip-ng: add version 4.0.7

      * rename windows library names in 4.0.7
```

### Docker-only Packages

If a package has no Conan recipe folder its conan package will be skipped at release time.

### Conan-only Packages

If a package can only be built using Conan its name must be added to the `conan_only` list
at the end of the `versions.yaml` file, see `gtest` as an example.

### Peeking into the Conan cache

When building a Conan package, `aswfdocker build --use-conan` uses [common/packages/Dockerfile](https://github.com/AcademySoftwareFoundation/aswf-docker/blob/main/packages/common/Dockerfile) which uses a
[Docker Cache Mount](https://docs.docker.com/build/cache/optimize/#use-cache-mounts) to store the persistent
cache of local Conan package builds (similarly for the [ccache](https://ccache.dev/) persistent cache):

```
RUN --mount=type=cache,target=${ASWF_CONAN_HOME}/d \
    --mount=type=cache,target=${CCACHE_DIR} \
    --mount=type=bind,rw,target=${ASWF_CONAN_HOME}/.conan2,source=packages/conan/settings \
    --mount=type=bind,rw,target=${ASWF_CONAN_HOME}/recipes,source=packages/conan/recipes \
    conan create \
    ...
```

By default the Conan cache lives in the `$CONAN_HOME/p` directory (where settings and profiles also live) but we relocate it to `${ASWF_CONAN_HOME}/d` by setting `core.cache:storage_path = /opt/conan_home/d` in `global.conf`
as per [Storage Configurations](https://docs.conan.io/2/reference/config_files/global_conf.html#storage-configurations).

During development it can be convenient to peek into the results of a Conan package build. You can use:

```
$ docker buildx du --verbose --filter Type=exec.cachemount
ID:		ltu9ddgwws6cblhemncn9uzaj
Created at:	2025-03-31 03:09:21.67231777 +0000 UTC
Mutable:	true
Reclaimable:	true
Shared:		false
Size:		93.56GB
Description:	cached mount /opt/conan_home/d from exec /bin/sh -c conan create       ${ASWF_CONAN_BUILD_MISSING}       --profile:all ${ASWF_CONAN_HOME}/.conan2/profiles_${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}       --name ${ASWF_PKG_NAME}       --version ${ASWF_PKG_VERSION}       --user ${ASWF_PKG_ORG}       --channel ${ASWF_CONAN_CHANNEL}       ${ASWF_CONAN_HOME}/recipes/${ASWF_PKG_NAME} with id "//opt/conan_home/d"
Usage count:	159
Last used:	14 minutes ago
Type:		exec.cachemount
```

to retrieve the volume ID for the cache mount, which is then accessible at a path similar to:

```
/var/lib/docker/overlay2/ltu9ddgwws6cblhemncn9uzaj/diff
```

At this level you will find hashed directories for each build of each Conan package (the first 5 letters of the package named are used for those hashed directory names,
not great when so many package names start with "open"...) which contain unpacked source for the package. One level deeper in:

```
/var/lib/docker/overlay2/ltu9ddgwws6cblhemncn9uzaj/diff/b
```

you will find the build and packaging directories, and in particular for an Qt build (say):

```
$ ls /var/lib/docker/overlay2/ltu9ddgwws6cblhemncn9uzaj/diff/b/qted742db53b77e
b  d  p
```

where the `b` directory contains the output of the build and the `p` directory will contain the installable Conan package:

```
$ ls /var/lib/docker/overlay2/ltu9ddgwws6cblhemncn9uzaj/diff/b/qted742db53b77e/p
bin  conaninfo.txt  conanmanifest.txt  doc  include  lib  libexec  licenses  metatypes  mkspecs  modules  phrasebooks  plugins  qml  resources  translations
```

Be careful when trying to modify this cache directory directly, as it is managed by
Conan and tracked in a [SQLite](https://www.sqlite.org/) database.
The [`conan cache`](https://docs.conan.io/2/reference/commands/cache.html) command
should be used to explicitly manipulate the cache.

### Debugging CMake in Conan issues

Most of the Conan packages use CMake to configure and build: debugging "CMake in Conan" can sometimes be tricky, one approach is to
look for the `build()` method in the package's `conanfile.py` which minimally looks like:

```
    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
```

and enable tracing / verbose in the `configure()` and `build()` calls:

```
    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure(cli_args=["--trace"])
        cmake.build(cli_args=["--verbose"])
```

To specifically look at how `CMake` is trying to find a package, in the `generate()` method you can add:

```
    def generate(self):
        tc = CMakeToolchain(self)
        ...
        tc.cache_variables["CMAKE_FIND_DEBUG_MODE"] = "ON" # enable find debug
        tc.generate()
        cd = CMakeDeps(self)
        cd.generate()
```

## Releasing new Docker Images

The [CHANGELOG.md](CHANGELOG.md) file needs to be updated with the date of the change
and the list of new Docker image versions that will be built by the CI infrastructure.

GitHub releases will trigger a `Release` GitHub action that will build the corresponding
image and push it to Docker Hub.

### Build

`aswfdocker build` builds CI packages and CI images.
Example use: just build a single package for testing:

```bash
# Build and push USD package to aswftesting
aswfdocker --verbose build -t PACKAGE --group vfx --version 2019 --target usd --push YES
# Build and push ci-vfxall image to aswftesting
aswfdocker --verbose build -t IMAGE --group vfx --version 2019 --target vfxall --push YES
```

If you are building on system with multiple cores, you may want to set the environment variable:

```
DOCKER_BUILDKIT=1
```

before running `aswfdocker build`, as that will allow Docker BuildKit to run multiple builds in parallel. This is mostly useful when building smaller larger groups of smaller packages: when building individual large packages like Qt or Clang/LLVM,
CMake will run parallel compiles. `DOCKER_BUILDKIT=1` is set when building on GitHub Actions.

### Migrate

`aswfdocker migrate` can migrate images between Docker organizations, should only be used on package images
that are very heavy to build such as clang or qt.
Example use: migrate a single package from `aswftesting` to `aswf` Docker Hub organization.

```bash
aswfdocker --verbose migrate --from aswftesting --to aswf --package usd
```

### Updating versions

If a version number of a package or an image needs to be updated, the `versions.yaml` file is the main data source.
In order to update the templated images with updated version numbers, run `aswfdocker dockergen`.

### Manually push new packages

When rebuilding all packages from the CI is overkill, and if you have access to the right Docker Hub organizations, it is possible
to manually build and push packages and images by overriding the automatic discovery of current repo and branch.
E.g. to build and push a new `ninja` package these commands can be run to push to `aswf` and `aswftesting` organizations:

```bash
# push to aswftesting
aswfdocker --verbose --repo-uri https://github.com/AcademySoftwareFoundation/aswf-docker --source-branch refs/heads/testing build -t PACKAGE --group common --version 1 --target ninja --push YES
# push to aswf
aswfdocker --verbose --repo-uri https://github.com/AcademySoftwareFoundation/aswf-docker --source-branch refs/heads/main build -t PACKAGE --group common --version 1 --target ninja --push YES
```

### Manual GitHub release creation

* Create a new release in [GitHub New Release](https://github.com/AcademySoftwareFoundation/aswf-docker/releases/new)
    * Use the following tag format: `ci-NAME:X.Y` (e.g. `ci-common:1.4`)
    * Use the following release name format: `aswf/ci-NAME:X.Y` (e.g. `aswf/ci-common:1.4`)
    * Enter the release notes for that particular image
    * Click Create
* Run a manual build in GitHub Actions on the specific tagged commit created before

### Automatic GitHub release creation

* Generate a GitHub token to allow `aswfdocker release` to create GitHub releases:
  [GitHub Settings](https://github.com/settings/tokens) with **"repo"** permissions.
* Configure the token in the `aswfdocker` settings by running:
  ```bash
  aswfdocker settings --github-access-token MYTOKEN
  ```
* Run the `release` command for a given image:
  ```bash
  aswfdocker release -n aswftesting/ci-base:2021
  ```
  or for a whole group of images:
  ```bash
  aswfdocker release -t PACKAGE -g base1 -v 2018 --docker-org aswftesting -m "Testing release"
  ```

An email address must be publicly visible in your GitHub profile in order for the [PyGithub module](https://github.com/PyGithub/PyGithub) used
by `aswfdocker` to work. For pre-releases you can use the `--sha` option to build from a specific commit.

### Adding a new `ci` image

Let's consider the addition of a new `ci-xyz` Docker image to help the maintainers of the `xyz` library. The `ci-xyz` Docker image
should be prepared with most upstream dependencies of the `xyz` library.

It is usually a good idea to add this `xyz` package to the `vfxall` library so that it can be tested there.

* Add a new `xyz` version section in the `versions.yaml`, for both the `ci-package-xyz` Docker package and the `ci-xyz` for the CI image.
* Create a new `ci-xyx/Dockerfile` using an existing one as an example (e.g. `ci-otio/Dockerfile`).
* Create a new `scripts/vfx/build_xyz.sh` file that builds and installs `xyz` from source.
* Add a new `xyz` section at the end of the `packages/Dockerfile` file to build the `ci-package-xyz` Docker package using the previous script.
* Add the `xyz` package to the `ci-vfxall/Dockerfile` image.
* Test the scripts by running these commands in order and manually checking if everything works
  ```bash
  # Build the CI image
  aswfdocker build -n aswftesting/ci-xyz:2019
  # Build the CI package (a small Docker image that contains only the xyz build artifacts)
  aswfdocker build -n aswftesting/ci-package-xyz:2019 --progress plain
  # Buils the `vfxall` package that should now contain the `xyz` package
  aswfdocker build -n aswftesting/ci-vfxall:2019
  # Now run the vfxall image locally to test if xyz is working properly
  docker run --gpus=all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v `pwd`:/project --rm -it aswftesting/ci-vfxall:2019 bash
  ```
* Do a pre-release of the new `ci-package-xyz` image so it can be used by the GitHub Action builds and tests:
  ```bash
  # Create a GitHub release to build the `ci-package-xyz:2___` image via a GitHub action
  aswfdocker release -n aswftesting/ci-package-xyz:2019 --sha `git rev-parse HEAD` --github-org MY_GITHUB_ORG
  aswfdocker release -n aswftesting/ci-package-xyz:2020 --sha `git rev-parse HEAD` --github-org MY_GITHUB_ORG
  aswfdocker release -n aswftesting/ci-package-xyz:2021 --sha `git rev-parse HEAD` --github-org MY_GITHUB_ORG
  ```
* Create the Pull Request with these changes

Check [#66](https://github.com/AcademySoftwareFoundation/aswf-docker/pull/66) for an example.

### Example of a large re-release of all supported images

```bash
# Image for building Conan packages
aswfdocker release -t IMAGE -g baseos-gl-conan -v 4 -v 5 -v 6 --target baseos-gl-conan --docker-org aswf -m "RELEASE_NOTES!"

# Common packages
aswfdocker release -t PACKAGE -g common -v 4 -v 5 -v 6 --target ninja -target cmake --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g common -v 4-clang16 -v 4-clang17 -v 5-clang18 -v 5-clang19 -v 6-clang19 -v 6-clang20 --target clang --docker-org aswf -m "RELEASE_NOTES!"
# Wait for clang builds to finish (from 2 to 3 hours!)

# ci-common needs to be built before base packages can be built
aswfdocker release -t IMAGE -g common -v 4-clang16 -v 4-clang17 -v 5-clang18 -v 5-clang19 -v 6-clang19 -v 6-clang20 --docker-org aswf -m "RELEASE_NOTES!"

# Base packages
aswfdocker release -t PACKAGE -g base1-wrappers -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g base1-1 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g base1-2 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g base1-3 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"

aswfdocker release -t PACKAGE -g base2-wrappers -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g base2-2 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
# Wait for Qt builds to finish (2-6 hours!)

# Usually some Qt build will fail as too big and too slow for free GitHub actions... So here's how to build qt locally:
# This is no longer valid, as Qt is now only build as a Conan package
aswfdocker --repo-uri https://github.com/AcademySoftwareFoundation/aswf-docker --source-branch refs/heads/main --verbose build -n aswf/ci-package-qt:2025
docker push aswf/ci-package-qt:2025
docker push aswf/ci-package-qt:2025-6.5.4
docker push aswf/ci-package-qt:preview
docker push aswf/ci-package-qt:2025.0

# Once all Qt are out, release PySide packages
aswfdocker release -t PACKAGE -g base3 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"

# Wait for all Qt and Pyside builds to finish, then build downstream packages:
# VFX packages
aswfdocker release -t PACKAGE -g vfx1-wrappers -g vfx1-1 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g vfx1-2 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g vfx1-3 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g vfx1-4 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g vfx1-5 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g vfx2-1 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t PACKAGE -g vfx2 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"

# Finally build the CI images
aswfdocker release -t IMAGE -g base -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t IMAGE -g vfx1 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t IMAGE -g vfx2 -v 2024 -v 2025 -v 2026 --docker-org aswf -m "RELEASE_NOTES!"
aswfdocker release -t IMAGE -g vfx3 -v 2024-clang16 -v 2024-clang17 -v 2025-clang18 -v 2025-clang19 -v 2026-clang19 -v 2026-clang20 --docker-org aswf -m "RELEASE_NOTES!"
```
