# Docker Images for the Academy Software Foundation

[![License](https://img.shields.io/github/license/AcademySoftwareFoundation/aswf-docker)](https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)  
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=AcademySoftwareFoundation_aswf_docker&metric=coverage)](https://sonarcloud.io/dashboard?id=AcademySoftwareFoundation_aswf_docker) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=AcademySoftwareFoundation_aswf_docker&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=AcademySoftwareFoundation_aswf_docker)  
[![Test Build Docker Images](https://github.com/AcademySoftwareFoundation/aswf-docker/workflows/Test%20Build%20Docker%20Images/badge.svg)](https://github.com/AcademySoftwareFoundation/aswf-docker/actions?query=workflow%3A%22Test+Build+Docker+Images%22) [![Test Python aswfdocker Library](https://github.com/AcademySoftwareFoundation/aswf-docker/workflows/Test%20Python%20aswfdocker%20Library/badge.svg)](https://github.com/AcademySoftwareFoundation/aswf-docker/actions?query=workflow%3A%22Test+Python+aswfdocker+Library%22)  

More information:
* [VFXPlatform](https://vfxplatform.com)
* [ASWF](https://aswf.io)

Changes are documented in [CHANGELOG.md](CHANGELOG.md)

## CI Images

These images are for Continuous Integration testing of various project managed by the ASWF.
Each image (apart from `ci-common`) is available for multiple VFX Platform Years.

| Image  | Stats | Description |
| ------ | ----- | ----------- |
| [aswf/ci-common:1](https://hub.docker.com/r/aswf/ci-common/tags?name=1) ![Image Version](https://img.shields.io/docker/v/aswf/ci-common/latest) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-common/latest) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-common) | A base CentOS-7 image with devtoolset-6 (GCC-6.3.1), clang-7 and cuda-10.2. |
| [aswf/ci-common:2](https://hub.docker.com/r/aswf/ci-common/tags?name=2) ![Image Version](https://img.shields.io/docker/v/aswf/ci-common/preview) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-common/preview) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-common) | A base CentOS-7 image with devtoolset-9.1 (GCC-9.3.1), clang-10 and cuda-11. |
| [aswf/ci-base:2018](https://hub.docker.com/r/aswf/ci-base/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:1` with most VFX Platform requirements pre-installed. |
| [aswf/ci-base:2019](https://hub.docker.com/r/aswf/ci-base/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:1` with most VFX Platform requirements pre-installed. |
| [aswf/ci-base:2020](https://hub.docker.com/r/aswf/ci-base/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:1` with most VFX Platform requirements pre-installed. |
| [aswf/ci-base:2021](https://hub.docker.com/r/aswf/ci-base/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:2` with most VFX Platform requirements pre-installed. |
| [aswf/ci-openexr:2018](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:1`, comes with all OpenEXR upstream dependencies pre-installed. |
| [aswf/ci-openexr:2019](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:1`, comes with all OpenEXR upstream dependencies pre-installed. |
| [aswf/ci-openexr:2020](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:1`, comes with all OpenEXR upstream dependencies pre-installed. |
| [aswf/ci-openexr:2021](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:2`, comes with all OpenEXR upstream dependencies pre-installed. |
| [aswf/ci-ocio:2018](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:1`, comes with all OpenColorIO upstream dependencies pre-installed. |
| [aswf/ci-ocio:2019](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:1`, comes with all OpenColorIO upstream dependencies pre-installed. |
| [aswf/ci-ocio:2020](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:1`, comes with all OpenColorIO upstream dependencies pre-installed. |
| [aswf/ci-ocio:2021](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:2`, comes with all OpenColorIO upstream dependencies pre-installed. |
| [aswf/ci-opencue:2018](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:1`, comes with all OpenCue upstream dependencies pre-installed. |
| [aswf/ci-opencue:2019](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:1`, comes with all OpenCue upstream dependencies pre-installed. |
| [aswf/ci-opencue:2020](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:1`, comes with all OpenCue upstream dependencies pre-installed. |
| [aswf/ci-opencue:2021](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:2`, comes with all OpenCue upstream dependencies pre-installed. |
| [aswf/ci-openvdb:2018](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:1`, comes with all OpenVDB upstream dependencies pre-installed. |
| [aswf/ci-openvdb:2019](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:1`, comes with all OpenVDB upstream dependencies pre-installed. |
| [aswf/ci-openvdb:2020](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:1`, comes with all OpenVDB upstream dependencies pre-installed. |
| [aswf/ci-openvdb:2021](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:2`, comes with all OpenVDB upstream dependencies pre-installed. |
| [aswf/ci-usd:2019](https://hub.docker.com/r/aswf/ci-usd/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:1`, comes with all USD upstream dependencies pre-installed. |
| [aswf/ci-usd:2020](https://hub.docker.com/r/aswf/ci-usd/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:1`, comes with all USD upstream dependencies pre-installed. |
| [aswf/ci-usd:2021](https://hub.docker.com/r/aswf/ci-usd/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:2`, comes with all USD upstream dependencies pre-installed. |
| [aswf/ci-osl:2018](https://hub.docker.com/r/aswf/ci-osl/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:1`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| [aswf/ci-osl:2019](https://hub.docker.com/r/aswf/ci-osl/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:1`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| [aswf/ci-osl:2020](https://hub.docker.com/r/aswf/ci-osl/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:1`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| [aswf/ci-osl:2021](https://hub.docker.com/r/aswf/ci-osl/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:2`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| [aswf/ci-vfxall:2019](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:1`, comes with most VFX packages pre-installed. |
| [aswf/ci-vfxall:2020](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:1`, comes with most VFX packages pre-installed. |
| [aswf/ci-vfxall:2021](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:2`, comes with most VFX packages pre-installed. |

### Versions

The `ASWF_VFXPLATFORM_VERSION` is the calendar year mentioned in the
VFX Platform, e.g. `2019`.

The `ASWF_VERSION` is a semantic version made of the `ASWF_VFXPLATFORM_VERSION`
as the major version number, and a minor version number to indicate minor
changes in the Docker Image that still point to the same calendar year version,
e.g. `2019.0` would be followed if necessary by a `2019.1` version.
The minor version here does *not* point to a calendar month or quarter, it is
solely to express that the image has changed internally. We could also have a
patch version.

### Image Tags

The most precise version tag is the `ASWF_VERSION` of the image, e.g.
`aswf/ci-base:2019.0`, but it is recommended to use the
`ASWF_VFXPLATFORM_VERSION` as the tag to use in CI pipelines, e.g.
`aswf/ci-openexr:2019`.

The `latest` tag is pointing to the current VFX Platform year images, e.g.
`aswf/ci-openexr:latest` points to `aswf/ci-openexr:2019.0` but will be
updated to point to `aswf/ci-openexr:2020.0` in the calendar year 2020.

## Testing Images

There is another Docker Hub organization with copies of the `aswf` Docker
images called `aswftesting`, images published there are for general testing and
experimentation. Images can be pushed by any fork of the official repo as long
as the branch is called `testing`. Images in this org will change without
notice and could be broken in many unexpected ways!

To get write access to the `aswftesting` Docker Hub organization you can open
a Jira issue [there](https://jira.aswf.io).

### Status

As of December 2020 there are full 2018, 2019 and 2020
[VFX Platform](https://vfxplatform.com) compliant images. A preview of 2021
with GCC 9.3.1 (DTS 9.1), Clang 10 and CUDA 11 is also available.

## CI Packages

In order to decouple the building of packages (which can take a lot of time,
such as clang, Qt and USD) from the management of the CI Images, the packages
are built and stored into "scratch" Docker images that can be "copied" into the
CI images at image build time by Docker.

Storing these CI packages into Docker images has the additional benefit of
being completely free to store on the Docker Hub repository.
The main negative point about this way of storing build artifacts is that
tarballs are not available directly to download. It is very trivial to generate
one and the provided `download-package.sh` script can be used to generate a
local tarball from any package.

Also, CI packages are built using experimental Docker syntax that allows cache
folders to be mounted at build time, and is built with `docker buildx`. The new
Docker BuildKit system allows the building of many packages in parallel in an
efficient way with support for [ccache](https://ccache.dev/).

## Python Utilities

Check [aswfdocker](python/README.md) for python utility usage.

## Manual Builds

To build packages and images locally follow the instructions to install the
[aswfdocker](python/README.md) python utility.

### Packages

Packages require a recent Docker version with
[buildx](https://docs.docker.com/buildx/working-with-buildx/) installed and
enabled.

To build all packages (very unlikely to succeed unless run on a very very
powerful machine!):

```bash
aswfdocker --verbose build -t PACKAGE
```

To build a single package, e.g. USD:

```bash
# First list the available CI packages to know which package belong to which "group":
aswfdocker packages
# Then run the build
aswfdocker --verbose build -t PACKAGE --group vfx --version 2019 --target usd
# Or the simpler but less flexible syntax:
aswfdocker build -n aswftesting/ci-package-usd:2019
```

### Images
Images can be built with recent Docker versions but do not require
[buildx](https://docs.docker.com/buildx/working-with-buildx/) but it is
recommended to speed up large builds.

To build all images (very unlikely to succeed unless run on a very very powerful machine!):

```bash
aswfdocker --verbose build -t IMAGE
```

To build a single image:

```bash
# First list the available CI images to know which package belong to which "group":
aswfdocker images
# Then run the build
aswfdocker --verbose build -t IMAGE --group vfx1 --version 2019 --target openexr
# Or the simpler but less flexible syntax:
aswfdocker build -n aswftesting/ci-openexr:2019
```
