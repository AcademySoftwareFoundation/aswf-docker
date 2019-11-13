ARG ASWF_ORG=aswftesting
ARG CI_COMMON_VERSION=1
ARG VFXPLATFORM_VERSION=2019

FROM ${ASWF_ORG}/ci-package-clang:${CI_COMMON_VERSION} as ci-package-clang

FROM ${ASWF_ORG}/ci-package-python:${VFXPLATFORM_VERSION} as ci-package-python
FROM ${ASWF_ORG}/ci-package-tbb:${VFXPLATFORM_VERSION} as ci-package-tbb
FROM ${ASWF_ORG}/ci-package-boost:${VFXPLATFORM_VERSION} as ci-package-boost
FROM ${ASWF_ORG}/ci-package-cppunit:${VFXPLATFORM_VERSION} as ci-package-cppunit
FROM ${ASWF_ORG}/ci-package-log4cplus:${VFXPLATFORM_VERSION} as ci-package-log4cplus
FROM ${ASWF_ORG}/ci-package-glew:${VFXPLATFORM_VERSION} as ci-package-glew
FROM ${ASWF_ORG}/ci-package-glfw:${VFXPLATFORM_VERSION} as ci-package-glfw
FROM ${ASWF_ORG}/ci-package-qt:${VFXPLATFORM_VERSION} as ci-package-qt
FROM ${ASWF_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION} as ci-package-pyside

FROM ${ASWF_ORG}/ci-package-openexr:${VFXPLATFORM_VERSION} as ci-package-openexr
FROM ${ASWF_ORG}/ci-package-blosc:${VFXPLATFORM_VERSION} as ci-package-blosc
FROM ${ASWF_ORG}/ci-package-alembic:${VFXPLATFORM_VERSION} as ci-package-alembic
FROM ${ASWF_ORG}/ci-package-oiio:${VFXPLATFORM_VERSION} as ci-package-oiio
FROM ${ASWF_ORG}/ci-package-ocio:${VFXPLATFORM_VERSION} as ci-package-ocio
FROM ${ASWF_ORG}/ci-package-opensubdiv:${VFXPLATFORM_VERSION} as ci-package-opensubdiv
FROM ${ASWF_ORG}/ci-package-ptex:${VFXPLATFORM_VERSION} as ci-package-ptex
FROM ${ASWF_ORG}/ci-package-openvdb:${VFXPLATFORM_VERSION} as ci-package-openvdb
FROM ${ASWF_ORG}/ci-package-usd:${VFXPLATFORM_VERSION} as ci-package-usd

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION} as ci-vfxall

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
LABEL org.label-schema.name="$ASWF_ORG/base-vfxall"
LABEL org.label-schema.description="All VFX Packages CI Docker Image"
LABEL org.label-schema.url="http://aswf.io/"
LABEL org.label-schema.vcs-url="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="AcademySoftwareFoundation"
LABEL org.label-schema.version=$VFXPLATFORM_VERSION
LABEL org.label-schema.docker.cmd="docker run -v `pwd`:/tmp/project -it $ASWF_ORG/base-vfxall bash"

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages:${PYTHONPATH} \
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
COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-glfw /. /usr/local/
COPY --from=ci-package-log4cplus /. /usr/local/
COPY --from=ci-package-qt /. /usr/local/
COPY --from=ci-package-pyside /. /usr/local/

COPY --from=ci-package-openexr /. /usr/local/
COPY --from=ci-package-oiio /. /usr/local/
COPY --from=ci-package-ocio /. /usr/local/
COPY --from=ci-package-ptex /. /usr/local/
COPY --from=ci-package-opensubdiv /. /usr/local/
COPY --from=ci-package-alembic /. /usr/local/
COPY --from=ci-package-blosc /. /usr/local/
COPY --from=ci-package-openvdb /. /usr/local/
COPY --from=ci-package-usd /. /usr/local/


RUN export DOWNLOADS_DIR=/tmp/downloads && \
    mkdir /tmp/downloads && \
    source /tmp/versions_base.sh && \
    /tmp/install_cmake.sh && \
    /tmp/patchup.sh && \
    rm -rf /tmp/downloads

