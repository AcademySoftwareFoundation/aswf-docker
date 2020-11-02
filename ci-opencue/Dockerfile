# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG ASWF_ORG
ARG ASWF_PKG_ORG
ARG CI_COMMON_VERSION
ARG CLANG_MAJOR_VERSION
ARG CMAKE_VERSION
ARG NUMPY_VERSION
ARG PYTHON_VERSION
ARG VFXPLATFORM_VERSION

FROM ${ASWF_PKG_ORG}/ci-package-python:${VFXPLATFORM_VERSION}-${PYTHON_VERSION} as ci-package-python
FROM ${ASWF_PKG_ORG}/ci-package-cmake:${VFXPLATFORM_VERSION}-${CMAKE_VERSION} as ci-package-cmake

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${CLANG_MAJOR_VERSION} as ci-opencue

ARG ASWF_ORG
ARG ASWF_VERSION
ARG CMAKE_VERSION
ARG NUMPY_VERSION
ARG PYTHON_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/base-opencue"
LABEL org.opencontainers.image.title="OpenCue CI Docker Image"
LABEL org.opencontainers.image.description="Contains: python-${PYTHON_VERSION}, tbb-${TBB_VERSION}, boost-${BOOST_VERSION} and other OpenColorIO upstream dependencies"
LABEL org.opencontainers.image.url="http://aswf.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/ci-opencue/Dockerfile"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.version="${ASWF_VERSION}"

LABEL com.vfxplatform.version="${VFXPLATFORM_VERSION}"

LABEL io.aswf.docker.versions.cmake="${CMAKE_VERSION}"
LABEL io.aswf.docker.versions.numpy="${NUMPY_VERSION}"
LABEL io.aswf.docker.versions.python="${PYTHON_VERSION}"

ENV ASWF_ORG=${ASWF_ORG}
ENV ASWF_VERSION=${ASWF_VERSION}
ENV CMAKE_VERSION=${CMAKE_VERSION}
ENV NUMPY_VERSION=${NUMPY_VERSION}
ENV PYTHON_VERSION=${PYTHON_VERSION}
ENV VFXPLATFORM_VERSION=${VFXPLATFORM_VERSION}

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION_MAJOR_MINOR}/site-packages:${PYTHONPATH}

COPY --from=ci-package-python /. /usr/local/
COPY --from=ci-package-cmake /. /usr/local/

RUN yum -y install \
    java-1.8.0-openjdk.x86_64 \
    java-1.8.0-openjdk-devel.x86_64
