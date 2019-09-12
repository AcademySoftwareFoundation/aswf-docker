ARG CI_COMMON_VERSION=1.0
ARG ASWF_ORG=aswfstaging
FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}

ARG VFXPLATFORM_VERSION=2019
ARG BUILD_DATE=dev
ARG VCS_REF=dev
ARG PYTHON_VERSION=2.7

LABEL maintainer="aloys.baillet@gmail.com"
LABEL com.vfxplatform.version=$VFXPLATFORM_VERSION
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="$ASWF_ORG/base-opencue"
LABEL org.label-schema.description="OpenCue CI Docker Image"
LABEL org.label-schema.url="http://aswf.io/"
LABEL org.label-schema.vcs-url="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="AcademySoftwareFoundation"
LABEL org.label-schema.version=$VFXPLATFORM_VERSION
LABEL org.label-schema.docker.cmd="docker run -v `pwd`:/tmp/project -it $ASWF_ORG/base-opencue bash"

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages:${PYTHONPATH} \
    VFXPLATFORM_VERSION=$VFXPLATFORM_VERSION

COPY scripts/$VFXPLATFORM_VERSION/versions_base.sh \
     scripts/$VFXPLATFORM_VERSION/patchup.sh \
     scripts/base/*.sh \
     /tmp/

RUN source /tmp/versions_base.sh && \
    /tmp/install_python.sh && \
    /tmp/patchup.sh

COPY scripts/$VFXPLATFORM_VERSION/versions_vfx.sh \
     scripts/vfx/*.sh \
     /tmp/

RUN source /tmp/versions_vfx.sh

RUN yum -y install \
    fontconfig \
    freetype \
    java-1.8.0-openjdk.x86_64 \
    java-1.8.0-openjdk-devel.x86_64 \
    libXi \
    libXrender \
    Xvfb

# This is needed for Xvfb to function properly.
RUN dbus-uuidgen > /etc/machine-id

RUN pip install coverage
