# syntax=docker/dockerfile:1.10
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
FROM ${ASWF_BASEOS_IMAGE}:${ASWF_CUDA_VERSION}-runtime-${ASWF_BASEOS_DISTRO} AS ci-baseos-gl-os

ARG CI_COMMON_VERSION
ENV CI_COMMON_VERSION=${CI_COMMON_VERSION}
ARG ASWF_CUDA_VERSION
ENV ASWF_CUDA_VERSION=${ASWF_CUDA_VERSION}
ARG ASWF_GLVND_VERSION
ENV ASWF_GLVND_VERSION=${ASWF_GLVND_VERSION}
ARG ASWF_DTS_VERSION
ENV ASWF_DTS_VERSION=${ASWF_DTS_VERSION}
ARG ASWF_DTS_PREFIX
ENV ASWF_DTS_PREFIX=${ASWF_DTS_PREFIX}
ARG ASWF_CMAKE_VERSION
ENV ASWF_CMAKE_VERSION=${ASWF_CMAKE_VERSION}
ARG ASWF_YQ_VERSION
ENV ASWF_YQ_VERSION=${ASWF_YQ_VERSION}

COPY ../scripts/common/install_cudadevel.sh /tmp/

RUN --mount=type=cache,sharing=private,target=/var/cache/yum \
    /tmp/install_cudadevel.sh

COPY ../scripts/common/install_yumpackages.sh /tmp/

RUN --mount=type=cache,sharing=private,target=/var/cache/yum \
    /tmp/install_yumpackages.sh

COPY scripts/common/install_opengl.sh /tmp/

ARG ASWF_BASEOS_DISTRO
ENV ASWF_BASEOS_DISTRO=${ASWF_BASEOS_DISTRO}
RUN /tmp/install_opengl.sh

ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics
ENV PKG_CONFIG_PATH \
    /usr/local/lib/pkgconfig

COPY scripts/common/install_optix.sh /tmp/

RUN /tmp/install_optix.sh

COPY scripts/common/install_pippackages.sh /tmp/

RUN --mount=type=cache,sharing=private,target=/root/.cache/pip \
    /tmp/install_pippackages.sh

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

COPY scripts/common/install_yq.sh /tmp/

RUN /tmp/install_yq.sh

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
ARG ASWF_DTS_VERSION
ENV ASWF_DTS_VERSION=${ASWF_DTS_VERSION}
ARG ASWF_DTS_PREFIX
ENV ASWF_DTS_PREFIX=${ASWF_DTS_PREFIX}
ARG CI_COMMON_VERSION
ARG ASWF_CONAN_HOME
ARG ASWF_PKG_NAME
ARG ASWF_PKG_ORG
ARG ASWF_PKG_VERSION
ARG ASWF_NINJA_VERSION
ENV ASWF_NINJA_VERSION=${ASWF_NINJA_VERSION}
ARG ASWF_CLANG_VERSION
ENV ASWF_CLANG_VERSION=${ASWF_CLANG_VERSION}
ARG ASWF_PYSIDE_CLANG_VERSION
ENV ASWF_PYSIDE_CLANG_VERSION=${ASWF_CLANG_VERSION}
ARG ASWF_CPYTHON_VERSION
ENV ASWF_CPYTHON_VERSION=${ASWF_CPYTHON_VERSION}
ARG ASWF_PYTHON_MAJOR_MINOR_VERSION
ENV ASWF_PYTHON_MAJOR_MINOR_VERSION=${ASWF_PYTHON_MAJOR_MINOR_VERSION}
ARG ASWF_NUMPY_VERSION
ENV ASWF_NUMPY_VERSION=${ASWF_NUMPY_VERSION}
ARG ASWF_CMAKE_VERSION
ENV ASWF_CMAKE_VERSION=${ASWF_CMAKE_VERSION}
ARG ASWF_PYBIND11_VERSION
ENV ASWF_PYBIND11_VERSION=${ASWF_PYBIND11_VERSION}
ARG ASWF_BOOST_VERSION
ENV ASWF_BOOST_VERSION=${ASWF_BOOST_VERSION}
ARG ASWF_QT_VERSION
ENV ASWF_QT_VERSION=${ASWF_QT_VERSION}
ARG ASWF_BLOSC_VERSION
ENV ASWF_BLOSC_VERSION=${ASWF_BLOSC_VERSION}
ARG ASWF_GLEW_VERSION
ENV ASWF_GLEW_VERSION=${ASWF_GLEW_VERSION}
ARG ASWF_GLFW_VERSION
ENV ASWF_GLFW_VERSION=${ASWF_GLFW_VERSION}
ARG ASWF_ONETBB_VERSION
ENV ASWF_ONETBB_VERSION=${ASWF_ONETBB_VERSION}
ARG ASWF_MD4C_VERSION
ENV ASWF_MD4C_VERSION=${ASWF_MD4C_VERSION}
ARG ASWF_FREETYPE_VERSION
ENV ASWF_FREETYPE_VERSION=${ASWF_FREETYPE_VERSION}

# These are a bit of a circular dependency, but ci-conan-package-builder
# is also used to build vfx1/vfx2 packages

ARG ASWF_IMATH_VERSION
ENV ASWF_IMATH_VERSION=${ASWF_IMATH_VERSION}
ARG ASWF_OPENEXR_VERSION
ENV ASWF_OPENEXR_VERSION=${ASWF_OPENEXR_VERSION}
ARG ASWF_OPENSUBDIV_VERSION
ENV ASWF_OPENSUBDIV_VERSION=${ASWF_OPENSUBDIV_VERSION}
ARG ASWF_PARTIO_VERSION
ENV ASWF_PARTIO_VERSION=${ASWF_PARTIO_VERSION}
ARG ASWF_PTEX_VERSION
ENV ASWF_PTEX_VERSION=${ASWF_PTEX_VERSION}
ARG ASWF_OIIO_VERSION
ENV ASWF_OIIO_VERSION=${ASWF_OIIO_VERSION}

ARG ASWF_EXPAT_VERSION
ENV ASWF_EXPAT_VERSION=${ASWF_EXPAT_VERSION}

ENV ASWF_CONAN_ROOT=/opt/conan \
    CCACHE_DIR=/tmp/ccache \
    CONAN_NON_INTERACTIVE=1

# Clang needs to know where DTS gcc lives, with newer Conan generators
# the generate() method doesn't seem to have access to build/host env vars
# set in profile or on the conan command line.
ENV GCC_INSTALL_PREFIX=/opt/rh/${ASWF_DTS_PREFIX}-${ASWF_DTS_VERSION}/root/usr

# With "conan create --profile" we no longer need to set a default profile
ENV CONAN_HOME=${ASWF_CONAN_HOME}/.conan2

# In case we have a Conan Center Index style config.yaml to support different
# recipes per package.
ENV ASWF_PKG_DIR=${ASWF_CONAN_HOME}/recipes/${ASWF_PKG_NAME}
ENV ASWF_PKG_YML=${ASWF_PKG_DIR}/config.yml

RUN --mount=type=cache,target=${ASWF_CONAN_HOME}/d \
    --mount=type=cache,target=${CCACHE_DIR} \
    --mount=type=bind,rw,target=${ASWF_CONAN_HOME}/.conan2,source=packages/conan/settings \
    --mount=type=bind,rw,target=${ASWF_CONAN_HOME}/recipes,source=packages/conan/recipes \
    conan create \
      ${ASWF_CONAN_KEEP_SOURCE} \
      ${ASWF_CONAN_KEEP_BUILD} \
      ${ASWF_CONAN_BUILD_MISSING} \
      --profile:all ${ASWF_CONAN_HOME}/.conan2/profiles_${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL} \
      --name ${ASWF_PKG_NAME} \
      --version ${ASWF_PKG_VERSION} \
      --user ${ASWF_PKG_ORG} \
      --channel ${ASWF_CONAN_CHANNEL} \
      ${ASWF_PKG_DIR}/$(if [ -f ${ASWF_PKG_YML} ] ; then yq '.versions["'"${ASWF_PKG_VERSION}"'"].folder' ${ASWF_PKG_YML} ; fi)

# Upload build to repository if called for
RUN --mount=type=cache,target=${ASWF_CONAN_HOME}/d \
    --mount=type=cache,target=${CCACHE_DIR} \
    --mount=type=bind,rw,target=${ASWF_CONAN_HOME}/.conan2,source=packages/conan/settings \
    --mount=type=bind,rw,target=${ASWF_CONAN_HOME}/recipes,source=packages/conan/recipes \
    --mount=type=secret,id=conan_login_username,env=CONAN_LOGIN_USERNAME \
    --mount=type=secret,id=conan_password,env=CONAN_PASSWORD \
    if [ -n "${ASWF_CONAN_PUSH}" ] ; then \
      conan upload --remote ${ASWF_PKG_ORG} ${ASWF_PKG_NAME}/${ASWF_PKG_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL} ;\
    else \
      echo "conan upload of package ${ASWF_PKG_NAME} skipped" ; \
    fi
