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
ARG QT_VERSION
ARG USD_VERSION

# Required base packages built in previous stages
FROM ${ASWF_ORG}/ci-package-cmake:${VFXPLATFORM_VERSION}-${CMAKE_VERSION} as ci-package-cmake-external
FROM ${ASWF_ORG}/ci-package-cppunit:${VFXPLATFORM_VERSION}-${CPPUNIT_VERSION} as ci-package-cppunit-external
FROM ${ASWF_ORG}/ci-package-python:${VFXPLATFORM_VERSION}-${PYTHON_VERSION} as ci-package-python-external
FROM ${ASWF_ORG}/ci-package-boost:${VFXPLATFORM_VERSION}-${BOOST_VERSION} as ci-package-boost-external
FROM ${ASWF_ORG}/ci-package-tbb:${VFXPLATFORM_VERSION}-${TBB_VERSION} as ci-package-tbb-external
FROM ${ASWF_ORG}/ci-package-qt:${VFXPLATFORM_VERSION}-${QT_VERSION} as ci-package-qt-external
FROM ${ASWF_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION}-${PYSIDE_VERSION} as ci-package-pyside-external

FROM ${ASWF_ORG}/ci-package-openexr:${VFXPLATFORM_VERSION}-${OPENEXR_VERSION} as ci-package-openexr-external
FROM ${ASWF_ORG}/ci-package-blosc:${VFXPLATFORM_VERSION}-${BLOSC_VERSION} as ci-package-blosc-external
FROM ${ASWF_ORG}/ci-package-glew:${VFXPLATFORM_VERSION}-${GLEW_VERSION} as ci-package-glew-external
FROM ${ASWF_ORG}/ci-package-glfw:${VFXPLATFORM_VERSION}-${GLFW_VERSION} as ci-package-glfw-external
FROM ${ASWF_ORG}/ci-package-alembic:${VFXPLATFORM_VERSION}-${ALEMBIC_VERSION} as ci-package-alembic-external
FROM ${ASWF_ORG}/ci-package-openvdb:${VFXPLATFORM_VERSION}-${OPENVDB_VERSION} as ci-package-openvdb-external
FROM ${ASWF_ORG}/ci-package-oiio:${VFXPLATFORM_VERSION}-${OIIO_VERSION} as ci-package-oiio-external
FROM ${ASWF_ORG}/ci-package-ocio:${VFXPLATFORM_VERSION}-${OCIO_VERSION} as ci-package-ocio-external

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


#################### ci-partio-builder ####################
FROM ci-base-builder as ci-partio-builder

ARG PARTIO_VERSION
ENV PARTIO_VERSION=${PARTIO_VERSION}

COPY ../scripts/vfx/build_partio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_partio.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-partio ####################
FROM scratch as ci-package-partio

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG PARTIO_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-partio"
LABEL org.opencontainers.image.title="Partio package built for ASWF docker images"
LABEL org.opencontainers.image.description="Partio headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/wdas/partio"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${PARTIO_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.partio="${PARTIO_VERSION}"

COPY --from=ci-partio-builder /package/. /


#################### ci-osl-builder ####################
FROM ci-partio-builder as ci-osl-builder

ARG OSL_VERSION
ENV OSL_VERSION=${OSL_VERSION}

COPY --from=ci-package-openexr-external /. /usr/local/
COPY --from=ci-package-oiio-external /. /usr/local/

COPY ../scripts/vfx/build_osl.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_osl.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-osl ####################
FROM scratch as ci-package-osl

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG OSL_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-osl"
LABEL org.opencontainers.image.title="OpenShadingLanguage package built for ASWF docker images"
LABEL org.opencontainers.image.description="OpenShadingLanguage headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/imageworks/OpenShadingLanguage"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${OSL_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.osl="${OSL_VERSION}"

COPY --from=ci-osl-builder /package/. /


#################### ci-ptex-builder ####################
FROM ci-base-builder as ci-ptex-builder

ARG PTEX_VERSION
ENV PTEX_VERSION=${PTEX_VERSION}

COPY ../scripts/vfx/build_ptex.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_ptex.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-ptex ####################
FROM scratch as ci-package-ptex

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG PTEX_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-ptex"
LABEL org.opencontainers.image.title="Ptex package built for ASWF docker images"
LABEL org.opencontainers.image.description="Ptex headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/wdas/ptex"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${PTEX_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.ptex="${PTEX_VERSION}"

COPY --from=ci-ptex-builder /package/. /


#################### ci-opensubdiv-builder ####################
FROM ci-ptex-builder as ci-opensubdiv-builder

ARG OPENSUBDIV_VERSION
ENV OPENSUBDIV_VERSION=${OPENSUBDIV_VERSION}

COPY ../scripts/vfx/build_opensubdiv.sh \
     /tmp/

COPY --from=ci-package-glew-external /. /usr/local/
COPY --from=ci-package-tbb-external /. /usr/local/
COPY --from=ci-package-glfw-external /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_opensubdiv.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-opensubdiv ####################
FROM scratch as ci-package-opensubdiv

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG OPENSUBDIV_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-opensubdiv"
LABEL org.opencontainers.image.title="OpenSubdiv package built for ASWF docker images"
LABEL org.opencontainers.image.description="OpenSubdiv headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/PixarAnimationStudios/OpenSubdiv"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${OPENSUBDIV_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.opensubdiv="${OPENSUBDIV_VERSION}"

COPY --from=ci-opensubdiv-builder /package/. /


#################### ci-openvdb-builder ####################
FROM ci-base-builder as ci-openvdb-builder

ARG OPENVDB_VERSION
ENV OPENVDB_VERSION=${OPENVDB_VERSION}

COPY ../scripts/vfx/build_openvdb.sh \
     /tmp/

COPY --from=ci-package-openexr-external /. /usr/local/
COPY --from=ci-package-glew-external /. /usr/local/
COPY --from=ci-package-tbb-external /. /usr/local/
COPY --from=ci-package-cppunit-external /. /usr/local/
COPY --from=ci-package-glfw-external /. /usr/local/
COPY --from=ci-package-blosc-external /. /usr/local/

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


#################### ci-usd-builder ####################
FROM ci-opensubdiv-builder as ci-usd-builder

ARG USD_VERSION
ENV USD_VERSION=${USD_VERSION}

COPY --from=ci-package-glew-external /. /usr/local/
COPY --from=ci-package-alembic-external /. /usr/local/
COPY --from=ci-package-openvdb-external /. /usr/local/
COPY --from=ci-package-oiio-external /. /usr/local/
COPY --from=ci-package-ocio-external /. /usr/local/
COPY --from=ci-package-qt-external /. /usr/local/
COPY --from=ci-package-pyside-external /. /usr/local/

COPY ../scripts/vfx/build_usd.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_usd.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-usd ####################
FROM scratch as ci-package-usd

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG USD_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-usd"
LABEL org.opencontainers.image.title="USD package built for ASWF docker images"
LABEL org.opencontainers.image.description="USD (Universal Scene Description) headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/PixarAnimationStudios/USD"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${USD_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.usd="${USD_VERSION}"

COPY --from=ci-usd-builder /package/. /


#################### ci-otio-builder ####################
FROM ci-base-builder as ci-otio-builder

ARG OTIO_VERSION
ENV OTIO_VERSION=${OTIO_VERSION}

COPY --from=ci-package-qt-external /. /usr/local/
COPY --from=ci-package-pyside-external /. /usr/local/

COPY ../scripts/vfx/build_otio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_otio.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-otio ####################
FROM scratch as ci-package-otio

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG DTS_VERSION
ARG OTIO_VERSION
ARG VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-otio"
LABEL org.opencontainers.image.title="OpenTimelineIO package built for ASWF docker images"
LABEL org.opencontainers.image.description="OpenTimelineIO headers and binaries to be installed in ASWF docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/PixarAnimationStudios/OpenTimelineIO"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${OTIO_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${DTS_VERSION}"
LABEL io.aswf.docker.versions.otio="${OTIO_VERSION}"

COPY --from=ci-otio-builder /package/. /

