# syntax = docker/dockerfile:experimental
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# "Global" ARGs
ARG ASWF_ORG
ARG CCACHE_VERSION
ARG CI_COMMON_VERSION
ARG CLANG_VERSION
ARG CUDA_VERSION
ARG DTS_VERSION
ARG NINJA_VERSION

#################### ci-centos7-gl-packages ####################
FROM nvidia/cudagl:${CUDA_VERSION}-devel-centos7 as ci-centos7-gl-packages

ARG CI_COMMON_VERSION
ENV CI_COMMON_VERSION=${CI_COMMON_VERSION}
ARG CUDA_VERSION
ENV CUDA_VERSION=${CUDA_VERSION}
ARG DTS_VERSION
ENV DTS_VERSION=${DTS_VERSION}

COPY ../scripts/common/install_yumpackages.sh \
     /tmp/

RUN --mount=type=cache,sharing=private,target=/var/cache/yum \
    /tmp/install_yumpackages.sh

COPY ../scripts/common/install_dev_ccache.sh \
     ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     ../scripts/common/install_dev_cmake.sh \
     /tmp/

ENV DOWNLOADS_DIR=/tmp/downloads \
    CCACHE_DIR=/tmp/ccache \
    ASWF_INSTALL_PREFIX=/usr/local \
    LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/lib64:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/lib:${LD_LIBRARY_PATH} \
    PATH=/opt/aswfbuilder/bin:/usr/local/bin:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/bin/:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin

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
ARG CLANG_VERSION
ARG DTS_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-clang"
LABEL org.opencontainers.image.title="Clang package built for ASWF docker images"
LABEL org.opencontainers.image.description="Clang (llvm) build artifacts to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://llvm.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
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
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${NINJA_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.ninja="${NINJA_VERSION}"

COPY --from=ci-ninja-builder /package/. /


