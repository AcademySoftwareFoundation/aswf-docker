# "Global" ARGs
ARG CUDA_VERSION=10.1
ARG ASWF_ORG=aswftesting
ARG CI_COMMON_VERSION=1
ARG BUILD_DATE=dev
ARG VCS_REF=dev

# ARGS are not accepted in "COPY --from" directives so these aliases are necessary
FROM ${ASWF_ORG}/ci-package-python:${VFXPLATFORM_VERSION} as ci-package-python
FROM ${ASWF_ORG}/ci-package-tbb:${VFXPLATFORM_VERSION} as ci-package-tbb
FROM ${ASWF_ORG}/ci-package-boost:${VFXPLATFORM_VERSION} as ci-package-boost
FROM ${ASWF_ORG}/ci-package-cppunit:${VFXPLATFORM_VERSION} as ci-package-cppunit
FROM ${ASWF_ORG}/ci-package-log4cplus:${VFXPLATFORM_VERSION} as ci-package-log4cplus
FROM ${ASWF_ORG}/ci-package-glew:${VFXPLATFORM_VERSION} as ci-package-glew
FROM ${ASWF_ORG}/ci-package-glfw:${VFXPLATFORM_VERSION} as ci-package-glfw
FROM ${ASWF_ORG}/ci-package-qt:${VFXPLATFORM_VERSION} as ci-package-qt
FROM ${ASWF_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION} as ci-package-pyside

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION} as ci-baseqt

ARG ASWF_ORG
ARG VFXPLATFORM_VERSION
ARG ASWF_VERSION
ARG BUILD_DATE
ARG VCS_REF
ARG PYTHON_VERSION

LABEL maintainer="aloys.baillet@gmail.com"
LABEL com.vfxplatform.version=$VFXPLATFORM_VERSION

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="$ASWF_ORG/baseqt-ci"
LABEL org.label-schema.description="Base with Qt and PySide CI Docker Image"
LABEL org.label-schema.url="http://aswf.io/"
LABEL org.label-schema.vcs-url="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="AcademySoftwareFoundation"
LABEL org.label-schema.version=$VFXPLATFORM_VERSION
LABEL org.label-schema.docker.cmd="docker run -v `pwd`:/tmp/project -it $ASWF_ORG/baseqt-ci bash"

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages:${PYTHONPATH} \
    VFXPLATFORM_VERSION=$VFXPLATFORM_VERSION \
    ASWF_VERSION=${ASWF_VERSION} \
    ASWF_ORG=${ASWF_ORG}

COPY scripts/$VFXPLATFORM_VERSION/versions_base.sh \
     scripts/$VFXPLATFORM_VERSION/patchup.sh \
     scripts/base/*.sh \
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

RUN export DOWNLOADS_DIR=/tmp/downloads && \
    mkdir /tmp/downloads && \
    source /tmp/versions_base.sh && \
    /tmp/install_cmake.sh && \
    /tmp/patchup.sh && \
    rm -rf /tmp/downloads
