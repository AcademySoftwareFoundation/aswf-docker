ARG ASWF_ORG=aswfstaging
ARG VFXPLATFORM_VERSION=2019
FROM $ASWF_ORG/ci-base:$VFXPLATFORM_VERSION

ARG BUILD_DATE
ARG VCS_REF

LABEL maintainer="aloys.baillet@gmail.com"
LABEL com.vfxplatform.version=$VFXPLATFORM_VERSION
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="$ASWF_ORG/base-ocio"
LABEL org.label-schema.description="Base CI Docker Image"
LABEL org.label-schema.url="http://aswf.io/"
LABEL org.label-schema.vcs-url="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="AcademySoftwareFoundation"
LABEL org.label-schema.version=$VFXPLATFORM_VERSION
LABEL org.label-schema.docker.cmd="docker run -v `pwd`:/tmp/project -it $ASWF_ORG/base-ocio bash"

RUN echo VFXPLATFORM_VERSION=$VFXPLATFORM_VERSION
COPY scripts/$VFXPLATFORM_VERSION/versions_vfx.sh \
     scripts/vfx/*.sh \
     /tmp/

RUN source /tmp/versions_vfx.sh && \
    /tmp/install_openexr.sh && \
    /tmp/install_oiio.sh
