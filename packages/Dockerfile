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

# Required base packages built in previous passes to speed things up
FROM ${ASWF_ORG}/ci-package-clang:${CI_COMMON_VERSION} as ci-package-clang-external
FROM ${ASWF_ORG}/ci-package-python:${VFXPLATFORM_VERSION} as ci-package-python-external
FROM ${ASWF_ORG}/ci-package-boost:${VFXPLATFORM_VERSION} as ci-package-boost-external
FROM ${ASWF_ORG}/ci-package-qt:${VFXPLATFORM_VERSION} as ci-package-qt-external
FROM ${ASWF_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION} as ci-package-pyside-external

#################### ci-centos7-gl-packages ####################
FROM nvidia/cudagl:${CUDA_VERSION}-devel-centos7 as ci-centos7-gl-packages

ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG CUDA_VERSION

COPY ../scripts/common/install_yumpackages.sh \
     ../scripts/${CI_COMMON_VERSION}/versions_common.sh \
     ../scripts/common/install_dev_ccache.sh \
     ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

RUN --mount=type=cache,sharing=private,target=/var/cache/yum \
    source /tmp/versions_common.sh && \
    /tmp/install_yumpackages.sh

ENV CI_COMMON_VERSION=${CI_COMMON_VERSION} \
    DOWNLOADS_DIR=/tmp/downloads \
    CCACHE_DIR=/tmp/ccache \
    ASWF_INSTALL_PREFIX=/usr/local \
    LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/lib64:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/lib:${LD_LIBRARY_PATH} \
    PATH=/opt/aswfbuilder/bin:/usr/local/bin:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/bin/:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin \
    CUDA_VERSION=${CUDA_VERSION}

RUN --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_common.sh && \
    /tmp/install_dev_ccache.sh


#################### ci-clang-builder ####################
FROM ci-centos7-gl-packages as ci-clang-builder

ARG CI_COMMON_VERSION

COPY ../scripts/${CI_COMMON_VERSION}/versions_common.sh \
     ../scripts/common/build_clang.sh \
     ../scripts/common/install_dev_cmake.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,target=/tmp/downloads \
    source /tmp/versions_common.sh && \
    /tmp/install_dev_cmake.sh && \
    /tmp/before_build.sh && \
    /tmp/build_clang.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-clang ####################
# This build target is used to generate a packages of clang that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-clang

COPY --from=ci-clang-builder /package/. /


#################### ci-ninja-builder ####################
FROM ci-centos7-gl-packages as ci-ninja-builder

ARG CI_COMMON_VERSION

COPY ../scripts/${CI_COMMON_VERSION}/versions_common.sh \
     ../scripts/common/build_ninja.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,target=/tmp/downloads \
    source /tmp/versions_common.sh && \
    /tmp/before_build.sh && \
    /tmp/build_ninja.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-ninja ####################
# This build target is used to generate a packages of ninja that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-ninja

COPY --from=ci-ninja-builder /package/. /


#################### ci-base-builder ####################
FROM ci-centos7-gl-packages as ci-base-builder

ARG VFXPLATFORM_VERSION
ARG PYTHON_VERSION

ENV PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${PYTHON_VERSION}/site-packages:${PYTHONPATH}
ENV VFXPLATFORM_VERSION=${VFXPLATFORM_VERSION}

COPY ../scripts/${VFXPLATFORM_VERSION}/versions_base.sh \
     ../scripts/base/install_cmake.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/install_cmake.sh


#################### ci-python-builder ####################
FROM ci-base-builder as ci-python-builder

COPY ../scripts/${VFXPLATFORM_VERSION}/versions_base.sh \
     ../scripts/base/build_python.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_python.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-boost ####################
# This build target is used to generate a packages of boost that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-python

COPY --from=ci-python-builder /package/. /


#################### ci-boost-builder ####################
FROM ci-python-builder as ci-boost-builder

ARG VFXPLATFORM_VERSION
ARG PYTHON_VERSION

COPY ../scripts/base/build_boost.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_boost.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-boost ####################
# This build target is used to generate a packages of boost that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-boost

COPY --from=ci-boost-builder /package/. /


#################### ci-tbb-builder ####################
FROM ci-python-builder as ci-tbb-builder

COPY ../scripts/base/build_tbb.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_tbb.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-tbb ####################
# This build target is used to generate a packages of tbb that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-tbb

COPY --from=ci-tbb-builder /package/. /


#################### ci-cppunit-builder ####################
FROM ci-python-builder as ci-cppunit-builder

COPY ../scripts/base/build_cppunit.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_cppunit.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-cppunit ####################
# This build target is used to generate a packages of cppunit that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-cppunit

COPY --from=ci-cppunit-builder /package/. /


#################### ci-log4cplus-builder ####################
FROM ci-python-builder as ci-log4cplus-builder

COPY ../scripts/base/build_log4cplus.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_log4cplus.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-log4cplus ####################
# This build target is used to generate a packages of log4cplus that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-log4cplus

COPY --from=ci-log4cplus-builder /package/. /


#################### ci-glew-builder ####################
FROM ci-python-builder as ci-glew-builder

COPY ../scripts/base/build_glew.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_glew.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-glew ####################
# This build target is used to generate a packages of glew that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-glew

COPY --from=ci-glew-builder /package/. /



#################### ci-glfw-builder ####################
FROM ci-python-builder as ci-glfw-builder

COPY ../scripts/base/build_glfw.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_glfw.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-glfw ####################
# This build target is used to generate a packages of glfw that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-glfw

COPY --from=ci-glfw-builder /package/. /


#################### ci-qt-builder ####################
FROM ci-python-builder as ci-qt-builder

COPY ../scripts/base/build_qt.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_qt.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-qt ####################
# This build target is used to generate a packages of qt that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-qt

COPY --from=ci-qt-builder /package/. /


#################### ci-pyside-builder ####################
FROM ci-python-builder as ci-pyside-builder

# Workaround pyside issue with Qt headers within system location https://bugreports.qt.io/browse/PYSIDE-787
COPY --from=ci-package-qt-external /. /tmp/qt5temp

COPY ../scripts/base/build_pyside.sh \
     /tmp/

COPY --from=ci-package-clang-external /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_pyside.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-pyside ####################
# This build target is used to generate a packages of pyside that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-pyside

COPY --from=ci-pyside-builder /package/. /



#################### ci-openexr-builder ####################
FROM ci-base-builder as ci-openexr-builder

COPY --from=ci-package-python-external /. /usr/local/
COPY --from=ci-package-boost-external /. /usr/local/

COPY ../scripts/$VFXPLATFORM_VERSION/versions_vfx.sh \
     ../scripts/vfx/build_openexr.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_openexr.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-openexr ####################
# This build target is used to generate a packages of openexr that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-openexr

COPY --from=ci-openexr-builder /package/. /


#################### ci-blosc-builder ####################
FROM ci-python-builder as ci-blosc-builder

COPY ../scripts/$VFXPLATFORM_VERSION/versions_vfx.sh \
     ../scripts/vfx/build_blosc.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_blosc.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-blosc ####################
# This build target is used to generate a packages of blosc that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-blosc

COPY --from=ci-blosc-builder /package/. /


#################### ci-partio-builder ####################
FROM ci-python-builder as ci-partio-builder

COPY ../scripts/$VFXPLATFORM_VERSION/versions_vfx.sh \
     ../scripts/vfx/build_partio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_partio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-partio ####################
# This build target is used to generate a packages of partio that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-partio

COPY --from=ci-partio-builder /package/. /


#################### ci-oiio-builder ####################
FROM ci-openexr-builder as ci-oiio-builder

COPY ../scripts/vfx/build_oiio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_oiio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-oiio ####################
# This build target is used to generate a packages of oiio that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-oiio

COPY --from=ci-oiio-builder /package/. /


#################### ci-ocio-builder ####################
FROM ci-oiio-builder as ci-ocio-builder

COPY ../scripts/vfx/build_ocio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_ocio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-ocio ####################
# This build target is used to generate a packages of ocio that
# can be placed in a downloadable artifact

FROM scratch as ci-package-ocio

COPY --from=ci-ocio-builder /package/. /


#################### ci-oiio-util-builder ####################
FROM ci-ocio-builder as ci-oiio-util-builder

COPY ../scripts/vfx/build_oiio_util.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_oiio_util.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-oiio ####################
# This build target is used to generate a packages of oiio that
# can be placed in a downloadable artifact

FROM scratch as ci-package-oiio

COPY --from=ci-oiio-util-builder /package/. /


#################### ci-osl-builder ####################
FROM ci-oiio-builder as ci-osl-builder

COPY --from=ci-package-clang-external /. /usr/local/
COPY --from=ci-package-qt-external /. /usr/local/
COPY --from=ci-package-partio /. /usr/local/

COPY ../scripts/vfx/build_osl.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_osl.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-osl ####################
# This build target is used to generate a packages of osl that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-osl

COPY --from=ci-osl-builder /package/. /


#################### ci-alembic-builder ####################
FROM ci-openexr-builder as ci-alembic-builder

COPY ../scripts/vfx/build_alembic.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_alembic.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-alembic ####################
# This build target is used to generate a packages of alembic that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-alembic

COPY --from=ci-alembic-builder /package/. /



#################### ci-ptex-builder ####################
FROM ci-openexr-builder as ci-ptex-builder

COPY ../scripts/vfx/build_ptex.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_ptex.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-ptex ####################
# This build target is used to generate a packages of ptex that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-ptex

COPY --from=ci-ptex-builder /package/. /




#################### ci-opensubdiv-builder ####################
FROM ci-ptex-builder as ci-opensubdiv-builder

COPY ../scripts/vfx/build_opensubdiv.sh \
     /tmp/

COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-tbb /. /usr/local/
COPY --from=ci-package-glfw /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_opensubdiv.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-opensubdiv ####################
# This build target is used to generate a packages of opensubdiv that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-opensubdiv

COPY --from=ci-opensubdiv-builder /package/. /




#################### ci-openvdb-builder ####################
FROM ci-openexr-builder as ci-openvdb-builder

COPY ../scripts/vfx/build_openvdb.sh \
     /tmp/

COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-tbb /. /usr/local/
COPY --from=ci-package-cppunit /. /usr/local/
COPY --from=ci-package-glfw /. /usr/local/
COPY --from=ci-package-blosc /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_openvdb.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-openvdb ####################
# This build target is used to generate a packages of openvdb that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-openvdb

COPY --from=ci-openvdb-builder /package/. /




#################### ci-usd-builder ####################
FROM ci-opensubdiv-builder as ci-usd-builder

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
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_usd.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-usd ####################
# This build target is used to generate a packages of usd that 
# can be placed in a downloadable artifact

FROM scratch as ci-package-usd

COPY --from=ci-usd-builder /package/. /


