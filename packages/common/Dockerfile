# syntax = docker/dockerfile:1.4
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# "Global" ARGs
ARG ASWF_ORG
ARG ASWF_CCACHE_VERSION
ARG ASWF_CONAN_VERSION
ARG ASWF_CONAN_REMOTE
ARG ASWF_CONAN_PYTHON_VERSION
ARG CI_COMMON_VERSION
ARG ASWF_CLANG_VERSION
ARG ASWF_CUDA_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
ARG ASWF_NINJA_VERSION
ARG ASWF_BASEOS_DISTRO
ARG ASWF_BASEOS_IMAGE


#################### ci-baseos-gl-os ####################
FROM ${ASWF_BASEOS_IMAGE}:${ASWF_CUDA_VERSION}-devel-${ASWF_BASEOS_DISTRO} AS ci-baseos-gl-os

ARG CI_COMMON_VERSION
ENV CI_COMMON_VERSION=${CI_COMMON_VERSION}
ARG ASWF_CUDA_VERSION
ENV ASWF_CUDA_VERSION=${ASWF_CUDA_VERSION}
ARG ASWF_DTS_VERSION
ENV ASWF_DTS_VERSION=${ASWF_DTS_VERSION}
ARG ASWF_DTS_PREFIX
ENV ASWF_DTS_PREFIX=${ASWF_DTS_PREFIX}

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
    LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:/opt/rh/${ASWF_DTS_PREFIX}-${ASWF_DTS_VERSION}/root/usr/lib64:/opt/rh/${ASWF_DTS_PREFIX}-${ASWF_DTS_VERSION}/root/usr/lib:${LD_LIBRARY_PATH} \
    PATH=/opt/aswfbuilder/bin:/usr/local/bin:/opt/rh/${ASWF_DTS_PREFIX}-${ASWF_DTS_VERSION}/root/usr/bin:/opt/app-root/src/bin:/opt/rh/${ASWF_DTS_PREFIX}-${ASWF_DTS_VERSION}/root/usr/bin/:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin

RUN --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/install_dev_cmake.sh && \
    /tmp/install_dev_ccache.sh


#################### ci-baseos-gl-conan ####################
FROM ci-baseos-gl-os AS ci-baseos-gl-conan

ARG ASWF_CONAN_VERSION
ARG ASWF_CONAN_PYTHON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX

ENV ASWF_CONAN_ROOT=/opt/conan

COPY ../scripts/common/install_conan.sh /tmp/

RUN --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/install_conan.sh


#################### ci-clang-builder ####################
FROM ci-baseos-gl-os AS ci-clang-builder
ARG ASWF_CLANG_VERSION
ENV ASWF_CLANG_VERSION=${ASWF_CLANG_VERSION}

COPY ../scripts/common/build_clang.sh \
     ../scripts/base/build_python.sh \
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
ARG ASWF_CLANG_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-clang"
LABEL org.opencontainers.image.title="Clang package built for ASWF Docker images"
LABEL org.opencontainers.image.description="Clang (llvm) build artifacts to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://llvm.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_CLANG_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.clang="${ASWF_CLANG_VERSION}"

COPY --from=ci-clang-builder /package/. /


#################### ci-ninja-builder ####################
FROM ci-baseos-gl-os AS ci-ninja-builder

ARG ASWF_NINJA_VERSION
ENV ASWF_NINJA_VERSION=${ASWF_NINJA_VERSION}

COPY ../scripts/common/build_ninja.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_ninja.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-ninja ####################
FROM scratch AS ci-package-ninja

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
ARG ASWF_NINJA_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-ninja"
LABEL org.opencontainers.image.title="Ninja package built for ASWF Docker images"
LABEL org.opencontainers.image.description="Ninja binary to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://ninja-build.org/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_NINJA_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.ninja="${ASWF_NINJA_VERSION}"

COPY --from=ci-ninja-builder /package/. /

#################### ci-conan-package-builder ####################
FROM ci-baseos-gl-conan AS ci-conan-package-builder

ARG ASWF_ORG
ARG ASWF_CCACHE_VERSION
ARG ASWF_CONAN_CHANNEL
ARG ASWF_CONAN_VERSION
ARG ASWF_CONAN_REMOTE
ARG ASWF_CONAN_PYTHON_VERSION
ARG ASWF_CONAN_KEEP_SOURCE
ARG ASWF_CONAN_KEEP_BUILD
ARG ASWF_CONAN_BUILD_MISSING
ARG ASWF_CONAN_PUSH
ARG CI_COMMON_VERSION
ARG CONAN_USER_HOME
ARG ASWF_PKG_NAME
ARG ASWF_PKG_ORG
ARG ASWF_PKG_VERSION
ARG ASWF_PYTHON_VERSION
ENV ASWF_PYTHON_VERSION=${ASWF_PYTHON_VERSION}
ARG ASWF_NUMPY_VERSION
ENV ASWF_NUMPY_VERSION=${ASWF_NUMPY_VERSION}

ENV ASWF_CONAN_ROOT=/opt/conan \
    CCACHE_DIR=/tmp/ccache \
    CONAN_NON_INTERACTIVE=1

# With "conan create --profile" we no longer need to set a default profile
RUN --mount=type=cache,target=${CONAN_USER_HOME}/d \
    --mount=type=cache,target=${CCACHE_DIR} \
    --mount=type=bind,rw,target=${CONAN_USER_HOME}/.conan,source=packages/conan/settings \
    --mount=type=bind,rw,target=${CONAN_USER_HOME}/recipes,source=packages/conan/recipes \
    conan create ${CONAN_USER_HOME}/recipes/${ASWF_PKG_NAME} ${ASWF_PKG_NAME}/${ASWF_PKG_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL} \
      ${ASWF_CONAN_KEEP_SOURCE} ${ASWF_CONAN_KEEP_BUILD} ${ASWF_CONAN_BUILD_MISSING} --profile ${ASWF_CONAN_CHANNEL}

RUN --mount=type=cache,target=${CONAN_USER_HOME}/d \
    --mount=type=cache,target=${CCACHE_DIR} \
    --mount=type=bind,rw,target=${CONAN_USER_HOME}/.conan,source=packages/conan/settings \
    --mount=type=bind,rw,target=${CONAN_USER_HOME}/recipes,source=packages/conan/recipes \
    conan alias ${ASWF_PKG_NAME}/latest@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL} ${ASWF_PKG_NAME}/${ASWF_PKG_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}

# Upload build to repository if called for
RUN --mount=type=cache,target=${CONAN_USER_HOME}/d \
    --mount=type=cache,target=${CCACHE_DIR} \
    --mount=type=bind,rw,target=${CONAN_USER_HOME}/.conan,source=packages/conan/settings \
    --mount=type=bind,rw,target=${CONAN_USER_HOME}/recipes,source=packages/conan/recipes \
    if [ -n "${ASWF_CONAN_PUSH}" ] ; then \
      conan upload --all -r ${ASWF_PKG_ORG} ${ASWF_PKG_NAME}/${ASWF_PKG_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL} ;\
    else \
      echo "conan upload of package ${ASWF_PKG_NAME} skipped" ; \
    fi

# Upload build alias to latest if called for
RUN --mount=type=cache,target=${CONAN_USER_HOME}/d \
    --mount=type=cache,target=${CCACHE_DIR} \
    --mount=type=bind,rw,target=${CONAN_USER_HOME}/.conan,source=packages/conan/settings \
    --mount=type=bind,rw,target=${CONAN_USER_HOME}/recipes,source=packages/conan/recipes \
    if [ -n "${ASWF_CONAN_PUSH}" ] ; then \
      conan upload --all -r ${ASWF_PKG_ORG} ${ASWF_PKG_NAME}/latest@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL} ;\
    else \
      echo "conan upload of package ${ASWF_PKG_NAME} alias skipped" ;\
    fi
