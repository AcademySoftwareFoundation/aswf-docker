# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG ASWF_ORG=aswftesting
ARG ASWF_PKG_ORG=aswftesting
ARG CI_COMMON_VERSION=1
ARG VFXPLATFORM_VERSION=2019

FROM ${ASWF_PKG_ORG}/ci-package-python:${VFXPLATFORM_VERSION} as ci-package-python
FROM ${ASWF_PKG_ORG}/ci-package-tbb:${VFXPLATFORM_VERSION} as ci-package-tbb
FROM ${ASWF_PKG_ORG}/ci-package-boost:${VFXPLATFORM_VERSION} as ci-package-boost
FROM ${ASWF_PKG_ORG}/ci-package-glew:${VFXPLATFORM_VERSION} as ci-package-glew
FROM ${ASWF_PKG_ORG}/ci-package-glfw:${VFXPLATFORM_VERSION} as ci-package-glfw

FROM ${ASWF_PKG_ORG}/ci-package-openexr:${VFXPLATFORM_VERSION} as ci-package-openexr
FROM ${ASWF_PKG_ORG}/ci-package-ocio:${VFXPLATFORM_VERSION} as ci-package-ocio
FROM ${ASWF_PKG_ORG}/ci-package-oiio:${VFXPLATFORM_VERSION} as ci-package-oiio

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION} as ci-ocio

ARG ASWF_ORG
ARG VFXPLATFORM_VERSION
ARG ASWF_VERSION
ARG PYTHON_VERSION=2.7

LABEL maintainer="aloys.baillet@gmail.com"
LABEL com.vfxplatform.version=$VFXPLATFORM_VERSION
LABEL org.opencontainers.image.name="$ASWF_ORG/base-ocio"
LABEL org.opencontainers.image.description="OpenColorIO CI Docker Image"
LABEL org.opencontainers.image.url="http://aswf.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.version=$VFXPLATFORM_VERSION

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages:/usr/local/lib64/python${PYTHON_VERSION}/site-packages:${PYTHONPATH} \
    VFXPLATFORM_VERSION=$VFXPLATFORM_VERSION \
    LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64 \
    ASWF_VERSION=${ASWF_VERSION} \
    ASWF_ORG=${ASWF_ORG}

COPY scripts/$VFXPLATFORM_VERSION/versions_base.sh \
     scripts/$VFXPLATFORM_VERSION/versions_vfx.sh \
     scripts/$VFXPLATFORM_VERSION/patchup.sh \
     scripts/base/install_cmake.sh \
     /tmp/

COPY --from=ci-package-python /. /usr/local/
COPY --from=ci-package-tbb /. /usr/local/
COPY --from=ci-package-boost /. /usr/local/
COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-openexr /. /usr/local/
COPY --from=ci-package-ocio /. /usr/local
COPY --from=ci-package-oiio /. /usr/local/

RUN export DOWNLOADS_DIR=/tmp/downloads && \
    mkdir /tmp/downloads && \
    source /tmp/versions_base.sh && \
    /tmp/install_cmake.sh && \
    /tmp/patchup.sh && \
    rm -rf /tmp/downloads
