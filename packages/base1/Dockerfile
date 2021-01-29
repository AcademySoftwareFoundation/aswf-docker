# syntax = docker/dockerfile:experimental
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


#################### ci-centos7-gl-packages ####################
FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${ASWF_CLANG_MAJOR_VERSION} as ci-centos7-gl-packages

COPY ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

ENV DOWNLOADS_DIR=/tmp/downloads \
    CCACHE_DIR=/tmp/ccache \
    ASWF_INSTALL_PREFIX=/usr/local


#################### ci-cmake-builder ####################
FROM ci-centos7-gl-packages as ci-cmake-builder

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
FROM scratch as ci-package-cmake

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_CMAKE_VERSION
ARG ASWF_DTS_VERSION
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
FROM ci-cmake-builder as ci-base-builder

ARG ASWF_PYTHON_MAJOR_MINOR_VERSION
ENV ASWF_PYTHON_MAJOR_MINOR_VERSION=${ASWF_PYTHON_MAJOR_MINOR_VERSION}
ARG ASWF_VFXPLATFORM_VERSION
ENV ASWF_VFXPLATFORM_VERSION=${ASWF_VFXPLATFORM_VERSION}

ENV PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${ASWF_PYTHON_MAJOR_MINOR_VERSION}/site-packages:${PYTHONPATH}


#################### ci-python-builder ####################
FROM ci-base-builder as ci-python-builder

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
FROM scratch as ci-package-python

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
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


#################### ci-boost-builder ####################
FROM ci-python-builder as ci-boost-builder

ARG ASWF_BOOST_VERSION
ENV ASWF_BOOST_VERSION=${ASWF_BOOST_VERSION}

COPY ../scripts/base/build_boost.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_boost.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-boost ####################
FROM scratch as ci-package-boost

ARG ASWF_ORG
ARG ASWF_BOOST_VERSION
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-boost"
LABEL org.opencontainers.image.title="Boost package built for ASWF Docker images"
LABEL org.opencontainers.image.description="Boost binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://www.boost.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_BOOST_VERSION}"
LABEL org.opencontainers.image.licenses="BSL-1.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.boost="${ASWF_BOOST_VERSION}"

COPY --from=ci-boost-builder /package/. /


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


#################### ci-tbb-builder ####################
FROM ci-base-builder as ci-tbb-builder

ARG ASWF_TBB_VERSION
ENV ASWF_TBB_VERSION=${ASWF_TBB_VERSION}

COPY ../scripts/base/build_tbb.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_tbb.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-tbb ####################
FROM scratch as ci-package-tbb

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_TBB_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-tbb"
LABEL org.opencontainers.image.title="Intel TBB package built for ASWF Docker images"
LABEL org.opencontainers.image.description="TBB binaries and headers to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://software.intel.com/en-us/tbb"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_TBB_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.tbb="${ASWF_TBB_VERSION}"

COPY --from=ci-tbb-builder /package/. /


#################### ci-cppunit-builder ####################
FROM ci-python-builder as ci-cppunit-builder

ARG ASWF_CPPUNIT_VERSION
ENV ASWF_CPPUNIT_VERSION=${ASWF_CPPUNIT_VERSION}

COPY ../scripts/base/build_cppunit.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_cppunit.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-cppunit ####################
FROM scratch as ci-package-cppunit

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_CPPUNIT_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-cppunit"
LABEL org.opencontainers.image.title="CppUnit package built for ASWF Docker images"
LABEL org.opencontainers.image.description="CppUnit headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://www.boost.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_CPPUNIT_VERSION}"
LABEL org.opencontainers.image.licenses="LGPL-2.1-only"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.cppunit="${ASWF_CPPUNIT_VERSION}"

COPY --from=ci-cppunit-builder /package/. /


#################### ci-log4cplus-builder ####################
FROM ci-python-builder as ci-log4cplus-builder

ARG ASWF_LOG4CPLUS_VERSION
ENV ASWF_LOG4CPLUS_VERSION=${ASWF_LOG4CPLUS_VERSION}

COPY ../scripts/base/build_log4cplus.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_log4cplus.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-log4cplus ####################
FROM scratch as ci-package-log4cplus

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_LOG4CPLUS_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-log4cplus"
LABEL org.opencontainers.image.title="log4cplus package built for ASWF Docker images"
LABEL org.opencontainers.image.description="log4cplus headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://sourceforge.net/projects/log4cplus/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_LOG4CPLUS_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-2-Clause AND Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.log4cplus="${ASWF_LOG4CPLUS_VERSION}"

COPY --from=ci-log4cplus-builder /package/. /


#################### ci-glew-builder ####################
FROM ci-python-builder as ci-glew-builder

ARG ASWF_GLEW_VERSION
ENV ASWF_GLEW_VERSION=${ASWF_GLEW_VERSION}

COPY ../scripts/base/build_glew.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_glew.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-glew ####################
FROM scratch as ci-package-glew

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_GLEW_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-glew"
LABEL org.opencontainers.image.title="glew package built for ASWF Docker images"
LABEL org.opencontainers.image.description="glew headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="http://glew.sourceforge.net/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_GLEW_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause AND MIT"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.glew="${ASWF_GLEW_VERSION}"

COPY --from=ci-glew-builder /package/. /


#################### ci-glfw-builder ####################
FROM ci-python-builder as ci-glfw-builder

ARG ASWF_GLFW_VERSION
ENV ASWF_GLFW_VERSION=${ASWF_GLFW_VERSION}

COPY ../scripts/base/build_glfw.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_glfw.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-glfw ####################
FROM scratch as ci-package-glfw

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_GLFW_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-glfw"
LABEL org.opencontainers.image.title="glfw package built for ASWF Docker images"
LABEL org.opencontainers.image.description="glfw headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://www.glfw.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_GLFW_VERSION}"
LABEL org.opencontainers.image.licenses="Zlib"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.glfw="${ASWF_GLFW_VERSION}"

COPY --from=ci-glfw-builder /package/. /
