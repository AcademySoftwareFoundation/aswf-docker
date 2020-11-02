# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG ASWF_ORG
ARG ASWF_PKG_ORG
ARG BOOST_VERSION
ARG CI_COMMON_VERSION
ARG CLANG_MAJOR_VERSION
ARG CMAKE_VERSION
ARG CPPUNIT_VERSION
ARG GLEW_VERSION
ARG GLFW_VERSION
ARG LOG4CPLUS_VERSION
ARG NUMPY_VERSION
ARG PYSIDE_VERSION
ARG PYTHON_VERSION
ARG QT_VERSION
ARG TBB_VERSION
ARG VFXPLATFORM_VERSION

FROM ${ASWF_PKG_ORG}/ci-package-python:${VFXPLATFORM_VERSION}-${PYTHON_VERSION} as ci-package-python
FROM ${ASWF_PKG_ORG}/ci-package-tbb:${VFXPLATFORM_VERSION}-${TBB_VERSION} as ci-package-tbb
FROM ${ASWF_PKG_ORG}/ci-package-boost:${VFXPLATFORM_VERSION}-${BOOST_VERSION} as ci-package-boost
FROM ${ASWF_PKG_ORG}/ci-package-cppunit:${VFXPLATFORM_VERSION}-${CPPUNIT_VERSION} as ci-package-cppunit
FROM ${ASWF_PKG_ORG}/ci-package-log4cplus:${VFXPLATFORM_VERSION}=${LOG4CPLUS_VERSION} as ci-package-log4cplus
FROM ${ASWF_PKG_ORG}/ci-package-glew:${VFXPLATFORM_VERSION}-${GLEW_VERSION} as ci-package-glew
FROM ${ASWF_PKG_ORG}/ci-package-glfw:${VFXPLATFORM_VERSION}-${GLFW_VERSION} as ci-package-glfw
FROM ${ASWF_PKG_ORG}/ci-package-cmake:${VFXPLATFORM_VERSION}-${CMAKE_VERSION} as ci-package-cmake
FROM ${ASWF_PKG_ORG}/ci-package-qt:${VFXPLATFORM_VERSION}-${QT_VERSION} as ci-package-qt
FROM ${ASWF_PKG_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION}-${PYSIDE_VERSION} as ci-package-pyside

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${CLANG_MAJOR_VERSION} as ci-baseqt

ARG ASWF_ORG
ARG ASWF_VERSION
ARG BOOST_VERSION
ARG CMAKE_VERSION
ARG CPPUNIT_VERSION
ARG GLEW_VERSION
ARG GLFW_VERSION
ARG LOG4CPLUS_VERSION
ARG NUMPY_VERSION
ARG PYSIDE_VERSION
ARG PYTHON_VERSION
ARG QT_VERSION
ARG TBB_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/baseqt-ci"
LABEL org.opencontainers.image.title="Base with Qt and PySide CI Docker Image"
LABEL org.opencontainers.image.description="Contains: qt-${QT_VERSION}, pyside-${PYSIDE_VERSION} and other base libraries"
LABEL org.opencontainers.image.url="http://aswf.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/ci-baseqt/Dockerfile"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.version="${ASWF_VERSION}"

LABEL com.vfxplatform.version="${VFXPLATFORM_VERSION}"

LABEL io.aswf.docker.versions.boost="${BOOST_VERSION}"
LABEL io.aswf.docker.versions.cmake="${CMAKE_VERSION}"
LABEL io.aswf.docker.versions.cppunit="${CPPUNIT_VERSION}"
LABEL io.aswf.docker.versions.glew="${GLEW_VERSION}"
LABEL io.aswf.docker.versions.glfw="${GLFW_VERSION}"
LABEL io.aswf.docker.versions.log4cplus="${LOG4CPLUS_VERSION}"
LABEL io.aswf.docker.versions.numpy="${NUMPY_VERSION}"
LABEL io.aswf.docker.versions.python="${PYTHON_VERSION}"
LABEL io.aswf.docker.versions.tbb="${TBB_VERSION}"
LABEL io.aswf.docker.versions.qt="${QT_VERSION}"
LABEL io.aswf.docker.versions.pyside="${PYSIDE_VERSION}"

ENV ASWF_ORG=${ASWF_ORG}
ENV BOOST_VERSION=${BOOST_VERSION}
ENV CMAKE_VERSION=${CMAKE_VERSION}
ENV CPPUNIT_VERSION=${CPPUNIT_VERSION}
ENV GLEW_VERSION=${GLEW_VERSION}
ENV GLFW_VERSION=${GLFW_VERSION}
ENV LOG4CPLUS_VERSION=${LOG4CPLUS_VERSION}
ENV NUMPY_VERSION=${NUMPY_VERSION}
ENV PYSIDE_VERSION=${PYSIDE_VERSION}
ENV PYTHON_VERSION=${PYTHON_VERSION}
ENV QT_VERSION=${QT_VERSION}
ENV TBB_VERSION=${TBB_VERSION}

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION_MAJOR_MINOR}/site-packages:${PYTHONPATH}

COPY --from=ci-package-python /. /usr/local/
COPY --from=ci-package-tbb /. /usr/local/
COPY --from=ci-package-boost /. /usr/local/
COPY --from=ci-package-cppunit /. /usr/local/
COPY --from=ci-package-log4cplus /. /usr/local/
COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-glfw /. /usr/local/
COPY --from=ci-package-cmake /. /usr/local/
COPY --from=ci-package-qt /. /usr/local/
COPY --from=ci-package-pyside /. /usr/local/
