# syntax = docker/dockerfile:experimental
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# "Global" ARGs
ARG ASWF_ORG
ARG BOOST_VERSION
ARG CI_COMMON_VERSION
ARG CLANG_VERSION
ARG CLANG_MAJOR_VERSION
ARG CMAKE_VERSION
ARG CPPUNIT_VERSION
ARG CUDA_VERSION
ARG DTS_VERSION
ARG GLEW_VERSION
ARG GLFW_VERSION
ARG LOG4CPLUS_VERSION
ARG NINJA_VERSION
ARG NUMPY_VERSION
ARG PYTHON_VERSION
ARG PYTHON_VERSION_MAJOR_MINOR
ARG TBB_VERSION
ARG VFXPLATFORM_VERSION


#################### ci-centos7-gl-packages ####################
FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${CLANG_MAJOR_VERSION} as ci-centos7-gl-packages

COPY ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

ENV DOWNLOADS_DIR=/tmp/downloads \
    CCACHE_DIR=/tmp/ccache \
    ASWF_INSTALL_PREFIX=/usr/local


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
ARG CMAKE_VERSION
ARG DTS_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-ninja"
LABEL org.opencontainers.image.title="CMake package built for ASWF docker images"
LABEL org.opencontainers.image.description="CMake binary to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://cmake.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${CMAKE_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.cmake="${CMAKE_VERSION}"

COPY --from=ci-cmake-builder /package/. /


#################### ci-base-builder ####################
FROM ci-cmake-builder as ci-base-builder

ARG PYTHON_VERSION_MAJOR_MINOR
ENV PYTHON_VERSION_MAJOR_MINOR=${PYTHON_VERSION_MAJOR_MINOR}
ARG VFXPLATFORM_VERSION
ENV VFXPLATFORM_VERSION=${VFXPLATFORM_VERSION}

ENV PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${PYTHON_VERSION_MAJOR_MINOR}/site-packages:${PYTHONPATH}


#################### ci-python-builder ####################
FROM ci-base-builder as ci-python-builder

ARG NUMPY_VERSION
ENV NUMPY_VERSION=${NUMPY_VERSION}
ARG PYTHON_VERSION
ENV PYTHON_VERSION=${PYTHON_VERSION}

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
ARG DTS_VERSION
ARG NUMPY_VERSION
ARG PYTHON_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-python"
LABEL org.opencontainers.image.title="Python and numpy packages built for ASWF docker images"
LABEL org.opencontainers.image.description="Python (PSF-2.0 license) and numpy (BSD-3-Clause license) to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://www.python.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${PYTHON_VERSION}"
LABEL org.opencontainers.image.licenses="PSF-2.0 AND BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.python="${PYTHON_VERSION}"
LABEL io.aswf.docker.versions.numpy="${NUMPY_VERSION}"

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
FROM scratch as ci-package-boost

ARG ASWF_ORG
ARG BOOST_VERSION
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-boost"
LABEL org.opencontainers.image.title="Boost package built for ASWF docker images"
LABEL org.opencontainers.image.description="Boost binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://www.boost.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${BOOST_VERSION}"
LABEL org.opencontainers.image.licenses="BSL-1.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.boost="${BOOST_VERSION}"

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
FROM scratch as ci-package-tbb

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG TBB_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-tbb"
LABEL org.opencontainers.image.title="Intel TBB package built for ASWF docker images"
LABEL org.opencontainers.image.description="TBB binaries and headers to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://software.intel.com/en-us/tbb"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${TBB_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.boost="${TBB_VERSION}"

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
FROM scratch as ci-package-cppunit

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG CPPUNIT_VERSION
ARG DTS_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-cppunit"
LABEL org.opencontainers.image.title="CppUnit package built for ASWF docker images"
LABEL org.opencontainers.image.description="CppUnit headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://www.boost.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${CPPUNIT_VERSION}"
LABEL org.opencontainers.image.licenses="LGPL-2.1-only"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.cppunit="${CPPUNIT_VERSION}"

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
FROM scratch as ci-package-log4cplus

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG LOG4CPLUS_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-log4cplus"
LABEL org.opencontainers.image.title="log4cplus package built for ASWF docker images"
LABEL org.opencontainers.image.description="log4cplus headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://sourceforge.net/projects/log4cplus/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${LOG4CPLUS_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-2-Clause AND Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.log4cplus="${LOG4CPLUS_VERSION}"

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
FROM scratch as ci-package-glew

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG GLEW_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-glew"
LABEL org.opencontainers.image.title="glew package built for ASWF docker images"
LABEL org.opencontainers.image.description="glew headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="http://glew.sourceforge.net/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${GLEW_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause AND MIT"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.glew="${GLEW_VERSION}"

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
FROM scratch as ci-package-glfw

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG GLFW_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-glfw"
LABEL org.opencontainers.image.title="glfw package built for ASWF docker images"
LABEL org.opencontainers.image.description="glfw headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://www.glfw.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${GLFW_VERSION}"
LABEL org.opencontainers.image.licenses="Zlib"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.glfw="${GLFW_VERSION}"

COPY --from=ci-glfw-builder /package/. /
