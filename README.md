# Docker Images for the Academy Software Foundation

[![License](https://img.shields.io/github/license/AcademySoftwareFoundation/aswf-docker)](https://github.com/AcademySoftwareFoundation/aswf-docker/blob/main/LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)  
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=AcademySoftwareFoundation_aswf-docker&metric=coverage)](https://sonarcloud.io/dashboard?id=AcademySoftwareFoundation_aswf-docker) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=AcademySoftwareFoundation_aswf-docker&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=AcademySoftwareFoundation_aswf-docker)  
[![Test Build Docker Images](https://github.com/AcademySoftwareFoundation/aswf-docker/workflows/Test%20Build%20Docker%20Images/badge.svg)](https://github.com/AcademySoftwareFoundation/aswf-docker/actions?query=workflow%3A%22Test+Build+Docker+Images%22) [![Test Python aswfdocker Library](https://github.com/AcademySoftwareFoundation/aswf-docker/workflows/Test%20Python%20aswfdocker%20Library/badge.svg)](https://github.com/AcademySoftwareFoundation/aswf-docker/actions?query=workflow%3A%22Test+Python+aswfdocker+Library%22)  

More information:
* [VFXPlatform](https://vfxplatform.com)
* [ASWF](https://aswf.io)

Changes are documented in [CHANGELOG.md](CHANGELOG.md)

## CI Images

These images are for Continuous Integration testing of various project managed by the ASWF. Each image is available for multiple VFX Platform Years, some versions of `ci-common` are common to multiple VFX Platform Years. Docker Hub stats do not break down pull count statistics per image tag, the pull count is an aggregate for all tags of an image.

The `ci-packagename` image contains all the dependencies required to build `packagename` and is meant to be used in that package's CI process, it does not include the package itself. The `ci-vfxall` image contains builds of every package, installed in `/usr/local`.

| Image | Image Version | Stats | Description |
| ----- | ------------- | ----- | ----------- |
| [aswf/ci-common](https://hub.docker.com/r/aswf/ci-common) | [aswf/ci-common:1](https://hub.docker.com/r/aswf/ci-common/tags?name=1) ![Image Version](https://img.shields.io/docker/v/aswf/ci-common/1) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-common/1) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-common) | A base CentOS-7 image with devtoolset-6 (GCC-6.3.1), clang-6-10 and cuda-10.2. |
| | [aswf/ci-common:2](https://hub.docker.com/r/aswf/ci-common/tags?name=2) ![Image Version](https://img.shields.io/docker/v/aswf/ci-common/2) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-common/2) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-common) | A base CentOS-7 image with devtoolset-9.1 (GCC-9.3.1), clang-10-14 and cuda-11.4. |
| | [aswf/ci-common:3](https://hub.docker.com/r/aswf/ci-common/tags?name=3) ![Image Version](https://img.shields.io/docker/v/aswf/ci-common/3) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-common/3) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-common) | A base RockyLinux-8 image with gcc-toolset-11 (GCC-11.2.x), clang-14-15 and cuda-11.8. |
| | [aswf/ci-common:4](https://hub.docker.com/r/aswf/ci-common/tags?name=4) ![Image Version](https://img.shields.io/docker/v/aswf/ci-common/4) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-common/4) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-common) | A base RockyLinux-8 image with gcc-toolset-11 (GCC-11.2.x), clang-16-17 and cuda-12.6.3. |
| | [aswf/ci-common:5](https://hub.docker.com/r/aswf/ci-common/tags?name=5) ![Image Version](https://img.shields.io/docker/v/aswf/ci-common/5) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-common/5) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-common) | A base RockyLinux-8 image with gcc-toolset-11 (GCC-11.2.x), clang-18-19 and cuda-12.6.3. |
| | [aswf/ci-common:6](https://hub.docker.com/r/aswf/ci-common/tags?name=6) ![Image Version](https://img.shields.io/docker/v/aswf/ci-common/6) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-common/6) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-common) | A base RockyLinux-9 image with gcc-toolset-14 (GCC-14.2.x), clang-19-20 and cuda-12.9.1. |
| [aswf/ci-base](https://hub.docker.com/r/aswf/ci-base) | [aswf/ci-base:2018](https://hub.docker.com/r/aswf/ci-base/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:1` with most VFX Platform requirements pre-installed. |
| | [aswf/ci-base:2019](https://hub.docker.com/r/aswf/ci-base/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:1: with most VFX Platform requirements pre-installed. |
| | [aswf/ci-base:2020](https://hub.docker.com/r/aswf/ci-base/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:1: with most VFX Platform requirements pre-installed. |
| | [aswf/ci-base:2021](https://hub.docker.com/r/aswf/ci-base/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:2` with most VFX Platform requirements pre-installed. |
| | [aswf/ci-base:2022](https://hub.docker.com/r/aswf/ci-base/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:2` with most VFX Platform requirements pre-installed. |
| | [aswf/ci-base:2023](https://hub.docker.com/r/aswf/ci-base/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:3` with most VFX Platform requirements pre-installed. |
| | [aswf/ci-base:2024](https://hub.docker.com/r/aswf/ci-base/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:4` with most VFX Platform requirements pre-installed. |
| | [aswf/ci-base:2025](https://hub.docker.com/r/aswf/ci-base/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:5` with most VFX Platform requirements pre-installed. |
| | [aswf/ci-base:2026](https://hub.docker.com/r/aswf/ci-base/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-base/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-base/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-base) | Based on `aswf/ci-common:6` with most VFX Platform requirements pre-installed. |
| [aswf/ci-baseqt](https://hub.docker.com/r/aswf/ci-baseqt) | [aswf/ci-baseqt:2018](https://hub.docker.com/r/aswf/ci-baseqt/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-baseqt/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-baseqt/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-baseqt) | Based on `aswf/ci-common:1` with most VFX Platform requirements pre-installed with Qt and PySide. |
| | [aswf/ci-baseqt:2019](https://hub.docker.com/r/aswf/ci-baseqt/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-baseqt/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-baseqt/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-baseqt) | Based on `aswf/ci-common:1: with most VFX Platform requirements pre-installed with Qt and PySide. |
| | [aswf/ci-baseqt:2020](https://hub.docker.com/r/aswf/ci-baseqt/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-baseqt/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-baseqt/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-baseqt) | Based on `aswf/ci-common:1: with most VFX Platform requirements pre-installed with Qt and PySide. |
| | [aswf/ci-baseqt:2021](https://hub.docker.com/r/aswf/ci-baseqt/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-baseqt/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-baseqt/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-baseqt) | Based on `aswf/ci-common:2` with most VFX Platform requirements pre-installed with Qt and PySide. |
| | [aswf/ci-baseqt:2022](https://hub.docker.com/r/aswf/ci-baseqt/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-baseqt/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-baseqt/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-baseqt) | Based on `aswf/ci-common:2` with most VFX Platform requirements pre-installed with Qt and PySide. |
| | [aswf/ci-baseqt:2023](https://hub.docker.com/r/aswf/ci-baseqt/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-baseqt/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-baseqt/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-baseqt) | Based on `aswf/ci-common:3` with most VFX Platform requirements pre-installed with Qt and PySide. |
| | [aswf/ci-baseqt:2024](https://hub.docker.com/r/aswf/ci-baseqt/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-baseqt/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-baseqt/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-baseqt) | Based on `aswf/ci-common:4` with most VFX Platform requirements pre-installed with Qt and Pyside. |
| | [aswf/ci-baseqt:2025](https://hub.docker.com/r/aswf/ci-baseqt/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-baseqt/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-baseqt/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-baseqt) | Based on `aswf/ci-common:5` with most VFX Platform requirements pre-installed with Qt and PySide. |
| | [aswf/ci-baseqt:2026](https://hub.docker.com/r/aswf/ci-baseqt/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-baseqt/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-baseqt/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-baseqt) | Based on `aswf/ci-common:6` with most VFX Platform requirements pre-installed with Qt and PySide. |
| [aswf/ci-imath](https://hub.docker.com/r/aswf/ci-imath) | [aswf/ci-imath:2024](https://hub.docker.com/r/aswf/ci-imath/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-imath/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-imath/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-imath) | Based on `aswf/ci-common:4`, comes with all Imath upstream dependencies pre-installed. |
| | [aswf/ci-imath:2025](https://hub.docker.com/r/aswf/ci-imath/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-imath/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-imath/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-imath) | Based on `aswf/ci-common:5`, comes with all Imath upstream dependencies pre-installed. |
| | [aswf/ci-imath:2026](https://hub.docker.com/r/aswf/ci-imath/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-imath/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-imath/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-imath) | Based on `aswf/ci-common:6`, comes with all Imath upstream dependencies pre-installed. |
| [aswf/ci-openexr](https://hub.docker.com/r/aswf/ci-openexr) | [aswf/ci-openexr:2018](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:1`, comes with all Imath and OpenEXR upstream dependencies pre-installed. |
| | [aswf/ci-openexr:2019](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:1`, comes with all Imath and OpenEXR upstream dependencies pre-installed. |
| | [aswf/ci-openexr:2020](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:1`, comes with all Imath and OpenEXR upstream dependencies pre-installed. |
| | [aswf/ci-openexr:2021](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:2`, comes with all Imath and OpenEXR upstream dependencies pre-installed. |
| | [aswf/ci-openexr:2022](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:2`, comes with all Imath and OpenEXR upstream dependencies pre-installed. |
| | [aswf/ci-openexr:2023](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:3`, comes with all Imath and OpenEXR upstream dependencies pre-installed. |
| | [aswf/ci-openexr:2024](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:4`, comes with all OpenEXR upstream dependencies pre-installed. |
| | [aswf/ci-openexr:2025](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:5`, comes with all OpenEXR upstream dependencies pre-installed. |
| | [aswf/ci-openexr:2026](https://hub.docker.com/r/aswf/ci-openexr/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openexr/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openexr/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openexr) | Based on `aswf/ci-common:6`, comes with all OpenEXR upstream dependencies pre-installed. |
| [aswf/ci-ocio](https://hub.docker.com/r/aswf/ci-ocio) | [aswf/ci-ocio:2018](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:1`, comes with all OpenColorIO upstream dependencies pre-installed. |
| | [aswf/ci-ocio:2019](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:1`, comes with all OpenColorIO upstream dependencies pre-installed. |
| | [aswf/ci-ocio:2020](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:1`, comes with all OpenColorIO upstream dependencies pre-installed. |
| | [aswf/ci-ocio:2021](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:2`, comes with all OpenColorIO upstream dependencies pre-installed. |
| | [aswf/ci-ocio:2022](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:2`, comes with all OpenColorIO upstream dependencies pre-installed. |
| | [aswf/ci-ocio:2023](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:3`, comes with all OpenColorIO upstream dependencies pre-installed. |
| | [aswf/ci-ocio:2024](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:4`, comes with all OpenColorIO upstream dependencies pre-installed. |
| | [aswf/ci-ocio:2025](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:5`, comes with all OpenColorIO upstream dependencies pre-installed. |
| | [aswf/ci-ocio:2026](https://hub.docker.com/r/aswf/ci-ocio/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-ocio/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-ocio/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-ocio) | Based on `aswf/ci-common:6`, comes with all OpenColorIO upstream dependencies pre-installed. |
| [aswf/ci-opencue](https://hub.docker.com/r/aswf/ci-opencue) | [aswf/ci-opencue:2018](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:1`, comes with all OpenCue upstream dependencies pre-installed. |
| | [aswf/ci-opencue:2019](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:1`, comes with all OpenCue upstream dependencies pre-installed. |
| | [aswf/ci-opencue:2020](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:1`, comes with all OpenCue upstream dependencies pre-installed. |
| | [aswf/ci-opencue:2021](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:2`, comes with all OpenCue upstream dependencies pre-installed. |
| | [aswf/ci-opencue:2022](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:2`, comes with all OpenCue upstream dependencies pre-installed. |
| | [aswf/ci-opencue:2023](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:3`, comes with all OpenCue upstream dependencies pre-installed. |
| | [aswf/ci-opencue:2024](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:4`, comes with all OpenCue upstream dependencies pre-installed. |
| | [aswf/ci-opencue:2025](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:5`, comes with all OpenCue upstream dependencies pre-installed. |
| | [aswf/ci-opencue:2026](https://hub.docker.com/r/aswf/ci-opencue/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-opencue/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-opencue/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-opencue) | Based on `aswf/ci-common:6`, comes with all OpenCue upstream dependencies pre-installed. |
| [aswf/ci-openvdb](https://hub.docker.com/r/aswf/ci-openvdb) | [aswf/ci-openvdb:2018](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:1`, comes with all OpenVDB upstream dependencies pre-installed. |
| | [aswf/ci-openvdb:2019](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:1`, comes with all OpenVDB upstream dependencies pre-installed. |
| | [aswf/ci-openvdb:2020](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:1`, comes with all OpenVDB upstream dependencies pre-installed. |
| | [aswf/ci-openvdb:2021](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:2`, comes with all OpenVDB upstream dependencies pre-installed. |
| | [aswf/ci-openvdb:2022](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:2`, comes with all OpenVDB upstream dependencies pre-installed. |
| | [aswf/ci-openvdb:2023](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:3`, comes with all OpenVDB upstream dependencies pre-installed. |
| | [aswf/ci-openvdb:2024](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:4`, comes with all OpenVDB upstream dependencies pre-installed. |
| | [aswf/ci-openvdb:2025](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:5`, comes with all OpenVDB upstream dependencies pre-installed. |
| | [aswf/ci-openvdb:2026](https://hub.docker.com/r/aswf/ci-openvdb/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openvdb/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openvdb/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openvdb) | Based on `aswf/ci-common:6`, comes with all OpenVDB upstream dependencies pre-installed. |
| [aswf/ci-otio](https://hub.docker.com/r/aswf/ci-otio) | [aswf/ci-otio:2019](https://hub.docker.com/r/aswf/ci-otio/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-otio/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-otio/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-otio) | Based on `aswf/ci-common:1`, comes with all OpenTimelineIO upstream dependencies pre-installed. |
| | [aswf/ci-otio:2020](https://hub.docker.com/r/aswf/ci-otio/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-otio/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-otio/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-otio) | Based on `aswf/ci-common:1`, comes with all OpenTimelineIO upstream dependencies pre-installed. |
| | [aswf/ci-otio:2021](https://hub.docker.com/r/aswf/ci-otio/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-otio/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-otio/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-otio) | Based on `aswf/ci-common:2`, comes with all OpenTimelineIO upstream dependencies pre-installed. |
| | [aswf/ci-otio:2022](https://hub.docker.com/r/aswf/ci-otio/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-otio/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-otio/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-otio) | Based on `aswf/ci-common:2`, comes with all OpenTimelineIO upstream dependencies pre-installed. |
| | [aswf/ci-otio:2023](https://hub.docker.com/r/aswf/ci-otio/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-otio/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-otio/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-otio) | Based on `aswf/ci-common:3`, comes with all OpenTimelineIO upstream dependencies pre-installed. |
| | [aswf/ci-otio:2024](https://hub.docker.com/r/aswf/ci-otio/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-otio/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-otio/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-otio) | Based on `aswf/ci-common:4`, comes with all OpenTimelineIO upstream dependencies pre-installed. |
| | [aswf/ci-otio:2025](https://hub.docker.com/r/aswf/ci-otio/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-otio/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-otio/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-otio) | Based on `aswf/ci-common:5`, comes with all OpenTimelineIO upstream dependencies pre-installed. |
| | [aswf/ci-otio:2026](https://hub.docker.com/r/aswf/ci-otio/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-otio/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-otio/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-otio) | Based on `aswf/ci-common:6`, comes with all OpenTimelineIO upstream dependencies pre-installed. |
| [aswf/ci-oiio](https://hub.docker.com/r/aswf/ci-oiio) | [aswf/ci-oiio](https://hub.docker.com/r/aswf/ci-oiio)| [aswf/ci-oiio:2024](https://hub.docker.com/r/aswf/ci-oiio/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-oiio/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-oiio/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-oiio) | Based on `aswf/ci-common:4`, comes with all OpenImageIO upstream dependencies pre-installed. |
| | [aswf/ci-oiio:2025](https://hub.docker.com/r/aswf/ci-oiio/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-oiio/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-oiio/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-oiio) | Based on `aswf/ci-common:5`, comes with all OpenImageIO upstream dependencies pre-installed. |
| | [aswf/ci-oiio:2026](https://hub.docker.com/r/aswf/ci-oiio/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-oiio/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-oiio/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-oiio) | Based on `aswf/ci-common:6`, comes with all OpenImageIO upstream dependencies pre-installed. |
| [aswf/ci-materialx](https://hub.docker.com/r/aswf/ci-materialx) | [aswf/ci-materialx:2023](https://hub.docker.com/r/aswf/ci-materialx/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-materialx/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-materialx/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-materialx) | Based on `aswf/ci-common:3`, comes with all MaterialX upstream dependencies pre-installed. |
| | [aswf/ci-materialx:2024](https://hub.docker.com/r/aswf/ci-materialx/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-materialx/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-materialx/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-materialx) | Based on `aswf/ci-common:4`, comes with all MaterialX upstream dependencies pre-installed. |
| | [aswf/ci-materialx:2025](https://hub.docker.com/r/aswf/ci-materialx/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-materialx/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-materialx/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-materialx) | Based on `aswf/ci-common:5`, comes with all MaterialX upstream dependencies pre-installed. |
| | [aswf/ci-materialx:2026](https://hub.docker.com/r/aswf/ci-materialx/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-materialx/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-materialx/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-materialx) | Based on `aswf/ci-common:6`, comes with all MaterialX upstream dependencies pre-installed. |
| [aswf/ci-usd](https://hub.docker.com/r/aswf/ci-usd) | [aswf/ci-usd:2019](https://hub.docker.com/r/aswf/ci-usd/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:1`, comes with all USD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2020](https://hub.docker.com/r/aswf/ci-usd/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:1`, comes with all USD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2021](https://hub.docker.com/r/aswf/ci-usd/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:2`, comes with all USD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2022](https://hub.docker.com/r/aswf/ci-usd/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:2`, comes with all USD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2023](https://hub.docker.com/r/aswf/ci-usd/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:3`, comes with all USD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2024](https://hub.docker.com/r/aswf/ci-usd/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:4`, comes with all USD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2025](https://hub.docker.com/r/aswf/ci-usd/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:5`, comes with all USD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2026](https://hub.docker.com/r/aswf/ci-usd/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:6`, comes with all USD upstream dependencies pre-installed. |
| [aswf/ci-osl](https://hub.docker.com/r/aswf/ci-osl) | [aswf/ci-osl:2018](https://hub.docker.com/r/aswf/ci-osl/tags?name=2018) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2018) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2018) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:1`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| | [aswf/ci-osl:2019](https://hub.docker.com/r/aswf/ci-osl/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:1`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| | [aswf/ci-osl:2020](https://hub.docker.com/r/aswf/ci-osl/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:1`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| | [aswf/ci-osl:2021](https://hub.docker.com/r/aswf/ci-osl/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:2`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| | [aswf/ci-osl:2022](https://hub.docker.com/r/aswf/ci-osl/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:2`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| | [aswf/ci-osl:2023](https://hub.docker.com/r/aswf/ci-osl/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:3`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| | [aswf/ci-osl:2024](https://hub.docker.com/r/aswf/ci-osl/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:4`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| | [aswf/ci-osl:2025](https://hub.docker.com/r/aswf/ci-osl/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:5`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| | [aswf/ci-osl:2026](https://hub.docker.com/r/aswf/ci-osl/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-osl/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-osl/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-osl) | Based on `aswf/ci-common:6`, comes with all OpenShadingLanguage upstream dependencies pre-installed. |
| [aswf/ci-openrv](https://hub.docker.com/r/aswf/ci-openrv) | [aswf/ci-openrv:2024](https://hub.docker.com/r/aswf/ci-openrv/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openrv/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openrv/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openrv) | Based on `aswf/ci-common:4`, comes with all OpenRV upstream dependencies pre-installed. |
| | [aswf/ci-openrv:2025](https://hub.docker.com/r/aswf/ci-openrv/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openrv/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openrv/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openrv) | Based on `aswf/ci-common:5`, comes with all OpenRV upstream dependencies pre-installed. |
| | [aswf/ci-openrv:2026](https://hub.docker.com/r/aswf/ci-openrv/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openrv/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openrv/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openrv) | Based on `aswf/ci-common:6`, comes with all OpenRV upstream dependencies pre-installed. |
| [aswf/ci-openfx](https://hub.docker.com/r/aswf/ci-openfx) | [aswf/ci-openfx:2024](https://hub.docker.com/r/aswf/ci-openfx/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openfx/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openfx/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openfx) | Based on `aswf/ci-common:4`, comes with all OpenFX upstream dependencies pre-installed. |
| | [aswf/ci-openfx:2025](https://hub.docker.com/r/aswf/ci-openfx/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openfx/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openfx/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openfx) | Based on `aswf/ci-common:5`, comes with all OpenFX upstream dependencies pre-installed. |
| | [aswf/ci-openfx:2026](https://hub.docker.com/r/aswf/ci-openfx/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-openfx/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-openfx/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-openfx) | Based on `aswf/ci-common:6`, comes with all OpenFX upstream dependencies pre-installed. |
| [aswf/ci-rawtoaces](https://hub.docker.com/r/aswf/ci-rawtoaces) | [aswf/ci-rawtoaces:2024](https://hub.docker.com/r/aswf/ci-rawtoaces/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-rawtoaces/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-rawtoaces/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-rawtoaces) | Based on `aswf/ci-common:4`, comes with all rawtoaces upstream dependencies pre-installed. |
| | [aswf/ci-rawtoaces:2025](https://hub.docker.com/r/aswf/ci-rawtoaces/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-rawtoaces/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-rawtoaces/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-rawtoaces) | Based on `aswf/ci-common:5`, comes with all rawtoaces upstream dependencies pre-installed. |
| | [aswf/ci-rawtoaces:2026](https://hub.docker.com/r/aswf/ci-rawtoaces/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-rawtoaces/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-rawtoaces/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-rawtoaces) | Based on `aswf/ci-common:6`, comes with all rawtoaces upstream dependencies pre-installed. |
| [aswf/ci-xstudio](https://hub.docker.com/r/aswf/ci-xstudio) | [aswf/ci-xstudio:2026](https://hub.docker.com/r/aswf/ci-xstudio/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-xstudio/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-xstudio/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-xstudio) | Based on `aswf/ci-common:6`, comes with all xSTUDIO upstream dependencies pre-installed. |
| [aswf/ci-vfxall](https://hub.docker.com/r/aswf/ci-vfxall) | [aswf/ci-vfxall:2019](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:1`, comes with most VFX packages pre-installed. |
| | [aswf/ci-vfxall:2020](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:1`, comes with most VFX packages pre-installed. |
| | [aswf/ci-vfxall:2021](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:2`, comes with most VFX packages pre-installed. |
| | [aswf/ci-vfxall:2022](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:2`, comes with most VFX packages pre-installed. |
| | [aswf/ci-vfxall:2023](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:3`, comes with most VFX packages pre-installed. |
| | [aswf/ci-vfxall:2024](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:4`, comes with most VFX packages pre-installed. |
| | [aswf/ci-vfxall:2025](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:5`, comes with most VFX packages pre-installed. |
| | [aswf/ci-vfxall:2026](https://hub.docker.com/r/aswf/ci-vfxall/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-vfxall/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-vfxall/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-vfxall) | Based on `aswf/ci-common:6`, comes with most VFX packages pre-installed. |

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
a ticket with the [Linux Foundation Project IT Services Support Portal]
(https://jira.linuxfoundation.org/plugins/servlet/desk/portal/2). You may need
to first create a free [Linux Foundation account](https://sso.linuxfoundation.org).

### Status

As of July 2025 there are full 2018, 2019, 2020, 2021, 2022,
2023, 2024 and 2025 [VFX Platform](https://vfxplatform.com) compliant images. The 2026 images are for testing purposes only and won't be complete until the fall of 2025 when some major ASWF packages release their new versions called for by the 2026 VFX Platform.

Note that the
pre-2024 versions of the images still exist but are not maintained / rebuilt anymore, which
means they might be obsolete (especially the OS part).

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

Starting with the 2023 versions, the non-ASWF dependencies and several of the ASWF
projects are being built as Conan packages only, with the eventual goal of getting
rid of all the ci-package-{packagename} intermediate Docker images, and mostly
assembling the CI build images from Conan packages.

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
