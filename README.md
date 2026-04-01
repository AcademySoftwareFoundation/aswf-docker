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
| | [aswf/ci-common:6](https://hub.docker.com/r/aswf/ci-common/tags?name=6) ![Image Version](https://img.shields.io/docker/v/aswf/ci-common/6) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-common/6) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-common) | A base RockyLinux-8 image with gcc-toolset-14 (GCC-14.2.x), clang-19-20 and cuda-12.9.1. |
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
| [aswf/ci-usd](https://hub.docker.com/r/aswf/ci-usd) | [aswf/ci-usd:2019](https://hub.docker.com/r/aswf/ci-usd/tags?name=2019) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2019) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2019) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:1`, comes with all OpenUSD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2020](https://hub.docker.com/r/aswf/ci-usd/tags?name=2020) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2020) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2020) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:1`, comes with all OpenUSD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2021](https://hub.docker.com/r/aswf/ci-usd/tags?name=2021) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2021) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2021) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:2`, comes with all OpenUSD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2022](https://hub.docker.com/r/aswf/ci-usd/tags?name=2022) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2022) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2022) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:2`, comes with all OpenUSD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2023](https://hub.docker.com/r/aswf/ci-usd/tags?name=2023) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2023) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2023) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:3`, comes with all OpenUSD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2024](https://hub.docker.com/r/aswf/ci-usd/tags?name=2024) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2024) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2024) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:4`, comes with all OpenUSD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2025](https://hub.docker.com/r/aswf/ci-usd/tags?name=2025) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2025) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2025) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:5`, comes with all OpenUSD upstream dependencies pre-installed. |
| | [aswf/ci-usd:2026](https://hub.docker.com/r/aswf/ci-usd/tags?name=2026) ![Image Version](https://img.shields.io/docker/v/aswf/ci-usd/2026) | ![Image Size](https://img.shields.io/docker/image-size/aswf/ci-usd/2026) ![Pulls](https://img.shields.io/docker/pulls/aswf/ci-usd) | Based on `aswf/ci-common:6`, comes with all OpenUSD upstream dependencies pre-installed. |
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
a ticket with the [Linux Foundation Project IT Services Support Portal](https://jira.linuxfoundation.org/plugins/servlet/desk/portal/2).
You may need to first create a free [Linux Foundation account](https://sso.linuxfoundation.org).

### Status

As of December 2025 there are full 2018, 2019, 2020, 2021, 2022,
2023, 2024, 2025 and 2026. [VFX Platform](https://vfxplatform.com) compliant images.

The pre-2024 versions of the images still exist but are not maintained / rebuilt anymore, which
means they might be obsolete (especially the OS part).

## CI Packages

In order to decouple the building of packages (which can take a lot of time,
such as clang, Qt and OpenUSD) from the creation of the CI images, the
component packages are built and stored as Conan packages. In previous versions some packages
were built and stored as individual docker images named `ci-packagename-package`
and uploaded to Docker Hub: this approach is no longer used, all packages
are built using Conan.

CI packages are built using BuildKit Docker syntax that allows cache
folders to be mounted at build time, and is built with `docker buildx`. The
Docker BuildKit system allows the building of many packages in parallel in an
efficient way with support for [ccache](https://ccache.dev/).

The Conan packages are then assembled into container images and uploaded
to Docker Hub: image `ci-openexr` (for instance) contains all the pre-built dependencies to build
OpenEXR, but does not contain a build of OpenEXR itself. The `ci-vfxall` image includes
builds of every package in `aswf-docker` and should contain a large number of the
dependencies required to build a typical C/C++ VFX library or application.

## Python Utilities

Check [aswfdocker](python/README.md) for python utility usage.

## Manual Builds

To build packages and images locally follow the instructions to install the
[aswfdocker](python/README.md) python utility.

The `group` names for `PACKAGE` and `IMAGE` builds are distinct and are defined in `versions.yaml`. At some point Conan dependency management will be leveraged to automatically determine build order, until then all the packages in group `vfx1-2` must be built before the ones in `vfx1-1`, and components in a given group do not depend on each other.

### Packages

Packages require a recent Docker version with
[buildx](https://docs.docker.com/buildx/working-with-buildx/) installed and
enabled.

To build all packages (very unlikely to succeed unless run on a very very
powerful machine!):

```bash
aswfdocker --verbose build -t PACKAGE
```

To build a single Conan package, e.g. OpenUSD:

```bash
# First list the available CI packages to know which package belong to which "group":
aswfdocker packages
# Then run the build
aswfdocker --verbose build --ci-image-type PACKAGE --group vfx-6 --version 2026 --use-coman --target openusd
# Or the simpler but less flexible syntax:
aswfdocker build --full-name aswftesting/ci-package-usd:2026
```

### Images

Images can be built with recent Docker versions but do not require
[buildx](https://docs.docker.com/buildx/working-with-buildx/) but it is
recommended to speed up large builds.

To build all images (very unlikely to succeed unless run on a very very powerful machine!):

```bash
aswfdocker --verbose build --ci-image-type IMAGE
```

To build a single image:

```bash
# First list the available CI images to know which package belong to which "group":
aswfdocker images
# Then run the build
aswfdocker --verbose build --ci-image-type IMAGE --group vfx1 --version 2026 --target openexr
# Or the simpler but less flexible syntax:
aswfdocker build --ci-image-type aswftesting/ci-openexr:2026
```

### Windows Considerations

Native Windows support is our goal, but due to limited resources, active development is intermittent. In the meantime, our existing build workflows work under WSL.

1. Download and install [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install)
    * Tested on a Windows mini server with an AMD Ryzen 7 6800U (8 cores / 16 logical processors) and 32GB of memory.

    * For decent performance, configure WSL to use 8 cores and a minimum of 14GB of memory.
    * We recommend using the WSL Settings GUI to manage these limits. If you prefer configuring manually via `.wslconfig`, see [WSL configuration settings](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

1. Confirm that Docker is properly configured to use WSL 2 for builds. Go [here](https://docs.docker.com/desktop/features/wsl/) for more information on Docker on WSL.

1. Install `uv` (winget example):

     `winget install --id=astral-sh.uv  -e`

    [Here](https://docs.astral.sh/uv/) are the `uv` docs. 


## Use Cases

### GitHub Actions

For Linux builds on GitHub Actions, in the workflow YAML file it is sufficient to specify:

```
container: aswf/ci-openexr:2026
```

or:

```
container:
  image: aswf/ci-openexr:2026
```

to cause the `aswf/ci-openexr:2026` container image to be pulled down from [Docker Hub](https://hub.docker.com/r/aswf/ci-openexr) and have the build run within the context of a container created from that image.

ASWF projects will typically use the [GitHub Actions `matrix` strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations) to run build against multiple VFX Platform years.

Projects which do not (yet) have dedicated container images can pick one from a project which is "close enough" in terms of dependencies, keeping in mind that `ci-openexr` only includes the dependencies to build the [OpenEXR project](https://github.com/AcademySoftwareFoundation/openexr), it does not contain a build of OpenEXR itself. When in doubt, the [`ci-vfxall`](https://hub.docker.com/r/aswf/ci-vfxall) image includes builds of every currently supported package.

A project's CI may wish to be more specific about the version of the container image it wishes to use, for instance:

```
container: aswf/ci-openxr:2026.3
```

pins to a specific release of the VFX Platform 2026 `ci-openexr` container image, whereas:

```
container: aswf/ci-openexr:2026
```

pulls the latest version available. A project can also decide to explicitly specify the SHA-256 signature of a container, in which case the numeric version can be appended as a comment, similarly to how GitHub Actions versions can be pinned to a SHA-256 signature:

```
container:
  image: aswf/ci-openexr@sha256:9ddf6fccd32619a23a02db56aa6761e0b87ffce7374fa103768ded0ae09f1120 # 2026.3
```

The SHA-256 signature can be found on the [Docker Hub tags page](https://hub.docker.com/r/aswf/ci-openexr/tags) for the container image, or with:

```
$ docker buildx imagetools inspect aswf/ci-openexr:2026.3 --format '{{ json .Manifest }}' | jq -r '.digest'
sha256:9ddf6fccd32619a23a02db56aa6761e0b87ffce7374fa103768ded0ae09f1120
```

Projects consuming these images should decide on the best policy for them:

- always pull the latest version for a VFX Platform year
- pin to a specific version for a VFX Plaform year
- pin to a specific version using a SHA-256 signature

The `aswf-docker` release process is fairly lengthy and complex, and in infrequent cases a specific version of a container image may have had to be re-released with the same version tag applied. We aim to minimize these occurances, which would typically occur only within a short window of time after the initial release. Once a container image version has been validated by its consumer project, it can be considered immutable.

### GPU Considerations

The container images include CUDA, OptiX, OpenGL and Vulkan libraries and can be used to run GPU accelerated workloads such as test suites for GPU accelerated code paths.

The host system must have the [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit) installed to allow GPU devices to be mapped into the container and accessible by a binary running inside it. The NVIDIA GPU driver also needs to be installed on the host: the Container Toolkit will map the hardware specific shared libraries into the container at startup time. There is no need to install the GPU driver in the container itself.

Academy Software Foundation projects running their CI in the context of the [https://github.com/AcademySoftwareFoundation/] GitHub organization have access to GPU accelerated hosted runners where the NVIDIA Container Toolkit is already installed.

#### CUDA CI Workloads

To run a CUDA workload, it is sufficient to map the GPU device with the `--gpus all` option:

```
container:
  image: aswf/ci-openexr:2026
  options: --gpus all
```

#### OptiX CI Workloads

The[Open Shading Language](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage) optionally uses NVIDIA OptiX for ray tracing acceleration. This requires additional [driver capabilities](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.10.0/user-guide.html#driver-capabilities) to be mapped into the container at startup time:

[https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/blob/main/.github/workflows/ci.yml]

```
container:
  image: aswf/ci-osl:2026-clang20.3
  options: '-e NVIDIA_DRIVER_CAPABILITIES=compute,graphics,utility --gpus all'
```

The `options` syntax may seem a bit odd but is what was empirically determined to pass the desired options to allow the required driver capabilities to be exposed and allow the OSL test suite to run its GPU accelerated components.

#### OpenGL CI Workloads

OpenGL Linux binaries typically require an X11 server to be running, which can be complicated to set up in a CI environment. Instead of using [GLX](https://registry.khronos.org/OpenGL/specs/gl/glx1.4.pdf) to interface OpenGL with an X11 server, OpenColorIO can optionally use [EGL](https://registry.khronos.org/EGL/specs/eglspec.1.0.pdf) to create an image buffer and render to it without the need for a running X server:

[OpenImageIO OpenGL helper core](https://github.com/AcademySoftwareFoundation/OpenColorIO/blob/main/src/libutils/oglapphelpers/oglapp.cpp)

OpenColorIO runs its GPU CI workloads on [AWS Codebuild](https://aws.amazon.com/codebuild/).

The `NVIDIA_DRIVER_CAPABILITIES` environment varible needs to be set to enable additional capabilities for OpenGL workloads:

```
NVIDIA_DRIVER_CAPABILITIES=compute,graphics,utility
```

#### OpenGL on a Workstation

In an X11 workstation environment, you can run an OpenGL binary inside a container with:

```
docker run -it --rm --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix aswftesting/ci-common:6 /usr/bin/glxgears
```

### Harvesting Pre-Built Binaries

The container images can be used to harvest pre-built binaries:

```bash
docker image pull aswf/ci-openexr:2026
docker create --name tmp-openexr aswf/ci-openexr:2026
docker cp tmp-openexr:/usr/local/lib/libImath-3_2.so.30.3.2.2 /tmp/libImath-3_2.so.30.3.2.2
docker rm tmp-openexr
```

A challenge is that when creating the image
`aswf/ci-openexr`, all the Conan packages which are pre-requisites to build OpenEXR (but not OpenEXR itself) get "flattened" into `/usr/local/`: this can make it difficult to extract only the binaries for a specific package. The list of files in a specific Conan package can be found in the [ASWF Artifactory Repository](https://linuxfoundation.jfrog.io/ui/packages)

### Downloading Conan Packages

In a local clone of the [aswf-docker repository](https://github.com/AcademySoftwareFoundation/aswf-docker) follow the instructions in [python/README.md](https://github.com/AcademySoftwareFoundation/aswf-docker/blob/main/python/README.md) to set up a dev environment and activate the venv virtual environment. You should then be able to fetch a pre-build Conan package with:

```bash
git clone https://github.com/AcademySoftwareFoundation/aswf-docker
cd aswf-docker
uv sync --all-extras
source .venv/bin/activate
CONAN_HOME=/path_to/aswf-docker/packages/conan/settings conan install -cc core.cache:storage_path=/tmp/conan_home/d --requires=imath/3.2.2@aswf/vfx2026 --profile:all=packages/conan/settings/profiles_aswf/vfx2026 --deployer-folder /tmp --deployer=direct_deploy
```

You will end up with the contents of the `imath` Conan package in `/tmp/direct_deploy/imath/`. You can use `--deployer=full_deploy` to get all of its transitive dependencies installed as well, this time in `/tmp/full_deploy/host/`:

```
$ ls /tmp/full_deploy/host
boost  bzip2  cpython  expat  gdbm  imath  libbacktrace  libffi  mpdecimal  openssl  pybind11  sqlite3  tcl  tk  util-linux-libuuid  xz_utils  zlib
```

This will also create a cache of Conan packages in `/tmp/conan_home/d/` which you may want to delete.
