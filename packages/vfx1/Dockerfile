# syntax = docker/dockerfile:experimental
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# "Global" ARGs
ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG CLANG_MAJOR_VERSION
ARG VFXPLATFORM_VERSION

ARG BOOST_VERSION
ARG CMAKE_VERSION
ARG CPPUNIT_VERSION
ARG GLEW_VERSION
ARG GLFW_VERSION
ARG PYTHON_VERSION
ARG PYTHON_VERSION_MAJOR_MINOR
ARG TBB_VERSION

ARG ALEMBIC_VERSION
ARG BLOSC_VERSION
ARG HDF5_VERSION
ARG OCIO_CONFIGS_VERSION
ARG OCIO_VERSION
ARG OIIO_VERSION
ARG OPENEXR_VERSION

# Required base packages built in previous stages
FROM ${ASWF_ORG}/ci-package-cmake:${VFXPLATFORM_VERSION}-${CMAKE_VERSION} as ci-package-cmake-external
FROM ${ASWF_ORG}/ci-package-python:${VFXPLATFORM_VERSION}-${PYTHON_VERSION} as ci-package-python-external
FROM ${ASWF_ORG}/ci-package-boost:${VFXPLATFORM_VERSION}-${BOOST_VERSION} as ci-package-boost-external
FROM ${ASWF_ORG}/ci-package-glew:${VFXPLATFORM_VERSION}-${GLEW_VERSION} as ci-package-glew-external
FROM ${ASWF_ORG}/ci-package-tbb:${VFXPLATFORM_VERSION}-${TBB_VERSION} as ci-package-tbb-external
FROM ${ASWF_ORG}/ci-package-cppunit:${VFXPLATFORM_VERSION}-${CPPUNIT_VERSION} as ci-package-cppunit-external
FROM ${ASWF_ORG}/ci-package-glfw:${VFXPLATFORM_VERSION}-${GLFW_VERSION} as ci-package-glfw-external

#################### ci-centos7-gl-packages ####################
FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${CLANG_MAJOR_VERSION} as ci-base-builder

COPY --from=ci-package-cmake-external /. /usr/local/
COPY --from=ci-package-python-external /. /usr/local/
COPY --from=ci-package-boost-external /. /usr/local/

COPY ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

ENV DOWNLOADS_DIR=/tmp/downloads \
    CCACHE_DIR=/tmp/ccache \
    ASWF_INSTALL_PREFIX=/usr/local \
    PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${PYTHON_VERSION_MAJOR_MINOR}/site-packages:${PYTHONPATH}

#################### ci-openexr-builder ####################
FROM ci-base-builder as ci-openexr-builder

ARG OPENEXR_VERSION
ENV OPENEXR_VERSION=${OPENEXR_VERSION}

COPY ../scripts/vfx/build_openexr.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_openexr.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-openexr ####################
FROM scratch as ci-package-openexr

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG OPENEXR_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-openexr"
LABEL org.opencontainers.image.title="OpenEXR package built for ASWF docker images"
LABEL org.opencontainers.image.description="OpenEXR headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/AcademySoftwareFoundation/openexr"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${OPENEXR_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.pyside="${OPENEXR_VERSION}"

COPY --from=ci-openexr-builder /package/. /



#################### ci-alembic-builder ####################
FROM ci-openexr-builder as ci-alembic-builder

ARG ALEMBIC_VERSION
ENV ALEMBIC_VERSION=${ALEMBIC_VERSION}
ARG HDF5_VERSION
ENV HDF5_VERSION=${HDF5_VERSION}

COPY ../scripts/vfx/build_alembic.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_alembic.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-alembic ####################
FROM scratch as ci-package-alembic

ARG ALEMBIC_VERSION
ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG HDF5_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-alembic"
LABEL org.opencontainers.image.title="Alembic package built for ASWF docker images"
LABEL org.opencontainers.image.description="Alembic headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/alembic/alembic"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ALEMBIC_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.alembic="${ALEMBIC_VERSION}"
LABEL io.aswf.docker.versions.hdf5="${HDF5_VERSION}"

COPY --from=ci-alembic-builder /package/. /


#################### ci-blosc-builder ####################
FROM ci-base-builder as ci-blosc-builder

ARG BLOSC_VERSION
ENV BLOSC_VERSION=${BLOSC_VERSION}

COPY ../scripts/vfx/build_blosc.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_blosc.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-blosc ####################
FROM scratch as ci-package-blosc

ARG ASWF_ORG
ARG BLOSC_VERSION
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-blosc"
LABEL org.opencontainers.image.title="Blosc package built for ASWF docker images"
LABEL org.opencontainers.image.description="Blosc headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/Blosc/c-blosc"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${BLOSC_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.blosc="${BLOSC_VERSION}"

COPY --from=ci-blosc-builder /package/. /


#################### ci-oiio-builder ####################
FROM ci-openexr-builder as ci-oiio-builder

ARG OIIO_VERSION
ENV OIIO_VERSION=${OIIO_VERSION}

COPY ../scripts/vfx/build_oiio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_oiio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-oiio ####################
FROM scratch as ci-package-oiio

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG OIIO_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-oiio"
LABEL org.opencontainers.image.title="OpenImageIO package built for ASWF docker images"
LABEL org.opencontainers.image.description="OpenImageIO headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/OpenImageIO/oiio"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${OIIO_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.oiio="${OIIO_VERSION}"

COPY --from=ci-oiio-builder /package/. /


#################### ci-ocio-builder ####################
FROM ci-oiio-builder as ci-ocio-builder

ARG OCIO_VERSION
ENV OCIO_VERSION=${OCIO_VERSION}
ARG OCIO_CONFIGS_VERSION
ENV OCIO_CONFIGS_VERSION=${OCIO_CONFIGS_VERSION}

COPY ../scripts/vfx/build_ocio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_ocio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-package-ocio ####################
FROM scratch as ci-package-ocio

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG OCIO_CONFIGS_VERSION
ARG OCIO_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-ocio"
LABEL org.opencontainers.image.title="OpenColorIO package built for ASWF docker images"
LABEL org.opencontainers.image.description="OpenColorIO headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/AcademySoftwareFoundation/OpenColorIO"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${OCIO_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.ocio="${OCIO_VERSION}"
LABEL io.aswf.docker.versions.ocioconfigs="${OCIO_CONFIGS_VERSION}"

COPY --from=ci-ocio-builder /package/. /


#################### ci-osl-builder ####################
FROM ci-oiio-builder as ci-osl-builder

ARG OSL_VERSION
ENV OSL_VERSION=${OSL_VERSION}

COPY --from=ci-package-clang-external /. /usr/local/
COPY --from=ci-package-qt-external /. /usr/local/
COPY --from=ci-package-partio /. /usr/local/

COPY ../scripts/vfx/build_osl.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    /tmp/before_build.sh && \
    /tmp/build_osl.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-openvdb-builder ####################
FROM ci-openexr-builder as ci-openvdb-builder

ARG OPENVDB_VERSION
ENV OPENVDB_VERSION=${OPENVDB_VERSION}

COPY ../scripts/vfx/build_openvdb.sh \
     /tmp/

COPY --from=ci-package-glew-external /. /usr/local/
COPY --from=ci-package-tbb-external /. /usr/local/
COPY --from=ci-package-cppunit-external /. /usr/local/
COPY --from=ci-package-glfw-external /. /usr/local/

COPY --from=ci-package-blosc /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_openvdb.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-openvdb ####################
FROM scratch as ci-package-openvdb

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG OPENVDB_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-openvdb"
LABEL org.opencontainers.image.title="OpenVDB package built for ASWF docker images"
LABEL org.opencontainers.image.description="OpenVDB headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/AcademySoftwareFoundation/openvdb"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${OPENVDB_VERSION}"
LABEL org.opencontainers.image.licenses="MPL-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.openvdb="${OPENVDB_VERSION}"

COPY --from=ci-openvdb-builder /package/. /


