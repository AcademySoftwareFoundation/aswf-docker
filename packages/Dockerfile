# syntax = docker/dockerfile:experimental
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# "Global" ARGs
ARG CI_COMMON_VERSION=1
ARG VFXPLATFORM_VERSION=2019
ARG PYTHON_VERSION=2.7
ARG CUDA_VERSION=10.2
ARG DTS_VERSION=6
ARG ASWF_ORG=aswftesting
ARG CLANG_VERSION
ARG NINJA_VERSION
ARG SONAR_VERSION
ARG CCACHE_VERSION
ARG BOOST_VERSION
ARG CMAKE_VERSION
ARG CPPUNIT_VERSION
ARG GLEW_VERSION
ARG GLFW_VERSION
ARG LOG4CPLUS_VERSION
ARG NUMPY_VERSION
ARG PYSIDE_VERSION
ARG PYTHON_VERSION
ARG QT_VERSION
ARG TBB_VERSION
ARG BLOSC_VERSION
ARG OIIO_VERSION
ARG OPENEXR_VERSION
ARG OCIO_VERSION
ARG OCIO_CONFIGS_VERSION
ARG HDF5_VERSION
ARG ALEMBIC_VERSION
ARG PTEX_VERSION
ARG OPENSUBDIV_VERSION
ARG OPENVDB_VERSION
ARG USD_VERSION
ARG OSL_VERSION
ARG OTIO_VERSION
ARG PARTIO_VERSION

# Required base packages built in previous passes to speed things up
FROM ${ASWF_ORG}/ci-package-clang:${CI_COMMON_VERSION}-${CLANG_VERSION} as ci-package-clang-external
FROM ${ASWF_ORG}/ci-package-python:${VFXPLATFORM_VERSION}-${PYTHON_VERSION} as ci-package-python-external
FROM ${ASWF_ORG}/ci-package-boost:${VFXPLATFORM_VERSION}-${BOOST_VERSION} as ci-package-boost-external
FROM ${ASWF_ORG}/ci-package-qt:${VFXPLATFORM_VERSION}-${QT_VERSION} as ci-package-qt-external
FROM ${ASWF_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION}-${PYSIDE_VERSION} as ci-package-pyside-external

#################### ci-centos7-gl-packages ####################
FROM nvidia/cudagl:${CUDA_VERSION}-devel-centos7 as ci-centos7-gl-packages

ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG CUDA_VERSION

COPY ../scripts/common/install_yumpackages.sh \
     /tmp/

RUN --mount=type=cache,sharing=private,target=/var/cache/yum \
    /tmp/install_yumpackages.sh

COPY ../scripts/common/install_dev_ccache.sh \
     ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     ../scripts/common/install_dev_cmake.sh \
     /tmp/

ENV CI_COMMON_VERSION=${CI_COMMON_VERSION} \
    DOWNLOADS_DIR=/tmp/downloads \
    CCACHE_DIR=/tmp/ccache \
    ASWF_INSTALL_PREFIX=/usr/local \
    LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/lib64:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/lib:${LD_LIBRARY_PATH} \
    PATH=/opt/aswfbuilder/bin:/usr/local/bin:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/bin/:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin \
    CUDA_VERSION=${CUDA_VERSION}

RUN --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/install_dev_cmake.sh && \
    /tmp/install_dev_ccache.sh


#################### ci-clang-builder ####################
FROM ci-centos7-gl-packages as ci-clang-builder
ARG CLANG_VERSION
ENV CLANG_VERSION=${CLANG_VERSION}

COPY ../scripts/common/build_clang.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,target=/tmp/downloads \
    /tmp/install_dev_cmake.sh && \
    /tmp/before_build.sh && \
    /tmp/build_clang.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-clang ####################
FROM scratch as ci-package-clang
ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG CLANG_VERSION
LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-clang"
LABEL org.opencontainers.image.title="Clang package built for ASWF docker images"
LABEL org.opencontainers.image.description="Clang (llvm) build artifacts to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://llvm.org/"
LABEL org.opencontainers.image.source="https://github.com/llvm/llvm-project"
LABEL org.opencontainers.image.version="${CLANG_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.clang="${CLANG_VERSION}"

COPY --from=ci-clang-builder /package/. /


#################### ci-ninja-builder ####################
FROM ci-centos7-gl-packages as ci-ninja-builder

ARG NINJA_VERSION
ENV NINJA_VERSION=${NINJA_VERSION}

COPY ../scripts/common/build_ninja.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_ninja.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-ninja ####################
FROM scratch as ci-package-ninja
ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG NINJA_VERSION
LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-ninja"
LABEL org.opencontainers.image.title="Ninja package built for ASWF docker images"
LABEL org.opencontainers.image.description="Ninja binary to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://ninja-build.org/"
LABEL org.opencontainers.image.source="https://github.com/ninja-build/ninja"
LABEL org.opencontainers.image.version="${NINJA_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.ninja="${NINJA_VERSION}"

COPY --from=ci-ninja-builder /package/. /


#################### ci-cmake-builder ####################
FROM ci-centos7-gl-packages as ci-cmake-builder

ARG CI_COMMON_VERSION
ARG CMAKE_VERSION
ENV CMAKE_VERSION=${CMAKE_VERSION}

COPY ../scripts/base/install_cmake.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/install_cmake.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-cmake ####################
FROM scratch as ci-package-cmake
ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG VFXPLATFORM_VERSION
ARG CMAKE_VERSION
LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-ninja"
LABEL org.opencontainers.image.title="CMake package built for ASWF docker images"
LABEL org.opencontainers.image.description="CMake binary to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://cmake.org/"
LABEL org.opencontainers.image.source="https://gitlab.kitware.com/cmake/cmake"
LABEL org.opencontainers.image.version="${CMAKE_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.cmake="${CMAKE_VERSION}"

COPY --from=ci-cmake-builder /package/. /


#################### ci-base-builder ####################
FROM ci-cmake-builder as ci-base-builder

ARG VFXPLATFORM_VERSION
ARG PYTHON_VERSION

ENV PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${PYTHON_VERSION}/site-packages:${PYTHONPATH}
ENV VFXPLATFORM_VERSION=${VFXPLATFORM_VERSION}


#################### ci-python-builder ####################
FROM ci-base-builder as ci-python-builder
ARG PYTHON_VERSION
ENV PYTHON_VERSION=${PYTHON_VERSION}
ARG NUMPY_VERSION
ENV NUMPY_VERSION=${NUMPY_VERSION}

COPY ../scripts/base/build_python.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_python.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-python ####################
# This build target is used to generate a packages of python that
# can be placed in a downloadable artifact
FROM scratch as ci-package-python
ARG PYTHON_VERSION
ENV PYTHON_VERSION=${PYTHON_VERSION}
ARG NUMPY_VERSION
ENV NUMPY_VERSION=${NUMPY_VERSION}

COPY --from=ci-python-builder /package/. /


#################### ci-boost-builder ####################
FROM ci-python-builder as ci-boost-builder
ARG BOOST_VERSION
ENV BOOST_VERSION=${BOOST_VERSION}

COPY ../scripts/base/build_boost.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_boost.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-boost ####################
# This build target is used to generate a packages of boost that
# can be placed in a downloadable artifact

FROM scratch as ci-package-boost
ARG BOOST_VERSION
ENV BOOST_VERSION=${BOOST_VERSION}

COPY --from=ci-boost-builder /package/. /


#################### ci-tbb-builder ####################
FROM ci-base-builder as ci-tbb-builder
ARG TBB_VERSION
ENV TBB_VERSION=${TBB_VERSION}

COPY ../scripts/base/build_tbb.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_tbb.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-tbb ####################
# This build target is used to generate a packages of tbb that
# can be placed in a downloadable artifact

FROM scratch as ci-package-tbb
ARG TBB_VERSION
ENV TBB_VERSION=${TBB_VERSION}

COPY --from=ci-tbb-builder /package/. /


#################### ci-cppunit-builder ####################
FROM ci-python-builder as ci-cppunit-builder
ARG CPPUNIT_VERSION
ENV CPPUNIT_VERSION=${CPPUNIT_VERSION}

COPY ../scripts/base/build_cppunit.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_cppunit.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-cppunit ####################
# This build target is used to generate a packages of cppunit that
# can be placed in a downloadable artifact

FROM scratch as ci-package-cppunit
ARG CPPUNIT_VERSION
ENV CPPUNIT_VERSION=${CPPUNIT_VERSION}

COPY --from=ci-cppunit-builder /package/. /


#################### ci-log4cplus-builder ####################
FROM ci-python-builder as ci-log4cplus-builder
ARG LOG4CPLUS_VERSION
ENV LOG4CPLUS_VERSION=${LOG4CPLUS_VERSION}

COPY ../scripts/base/build_log4cplus.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_log4cplus.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-log4cplus ####################
# This build target is used to generate a packages of log4cplus that
# can be placed in a downloadable artifact

FROM scratch as ci-package-log4cplus
ARG LOG4CPLUS_VERSION
ENV LOG4CPLUS_VERSION=${LOG4CPLUS_VERSION}

COPY --from=ci-log4cplus-builder /package/. /


#################### ci-glew-builder ####################
FROM ci-python-builder as ci-glew-builder
ARG GLEW_VERSION
ENV GLEW_VERSION=${GLEW_VERSION}

COPY ../scripts/base/build_glew.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_glew.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-glew ####################
# This build target is used to generate a packages of glew that
# can be placed in a downloadable artifact

FROM scratch as ci-package-glew
ARG GLEW_VERSION
ENV GLEW_VERSION=${GLEW_VERSION}

COPY --from=ci-glew-builder /package/. /



#################### ci-glfw-builder ####################
FROM ci-python-builder as ci-glfw-builder
ARG GLFW_VERSION
ENV GLFW_VERSION=${GLFW_VERSION}

COPY ../scripts/base/build_glfw.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_glfw.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-glfw ####################
# This build target is used to generate a packages of glfw that
# can be placed in a downloadable artifact

FROM scratch as ci-package-glfw
ARG GLFW_VERSION
ENV GLFW_VERSION=${GLFW_VERSION}

COPY --from=ci-glfw-builder /package/. /


#################### ci-qt-builder ####################
FROM ci-python-builder as ci-qt-builder
ARG QT_VERSION
ENV QT_VERSION=${QT_VERSION}

COPY ../scripts/base/build_qt.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_qt.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-qt ####################
# This build target is used to generate a packages of qt that
# can be placed in a downloadable artifact

FROM scratch as ci-package-qt
ARG QT_VERSION
ENV QT_VERSION=${QT_VERSION}

COPY --from=ci-qt-builder /package/. /


#################### ci-pyside-builder ####################
FROM ci-python-builder as ci-pyside-builder
ARG PYSIDE_VERSION
ENV PYSIDE_VERSION=${PYSIDE_VERSION}

# Workaround pyside issue with Qt headers within system location https://bugreports.qt.io/browse/PYSIDE-787
COPY --from=ci-package-qt-external /. /tmp/qt5temp

COPY ../scripts/base/build_pyside.sh \
     /tmp/

COPY --from=ci-package-clang-external /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_pyside.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-pyside ####################
# This build target is used to generate a packages of pyside that
# can be placed in a downloadable artifact

FROM scratch as ci-package-pyside
ARG PYSIDE_VERSION
ENV PYSIDE_VERSION=${PYSIDE_VERSION}

COPY --from=ci-pyside-builder /package/. /



#################### ci-openexr-builder ####################
FROM ci-base-builder as ci-openexr-builder
ARG OPENEXR_VERSION
ENV OPENEXR_VERSION=${OPENEXR_VERSION}

COPY --from=ci-package-python-external /. /usr/local/
COPY --from=ci-package-boost-external /. /usr/local/

COPY ../scripts/vfx/build_openexr.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_openexr.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-openexr ####################
# This build target is used to generate a packages of openexr that
# can be placed in a downloadable artifact

FROM scratch as ci-package-openexr
ARG OPENEXR_VERSION
ENV OPENEXR_VERSION=${OPENEXR_VERSION}

COPY --from=ci-openexr-builder /package/. /


#################### ci-blosc-builder ####################
FROM ci-python-builder as ci-blosc-builder
ARG BLOSC_VERSION
ENV BLOSC_VERSION=${BLOSC_VERSION}

COPY ../scripts/vfx/build_blosc.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_blosc.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-blosc ####################
# This build target is used to generate a packages of blosc that
# can be placed in a downloadable artifact

FROM scratch as ci-package-blosc
ARG BLOSC_VERSION
ENV BLOSC_VERSION=${BLOSC_VERSION}

COPY --from=ci-blosc-builder /package/. /


#################### ci-partio-builder ####################
FROM ci-python-builder as ci-partio-builder
ARG PARTIO_VERSION
ENV PARTIO_VERSION=${PARTIO_VERSION}

COPY ../scripts/vfx/build_partio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_partio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-partio ####################
# This build target is used to generate a packages of partio that
# can be placed in a downloadable artifact

FROM scratch as ci-package-partio
ARG PARTIO_VERSION
ENV PARTIO_VERSION=${PARTIO_VERSION}

COPY --from=ci-partio-builder /package/. /


#################### ci-oiio-builder ####################
FROM ci-openexr-builder as ci-oiio-builder
ARG OIIO_VERSION
ENV OIIO_VERSION=${OIIO_VERSION}

COPY ../scripts/vfx/build_oiio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_oiio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-oiio ####################
# This build target is used to generate a packages of oiio that
# can be placed in a downloadable artifact

FROM scratch as ci-package-oiio
ARG OIIO_VERSION
ENV OIIO_VERSION=${OIIO_VERSION}

COPY --from=ci-oiio-builder /package/. /


#################### ci-ocio-builder ####################
FROM ci-oiio-builder as ci-ocio-builder
ARG OCIO_VERSION
ENV OCIO_VERSION=${OCIO_VERSION}

COPY ../scripts/vfx/build_ocio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_ocio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-ocio ####################
# This build target is used to generate a packages of ocio that
# can be placed in a downloadable artifact

FROM scratch as ci-package-ocio
ARG OCIO_VERSION
ENV OCIO_VERSION=${OCIO_VERSION}

COPY --from=ci-ocio-builder /package/. /


#################### ci-osl-builder ####################
FROM ci-oiio-builder as ci-osl-builder
ARG OSL_VERSION
ENV OSL_VERSION=${OSL_VERSION}

COPY --from=ci-package-clang-external /. /usr/local/
COPY --from=ci-package-qt-external /. /usr/local/
COPY --from=ci-package-partio /. /usr/local/

COPY ../scripts/vfx/build_osl.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_osl.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-osl ####################
# This build target is used to generate a packages of osl that
# can be placed in a downloadable artifact

FROM scratch as ci-package-osl
ARG OSL_VERSION
ENV OSL_VERSION=${OSL_VERSION}

COPY --from=ci-osl-builder /package/. /


#################### ci-alembic-builder ####################
FROM ci-openexr-builder as ci-alembic-builder
ARG ALEMBIC_VERSION
ENV ALEMBIC_VERSION=${ALEMBIC_VERSION}

COPY ../scripts/vfx/build_alembic.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_alembic.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-alembic ####################
# This build target is used to generate a packages of alembic that
# can be placed in a downloadable artifact

FROM scratch as ci-package-alembic
ARG ALEMBIC_VERSION
ENV ALEMBIC_VERSION=${ALEMBIC_VERSION}

COPY --from=ci-alembic-builder /package/. /



#################### ci-ptex-builder ####################
FROM ci-openexr-builder as ci-ptex-builder
ARG PTEX_VERSION
ENV PTEX_VERSION=${PTEX_VERSION}

COPY ../scripts/vfx/build_ptex.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_ptex.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-ptex ####################
# This build target is used to generate a packages of ptex that
# can be placed in a downloadable artifact

FROM scratch as ci-package-ptex
ARG PTEX_VERSION
ENV PTEX_VERSION=${PTEX_VERSION}

COPY --from=ci-ptex-builder /package/. /




#################### ci-opensubdiv-builder ####################
FROM ci-ptex-builder as ci-opensubdiv-builder
ARG OPENSUBDIV_VERSION
ENV OPENSUBDIV_VERSION=${OPENSUBDIV_VERSION}

COPY ../scripts/vfx/build_opensubdiv.sh \
     /tmp/

COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-tbb /. /usr/local/
COPY --from=ci-package-glfw /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_opensubdiv.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-opensubdiv ####################
# This build target is used to generate a packages of opensubdiv that
# can be placed in a downloadable artifact

FROM scratch as ci-package-opensubdiv
ARG OPENSUBDIV_VERSION
ENV OPENSUBDIV_VERSION=${OPENSUBDIV_VERSION}

COPY --from=ci-opensubdiv-builder /package/. /




#################### ci-openvdb-builder ####################
FROM ci-openexr-builder as ci-openvdb-builder
ARG OPENVDB_VERSION
ENV OPENVDB_VERSION=${OPENVDB_VERSION}

COPY ../scripts/vfx/build_openvdb.sh \
     /tmp/

COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-tbb /. /usr/local/
COPY --from=ci-package-cppunit /. /usr/local/
COPY --from=ci-package-glfw /. /usr/local/
COPY --from=ci-package-blosc /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_openvdb.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-openvdb ####################
# This build target is used to generate a packages of openvdb that
# can be placed in a downloadable artifact

FROM scratch as ci-package-openvdb
ARG OPENVDB_VERSION
ENV OPENVDB_VERSION=${OPENVDB_VERSION}

COPY --from=ci-openvdb-builder /package/. /




#################### ci-usd-builder ####################
FROM ci-opensubdiv-builder as ci-usd-builder
ARG USD_VERSION
ENV USD_VERSION=${USD_VERSION}

COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-alembic /. /usr/local/
COPY --from=ci-package-openvdb /. /usr/local/
COPY --from=ci-package-oiio /. /usr/local/
COPY --from=ci-package-ocio /. /usr/local/
COPY --from=ci-package-qt-external /. /usr/local/
COPY --from=ci-package-pyside-external /. /usr/local/

COPY ../scripts/vfx/build_usd.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_usd.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-usd ####################
# This build target is used to generate a packages of usd that
# can be placed in a downloadable artifact

FROM scratch as ci-package-usd
ARG USD_VERSION
ENV USD_VERSION=${USD_VERSION}

COPY --from=ci-usd-builder /package/. /



#################### ci-otio-builder ####################
FROM ci-python-builder as ci-otio-builder
ARG OTIO_VERSION
ENV OTIO_VERSION=${OTIO_VERSION}

COPY --from=ci-package-clang-external /. /usr/local/
COPY --from=ci-package-qt-external /. /usr/local/
COPY --from=ci-package-pyside-external /. /usr/local/

COPY ../scripts/vfx/build_otio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_otio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-otio ####################
# This build target is used to generate a package of otio that
# can be placed in a downloadable artifact

FROM scratch as ci-package-otio
ARG OTIO_VERSION
ENV OTIO_VERSION=${OTIO_VERSION}

COPY --from=ci-otio-builder /package/. /

