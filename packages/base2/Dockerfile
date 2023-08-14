# syntax = docker/dockerfile:1.4
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# "Global" ARGs
ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_CMAKE_VERSION
ARG ASWF_CLANG_MAJOR_VERSION
ARG ASWF_PYTHON_VERSION
ARG ASWF_PYTHON_MAJOR_MINOR_VERSION
ARG ASWF_QT_VERSION
ARG ASWF_VFXPLATFORM_VERSION

#################### ci-baseos-gl-packages ####################
FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${ASWF_CLANG_MAJOR_VERSION} AS ci-baseos-gl-packages

ARG ASWF_CMAKE_VERSION
ARG ASWF_PKG_ORG
ARG ASWF_CONAN_CHANNEL
ARG ASWF_VFXPLATFORM_VERSION

ENV ASWF_CMAKE_VERSION=${ASWF_CMAKE_VERSION}
ENV ASWF_VFXPLATFORM_VERSION=${ASWF_VFXPLATFORM_VERSION}

COPY scripts/common/install_conanpackages.sh /tmp

# Use conan to install some packages
COPY <<EOF /usr/local/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
cmake/${ASWF_CMAKE_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

RUN --mount=type=bind,rw,target=/opt/conan_home/d,source=packages/conan/data \
    --mount=type=bind,rw,target=/opt/conan_home/.conan,source=packages/conan/settings \
    /tmp/install_conanpackages.sh /usr/local vfx${ASWF_VFXPLATFORM_VERSION}

COPY ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

ENV DOWNLOADS_DIR=/tmp/downloads \
    CCACHE_DIR=/tmp/ccache \
    ASWF_INSTALL_PREFIX=/usr/local


#################### ci-qt-builder ####################
FROM ci-baseos-gl-packages AS ci-qt-builder

ARG ASWF_QT_VERSION
ENV ASWF_QT_VERSION=${ASWF_QT_VERSION}

COPY ../scripts/base/build_qt.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_qt.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-qt ####################
FROM scratch AS ci-package-qt

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
ARG ASWF_QT_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-qt"
LABEL org.opencontainers.image.title="Qt package built for ASWF Docker images"
LABEL org.opencontainers.image.description="Qt headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://www.qt.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_QT_VERSION}"
LABEL org.opencontainers.image.licenses="https://doc.qt.io/qt-5/licenses-used-in-qt.html"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.glfw="${ASWF_QT_VERSION}"

COPY --from=ci-qt-builder /package/. /
