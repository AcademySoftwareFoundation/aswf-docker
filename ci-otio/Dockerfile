# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG ASWF_ORG=aswftesting
ARG ASWF_PKG_ORG=aswftesting
ARG CI_COMMON_VERSION=1
ARG VFXPLATFORM_VERSION=2019
ARG CLANG_MAJOR_VERSION=7

FROM ${ASWF_PKG_ORG}/ci-package-python:${VFXPLATFORM_VERSION} as ci-package-python
FROM ${ASWF_PKG_ORG}/ci-package-qt:${VFXPLATFORM_VERSION} as ci-package-qt
FROM ${ASWF_PKG_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION} as ci-package-pyside
FROM ${ASWF_PKG_ORG}/ci-package-cmake:${VFXPLATFORM_VERSION} as ci-package-cmake

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${CLANG_MAJOR_VERSION} as ci-otio

ARG ASWF_ORG
ARG VFXPLATFORM_VERSION
ARG ASWF_VERSION
ARG PYTHON_VERSION=2.7

LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL com.vfxplatform.version=$VFXPLATFORM_VERSION
LABEL org.opencontainers.image.name="$ASWF_ORG/ci-otio"
LABEL org.opencontainers.image.description="OpenTimelineIO CI Docker Image"
LABEL org.opencontainers.image.url="http://aswf.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.version=$VFXPLATFORM_VERSION

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION_MAJOR_MINOR}/site-packages:/usr/local/lib/python \
    VFXPLATFORM_VERSION=$VFXPLATFORM_VERSION \
    ASWF_VERSION=${ASWF_VERSION} \
    ASWF_ORG=${ASWF_ORG}

COPY --from=ci-package-python /. /usr/local/
COPY --from=ci-package-qt /. /usr/local/
COPY --from=ci-package-pyside /. /usr/local/
COPY --from=ci-package-cmake /. /usr/local/
