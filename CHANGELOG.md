# Changelog

All notable changes to this project will be documented in this file.

# 2025-07-XX

These releases no longer build / install libraries in `/usr/local/lib64`, they revert back to the default
`/usr/local/lib` supported by most packages and Conan recipes. This should hopefully be transparent to
consumers of these new images.

- 2024.3 release
  - using Conan 2 recipes
  - updated versions
    - Conan 2.18.1 (was 1.x)
    - CUDA 12.6.3 (was 12.6.1)
    - ccache 4.9.1 (was 4.8.3)
    - CMake 3.31.7 (was 3.27.9)
    - Ninja 1.13.1 (was 1.12.1)
    - Sonar Cloud 7.1.0.4889 (was 6.2.1.4610)
    - Alembic 1.8.8 (was 1.8.6)
    - Blosc 1.21.6 (was 1.21.5)
    - fmt 11.2.0 (was 11.1.4)
    - GLEW 2.2.0 (was 2.1.0)
    - GLFW 3.4 (was 3.3.8)
    - gtest 1.15.2 (was 1.14.0)
    - hdf5 1.14.6
    - lcms 2.17 (was 2.16)
    - log4cplus 2.1.2 (was 2.1.1)
    - minizip-ng 4.0.10 (was 4.0.8)
    - pybind11 2.13.6 (was 2.12.0)
    - opensubdive 3.6.1 (was 3.6.0)
    - python 3.11.13 (was 3.11.11)
    - Qt 6.5.6 (was 6.5.4)
    - OIIO 2.5.19.0 (was 2.5.18.0)
    - OpenFX 1.5s
    - PySide 6.5.6 (was 6.5.4)
- 2025.2
  - updated versions
    - Conan 2.18.1 (was 2.14.0)
    - Ninja 1.13.1 (was 1.12.1)
    - Sonar Cloud 7.1.0.4889 (was 6.2.1.4610)
    - LLVM 19.1.7 (was 19.1.1)
    - fmt 11.2.0 (was 11.1.4)
    - hdf5 1.14.6
    - lcms 2.17 (was 2.16)
    - minizip-ng 4.0.10 (was 4.0.8)
    - opensubdiv 3.6.1 (was 3.6.0)
    - python 3.11.13 (was 3.11.11)
    - Qt 6.5.6 (was 6.5.4)
    - OIIO 3.0.9.0 (was 3.0.6.1)
    - OpenEXR 3.3.5 (was 3.3.3)
    - OpenFX 1.5s
    - OpenVDB 12.0.1 (was 12.0.0)
    - OSL 1.14.7.0 (was 1.14.5.1)
    - PySide 6.5.6 (was 6.5.4)
    - USD 25.05.01 (was 25.05)
- 2026.0 draft images
  - pre-release for testing purposes, does not yet include final versions of late releasing packages for VFX Platform 2026 (OOCIO, OpenEXR, OpenVDB, OpenSubDiv)
  - OpenEXR includes a pre-release of 3.4.x
  - see `ci_common6` and `2026` sections of `versions.yaml` for full list of package versions
- to minimize local changes against upstream Conan recipes and avoid spending time fighting build systems which hard code `lib` as the destination directory, all changes related to landing DSOs and support files in `lib64` are reverted
- new Conan package and build images for OpenFX based on conanfile.py from OpenFX repo (Conan Center Index has older version)
  - adds dependant Conan package cimg
- new [Conan package and build images for rawtoaces](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/273)
  - adds dependant Conan packages libraw, jasper, jsonformoderncpp, ceres-solver, eigen , aces_container
- Alembic now [built with hdf5 dependency](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/254)
- OpenVDB now [built as a Conan package](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/231)
- OpenImageIO builds with libraw support](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/264) and OpenJPEG/JPEG2000 support
- system wrapper Conan packages
  - improved wrapper packages no longer declare include directories and libraries they don't include
  - query container OS for installed system package version instead of hard coding (pkgconfig / rpm)
- libuhdr Conan package renamed to libultrahdr and updated to match new Conan Center Index package
- blosc Conan package renamed to c-blosc to match Conan Center Index
- Qt now built against harfbuzz text shaping library from vendored Conan package
- aswfdocker utility gets "conandiff" option to show upstream changes to vendored Conan Center Index recipes to help
with keeping recipes up to date
  - merge upstream recipe changes, in particular changes for CMake 4 compatibility
  - `--keep_source` and `--keep_build` command line options are obsolete, no longer relevant with Conan 2
- install_conanpackages.sh script update to use the Conan full_deploy generator which can deploy all transitive dependencies for a package in one call, mimizing the need to include dependencies in the image.yaml sources for the ci-foo containers

# 2025-05-04

- 2025.1 images
  - transition to oneTBB 2021.13.0
    - support for Conan Center Index style config.yml to support separate recipes per package version
  - common images much slimmer, no longer include the following CUDA components
    - #183: Nsight Compute profiler
    - libcublas-devel-x-y
    - libcusparse-devel-x-y
    - libcufft-devel-x-y
    - libnpp-devel-x-y
    - libcusolver-devel-x-y
  - leverage [new NVIDIA repo](https://github.com/NVIDIA/optix-dev) to install OptiX headers
  - #255: fix build depenedency between tcl and tk wrappers
  - partio build correctly sets C++ standard
  - OpenSubDiv build preserves static libraries since its CMake files expect both static and dynamic libs to be present
- Version updates
  - CMake 3.31.7 (was 3.31.6)
  - CUDA 12.6.3 (was 12.6.1)
  - oneTBB 2021.13.0 (was 2020_u3)
  - OpenImageIO 3.0.6.1 (was 3.0.5.0)
  - OpenShadingLanguage 1.14.5.1 (was 1.14.5.0)
  - Optix 9.0 headers (previous most recent was 8.1)
  - PartIO 1.19.0 (was 1.17.3)
  - USD 25.05 (was 25.02a.eae7e67)

# 2025-04-08

- 2025.0 images
  - TBB transition to OneAPI remains to be done
- ASWF project versions
  - Imath: 3.1.2
  - MaterialX: 1.39.3
  - OCIO: 2.4.2
  - OIIO: 3.0.5.0
  - OpenEXR: 3.3.3
  - OpenVDB: 12.0.0
  - OSL: 1.14.5.0
  - OTIO: 0.17.0
- VFX Platform component versions
  - Boost: 1.85.0
  - Python: 3.11.11
  - Numpy: 1.26.4
  - PySide: 6.5.4
  - Qt: 6.5.4
  - TBB: 2020_u3
- "ASWF adjacent" component versions
  - Alembic: 1.8.8
  - OpenSubDiv: 3.6.0
  - Partio: 1.17.3
  - Ptex: 2.4.3
  - USD: 25.02a + commit eae7e67 for MaterialX 1.39.3 compatibility
- Generic components
  - b2: 5.2.1
  - blosc: 1.21.6
  - bzip2: 1.0.8
  - cppunit: 1.15.1
  - expat: 2.6.4
  - fmt: 11.1.4
  - freetype: 2.13.2
  - glew: 2.2.0
  - glfw: 3.4
  - gtest: 1.15.2
  - hdf5: 1.8.23
  - highway: 1.2.0
  - lcms: 2.16
  - libbacktrace: cci.20210118
  - libdeflate: 1.23
  - libiconv: 1.17
  - libjpeg_turbo: 3.0.4
  - libjxl: 0.11.1
  - libuhdr: 1.4.0
  - libwebp: 1.5.0
  - libxcrypt: 4.4.36
  - log4cplus: 2.1.2
  - lz4: 1.10.0
  - md4c: 0.4.8
  - minizip_ng: 4.0.8
  - pugixml: 1.14
  - pybind11: 2.13.6
  - pystring: 1.1.4
  - snappy: 1.1.10
  - tsl-robin-map: 1.3.0
  - yaml-cpp: 0.8.0
  - zlib: 1.3.1
  - zstd: 1.5.6
- common image components
  - Rocky Linux 8.10
  - CUDA 12.6.1
  - OptiX 7.3 to 8.1
  - Conan 2.14.0
  - CMake 3.31.6
  - Ninja 1.12.1
  - LLVM 18.1.8 and 19.1.1
- transition to Conan 2
  - update most Conan recipes from Conan Center Index, minimize differences from upstream
  - create empty wrapper packages to satisfy recipe requires() from OS image packages
  - build replacment packages to satisfy newer requires() than what Rocky 8 has (mostly compression and media libraries)

# 2024-10-05

- 2024.2 images
- update latest / preview / draft tags for Docker images
- update Python dependencies (resolve dependabot PRs)
- update pylint and fix pylint / pytest warnings
- Fix SonarCloud scanning
- Conan 1.65 (was 1.64)
- Expat 2.6.3 (was 2.5.0) to address CVEs CVE-2024-45492 CVE-2024-45491 CVE-2024-45490
- fixes #196 : ci-openrv build container. OpenRV doesn't build yet, waiting for Qt6 support.
  For now openrv builds in non-default review group.
- fixes #150 : rename master branch to main
- fixes #218 : only attempt to use larger runners when running in context of ASWF GitHub org.
- fixes #221 : ci-usd now includes Python dependencies
- fixes #148 : Vulkan SDK and runtime now included in all images, initially required
  for ci-openrv, but useful in general. Also Qt now built with Vulkan support
- CUDA 12.6.1 (was 12.3.0)
- Java 17 (was 11) for ci-opencue image
- Imath 3.1.12 (was 3.1.11)
- MaterialX 1.39.1 (was 1.38.10)
- OpenImageIO 2.15.16.0 (was 2.15.15.0)
- OpenShadingLanguage 1.13.11.0 (was 1.13.10.0)
- Python 3.11.10 (was 3.11.9)
- USD 24.08 (was 24.05)

### New CI Images

* `aswf/ci-common:4-clang16.2`, `aswf/ci-common:4-clang17.2` : A base Rocky 8.10 image with GCC 11.2.1 (DTS 11), Clang 16.0/17.0 and CUDA 12.3.
* `aswf/ci-base:2024.2`
* `aswf/ci-baseqt:2024.2`
* `aswf/ci-opencue:2024.2`
* `aswf/ci-openexr:2024.2`
* `aswf/ci-ocio:2024.2`
* `aswf/ci-oiio:2024.2`
* `aswf/ci-otio:2024.2`
* `aswf/ci-materialx:2024.2`
* `aswf/ci-usd:2024.2`
* `aswf/ci-openrv:2024.2`
* `aswf/ci-osl:2024-clang16.2`,`aswf/ci-osl:2024-clang17.2`
* `aswf/ci-openvdb:2024-clang16.2`, `aswf/ci-openvdb:2024-clang17.2`
* `aswf/ci-vfxall:2024-clang16.1`, `aswf/ci-vfxall:2024-clang17.1`

## 2024-09-02

- blosc moved to base1
- rework Conan packages to use CMakeToolChain, conandata.yml
- Conan packages mostly install to lib64 instead of lib (partial #120)
- libdeflate in base image for OpenEXR
- oiio build container (#173)
- Conan packages preserve DSO symlinks when installed (#194)
- Conan packages don't overwrite each other's installed license files
- Break circular dependency between OCIO and OIIO by compiling OCIO utils without OIIO (#54)
- Expat is now a Conan package (version in base image is too old)
- Qt now builds qtwebengine and qtmultimedia (will be needed for OpenRV)
- OpenEXR and Imath built as Conan packages only
- MaterialX 1.38.10 (was 1.38.8)
- Imath 3.1.11 (was 3.1.10)
- OpenEXR 3.2.4 (was 3.2.2)
- OpenImageIO 2.5.15.0 (was 2.5.8.0)
- OpenShadingLanguage 1.13.10.0 (was 1.13.6.1)
- OpenTimelineIO 0.17.0 (was 0.15)
- Conan 1.64 (was 1.62)
- CMake 3.27.9 (was 3.27.8)
- Clang 16.0.6 (was 16.0.4), 17.0.6 (was 17.0.1)
- pybind11 2.12.0 (was 2.11.1)
- Python 3.11.9 (was 3.11.8)
- USD 24.05 (was 23.11)

### New CI Images

* `aswf/ci-common:4-clang16.1`, `aswf/ci-common:4-clang17.1` : A base Rocky 8.9 image with GCC 11.2.1 (DTS 11), Clang 16.0/17.0 and CUDA 12.3.
* `aswf/ci-base:2024.1`
* `aswf/ci-baseqt:2024.1`
* `aswf/ci-opencue:2024.1`
* `aswf/ci-openexr:2024.1`
* `aswf/ci-ocio:2024.1`
* `aswf/ci-oiio:2024.1`
* `aswf/ci-otio:2024.1`
* `aswf/ci-materialx:2024.1`
* `aswf/ci-usd:2024.1`
* `aswf/ci-osl:2024-clang16.1`,`aswf/ci-osl:2024-clang17.1`
* `aswf/ci-openvdb:2024-clang16.1`, `aswf/ci-openvdb:2024-clang17.1`
* `aswf/ci-vfxall:2024-clang16.1`, `aswf/ci-vfxall:2024-clang17.1`

## 2024-02-19

* New ci-common-v4 for VFX Platform 2024 based on:
  * C++17 (unchanged)
  * Ccache 4.8.3 (from 4.7.4)
  * Clang 16.0.4 / 17.0.1
  * Conan 1.58.0 (from 1.47.0)
  * CUDA 12.3.0 (from 11.8.0)
  * OptiX 8.0 (in addition to 7.x)
  * gcc-toolset 11 / gcc 11.2.1 (unchanged)
  * glibc 2.28 (unchanged)
  * libstdc++11 new ABI
  * Ninja 1.11.1 (unchanged)
  * Rocky Linux 8.9 (from 8.8)
  * SonarScan 5.0.1.3006 (from 4.8.0.2856)
* Updated 2024 Packages
  * Alembic 1.8.6 (from 1.8.5)
  * Blosc 1.21.5 (from 1.17.0)
  * Boost 1.82.0 (from 1.80.0)
  * CMake 3.27.8 (from 3.27.2)
  * GLFW 3.3.8 (from 3.1.2)
  * gtest 1.14.0 (from 1.11.0)
  * Imath 3.1.10 (from 3.1.9)
  * log4cplus 2.1.1 (from 1.1.2)
  * MaterialX 1.38.8 (from 1.38.7)
  * NumPy 1.24.3 (from 1.23.5)
  * OpenColorIO 2.3.2 (from 2.2.1)
  * OpenEXR 3.2.2 (from 3.1.11)
  * OpenImageIO 2.5.8.0 (from 2.4.13.0)
  * OpenSubdiv 3.6.0 (from 3.5.0)
  * OpenVDB 11.0.0 (from 10.0.1)
  * OpenShadingLanguage 1.13.6.1 (from 1.12.13.0)
  * OpenTimelineIO 0.15 (from 0.14.1)
  * PySide 6.5.3 (from 5.15.9.
  * Python 3.11.8 (from 3.10.11)
  * Qt 6.5.3 (from 5.15.9)
  * USD 23.11 (from 23.05)
* Unchanged 2024 Packages
  * CppUnit 1.15.1
  * GLEW 2.1.0
  * HDF5 1.8.23
  * Partio 1.17.1
  * Ptex 2.4.2
  * TBB 2020u3

### New CI Images

* `aswf/ci-common:4-clang16.0`, `aswf/ci-common:4-clang17.0` : A base Rocky 8 image with GCC 11.2.1 (DTS 11), Clang 16.0/17.0 and CUDA 12.3.
* `aswf/ci-base:2024.0`
* `aswf/ci-baseqt:2024.0`
* `aswf/ci-opencue:2024.0`
* `aswf/ci-openexr:202.0`
* `aswf/ci-ocio:2024.0`
* `aswf/ci-otio:2024.0`
* `aswf/ci-materialx:2024.0`
* `aswf/ci-usd:2024.0`
* `aswf/ci-osl:2024-clang16.0`,`aswf/ci-osl:2024-clang17.0`
* `aswf/ci-openvdb:2024-clang16.0`, `aswf/ci-openvdb:2024-clang17.0`
* `aswf/ci-vfxall:2024-clang16.0`, `aswf/ci-vfxall:2024-clang17.0'

### New Conan packages

* blosc
* opensubdiv
* partio
* ptex

### Packages that are now Conan only

* alembic
* clang
* ninja
* pyside
* pybind11
* qt

## 2023-11-12

* Fixes for local Conan builds
  * Conan builds into buildx caches, no longer weighing down build context

* OpenEXR and OpenVDB build container now include pybind11

### New CI Images

* `aswf/ci-common:3-clang14.2`, `aswf/ci-common:3-clang15.2` : A base Rocky 8.8 image with GCC 11.2.1 (DTS 11), Clang 14.0/15.0 and CUDA 11.8.
* `aswf/ci-base:2023.2`
* `aswf/ci-baseqt:2023.2`
* `aswf/ci-opencue:2023.2`
* `aswf/ci-openexr:2023.2`
* `aswf/ci-ocio:2023.2`
* `aswf/ci-otio:2023.2`
* `aswf/ci-materialx:2023.2`
* `aswf/ci-usd:2023.2`
* `aswf/ci-osl:2023-clang14.2`,`aswf/ci-osl:2023-clang15.2`
* `aswf/ci-openvdb:2023-clang14.2`, `aswf/ci-openvdb:2023-clang15.2`
* `aswf/ci-vfxall:2023-clang14.2`, `aswf/ci-vfxall:2023-clang15.2'

## 2023-08-15

* NVIDIA Optix SDK includes
  * 7.0.0, 7.3.0, 7.4.0, 7.5.0, 7.6.0, 7.7.0
  * Installed in /usr/local/NVIDIA-OptiX-SDK-7.x.x/include/

* Updated 2023 packages
  * OpenEXR 3.1.11 (from 3.1.8)
  * OpenImageIO 2.4.13.0 (from 2.4.9.0)
  * OpenShadingLanguage 1.12.13.0 (from 1.12.10.0)
  * Alembic 1.8.5 (from 1.8.4)
  * Partio 1.17.1 (from 1.14.6)
  * Cmake 3.27.2 (from 3.25.2)
  * Pybind11 2.9.2 (from 2.8.1)
  * Python 3.10.11 (from 3.10.9)

* Additional packages built as Conan-only
  * boost
  * cmake
  * cppunit
  * glew
  * glfw
  * log4cplus

* Default tagging for -clang15 images
  * Previous years used oldest clang version for default version tag, now using latest
  * ci-common:3 now points to :3-clang15
  * ci-{openvdb,osl,vfxall}:2023 now points to :2023-clang15

### New CI Images

* `aswf/ci-common:3-clang14.1`, `aswf/ci-common:3-clang15.1` : A base Rocky 8 image with GCC 11.2.1 (DTS 11), Clang 14.0/15.0 and CUDA 11.8.
* `aswf/ci-base:2023.1`
* `aswf/ci-baseqt:2023.1`
* `aswf/ci-opencue:2023.1`
* `aswf/ci-openexr:2023.1`
* `aswf/ci-ocio:2023.1`
* `aswf/ci-otio:2023.1`
* `aswf/ci-materialx:2023.1`
* `aswf/ci-usd:2023.1`
* `aswf/ci-osl:2023-clang14.1`,`aswf/ci-osl:2023-clang15.1`
* `aswf/ci-openvdb:2023-clang14.1`, `aswf/ci-openvdb:2023-clang15.1`
* `aswf/ci-vfxall:2023-clang14.1`, `aswf/ci-vfxall:2023-clang15.1'

## 2023-06-06

* New ci-common-v3 for VFX Platform 2023 based on:
  * C++17 (unchanged)
  * Ccache 4.7.4 (from 4.0)
  * Clang 14.0.6 (from 14.0.0)
  * Clang 15.0.7
  * Conan 1.58.0 (from 1.47.0)
  * CUDA 11.8 (from 11.4.0)
  * gcc-toolset 11 / gcc 11.2.1 (from DTS 9 / gcc 9.3.1)
  * glibc 2.28 (from 2.17)
  * libstdc++11 new ABI
  * Ninja 1.11.1 (from 1.11.0)
  * Rocky Linux 8.8 (from CentOS 7.9)
  * SonarScan 4.8.0.2856 (from 4.7.0.2747)
* Updated 2023 Packages
  * Alembic 1.8.4 (from 1.8.2)
  * Boost 1.80.0 (from 1.76.0)
  * CMake 3.25.2 (from 3.22.0)
  * Hdf5 1.8.23 (from 1.8.21)
  * Imath 3.1.9
  * MaterialX 1.38.7 (from 1.38.5)
  * NumPy 1.23.5 (from 1.20)
  * OpenColorIO 2.2.1 (from 2.1.1)
  * OpenEXR 3.1.8
  * OpenImageIO 2.4.9.0 (from 2.4.5.0)
  * OpenSubdiv 3.5.0 (from 3.4.4)
  * OpenVDB 10.0.1 (from 9.1.0)
  * OpenShadingLanguage 1.12.10.0 (from 1.12.7.0)
  * OpenTimelineIO 0.15 (from 0.14.1)
  * Partio 1.14.6 (from 1.14.0)
  * Ptex 2.4.2 (from 2.4.0)
  * PySide 5.15.9 (from 5.15.2)
  * Python 3.10.9 (from 3.9.15)
  * Qt 5.15.9 (from 5.15.2)
  * USD 23.05 (from 22.11)
* Unchanged 2023 Packages
  * Blosc 1.17.0
  * CppUnit 1.15.1
  * GLEW 2.1.0
  * GLFW 3.1.2
  * gtest 1.11.0
  * HDF5 1.8.23
  * log4cplus 1.1.2
  * TBB 2020u3

### New CI Images

* `aswf/ci-common:3-clang14.0`, `aswf/ci-common:3-clang15.0` : A base Rocky 8 image with GCC 11.2.1 (DTS 11), Clang 14.0/15.0 and CUDA 11.8.
* `aswf/ci-base:2023.0`
* `aswf/ci-baseqt:2023.0`
* `aswf/ci-opencue:2023.0`
* `aswf/ci-openexr:2023.0`
* `aswf/ci-ocio:2023.0`
* `aswf/ci-otio:2023.0`
* `aswf/ci-materialx:2023.0`
* `aswf/ci-usd:2023.0`
* `aswf/ci-osl:2023-clang14.0`,`aswf/ci-osl:2023-clang15.0`
* `aswf/ci-openvdb:2023-clang14.0`, `aswf/ci-openvdb:2023-clang15.0`
* `aswf/ci-vfxall:2023-clang14.0`, `aswf/ci-vfxall:2023-clang15.0'

## 2023-01-21

* Added missing MaterialX to `ci-vfxall`

### New CI Images

* `aswf/ci-vfxall:2022-clang10.13`, `aswf/ci-vfxall:2022-clang11.13`, `aswf/ci-vfxall:2022-clang12.4`, `aswf/ci-vfxall:2022-clang13.4`, `aswf/ci-vfxall:2022-clang14.3`

## 2023-01-06

* Updated 2022 Packages
  * Blosc 1.17.0 (from 1.5.0)
  * MaterialX 1.38.5 (from 1.38.0)
  * OpenImageIO 2.4.5.0 (from 2.3.16.0)
  * OpenVDB 9.1.0 (from 9.0.0)
  * OpenShadingLanguage 1.12.7.0 (from 1.11.17.0)
  * Python 3.9.15 (from 3.9.11)
  * USD 22.11 (from 22.05a)
* Use conan build of TBB to fix #159
* Use conan build of Python to fix #160
* Updated github action versions (with new pipenv cache)

### New CI Images

* `aswf/ci-base:2022.4`
* `aswf/ci-baseqt:2022.4`
* `aswf/ci-opencue:2022.3`
* `aswf/ci-openexr:2022.3`
* `aswf/ci-ocio:2022.4`
* `aswf/ci-otio:2022.3`
* `aswf/ci-materialx:2022.1`
* `aswf/ci-usd:2022.4`
* `aswf/ci-osl:2022-clang10.11`, `aswf/ci-osl:2022-clang11.11`, `aswf/ci-osl:2022-clang12.2`, `aswf/ci-osl:2022-clang13.2`, `aswf/ci-osl:2022-clang14.1`
* `aswf/ci-openvdb:2022-clang10.12`, `aswf/ci-openvdb:2022-clang11.12`, `aswf/ci-openvdb:2022-clang12.3`, `aswf/ci-openvdb:2022-clang13.3`, `aswf/ci-openvdb:2022-clang14.2`
* `aswf/ci-vfxall:2022-clang10.12`, `aswf/ci-vfxall:2022-clang11.12`, `aswf/ci-vfxall:2022-clang12.3`, `aswf/ci-vfxall:2022-clang13.3`, `aswf/ci-vfxall:2022-clang14.2`

## 2022-06-06

* Updated ci-common-v2 to CentOS-7.9 and CUDA-11.4
* Added clang-14 for ci-common-v2
* Updated Conan to 1.47.0 (from 1.42.0)
* Added MaterialX 1.38.0 (version required by USD 22.05a)
* Updated 2022 Packages
  * Imath 3.1.5 (from 3.1.3)
  * OpenColorIO 2.1.1 (from 2.1.0)
  * OpenImageIO 2.3.16.0 (from 2.3.9.1)
  * OpenEXR 3.1.5 (from 3.1.3)
  * OpenShadingLanguage 1.11.17.0 (from 1.11.16.0)
  * OpenTimelineIO 0.14.1 (from 0.14)
  * Python 3.9.11 (from 3.9.7)
  * USD 22.05a (from 21.11)

### New CI Images

* `aswf/ci-common:2-clang10.5`, `aswf/ci-common:2-clang11.6`, `aswf/ci-common:2-clang12.1`, `aswf/ci-common:2-clang13.1`, `aswf/ci-common:2-clang14.0`
* `aswf/ci-base:2022.3`, `aswf/ci-baseqt:2022.3`
* `aswf/ci-opencue:2022.2`
* `aswf/ci-openexr:2022.2`
* `aswf/ci-ocio:2022.3`
* `aswf/ci-otio:2022.2`
* `aswf/ci-materialx:2022.0`
* `aswf/ci-usd:2022.3`
* `aswf/ci-osl:2022-clang10.10`, `aswf/ci-osl:2022-clang11.10`, `aswf/ci-osl:2022-clang12.1`, `aswf/ci-osl:2022-clang13.1`, `aswf/ci-osl:2022-clang14.0`
* `aswf/ci-openvdb:2022-clang10.10`, `aswf/ci-openvdb:2022-clang11.10`, `aswf/ci-openvdb:2022-clang12.1`, `aswf/ci-openvdb:2022-clang13.1`, `aswf/ci-openvdb:2022-clang14.0`
* `aswf/ci-vfxall:2022-clang10.10`, `aswf/ci-vfxall:2022-clang11.10`, `aswf/ci-vfxall:2022-clang12.1`, `aswf/ci-vfxall:2022-clang13.1`, `aswf/ci-vfxall:2022-clang14.0`

## 2021-11-20

* Updated 2022 Packages:
  * CMake 3.22.0 (from 3.20.5)
  * GTest 1.11.0 (new)
  * OpenImageIO 2.3.9.1 (from 2.3.7.2)
  * OpenEXR 3.1.3 (from 3.1.1)
  * OpenVDB 9.0.0 (from 8.1.0)
  * OpenShadingLanguage 1.11.16.0 (from 1.11.15.0)
  * OpenTimelineIO 0.14 (from 0.13)
  * Pybind11 2.8.1 (from 2.6.2)
  * USD 21.11 (from 21.05)
* Added GoogleTest (gtest):
  * vfx2019: 1.8.1
  * vfx2020: 1.10.0
  * vfx2021: 1.11.0
  * vfx2022: 1.11.0
* New [Conan](https://conan.io) base packages:
  * All base packages are already available [here](https://linuxfoundation.jfrog.io/ui/packages) with recipes [here](packages/conan/recipes).
  * Easily installed using a command such as `conan install clang/13.0.0@aswftesting/ci_common1 -g deploy`
  * Or with a `conanfile.txt` such as this:

```ini
[generators]
cmake_find_package_multi
virtualenv
[requires]
boost/latest@aswf/vfx2021
cmake/latest@aswf/vfx2021
cppunit/latest@aswf/vfx2021
glew/latest@aswf/vfx2021
glfw/latest@aswf/vfx2021
gtest/latest@aswf/vfx2021
log4cplus/latest@aswf/vfx2021
pybind11/latest@aswf/vfx2021
python/latest@aswf/vfx2021
tbb/latest@aswf/vfx2021
```

### New CI Images

* `aswf/ci-base:2019.9`, `aswf/ci-base:2020.9`, `aswf/ci-base:2021.6`, `aswf/ci-base:2022.2`
* `aswf/ci-baseqt:2019.2`, `aswf/baseqt:2020.2`, `aswf/baseqt:2021.3`, `aswf/baseqt:2022.2`
* `aswf/ci-ocio:2022.2`
* `aswf/ci-usd:2022.2`
* `aswf/ci-osl:2022-clang10.9`, `aswf/ci-osl:2022-clang11.9`, `aswf/ci-osl:2022-clang12.0`, `aswf/ci-osl:2022-clang13.0`
* `aswf/ci-openvdb:2022-clang10.9`, `aswf/ci-openvdb:2022-clang11.9`, `aswf/ci-openvdb:2022-clang12.0`, `aswf/ci-openvdb:2022-clang13.0`
* `aswf/ci-vfxall:2022-clang10.9`, `aswf/ci-vfxall:2022-clang11.9`, `aswf/ci-vfxall:2022-clang12.0`, `aswf/ci-vfxall:2022-clang13.0`

## 2021-09-04

* Updated 2022 Packages:
  * Python 3.9.7 (from 3.9.5)
  * Boost 1.76.0 (from 1.75.0)
  * OpenColorIO 2.1.0 (from 2.0.1)
  * OpenImageIO 2.3.7.2 (from 2.2.16.0)
  * Imath 3.1.3 (from 3.0.5)
  * OpenEXR 3.1.1 (from 3.0.5)
  * OpenSubdiv 3.4.4 (from 3.4.3)
  * OpenShadingLanguage 1.11.15.0 (from 1.11.14.2)
* `ci-osl` 2022 Updates:
  * Added TBB and OpenVDB
* `ci-ocio` 2022 Updates:
  * Add OSL
  * Add pybind11

### New CI Images

* `aswf/ci-base:2022.1`
* `aswf/ci-baseqt:2022.1`
* `aswf/ci-ocio:2022.1`
* `aswf/ci-opencue:2022.1`
* `aswf/ci-openexr:2022.1`
* `aswf/ci-otio:2022.1`
* `aswf/ci-usd:2022.1`
* `aswf/ci-openvdb:2022-clang10.8`, `aswf/ci-openvdb:2022-clang11.8`
* `aswf/ci-osl:2022-clang10.8`, `aswf/ci-osl:2022-clang11.8`
* `aswf/ci-vfxall:2022-clang10.8`, `aswf/ci-vfxall:2022-clang11.8`


## 2021-07-03

* Added new Imath package. N.B. that the package is a dummy empty package for versions 2 of IlmBase/OpenEXR. It is only meaningful since VFX-2022 and Imath-3.
* Added new VFX 2022 Draft images with the following versions:
  * python-3.9.5
  * tbb-2020_U3
  * boost-1.75.0
  * cppunit-1.15.1
  * log4cplus-1.1.2
  * glew-2.1.0
  * glfw-3.1.2
  * qt-5.15.2
  * pyside-5.15.2
  * cmake-3.20.5
  * openexr-3.0.5
  * blosc-1.5.0
  * alembic-1.8.2
  * oiio-2.2.16.0
  * ocio-2.0.1
  * opensubdiv-3_4_3
  * ptex-2.4.0
  * openvdb-8.1.0
  * usd-21.05
  * partio-1.14.0
  * osl-1.11.14.2
  * otio-0.13
  * numpy-1.20
* hdf5-1.8.21
* Stopped active maintenance of VFX 2018 images (images are still available on dockerhub, but will not be rebuilt anymore, the OS packages and sonar utilities will become stale over time!)

### New CI Images

* `ci-base:2022.0`
* `ci-baseqt:2022.0`
* `ci-opencue:2022.0`
* `ci-openexr:2022.0`
* `ci-ocio:2022.0`
* `ci-otio:2022.0`
* `ci-usd:2022.0`
* `ci-osl:2022-clang10.7`, `ci-osl:2022-clang11.7`
* `ci-openvdb:2022-clang10.7`, `ci-openvdb:2022-clang11.7`
* `ci-vfxall:2022-clang10.7`, `ci-vfxall:2022-clang11.7`


## 2021-06-19

### Changed
* Updated to sonar scanner cli v4.6.2.2472 and latest build wrapper

### New CI Images

- `ci-common`:
    - "1-clang6.8"
    - "1-clang7.8"
    - "1-clang8.8"
    - "1-clang9.8"
    - "1-clang10.8"
    - "2-clang10.4"
    - "2-clang11.4"
- `ci-base`:
    - "2018.8"
    - "2019.8"
    - "2020.8"
    - "2021.5"
- `ci-baseqt`:
    - "2018.1"
    - "2019.1"
    - "2020.1"
    - "2021.2"
- `ci-openexr`:
    - "2018.8"
    - "2019.8"
    - "2020.8"
    - "2021.5"
- `ci-ocio`:
    - "2018.9"
    - "2019.9"
    - "2020.8"
    - "2021.6"
- `ci-opencue`:
    - "2018.10"
    - "2019.10"
    - "2020.10"
    - "2021.7"
- `ci-usd`:
    - "2019.9"
    - "2020.8"
    - "2021.6"
- `ci-otio`:
    - "2019.3"
    - "2020.3"
    - "2021.5"
- `ci-osl`:
    - "2018-clang7.5"
    - "2019-clang6.5"
    - "2019-clang7.5"
    - "2019-clang8.5"
    - "2019-clang9.5"
    - "2019-clang10.5"
    - "2020-clang7.5"
    - "2021-clang10.7"
    - "2021-clang11.7"
- `ci-openvdb`:
    - "2018-clang7.8"
    - "2019-clang6.8"
    - "2019-clang7.8"
    - "2019-clang8.8"
    - "2019-clang9.8"
    - "2020-clang7.8"
    - "2021-clang10.6"
- `ci-vfxall`:
    - "2019-clang6.12"
    - "2019-clang7.12"
    - "2019-clang8.12"
    - "2019-clang9.12"
    - "2020-clang7.10"
    - "2021-clang10.7"


## 2021-05-12

### Changed

* Added OpenColorIO to `ci-osl` image
* Updated patch versions of VFX 2021 packages: 
  * OpenColorIO-2.0.1 (was 2.0.0)
  * OpenImageIO-2.2.15 (was 2.2.10)
  * OpenEXR-2.5.5 (was 2.5.2)
  * OpenVDB-8.0.1 (was 8.0.0)
  * OpenShadingLanguage-1.11.13 (was 1.11.10)
  * OpenTimelineIO-0.13 (was 0.12.1)
  * USD-21.05 (was 21.02)

### New CI Packages
* `ci-package-openexr-2021.2`
* `ci-package-ocio-2021.3`
* `ci-package-oiio-2021.3`
* `ci-package-openvdb-2021.2`
* `ci-package-usd-2021.4`
* `ci-package-osl-2021.2`
* `ci-package-otio-2021.2`

### New CI Images
* `ci-osl:2018-clang7.4`, `ci-osl:2019-clang6.4`, `ci-osl:2019-clang7.4`, `ci-osl:2019-clang8.4`, `ci-osl:2019-clang9.4`, `ci-osl:2019-clang10.4`, `ci-osl:2020-clang7.4`
* `aswf/ci-osl:2021-clang11.6`, `aswf/ci-osl:2021-clang10.6`
* `aswf/ci-ocio:2021.5`
* `aswf/ci-otio:2021.4`
* `aswf/ci-usd:2021.5`
* `aswf/ci-openvdb:2021-clang10.5`
* `aswf/ci-vfxall:2021-clang10.6`


## 2020-12-20

### Added

* Added PyBind11 2.6.2

### Changed

* Updated Qt in VFX-2021 images to version 5.15.2
* Updated Python to 3.7.9
* Updated cmake to 3.19.3
* Updated numpy to 1.19
* Updated Boost to 1.73.0
* Updated TBB to 2020_U2
* Updated Alembic to 1.7.16
* Updated USD to version 21.02
* Updated OpenColorIO to 2.0.0
* Updated OpenImageIO to 2.2.10.0
* Updated OpenEXR to 2.5.2
* Updated OpenVDB to 8.0.0
* Updated OpenShadingLanguage to 1.11.10.0
* Updated PartIO to 1.14.0


### New CI Packages:

* `ci-package-cmake:2021.1`
* `ci-package-python:2021.2`
* `ci-package-boost:2021.2`
* `ci-package-tbb:2021.2`
* `ci-package-qt:2021.2`
* `ci-package-pyside:2021.2`
* `ci-package-pybind11:2019.0`, `ci-package-pybind11:2020.0`, `ci-package-pybind11:2021.0`
* `ci-package-usd:2021.3`
* `ci-package-openexr:2021.2`
* `ci-package-alembic:2021.2`
* `ci-package-ocio:2021.3`
* `ci-package-oiio:2021.3`
* `ci-package-openvdb:2021.2`
* `ci-package-usd:2021.4`
* `ci-package-partio:2021.2`
* `ci-package-osl:2021.2`
* `ci-package-otio:2021.2`

### New CI Images:

* `ci-common:2-clang10.3`, `ci-common:2-clang11.3`
* `ci-base:2021.4`
* `ci-baseqt:2021.1`
* `ci-openexr:2021.4`
* `ci-ocio:2021.4`
* `ci-opencue:2021.4`
* `ci-openvdb:clang10-2021.4`
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

* Next image releases will contain newer [OCI Annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md)



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
