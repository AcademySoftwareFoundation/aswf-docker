# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG ALEMBIC_VERSION
ARG ASWF_ORG
ARG ASWF_PKG_ORG
ARG BLOSC_VERSION
ARG BOOST_VERSION
ARG CI_COMMON_VERSION
ARG CLANG_MAJOR_VERSION
ARG CMAKE_VERSION
ARG CPPUNIT_VERSION
ARG GLEW_VERSION
ARG GLFW_VERSION
ARG HDF5_VERSION
ARG LOG4CPLUS_VERSION
ARG NUMPY_VERSION
ARG OCIO_VERSION
ARG OIIO_VERSION
ARG OPENEXR_VERSION
ARG OPENSUBDIV_VERSION
ARG OPENVDB_VERSION
ARG PTEX_VERSION
ARG PYSIDE_VERSION
ARG PYTHON_VERSION
ARG PYTHON_VERSION_MAJOR_MINOR
ARG QT_VERSION
ARG TBB_VERSION
ARG VFXPLATFORM_VERSION

FROM ${ASWF_PKG_ORG}/ci-package-python:${VFXPLATFORM_VERSION}-${PYTHON_VERSION} as ci-package-python
FROM ${ASWF_PKG_ORG}/ci-package-tbb:${VFXPLATFORM_VERSION}-${TBB_VERSION} as ci-package-tbb
FROM ${ASWF_PKG_ORG}/ci-package-boost:${VFXPLATFORM_VERSION}-${BOOST_VERSION} as ci-package-boost
FROM ${ASWF_PKG_ORG}/ci-package-cppunit:${VFXPLATFORM_VERSION}-${CPPUNIT_VERSION} as ci-package-cppunit
FROM ${ASWF_PKG_ORG}/ci-package-log4cplus:${VFXPLATFORM_VERSION}-${LOG4CPLUS_VERSION} as ci-package-log4cplus
FROM ${ASWF_PKG_ORG}/ci-package-glew:${VFXPLATFORM_VERSION}-${GLEW_VERSION} as ci-package-glew
FROM ${ASWF_PKG_ORG}/ci-package-glfw:${VFXPLATFORM_VERSION}-${GLFW_VERSION} as ci-package-glfw
FROM ${ASWF_PKG_ORG}/ci-package-qt:${VFXPLATFORM_VERSION}-${QT_VERSION} as ci-package-qt
FROM ${ASWF_PKG_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION}-${PYSIDE_VERSION} as ci-package-pyside
FROM ${ASWF_PKG_ORG}/ci-package-cmake:${VFXPLATFORM_VERSION}-${CMAKE_VERSION} as ci-package-cmake
FROM ${ASWF_PKG_ORG}/ci-package-openexr:${VFXPLATFORM_VERSION}-${OPENEXR_VERSION} as ci-package-openexr
FROM ${ASWF_PKG_ORG}/ci-package-blosc:${VFXPLATFORM_VERSION}-${BLOSC_VERSION} as ci-package-blosc
FROM ${ASWF_PKG_ORG}/ci-package-alembic:${VFXPLATFORM_VERSION}-${ALEMBIC_VERSION} as ci-package-alembic
FROM ${ASWF_PKG_ORG}/ci-package-oiio:${VFXPLATFORM_VERSION}-${OIIO_VERSION} as ci-package-oiio
FROM ${ASWF_PKG_ORG}/ci-package-ocio:${VFXPLATFORM_VERSION}-${OCIO_VERSION} as ci-package-ocio
FROM ${ASWF_PKG_ORG}/ci-package-opensubdiv:${VFXPLATFORM_VERSION}-${OPENSUBDIV_VERSION} as ci-package-opensubdiv
FROM ${ASWF_PKG_ORG}/ci-package-ptex:${VFXPLATFORM_VERSION}-${PTEX_VERSION} as ci-package-ptex
FROM ${ASWF_PKG_ORG}/ci-package-openvdb:${VFXPLATFORM_VERSION}-${OPENVDB_VERSION} as ci-package-openvdb

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${CLANG_MAJOR_VERSION} as ci-usd

ARG ALEMBIC_VERSION
ARG ASWF_ORG
ARG BLOSC_VERSION
ARG BOOST_VERSION
ARG CI_COMMON_VERSION
ARG CLANG_MAJOR_VERSION
ARG CMAKE_VERSION
ARG CPPUNIT_VERSION
ARG GLEW_VERSION
ARG GLFW_VERSION
ARG HDF5_VERSION
ARG LOG4CPLUS_VERSION
ARG NUMPY_VERSION
ARG OCIO_VERSION
ARG OIIO_VERSION
ARG OPENEXR_VERSION
ARG OPENSUBDIV_VERSION
ARG OPENVDB_VERSION
ARG PTEX_VERSION
ARG PYSIDE_VERSION
ARG PYTHON_VERSION
ARG PYTHON_VERSION_MAJOR_MINOR
ARG QT_VERSION
ARG TBB_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-usd"
LABEL org.opencontainers.image.title="USD CI Docker Image"
LABEL org.opencontainers.image.description="Contains: python-${PYTHON_VERSION}, tbb-${TBB_VERSION}, boost-${BOOST_VERSION} and other USD upstream dependencies"
LABEL org.opencontainers.image.url="http://aswf.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/ci-usd/Dockerfile"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.version="${ASWF_VERSION}"

LABEL com.vfxplatform.version="${VFXPLATFORM_VERSION}"

LABEL io.aswf.docker.versions.alembic="${ALEMBIC_VERSION}"
LABEL io.aswf.docker.versions.blosc="${BLOSC_VERSION}"
LABEL io.aswf.docker.versions.boost="${BOOST_VERSION}"
LABEL io.aswf.docker.versions.cmake="${CMAKE_VERSION}"
LABEL io.aswf.docker.versions.cppunit="${CPPUNIT_VERSION}"
LABEL io.aswf.docker.versions.glew="${GLEW_VERSION}"
LABEL io.aswf.docker.versions.glfw="${GLFW_VERSION}"
LABEL io.aswf.docker.versions.hdf5="${HDF5_VERSION}"
LABEL io.aswf.docker.versions.log4cplus="${LOG4CPLUS_VERSION}"
LABEL io.aswf.docker.versions.numpy="${NUMPY_VERSION}"
LABEL io.aswf.docker.versions.ocio="${OCIO_VERSION}"
LABEL io.aswf.docker.versions.oiio="${OIIO_VERSION}"
LABEL io.aswf.docker.versions.openexr="${OPENEXR_VERSION}"
LABEL io.aswf.docker.versions.opensubdiv="${OPENSUBDIV_VERSION}"
LABEL io.aswf.docker.versions.openvdb="${OPENVDB_VERSION}"
LABEL io.aswf.docker.versions.ptex="${PTEX_VERSION}"
LABEL io.aswf.docker.versions.pyside="${PYSIDE_VERSION}"
LABEL io.aswf.docker.versions.python="${PYTHON_VERSION}"
LABEL io.aswf.docker.versions.qt="${QT_VERSION}"
LABEL io.aswf.docker.versions.tbb="${TBB_VERSION}"

ENV ALEMBIC_VERSION=${ALEMBIC_VERSION}
ENV ASWF_ORG=${ASWF_ORG}
ENV BLOSC_VERSION=${BLOSC_VERSION}
ENV BOOST_VERSION=${BOOST_VERSION}
ENV CI_COMMON_VERSION=${CI_COMMON_VERSION}
ENV CLANG_MAJOR_VERSION=${CLANG_MAJOR_VERSION}
ENV CMAKE_VERSION=${CMAKE_VERSION}
ENV CPPUNIT_VERSION=${CPPUNIT_VERSION}
ENV GLEW_VERSION=${GLEW_VERSION}
ENV GLFW_VERSION=${GLFW_VERSION}
ENV HDF5_VERSION=${HDF5_VERSION}
ENV LOG4CPLUS_VERSION=${LOG4CPLUS_VERSION}
ENV NUMPY_VERSION=${NUMPY_VERSION}
ENV OCIO_VERSION=${OCIO_VERSION}
ENV OIIO_VERSION=${OIIO_VERSION}
ENV OPENEXR_VERSION=${OPENEXR_VERSION}
ENV OPENSUBDIV_VERSION=${OPENSUBDIV_VERSION}
ENV OPENVDB_VERSION=${OPENVDB_VERSION}
ENV PTEX_VERSION=${PTEX_VERSION}
ENV PYSIDE_VERSION=${PYSIDE_VERSION}
ENV PYTHON_VERSION=${PYTHON_VERSION}
ENV PYTHON_VERSION_MAJOR_MINOR=${PYTHON_VERSION_MAJOR_MINOR}
ENV QT_VERSION=${QT_VERSION}
ENV TBB_VERSION=${TBB_VERSION}
ENV VFXPLATFORM_VERSION=${VFXPLATFORM_VERSION}

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION_MAJOR_MINOR}/site-packages:${PYTHONPATH}

COPY --from=ci-package-python /. /usr/local/
COPY --from=ci-package-tbb /. /usr/local/
COPY --from=ci-package-boost /. /usr/local/
COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-glfw /. /usr/local/
COPY --from=ci-package-log4cplus /. /usr/local/
COPY --from=ci-package-qt /. /usr/local/
COPY --from=ci-package-pyside /. /usr/local/
COPY --from=ci-package-cmake /. /usr/local/
COPY --from=ci-package-openexr /. /usr/local/
COPY --from=ci-package-oiio /. /usr/local/
COPY --from=ci-package-ocio /. /usr/local/
COPY --from=ci-package-ptex /. /usr/local/
COPY --from=ci-package-opensubdiv /. /usr/local/
COPY --from=ci-package-alembic /. /usr/local/
COPY --from=ci-package-blosc /. /usr/local/
COPY --from=ci-package-openvdb /. /usr/local/

RUN sudo pip install jinja2 PyOpenGL
