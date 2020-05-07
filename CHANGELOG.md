# Changelog
All notable changes to this project will be documented in this file.

## 2020-05-08
### Added
* New `aswf/ci-osl` images for Open Shading Language
* New `aswf/ci-package-partio` package
* New `aswf/ci-package-osl` package
### Changed
* Added OSL and clang into `aswf/ci-vfxall`
* Simplified ci image build system
* Free up space during build of docker images
### Fixed
* Fixed bug in python `aswfdocker build` command when build multiple versions simultaneously
### New CI Images:
* `aswf/ci-osl:2018.0`, `aswf/ci-osl:2019.0`, `aswf/ci-osl:2020.0`
* `aswf/ci-vfxall:2019.6`, `aswf/ci-vfxall:2020.4`

## 2020-04-28
### Added
* `ci:common:1.4`:
  * Updated clang compile options to help OSL
  * Added openjpeg2-devel for OIIO to help with OCIO builds
### New CI Images:
* `aswf/ci-common:1.4`
* `aswf/ci-base:2018.4`, `aswf/ci-base:2019.4`, `aswf/ci-base:2020.4`
* `aswf/ci-openexr:2018.4`, `aswf/ci-openexr:2019.4`, `aswf/ci-openexr:2020.4`
* `aswf/ci-openvdb:2018.4`, `aswf/ci-openvdb:2019.4`, `aswf/ci-openvdb:2020.4`
* `aswf/ci-ocio:2018.5`, `aswf/ci-ocio:2019.5`, `aswf/ci-ocio:2020.4`
* `aswf/ci-opencue:2018.4`, `aswf/ci-opencue:2019.4`, `aswf/ci-opencue:2020.4`
* `aswf/ci-usd:2019.5`, `aswf/ci-usd:2020.4`
* `aswf/ci-vfxall:2019.6`, `aswf/ci-vfxall:2020.4`

## 2020-04-26
### Changed:
* Enabled OpenImageIO tools build for future OSL needs
### Added:
* All 2020 packages are now built and available in new 2020 CI images for `ocio`, `usd` and `vfxall`.
### New CI Images:
* `aswf/ci-ocio:2018.4`, `aswf/ci-ocio:2019.4`, `aswf/ci-ocio:2020.3`
* `aswf/ci-usd:2019.4`, `aswf/ci-usd:2020.3`
* `aswf/ci-vfxall:2019.5`, `aswf/ci-vfxall:2020.3`

## 2020-04-23
### Added
* `ci:common:1.3`: Added aswfuser for non-root operations in the docker images. Can be used by running `runuser -l aswfuser -c 'COMMAND'`
* Rebuilt all ci images from fixed `ci-common:1.3` image.
### New CI Images:
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
* Added batch support for building docker packages and CI images, check README.md for examples.

## 2020-04-16
### Fixed
* `aswf/ci-common:1.2` contains a fix for the `ninja` binary that required a newer libstdc++: https://github.com/AcademySoftwareFoundation/aswf-docker/issues/34
### Changed
* Rebuilt all ci images from fixed `ci-common:1.2` image:
### New CI Images:
* `aswf/ci-common:1.2`
* `aswf/ci-base:2018.2`, `aswf/ci-base:2019.2`, `aswf/ci-base:2020.2`
* `aswf/ci-openexr:2018.2`, `aswf/ci-openexr:2019.2`, `aswf/ci-openexr:2020.2`
* `aswf/ci-ocio:2018.2`, `aswf/ci-ocio:2019.2`
* `aswf/ci-opencue:2018.2`, `aswf/ci-opencue:2019.2`, `aswf/ci-opencue:2020.2`
* `aswf/ci-openvdb:2018.2`, `aswf/ci-openvdb:2019.2`, `aswf/ci-openvdb:2020.2`

## 2020-02-17
### Added
* `aswfdocker packages` lists all ci packages.
* `aswfdocker images` lists all ci images.
* `aswfdocker migrate` allows migration of docker packages from one organisation to another.
* `aswfdocker build` builds docker ci packages and ci images.
* `aswfdocker getdockerorg` prints the current dockerhub organisation to use.
* `aswfdocker getdockerpush` prints if the images should be pushed.
### Removed
* All bash scripts...

## 2020-02-12
### Changed
* Updated `aswf/ci-vfxall:2019.2` with patch for USD-19.11 for DTS bug discussed here: https://github.com/Autodesk/maya-usd/pull/198 .

## 2019-12-21
### Added
* New `aswf/ci-opencue:2020.1` image [#21](/../../issues/21)

## 2019-12-16
### Changed
* All ci images have been rebuilt from docker packages, they should be identical to the previous `.0` version:

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
* `aswf/ci-opencue:2019.0`: new opencue image with java [#15](/../../issues/15)

## 2019-09-11
### Fixed
* Fixed system python in all images [#14](/../../issues/14)

## 2019-08-31
### Added
* Added `aswf/ci-openvdb:2020.0` [#12](/../../issues/12)
