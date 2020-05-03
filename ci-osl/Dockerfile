# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG ASWF_ORG=aswftesting
ARG ASWF_PKG_ORG=aswftesting
ARG CI_COMMON_VERSION=1
ARG VFXPLATFORM_VERSION=2019

FROM ${ASWF_PKG_ORG}/ci-package-clang:${CI_COMMON_VERSION} as ci-package-clang

FROM ${ASWF_PKG_ORG}/ci-package-python:${VFXPLATFORM_VERSION} as ci-package-python
FROM ${ASWF_PKG_ORG}/ci-package-boost:${VFXPLATFORM_VERSION} as ci-package-boost
FROM ${ASWF_PKG_ORG}/ci-package-qt:${VFXPLATFORM_VERSION} as ci-package-qt

FROM ${ASWF_PKG_ORG}/ci-package-openexr:${VFXPLATFORM_VERSION} as ci-package-openexr
FROM ${ASWF_PKG_ORG}/ci-package-oiio:${VFXPLATFORM_VERSION} as ci-package-oiio
FROM ${ASWF_PKG_ORG}/ci-package-partio:${VFXPLATFORM_VERSION} as ci-package-partio

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION} as ci-osl

ARG ASWF_ORG
ARG VFXPLATFORM_VERSION
ARG ASWF_VERSION
ARG PYTHON_VERSION=2.7
ARG BUILD_DATE=dev
ARG VCS_REF=dev

LABEL maintainer="aloys.baillet@gmail.com"
LABEL com.vfxplatform.version=$VFXPLATFORM_VERSION
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="$ASWF_ORG/base-osl"
LABEL org.label-schema.description="All VFX Packages CI Docker Image"
LABEL org.label-schema.url="http://aswf.io/"
LABEL org.label-schema.vcs-url="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="AcademySoftwareFoundation"
LABEL org.label-schema.version=$VFXPLATFORM_VERSION
LABEL org.label-schema.docker.cmd="docker run -v `pwd`:/tmp/project -it $ASWF_ORG/base-osl bash"

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages:/usr/local/lib/python \
    VFXPLATFORM_VERSION=$VFXPLATFORM_VERSION \
    ASWF_VERSION=${ASWF_VERSION} \
    ASWF_ORG=${ASWF_ORG}

COPY scripts/$VFXPLATFORM_VERSION/versions_base.sh \
     scripts/$VFXPLATFORM_VERSION/versions_vfx.sh \
     scripts/$VFXPLATFORM_VERSION/patchup.sh \
     scripts/base/install_cmake.sh \
     /tmp/


COPY --from=ci-package-clang /. /usr/local/
COPY --from=ci-package-python /. /usr/local/
COPY --from=ci-package-boost /. /usr/local/
COPY --from=ci-package-qt /. /usr/local/

COPY --from=ci-package-openexr /. /usr/local/
COPY --from=ci-package-oiio /. /usr/local/
COPY --from=ci-package-partio /. /usr/local/


RUN export DOWNLOADS_DIR=/tmp/downloads && \
    mkdir /tmp/downloads && \
    source /tmp/versions_base.sh && \
    /tmp/install_cmake.sh && \
    /tmp/patchup.sh && \
    rm -rf /tmp/downloads
