# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG CUDA_VERSION=10.2
ARG ASWF_ORG=aswftesting
ARG ASWF_PKG_ORG=aswftesting
ARG CI_COMMON_VERSION=1
ARG DTS_VERSION=6

FROM ${ASWF_PKG_ORG}/ci-package-clang:${CI_COMMON_VERSION} as ci-package-clang
FROM ${ASWF_PKG_ORG}/ci-package-ninja:${CI_COMMON_VERSION} as ci-package-ninja

FROM nvidia/cudagl:${CUDA_VERSION}-devel-centos7 as ci-common

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION

LABEL maintainer="aloys.baillet@gmail.com"

LABEL org.opencontainers.image.name="$ASWF_ORG/base-ci"
LABEL org.opencontainers.image.description="Common CI Docker Image"
LABEL org.opencontainers.image.url="http://aswf.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.version="1.0"

USER root

COPY scripts/${CI_COMMON_VERSION}/versions_common.sh \
     scripts/common/install_yumpackages.sh \
     /tmp/

RUN source /tmp/versions_common.sh && \
    /tmp/install_yumpackages.sh

RUN mkdir /opt/aswf
WORKDIR /opt/aswf

ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:/opt/rh/httpd24/root/usr/lib64:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/lib64:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/lib:${LD_LIBRARY_PATH} \
    PATH=/opt/rh/rh-git218/root/usr/bin:/usr/local/bin:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-${DTS_VERSION}/root/usr/bin/:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin \
    CI_COMMON_VERSION=${CI_COMMON_VERSION} \
    DTS_VERSION=${DTS_VERSION} \
    PERL5LIB=/opt/rh/rh-git218/root/usr/share/perl5/vendor_perl \
    MANPATH=/opt/rh/rh-git218/root/usr/share/man

COPY scripts/common/install_sonar.sh \
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
