# syntax = docker/dockerfile:1.3-labs
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# "Global" ARGs
ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_CLANG_MAJOR_VERSION
ARG ASWF_CMAKE_VERSION
ARG ASWF_PYTHON_VERSION
ARG ASWF_PYTHON_MAJOR_MINOR_VERSION
ARG ASWF_QT_VERSION
ARG ASWF_VFXPLATFORM_VERSION

# Required base packages built in previous stages
FROM ${ASWF_ORG}/ci-package-cmake:${ASWF_VFXPLATFORM_VERSION}-${ASWF_CMAKE_VERSION} as ci-package-cmake-external
FROM ${ASWF_ORG}/ci-package-qt:${ASWF_VFXPLATFORM_VERSION}-${ASWF_QT_VERSION} as ci-package-qt-external


#################### ci-baseos-gl-packages ####################
FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${ASWF_CLANG_MAJOR_VERSION} as ci-baseos-gl-packages

COPY --from=ci-package-cmake-external /. /usr/local/

COPY ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

ENV DOWNLOADS_DIR=/tmp/downloads \
    CCACHE_DIR=/tmp/ccache \
    ASWF_INSTALL_PREFIX=/usr/local \
    PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${ASWF_PYTHON_MAJOR_MINOR_VERSION}/site-packages:${PYTHONPATH}


#################### ci-pyside-builder ####################
FROM ci-baseos-gl-packages as ci-pyside-builder

ARG ASWF_PYTHON_VERSION
ARG ASWF_PYSIDE_VERSION
ARG ASWF_PKG_ORG
ARG ASWF_CONAN_CHANNEL
ARG ASWF_VFXPLATFORM_VERSION

ENV ASWF_PYTHON_VERSION=${ASWF_PYTHON_VERSION}
ENV ASWF_PYSIDE_VERSION=${ASWF_PYSIDE_VERSION}
ENV ASWF_PKG_ORG=${ASWF_PKG_ORG}
ENV ASWF_CONAN_CHANNEL=${ASWF_CONAN_CHANNEL}
ENV ASWF_VFXPLATFORM_VERSION=${ASWF_VFXPLATFORM_VERSION}

# Copy local conan packages if any
COPY packages/conan/data/ /opt/conan_home/d/
COPY packages/conan/settings/ /opt/conan_home/.conan/

RUN conan config set general.default_profile=vfx${ASWF_VFXPLATFORM_VERSION}

# Use conan to install some packages
COPY <<EOF /usr/local/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
python/${ASWF_PYTHON_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

RUN <<EOF
cd /usr/local/
conan install .
EOF

# Workaround pyside issue with Qt headers within system location https://bugreports.qt.io/browse/PYSIDE-787
COPY --from=ci-package-qt-external /. /tmp/qt5temp

COPY ../scripts/base/build_pyside.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_pyside.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-pyside ####################
FROM scratch as ci-package-pyside

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_PYSIDE_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-pyside"
LABEL org.opencontainers.image.title="PySide package built for ASWF Docker images"
LABEL org.opencontainers.image.description="PySide headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://www.qt.io/qt-for-python"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_PYSIDE_VERSION}"
LABEL org.opencontainers.image.licenses="LGPL-2.1"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.pyside="${ASWF_PYSIDE_VERSION}"

COPY --from=ci-pyside-builder /package/. /
