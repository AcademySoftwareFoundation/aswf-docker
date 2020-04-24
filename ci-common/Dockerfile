# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG CUDA_VERSION=10.1
ARG ASWF_ORG=aswftesting
ARG ASWF_PKG_ORG=aswftesting
ARG CI_COMMON_VERSION=1

FROM ${ASWF_PKG_ORG}/ci-package-clang:${CI_COMMON_VERSION} as ci-package-clang
FROM ${ASWF_PKG_ORG}/ci-package-ninja:${CI_COMMON_VERSION} as ci-package-ninja

FROM nvidia/cudagl:${CUDA_VERSION}-devel-centos7 as ci-common

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG BUILD_DATE=dev
ARG VCS_REF=dev

LABEL maintainer="aloys.baillet@gmail.com"

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="$ASWF_ORG/base-ci"
LABEL org.label-schema.description="Common CI Docker Image"
LABEL org.label-schema.url="http://aswf.io/"
LABEL org.label-schema.vcs-url="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="AcademySoftwareFoundation"
LABEL org.label-schema.version="1.0"
LABEL org.label-schema.docker.cmd="docker run -v `pwd`:/tmp/project -it $ASWF_ORG/common-ci bash"

USER root

COPY scripts/common/install_yumpackages.sh \
     /tmp/

RUN /tmp/install_yumpackages.sh

RUN mkdir /opt/aswf
WORKDIR /opt/aswf

ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:/opt/rh/devtoolset-6/root/usr/lib64:/opt/rh/devtoolset-6/root/usr/lib:${LD_LIBRARY_PATH} \
    PATH=/usr/local/bin:/opt/rh/devtoolset-6/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-6/root/usr/bin/:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin \
    CI_COMMON_VERSION=${CI_COMMON_VERSION}

COPY scripts/${CI_COMMON_VERSION}/versions_common.sh \
     scripts/common/install_sonar.sh \
     scripts/common/install_ccache.sh \
     /tmp/

COPY --from=ci-package-clang /. /usr/local/
COPY --from=ci-package-ninja /. /usr/local/

ENV CI_COMMON_VERSION=${CI_COMMON_VERSION} \
    ASWF_ORG=${ASWF_ORG}

RUN export DOWNLOADS_DIR=/tmp/downloads && \
    mkdir /tmp/downloads && \
    source /tmp/versions_common.sh && \
    /tmp/install_sonar.sh && \
    /tmp/install_ccache.sh && \
    rm -rf /tmp/downloads

COPY scripts/common/setup_aswfuser.sh /tmp
RUN /tmp/setup_aswfuser.sh
