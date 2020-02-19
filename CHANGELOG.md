# Changelog
All notable changes to this project will be documented in this file.

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
  * `aswf/ci-opencue:2018.1`, `aswf/ci-opencue:2019.1`
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
