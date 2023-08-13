# syntax = docker/dockerfile:1.4
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# "Global" ARGs
ARG ASWF_ORG
ARG ASWF_BOOST_VERSION
ARG CI_COMMON_VERSION
ARG ASWF_CLANG_VERSION
ARG ASWF_CLANG_MAJOR_VERSION
ARG ASWF_CMAKE_VERSION
ARG ASWF_CPPUNIT_VERSION
ARG ASWF_CUDA_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
ARG ASWF_GLEW_VERSION
ARG ASWF_GLFW_VERSION
ARG ASWF_LOG4CPLUS_VERSION
ARG ASWF_NINJA_VERSION
ARG ASWF_NUMPY_VERSION
ARG ASWF_PYBIND11_VERSION
ARG ASWF_PYTHON_VERSION
ARG ASWF_PYTHON_MAJOR_MINOR_VERSION
ARG ASWF_TBB_VERSION
ARG ASWF_VFXPLATFORM_VERSION


#################### ci-baseos-gl-packages ####################
FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${ASWF_CLANG_MAJOR_VERSION} AS ci-baseos-gl-packages

COPY ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

ENV DOWNLOADS_DIR=/tmp/downloads \
    CCACHE_DIR=/tmp/ccache \
    ASWF_INSTALL_PREFIX=/usr/local


#################### ci-cmake-builder ####################
FROM ci-baseos-gl-packages AS ci-cmake-builder

ARG CI_COMMON_VERSION
ARG ASWF_CMAKE_VERSION
ENV ASWF_CMAKE_VERSION=${ASWF_CMAKE_VERSION}

COPY ../scripts/base/install_cmake.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/install_cmake.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-cmake ####################
FROM scratch AS ci-package-cmake

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_CMAKE_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-ninja"
LABEL org.opencontainers.image.title="CMake package built for ASWF Docker images"
LABEL org.opencontainers.image.description="CMake binary to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://cmake.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_CMAKE_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.cmake="${ASWF_CMAKE_VERSION}"

COPY --from=ci-cmake-builder /package/. /


#################### ci-base-builder ####################
FROM ci-cmake-builder AS ci-base-builder

ARG ASWF_PYTHON_MAJOR_MINOR_VERSION
ENV ASWF_PYTHON_MAJOR_MINOR_VERSION=${ASWF_PYTHON_MAJOR_MINOR_VERSION}
ARG ASWF_VFXPLATFORM_VERSION
ENV ASWF_VFXPLATFORM_VERSION=${ASWF_VFXPLATFORM_VERSION}

ENV PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${ASWF_PYTHON_MAJOR_MINOR_VERSION}/site-packages:${PYTHONPATH}


#################### ci-python-builder ####################
FROM ci-base-builder AS ci-python-builder

ARG ASWF_NUMPY_VERSION
ENV ASWF_NUMPY_VERSION=${ASWF_NUMPY_VERSION}
ARG ASWF_PYTHON_VERSION
ENV ASWF_PYTHON_VERSION=${ASWF_PYTHON_VERSION}

COPY ../scripts/base/build_python.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_python.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-python ####################
FROM scratch AS ci-package-python

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
ARG ASWF_NUMPY_VERSION
ARG ASWF_PYTHON_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-python"
LABEL org.opencontainers.image.title="Python and numpy packages built for ASWF Docker images"
LABEL org.opencontainers.image.description="Python (PSF-2.0 license) and numpy (BSD-3-Clause license) to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://www.python.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_PYTHON_VERSION}"
LABEL org.opencontainers.image.licenses="PSF-2.0 AND BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.python="${ASWF_PYTHON_VERSION}"
LABEL io.aswf.docker.versions.numpy="${ASWF_NUMPY_VERSION}"

COPY --from=ci-python-builder /package/. /


#################### ci-pybind11-builder ####################
FROM ci-python-builder as ci-pybind11-builder

ARG ASWF_PYBIND11_VERSION
ENV ASWF_PYBIND11_VERSION=${ASWF_PYBIND11_VERSION}

COPY ../scripts/base/build_pybind11.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_pybind11.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-pybind11 ####################
FROM scratch as ci-package-pybind11

ARG ASWF_ORG
ARG ASWF_PYBIND11_VERSION
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-pybind11"
LABEL org.opencontainers.image.title="Pybind11 package built for ASWF Docker images"
LABEL org.opencontainers.image.description="Pybind11 binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/pybind/pybind11"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_PYBIND11_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.pybind11="${ASWF_PYBIND11_VERSION}"

COPY --from=ci-pybind11-builder /package/. /
