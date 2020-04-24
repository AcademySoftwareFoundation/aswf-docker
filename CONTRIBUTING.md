# Contributing to aswf-docker

Thank you for your interest in contributing to aswf-docker. This document
explains our contribution process and procedures:

* [Getting Information](#Getting-Information)
* [Legal Requirements](#Legal-Requirements)
* [Development Workflow](#Development-Workflow)
* [Versioning Policy](#Versioning-Policy)
* [Creating a Release](#Creating-a-Release)


## Getting Information

There are two primary ways to connect with the aswf-docker project:

* The [tac](https://lists.aswf.io/g/tac) mail list:
  This is a general mailing list which can be used to discuss CI issues, please
  use the #ci-working tag.

* [GitHub Issues](https://github.com/AcademySoftwareFoundation/aswf-docker/issues): GitHub
  Issues are used both to track bugs and to discuss feature requests.

### How to Report a Bug

aswf-docker use GitHub's issue tracking system for bugs and enhancements:
https://github.com/AcademySoftwareFoundation/aswf-docker/issues

If you are submitting a bug report, please be sure to note which
docker image you are using. Please give a specific account of

* what you tried
* what happened
* what you expected to happen instead

with enough detail that others can reproduce the problem.

### How to Request a Change

Open a GitHub issue: https://github.com/AcademySoftwareFoundation/aswf-docker/issues.

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
license. Contributions to the library should abide by that standard
license.

### Contributor License Agreements

Developers who wish to contribute code to be considered for inclusion
in the aswf-docker distribution must first complete a **Contributor
License Agreement**.

aswf-docker uses EasyCLA for managing CLAs, which automatically
checks to ensure CLAs are signed by a contributor before a commit
can be merged. 

* If you are an individual writing the code on your own time and
  you're SURE you are the sole owner of any intellectual property you
  contribute, you can [sign the CLA as an individual contributor](https://github.com/communitybridge/easycla/blob/master/contributors/sign-a-cla-as-an-individual-contributor-to-github.md).

* If you are writing the code as part of your job, or if there is any
  possibility that your employers might think they own any
  intellectual property you create, then you should use the [Corporate
  Contributor Licence
  Agreement](https://github.com/communitybridge/easycla/blob/master/contributors/contribute-to-a-github-company-project.md).

The aswf-docker CLAs are the standard forms used by Linux Foundation
projects and [recommended by the ASWF TAC](https://github.com/AcademySoftwareFoundation/tac/blob/master/process/contributing.md#contributor-license-agreement-cla).

### Commit Sign-Off

Every commit must be signed off.  That is, every commit log message
must include a “`Signed-off-by`” line (generated, for example, with
“`git commit --signoff`”), indicating that the committer wrote the
code and has the right to release it under the [Apache-2.0](LICENSE.md)
license. See https://github.com/AcademySoftwareFoundation/tac/blob/master/process/contributing.md#contribution-sign-off for more information on this requirement.

## Development Workflow

### Git Basics

Working with aswf-docker requires understanding a significant amount of
Git and GitHub based terminology. If you’re unfamiliar with these
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
to test them. The `aswfdocker` python utility wraps many of the complexities
of the Docker build process and must be installed locally before starting.
Please read the python [README.md](python/README.md) file for further instructions.

### Repository Structure and Commit Policy

The aswf-docker repository uses a simple branching and merging strategy.

All development work is done directly on the master branch. The master
branch represents the bleeding-edge of the project and most
contributions should be done on top of it.

After sufficient work is done on the master branch and the aswf-docker
leadership determines that a release is due, we will bump the relevant
internal versioning and tag a commit with the corresponding version
number, e.g. v2.0.1. Each Minor version also has its own “Release
Branch”, e.g. RB-1.1. This marks a branch of code dedicated to that
Major.Minor version, which allows upstream bug fixes to be
cherry-picked to a given version while still allowing the master
branch to continue forward onto higher versions. This basic repository
structure keeps maintenance low, while remaining simple to understand.

To reiterate, the master branch represents the latest development
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
namespace and serves as the “home base” for your development branches,
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

Contributions should be submitted as Github pull requests. See
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

4. Create a Github pull request from your topic branch.

5. Pull requests will be reviewed by project Committers and Contributors,
who may discuss, offer constructive feedback, request changes, or approve
the work.

6. Upon receiving the required number of Committer approvals (as
outlined in [Required Approvals](#required-approvals)), a Committer
other than the PR contributor may merge changes into the master
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

All functionality in the aswfdocker python library must be covered by an automated
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
[Prospector](http://prospector.landscape.io/en/master/) linter.

#### Copyright Notices

All new source files should begin with a copyright and license stating:

    # Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
    # SPDX-License-Identifier: Apache-2.0

## Versioning Policy

Any non-trivial change to the docker images should be followed by incrementing
the corresponding image version. We use MAJOR.MINOR versioning for all images.
Versioning is further explained in the [Readme](README.md#version) file.

## Releasing new Docker Images

All commits to master will trigger a rebuild and re-upload of all docker CI images
using the version number defined in the python 
[constants](https://github.com/aloysbaillet/aswf-docker/blob/master/python/aswfdocker/constants.py#L15) module.

The [CHANGELOG.md](CHANGELOG.md) file needs to be updated with the date of the change
and the list of new docker image versions that will be built by the CI infrastructure.
