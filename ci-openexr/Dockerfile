ARG ASWF_ORG=aswftesting
ARG CI_COMMON_VERSION=1
ARG VFXPLATFORM_VERSION=2019

FROM ${ASWF_ORG}/ci-package-python:${VFXPLATFORM_VERSION} as ci-package-python
FROM ${ASWF_ORG}/ci-package-boost:${VFXPLATFORM_VERSION} as ci-package-boost

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION} as ci-openexr

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
LABEL org.label-schema.name="$ASWF_ORG/openexr-ci"
LABEL org.label-schema.description="openexr CI Docker Image"
LABEL org.label-schema.url="http://aswf.io/"
LABEL org.label-schema.vcs-url="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="AcademySoftwareFoundation"
LABEL org.label-schema.version=$VFXPLATFORM_VERSION
LABEL org.label-schema.docker.cmd="docker run -v `pwd`:/tmp/project -it $ASWF_ORG/openexr-ci bash"

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages:${PYTHONPATH} \
    VFXPLATFORM_VERSION=$VFXPLATFORM_VERSION \
    ASWF_VERSION=${ASWF_VERSION} \
    ASWF_ORG=${ASWF_ORG}

COPY scripts/$VFXPLATFORM_VERSION/versions_base.sh \
     scripts/$VFXPLATFORM_VERSION/versions_vfx.sh \
     scripts/$VFXPLATFORM_VERSION/patchup.sh \
     scripts/base/*.sh \
     /tmp/

COPY --from=ci-package-python /. /usr/local/
COPY --from=ci-package-boost /. /usr/local/

RUN export DOWNLOADS_DIR=/tmp/downloads && \
    mkdir /tmp/downloads && \
    source /tmp/versions_base.sh && \
    /tmp/install_cmake.sh && \
    /tmp/patchup.sh && \
    rm -rf /tmp/downloads
