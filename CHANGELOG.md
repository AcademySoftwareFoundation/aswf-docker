# Changelog

All notable changes to this project will be documented in this file.

## 2020-12-20

### Changed

* Updated Qt in VFX-2021 images to version 5.15.2

### New CI Packages:

* `ci-package-qt:2021.2`
* `ci-package-pyside:2021.2`
* `ci-package-usd:2021.3`

### New CI Images:

* `ci-common:2-clang10.3`, `ci-common:2-clang11.3`
* `ci-baseqt:2021.1`
* `ci-osl:2021-clang10.4`, `ci-osl:2021-clang11.4`
* `ci-usd:2021.4`
* `ci-otio:2021.3`
* `ci-vfxall:2021-clang10.5`



## 2020-11-05

### Added

* Added `ci-baseqt` image which was not pushed in a while.
* All `ci-package-*` images now have their actual version in the label and in their tags (e.g. `aswf/ci-package-openexr:2019-2.3.0`).
* New `aswfdocker dockergen` command line tool to re-generate CI Image Dockerfiles and Readmes from a set of templates and current versions.

### Changed

* All CI images (except `ci-common`) are now automatically generated from a template and come with a `README.md` (also templated) containing all the current package version numbers.
* All package versions have been moved from version Bash scripts into the `versions.yaml` file, which enables the tagging of the image with these versions.
* VFX 2021 images are now built against CUDA-11.1.
* Update SonarQube client version 4.5.0.2216 (upgraded from 3.3.0.1492)

### New CI Packages

* `ci-package-clang:1-clang6.2`, `ci-package-clang:1-clang7.2`, `ci-package-clang:1-clang8.2`, `ci-package-clang:1-clang9.2`, `ci-package-clang:1-clang10.2`, `ci-package-clang:2-clang10.2`, `ci-package-clang:2-clang11.2`
* `ci-package-ninja:1.3`, `ci-package-ninja:2.1`
* `ci-package-cmake:2018.0`, `ci-package-cmake:2019.0`, `ci-package-cmake:2020.0`, `ci-package-cmake:2021.0`
* `ci-package-python:2018.2`, `ci-package-python:2019.2`, `ci-package-python:2020.2`, `ci-package-python:2021.1`
* `ci-package-boost:2018.2`, `ci-package-boost:2019.2`, `ci-package-boost:2020.2`, `ci-package-boost:2021.1`
* `ci-package-tbb:2018.2`, `ci-package-tbb:2019.2`, `ci-package-tbb:2020.2`, `ci-package-tbb:2021.1`
* `ci-package-cppunit:2018.2`, `ci-package-cppunit:2019.2`, `ci-package-cppunit:2020.2`, `ci-package-cppunit:2021.1`
* `ci-package-glew:2018.2`, `ci-package-glew:2019.2`, `ci-package-glew:2020.2`, `ci-package-glew:2021.2`
* `ci-package-glfw:2018.2`, `ci-package-glfw:2019.2`, `ci-package-glfw:2020.2`, `ci-package-glfw:2021.2`
* `ci-package-log4cplus:2018.2`, `ci-package-log4cplus:2019.2`, `ci-package-log4cplus:2020.2`, `ci-package-log4cplus:2021.1`
* `ci-package-qt:2018.2`, `ci-package-qt:2019.2`, `ci-package-qt:2020.2`, `ci-package-qt:2021.1`
* `ci-package-pyside:2018.2`, `ci-package-pyside:2019.2`, `ci-package-pyside:2020.2`, `ci-package-pyside:2021.1`
* `ci-package-blosc:2018.2`, `ci-package-blosc:2019.2`, `ci-package-blosc:2020.2`, `ci-package-blosc:2021.1`
* `ci-package-openexr:2018.2`, `ci-package-openexr:2019.2`, `ci-package-openexr:2020.2`, `ci-package-openexr:2021.1`
* `ci-package-alembic:2018.2`, `ci-package-alembic:2019.2`, `ci-package-alembic:2020.2`, `ci-package-alembic:2021.1`
* `ci-package-ocio:2018.2`, `ci-package-ocio:2019.2`, `ci-package-ocio:2020.2`, `ci-package-ocio:2021.2`
* `ci-package-oiio:2018.2`, `ci-package-oiio:2019.2`, `ci-package-oiio:2020.2`, `ci-package-oiio:2021.2`
* `ci-package-opensubdiv:2018.2`, `ci-package-opensubdiv:2019.2`, `ci-package-opensubdiv:2020.2`, `ci-package-opensubdiv:2021.2`
* `ci-package-ptex:2018.2`, `ci-package-ptex:2019.2`, `ci-package-ptex:2020.2`, `ci-package-ptex:2021.1`
* `ci-package-openvdb:2019.2`, `ci-package-openvdb:2020.2`, `ci-package-openvdb:2021.1`
* `ci-package-usd:2019.3`, `ci-package-usd:2020.2`, `ci-package-usd:2021.2`
* `ci-package-otio:2019.1`, `ci-package-otio:2020.1`, `ci-package-otio:2021.1`
* `ci-package-partio:2018.1`, `ci-package-partio:2019.1`, `ci-package-partio:2020.1`, `ci-package-partio:2021.1`
* `ci-package-osl:2018.1`, `ci-package-osl:2019.1`, `ci-package-osl:2020.1`, `ci-package-osl:2021.2`

### New CI Images

* `ci-common:1-clang6.7`, `ci-common:1-clang7.7`, `ci-common:1-clang8.7`, `ci-common:1-clang9.7`, `ci-common:1-clang10.7`, `ci-common:2-clang10.2`, `ci-common:2-clang11.2`
* `ci-base:2018.7`, `ci-base:2019.7`, `ci-base:2020.7`, `ci-base:2021.3`
* `ci-baseqt:2018.0`, `ci-baseqt:2019.0`, `ci-baseqt:2020.0`, `ci-baseqt:2021.0`
* `ci-openexr:2018.7`, `ci-openexr:2019.7`, `ci-openexr:2020.7`, `ci-openexr:2021.3`
* `ci-openvdb:2018-clang7.7`, `ci-openvdb:2019-clang6.7`, `ci-openvdb:2019-clang7.7`, `ci-openvdb:2019-clang8.7`, `ci-openvdb:2019-clang9.7`, `ci-openvdb:2020-clang7.7`, `ci-openvdb:2021-clang10.3`
* `ci-opencue:2018.7`, `ci-opencue:2019.7`, `ci-opencue:2020.7`, `ci-opencue:2021.3`
* `ci-ocio:2018.8`, `ci-ocio:2019.8`, `ci-ocio:2020.7`, `ci-ocio:2021.3`
* `ci-osl:2018-clang7.3`, `ci-osl:2019-clang6.3`, `ci-osl:2019-clang7.3`, `ci-osl:2019-clang8.3`, `ci-osl:2019-clang9.3`, `ci-osl:2019-clang10.3`, `ci-osl:2020-clang7.3`, `ci-osl:2021-clang10.3`, `ci-osl:2021-clang11.3`
* `ci-otio:2019.2`, `ci-otio:2020.2`, `ci-otio:2021.2`
* `ci-usd:2019.8`, `ci-usd:2020.7`, `ci-usd:2021.3`
* `ci-vfxall:2019-clang6.11`, `ci-vfxall:2019-clang7.11`, `ci-vfxall:2019-clang8.11`, `ci-vfxall:2019-clang9.11`, `ci-vfxall:2020-clang7.9`, `ci-vfxall:2021-clang10.4`



## 2020-10-21

### Added

* Added `clang-11.0.0` package.

### Fixed

* All Clang variants of `ci-vfxall` actually contained `clang7`.

### New CI Images

* `ci-common:2-clang11.2`
* `ci-osl:2019-clang10.2`, `ci-osl:2021-clang11.2`



## 2020-09-30

### Added

* Added `clang-tidy` into all Clang images: [#71](https://github.com/AcademySoftwareFoundation/aswf-docker/pull/71)
* New `ci-common:1-clang6`, `ci-common:1-clang7` (similar to `ci-common:1`), `ci-common:1-clang8`, `ci-common:1-clang9` and `ci-common:2-clang10`
* New `ci-openvdb:2019-clang6`, `ci-openvdb:2019-clang7` (similar to `ci-openvdb:2019`), `ci-openvdb:2019-clang8`, `ci-openvdb:2019-clang9` and `ci-openvdb:2021-clang10`
* New `ci-vfxall:2019-clang6`, `ci-vfxall:2019-clang7`, `ci-vfxall:2019-clang8`, `ci-vfxall:2019-clang9`, `ci-vfxall:2020-clang7`, `ci-vfxall:2021-clang10`
* Updated Clang 7 from clang-7.0.1 to clang-7.1.0

### Changed

* Cleanup of shell scripts: [#74](https://github.com/AcademySoftwareFoundation/aswf-docker/pull/74)
* Internal changes to Python `aswfdocker` utility to allow for Clang variants.
* Updated OpenVDB from `7.0.0` to `7.1.0`.
* Updated USD from `20.05` to `20.11`.

### New CI Images

* `ci-common:1-clang6.6`, `ci-common:1-clang7.6`, `ci-common:1-clang8.6`, `ci-common:1-clang9.6`, `ci-common:2-clang10.2`
* `ci-base:2018.6`, `ci-base:2019.6`, `ci-base:2020.6`, `ci-base:2021.2`
* `ci-openexr:2018.6`, `ci-openexr:2019.6`, `ci-openexr:2020.6`, `ci-openexr:2021.2`
* `ci-openvdb:2018-clang7.6`, `ci-openvdb:2019-clang6.6`, `ci-openvdb:2019-clang7.6`, `ci-openvdb:2019-clang8.6`, `ci-openvdb:2019-clang9.6`, `ci-openvdb:2020-clang7.6`, `ci-openvdb:2021-clang10.2`
* `ci-ocio:2018.7`, `ci-ocio:2019.7`, `ci-ocio:2020.6`, `ci-ocio:2021.2`
* `ci-opencue:2018.6`, `ci-opencue:2019.6`, `ci-opencue:2020.6`, `ci-opencue:2021.2`
* `ci-usd:2019.7`, `ci-usd:2020.6`, `ci-usd:2021.2`
* `ci-osl:2018-clang7.2`, `ci-osl:2019-clang6.2`, `ci-osl:2019-clang7.2`, `ci-osl:2019-clang8.2`, `ci-osl:2019-clang9.2`, `ci-osl:2020-clang7.2`, `ci-osl:2021-clang10.2`
* `ci-otio:2019.1`, `ci-otio:2020.1`, `ci-otio:2021.1`
* `ci-vfxall:2019-clang6.10`, `ci-vfxall:2019-clang7.10`, `ci-vfxall:2019-clang8.10`, `ci-vfxall:2019-clang9.10`, `ci-vfxall:2020-clang7.8`, `ci-vfxall:2021-clang10.3`



## 2020-08-01

### Added

* New `ci-otio` Docker image
* Added OpenTimelineIO 0.12 to `ci-vfxall`

### New CI Images

* `ci-otio:2019.0`, `ci-otio:2020.0`, `ci-otio:2021.0`
* `ci-vfxall:2019.9`, `ci-vfxall:2020.7`, `ci-vfxall:2021.2`



## 2020-06-20

### Changed

* `ci:common`:
  * Updated all images to new Git version 2.18: [#59](https://github.com/AcademySoftwareFoundation/aswf-docker/pull/59) by @bcipriano.

### New CI Images

* `aswf/ci-common:1.5`, `aswf/ci-common:2.1`
* `aswf/ci-base:2018.5`, `aswf/ci-base:2019.5`, `aswf/ci-base:2020.5`, `aswf/ci-base:2021.1`
* `aswf/ci-openexr:2018.5`, `aswf/ci-openexr:2019.5`, `aswf/ci-openexr:2020.5`, `aswf/ci-openexr:2021.1`
* `aswf/ci-openvdb:2018.5`, `aswf/ci-openvdb:2019.5`, `aswf/ci-openvdb:2020.5`, `aswf/ci-openvdb:2021.1`
* `aswf/ci-ocio:2018.6`, `aswf/ci-ocio:2019.6`, `aswf/ci-ocio:2020.5`, `aswf/ci-ocio:2021.1`
* `aswf/ci-opencue:2018.5`, `aswf/ci-opencue:2019.5`, `aswf/ci-opencue:2020.5`, `aswf/ci-opencue:2021.1`
* `aswf/ci-usd:2019.6`, `aswf/ci-usd:2020.5`, `aswf/ci-usd:2021.1`
* `aswf/ci-osl:2018.1`, `aswf/ci-osl:2019.1`, `aswf/ci-osl:2020.1`, `aswf/ci-osl:2021.1`
* `aswf/ci-vfxall:2019.8`, `aswf/ci-vfxall:2020.6`, `aswf/ci-vfxall:2021.1`



## 2020-06-10

### Added

* New `aswfdocker` version 0.2 with new `aswfdocker release` command line utility to create GitHub releases in batch.
* New release process based on GitHub Releases and GitHub Actions.

### Changed

* Next image releases will contain newer [OCI Annotations](https://github.com/opencontainers/image-spec/blob/master/annotations.md)



## 2020-06-01

### New CI Images

* `aswf/ci-common:2.0`: A base CentOS 7 image with GCC 9.3.1 (DTS 9.1), Clang 10.0 and CUDA.
* `aswf/ci-base:2021.0`
* `aswf/ci-openexr:2021.0`
* `aswf/ci-openvdb:2021.0`
* `aswf/ci-ocio:2021.0`
* `aswf/ci-opencue:2021.0`
* `aswf/ci-usd:2021.0`
* `aswf/ci-osl:2021.0`
* `aswf/ci-vfxall:2021.0`



## 2020-05-16

### Fixed

* Missing cppunit in `aswf/vfxall`: [#51](https://github.com/AcademySoftwareFoundation/aswf-docker/pull/51)

### New CI Images

* `aswf/ci-vfxall:2019.7`, `aswf/ci-vfxall:2020.5`



## 2020-05-08

### Added

* New `aswf/ci-osl` images for Open Shading Language
* New `aswf/ci-package-partio` package
* New `aswf/ci-package-osl` package

### Changed

* Added OSL and Clang into `aswf/ci-vfxall`
* Simplified CI image build system
* Free up space during build of Docker images

### Fixed

* Fixed bug in python `aswfdocker build` command when build multiple versions simultaneously

### New CI Images:
* `aswf/ci-osl:2018.0`, `aswf/ci-osl:2019.0`, `aswf/ci-osl:2020.0`
* `aswf/ci-vfxall:2019.6`, `aswf/ci-vfxall:2020.4`



## 2020-04-28

### Added

* `ci:common:1.4`:
  * Updated Clang compile options to help OSL
  * Added openjpeg2-devel for OIIO to help with OCIO builds

### New CI Images

* `aswf/ci-common:1.4`
* `aswf/ci-base:2018.4`, `aswf/ci-base:2019.4`, `aswf/ci-base:2020.4`
* `aswf/ci-openexr:2018.4`, `aswf/ci-openexr:2019.4`, `aswf/ci-openexr:2020.4`
* `aswf/ci-openvdb:2018.4`, `aswf/ci-openvdb:2019.4`, `aswf/ci-openvdb:2020.4`
* `aswf/ci-ocio:2018.5`, `aswf/ci-ocio:2019.5`, `aswf/ci-ocio:2020.4`
* `aswf/ci-opencue:2018.4`, `aswf/ci-opencue:2019.4`, `aswf/ci-opencue:2020.4`
* `aswf/ci-usd:2019.5`, `aswf/ci-usd:2020.4`
* `aswf/ci-vfxall:2019.6`, `aswf/ci-vfxall:2020.4`



## 2020-04-26

### Changed

* Enabled OpenImageIO tools build for future OSL needs

### Added

* All 2020 packages are now built and available in new 2020 CI images for `ocio`, `usd` and `vfxall`.

### New CI Images

* `aswf/ci-ocio:2018.4`, `aswf/ci-ocio:2019.4`, `aswf/ci-ocio:2020.3`
* `aswf/ci-usd:2019.4`, `aswf/ci-usd:2020.3`
* `aswf/ci-vfxall:2019.5`, `aswf/ci-vfxall:2020.3`



## 2020-04-23

### Added

* `ci:common:1.3`: Added aswfuser for non-root operations in the Docker images. Can be used by running `runuser -l aswfuser -c 'COMMAND'`
* Rebuilt all CI images from fixed `ci-common:1.3` image.

### New CI Images

* `aswf/ci-common:1.3`
* `aswf/ci-base:2018.3`, `aswf/ci-base:2019.3`, `aswf/ci-base:2020.3`
* `aswf/ci-openexr:2018.3`, `aswf/ci-openexr:2019.3`, `aswf/ci-openexr:2020.3`
* `aswf/ci-ocio:2018.3`, `aswf/ci-ocio:2019.3`
* `aswf/ci-opencue:2018.3`, `aswf/ci-opencue:2019.3`, `aswf/ci-opencue:2020.3`
* `aswf/ci-openvdb:2018.3`, `aswf/ci-openvdb:2019.3`, `aswf/ci-openvdb:2020.3`
* `aswf/ci-usd:2019.3`
* `aswf/ci-vfxall:2019.4`



## 2020-04-18

### Added

* Added batch support for building Docker packages and CI images, check README.md for examples.



## 2020-04-16

### Fixed

* `aswf/ci-common:1.2` contains a fix for the `ninja` binary that required a newer libstdc++: [#34](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/34)

### Changed

* Rebuilt all CI images from fixed `ci-common:1.2` image:

### New CI Images

* `aswf/ci-common:1.2`
* `aswf/ci-base:2018.2`, `aswf/ci-base:2019.2`, `aswf/ci-base:2020.2`
* `aswf/ci-openexr:2018.2`, `aswf/ci-openexr:2019.2`, `aswf/ci-openexr:2020.2`
* `aswf/ci-ocio:2018.2`, `aswf/ci-ocio:2019.2`
* `aswf/ci-opencue:2018.2`, `aswf/ci-opencue:2019.2`, `aswf/ci-opencue:2020.2`
* `aswf/ci-openvdb:2018.2`, `aswf/ci-openvdb:2019.2`, `aswf/ci-openvdb:2020.2`



## 2020-02-17

### Added

* `aswfdocker packages` lists all CI packages.
* `aswfdocker images` lists all CI images.
* `aswfdocker migrate` allows migration of Docker packages from one organization to another.
* `aswfdocker build` builds Docker CI packages and CI images.
* `aswfdocker getdockerorg` prints the current Docker Hub organization to use.
* `aswfdocker getdockerpush` prints if the images should be pushed.

### Removed

* All Bash scripts...



## 2020-02-12

### Changed

* Updated `aswf/ci-vfxall:2019.2` with patch for USD-19.11 for DTS bug discussed here: <https://github.com/Autodesk/maya-usd/pull/198>



## 2019-12-21

### Added

* New `aswf/ci-opencue:2020.1` image: [#21](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/21)



## 2019-12-16

### Changed

* All CI images have been rebuilt from Docker packages, they should be identical to the previous `.0` version:

  * `aswf/ci-common:1.1`
  * `aswf/ci-base:2018.1`, `aswf/ci-base:2019.1`, `aswf/ci-base:2020.1`
  * `aswf/ci-openexr:2018.1`, `aswf/ci-openexr:2019.1`, `aswf/ci-openexr:2020.1`
  * `aswf/ci-ocio:2018.1`, `aswf/ci-ocio:2019.1`
  * `aswf/ci-opencue:2018.1`, `aswf/ci-opencue:2019.1`, `aswf/ci-opencue:2020.1`
  * `aswf/ci-openvdb:2018.1`, `aswf/ci-openvdb:2019.1`, `aswf/ci-openvdb:2020.1`

### Added

* `aswf/ci-usd:2019.1`: contains all required packages to build USD
* `aswf/ci-vfxall:2019.1`: contains USD-19.11



## 2019-09-13

### Added

* `aswf/ci-opencue:2019.0`: new OpenCue image with Java: [#15](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/15)



## 2019-09-11

### Fixed

* Fixed system Python in all images: [#14](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/14)



## 2019-08-31

### Added

* Added `aswf/ci-openvdb:2020.0`: [#12](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/12)
