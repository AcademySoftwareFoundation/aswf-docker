# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG ALEMBIC_VERSION
ARG ASWF_ORG
ARG BLOSC_VERSION
ARG BOOST_VERSION
ARG CI_COMMON_VERSION
ARG CLANG_VERSION
ARG CMAKE_VERSION
ARG CPPUNIT_VERSION
ARG CUDA_VERSION
ARG DTS_VERSION
ARG GLEW_VERSION
ARG GLFW_VERSION
ARG HDF5_VERSION
ARG LOG4CPLUS_VERSION
ARG NUMPY_VERSION
ARG OCIO_CONFIGS_VERSION
ARG OCIO_VERSION
ARG OIIO_VERSION
ARG OPENEXR_VERSION
ARG OPENSUBDIV_VERSION
ARG OPENVDB_VERSION
ARG OSL_VERSION
ARG OTIO_VERSION
ARG PARTIO_VERSION
ARG PTEX_VERSION
ARG PYSIDE_VERSION
ARG PYTHON_VERSION
ARG PYTHON_VERSION_MAJOR_MINOR
ARG QT_VERSION
ARG TBB_VERSION
ARG USD_VERSION
ARG VFXPLATFORM_VERSION

FROM ${ASWF_PKG_ORG}/ci-package-python:${VFXPLATFORM_VERSION} as ci-package-python
FROM ${ASWF_PKG_ORG}/ci-package-tbb:${VFXPLATFORM_VERSION} as ci-package-tbb
FROM ${ASWF_PKG_ORG}/ci-package-boost:${VFXPLATFORM_VERSION} as ci-package-boost
FROM ${ASWF_PKG_ORG}/ci-package-cppunit:${VFXPLATFORM_VERSION} as ci-package-cppunit
FROM ${ASWF_PKG_ORG}/ci-package-log4cplus:${VFXPLATFORM_VERSION} as ci-package-log4cplus
FROM ${ASWF_PKG_ORG}/ci-package-glew:${VFXPLATFORM_VERSION} as ci-package-glew
FROM ${ASWF_PKG_ORG}/ci-package-glfw:${VFXPLATFORM_VERSION} as ci-package-glfw
FROM ${ASWF_PKG_ORG}/ci-package-qt:${VFXPLATFORM_VERSION} as ci-package-qt
FROM ${ASWF_PKG_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION} as ci-package-pyside
FROM ${ASWF_PKG_ORG}/ci-package-cmake:${VFXPLATFORM_VERSION} as ci-package-cmake
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
FROM ${ASWF_PKG_ORG}/ci-package-otio:${VFXPLATFORM_VERSION} as ci-package-otio

FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${CLANG_MAJOR_VERSION} as ci-vfxall

ARG ALEMBIC_VERSION
ARG ASWF_ORG
ARG BLOSC_VERSION
ARG BOOST_VERSION
ARG CI_COMMON_VERSION
ARG CLANG_VERSION
ARG CMAKE_VERSION
ARG CPPUNIT_VERSION
ARG CUDA_VERSION
ARG DTS_VERSION
ARG GLEW_VERSION
ARG GLFW_VERSION
ARG HDF5_VERSION
ARG LOG4CPLUS_VERSION
ARG NUMPY_VERSION
ARG OCIO_CONFIGS_VERSION
ARG OCIO_VERSION
ARG OIIO_VERSION
ARG OPENEXR_VERSION
ARG OPENSUBDIV_VERSION
ARG OPENVDB_VERSION
ARG OSL_VERSION
ARG OTIO_VERSION
ARG PARTIO_VERSION
ARG PTEX_VERSION
ARG PYSIDE_VERSION
ARG PYTHON_VERSION
ARG PYTHON_VERSION_MAJOR_MINOR
ARG QT_VERSION
ARG TBB_VERSION
ARG USD_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-vfxall"
LABEL org.opencontainers.image.title="VFX All Packages CI Docker Image"
LABEL org.opencontainers.image.description="Contains: all supported vfx and base packages"
LABEL org.opencontainers.image.url="http://aswf.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/ci-vfxall/Dockerfile"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.version="${ASWF_VERSION}"

LABEL com.vfxplatform.version="${VFXPLATFORM_VERSION}"

LABEL io.aswf.docker.versions.numpy="${NUMPY_VERSION}"
LABEL io.aswf.docker.versions.hdf5="${HDF5_VERSION}"
LABEL io.aswf.docker.versions.python=${PYTHON_VERSION}
LABEL io.aswf.docker.versions.tbb=${TBB_VERSION}
LABEL io.aswf.docker.versions.boost=${BOOST_VERSION}
LABEL io.aswf.docker.versions.cppunit=${CPPUNIT_VERSION}
LABEL io.aswf.docker.versions.log4cplus=${LOG4CPLUS_VERSION}
LABEL io.aswf.docker.versions.glew=${GLEW_VERSION}
LABEL io.aswf.docker.versions.glfw=${GLFW_VERSION}
LABEL io.aswf.docker.versions.qt=${QT_VERSION}
LABEL io.aswf.docker.versions.pyside=${PYSIDE_VERSION}
LABEL io.aswf.docker.versions.cmake=${CMAKE_VERSION}
LABEL io.aswf.docker.versions.openexr=${OPENEXR_VERSION}
LABEL io.aswf.docker.versions.blosc=${BLOSC_VERSION}
LABEL io.aswf.docker.versions.alembic=${ALEMBIC_VERSION}
LABEL io.aswf.docker.versions.oiio=${OIIO_VERSION}
LABEL io.aswf.docker.versions.ocio=${OCIO_VERSION}
LABEL io.aswf.docker.versions.opensubdiv=${OPENSUBDIV_VERSION}
LABEL io.aswf.docker.versions.ptex=${PTEX_VERSION}
LABEL io.aswf.docker.versions.openvdb=${OPENVDB_VERSION}
LABEL io.aswf.docker.versions.usd=${USD_VERSION}
LABEL io.aswf.docker.versions.partio=${PARTIO_VERSION}
LABEL io.aswf.docker.versions.osl=${OSL_VERSION}
LABEL io.aswf.docker.versions.otio=${OTIO_VERSION}

ENV ALEMBIC_VERSION=${ALEMBIC_VERSION}
ENV ASWF_ORG=${ASWF_ORG}
ENV BLOSC_VERSION=${BLOSC_VERSION}
ENV BOOST_VERSION=${BOOST_VERSION}
ENV CI_COMMON_VERSION=${CI_COMMON_VERSION}
ENV CLANG_VERSION=${CLANG_VERSION}
ENV CMAKE_VERSION=${CMAKE_VERSION}
ENV CPPUNIT_VERSION=${CPPUNIT_VERSION}
ENV CUDA_VERSION=${CUDA_VERSION}
ENV DTS_VERSION=${DTS_VERSION}
ENV GLEW_VERSION=${GLEW_VERSION}
ENV GLFW_VERSION=${GLFW_VERSION}
ENV HDF5_VERSION=${HDF5_VERSION}
ENV LOG4CPLUS_VERSION=${LOG4CPLUS_VERSION}
ENV NUMPY_VERSION=${NUMPY_VERSION}
ENV OCIO_CONFIGS_VERSION=${OCIO_CONFIGS_VERSION}
ENV OCIO_VERSION=${OCIO_VERSION}
ENV OIIO_VERSION=${OIIO_VERSION}
ENV OPENEXR_VERSION=${OPENEXR_VERSION}
ENV OPENSUBDIV_VERSION=${OPENSUBDIV_VERSION}
ENV OPENVDB_VERSION=${OPENVDB_VERSION}
ENV OSL_VERSION=${OSL_VERSION}
ENV OTIO_VERSION=${OTIO_VERSION}
ENV PARTIO_VERSION=${PARTIO_VERSION}
ENV PTEX_VERSION=${PTEX_VERSION}
ENV PYSIDE_VERSION=${PYSIDE_VERSION}
ENV PYTHON_VERSION=${PYTHON_VERSION}
ENV PYTHON_VERSION_MAJOR_MINOR=${PYTHON_VERSION_MAJOR_MINOR}
ENV QT_VERSION=${QT_VERSION}
ENV TBB_VERSION=${TBB_VERSION}
ENV USD_VERSION=${USD_VERSION}
ENV VFXPLATFORM_VERSION=${VFXPLATFORM_VERSION}

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION_MAJOR_MINOR}/site-packages:/usr/local/lib/python

COPY --from=ci-package-python /. /usr/local/
COPY --from=ci-package-tbb /. /usr/local/
COPY --from=ci-package-boost /. /usr/local/
COPY --from=ci-package-cppunit /. /usr/local/
COPY --from=ci-package-log4cplus /. /usr/local/
COPY --from=ci-package-glew /. /usr/local/
COPY --from=ci-package-glfw /. /usr/local/
COPY --from=ci-package-qt /. /usr/local/
COPY --from=ci-package-pyside /. /usr/local/
COPY --from=ci-package-cmake /. /usr/local/
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
COPY --from=ci-package-otio /. /usr/local/
