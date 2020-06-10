# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG ASWF_ORG=aswftesting
ARG ASWF_PKG_ORG=aswftesting
ARG CI_COMMON_VERSION=1
ARG VFXPLATFORM_VERSION=2019

FROM ${ASWF_PKG_ORG}/ci-package-python:${VFXPLATFORM_VERSION} as ci-package-python
FROM ${ASWF_PKG_ORG}/ci-package-tbb:${VFXPLATFORM_VERSION} as ci-package-tbb
FROM ${ASWF_PKG_ORG}/ci-package-boost:${VFXPLATFORM_VERSION} as ci-package-boost
FROM ${ASWF_PKG_ORG}/ci-package-cppunit:${VFXPLATFORM_VERSION} as ci-package-cppunit
FROM ${ASWF_PKG_ORG}/ci-package-log4cplus:${VFXPLATFORM_VERSION} as ci-package-log4cplus
FROM ${ASWF_PKG_ORG}/ci-package-glew:${VFXPLATFORM_VERSION} as ci-package-glew
FROM ${ASWF_PKG_ORG}/ci-package-glfw:${VFXPLATFORM_VERSION} as ci-package-glfw
FROM ${ASWF_PKG_ORG}/ci-package-qt:${VFXPLATFORM_VERSION} as ci-package-qt
FROM ${ASWF_PKG_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION} as ci-package-pyside

FROM ${ASWF_PKG_ORG}/ci-package-openexr:${VFXPLATFORM_VERSION} as ci-package-openexr
FROM ${ASWF_PKG_ORG}/ci-package-blosc:${VFXPLATFORM_VERSION} as ci-package-blosc
FROM ${ASWF_PKG_ORG}/ci-package-alembic:${VFXPLATFORM_VERSION} as ci-package-alembic
FROM ${ASWF_PKG_ORG}/ci-package-oiio:${VFXPLATFORM_VERSION} as ci-package-oiio
FROM ${ASWF_PKG_ORG}/ci-package-ocio:${VFXPLATFORM_VERSION} as ci-package-ocio
FROM ${ASWF_PKG_ORG}/ci-package-opensubdiv:${VFXPLATFORM_VERSION} as ci-package-opensubdiv
FROM ${ASWF_PKG_ORG}/ci-package-ptex:${VFXPLATFORM_VERSION} as ci-package-ptex
FROM ${ASWF_PKG_ORG}/ci-package-openvdb:${VFXPLATFORM_VERSION} as ci-package-openvdb
FROM ${ASWF_PKG_ORG}/ci-package-usd:${VFXPLATFORM_VERSION} as ci-package-usd
FROM ${ASWF_PKG_ORG}/ci-package-partio:${VFXPLATFORM_VERSION} as ci-package-partio
FROM ${ASWF_PKG_ORG}/ci-package-osl:${VFXPLATFORM_VERSION} as ci-package-osl

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION} as ci-vfxall

ARG ASWF_ORG
ARG VFXPLATFORM_VERSION
ARG ASWF_VERSION
ARG PYTHON_VERSION=2.7

LABEL maintainer="aloys.baillet@gmail.com"
LABEL com.vfxplatform.version=$VFXPLATFORM_VERSION
LABEL org.opencontainers.image.name="$ASWF_ORG/base-vfxall"
LABEL org.opencontainers.image.description="All VFX Packages CI Docker Image"
LABEL org.opencontainers.image.url="http://aswf.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.version=$VFXPLATFORM_VERSION

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages:/usr/local/lib64/python${PYTHON_VERSION}/site-packages:/usr/local/lib/python:/usr/local/lib64/python \
    VFXPLATFORM_VERSION=$VFXPLATFORM_VERSION \
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
COPY --from=ci-package-cppunit /. /usr/local/
COPY --from=ci-package-log4cplus /. /usr/local/
COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-glfw /. /usr/local/
COPY --from=ci-package-qt /. /usr/local/
COPY --from=ci-package-pyside /. /usr/local/

COPY --from=ci-package-openexr /. /usr/local/
COPY --from=ci-package-blosc /. /usr/local/
COPY --from=ci-package-alembic /. /usr/local/
COPY --from=ci-package-oiio /. /usr/local/
COPY --from=ci-package-ocio /. /usr/local/
COPY --from=ci-package-opensubdiv /. /usr/local/
COPY --from=ci-package-ptex /. /usr/local/
COPY --from=ci-package-openvdb /. /usr/local/
COPY --from=ci-package-usd /. /usr/local/
COPY --from=ci-package-partio /. /usr/local/
COPY --from=ci-package-osl /. /usr/local/


RUN export DOWNLOADS_DIR=/tmp/downloads && \
    mkdir /tmp/downloads && \
    source /tmp/versions_base.sh && \
    /tmp/install_cmake.sh && \
    /tmp/patchup.sh && \
    rm -rf /tmp/downloads
