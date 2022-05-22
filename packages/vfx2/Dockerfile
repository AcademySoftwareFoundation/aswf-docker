# syntax = docker/dockerfile:1.3-labs
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# "Global" ARGs
ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_CLANG_MAJOR_VERSION
ARG ASWF_VFXPLATFORM_VERSION

ARG ASWF_BOOST_VERSION
ARG ASWF_CMAKE_VERSION
ARG ASWF_CPPUNIT_VERSION
ARG ASWF_GLEW_VERSION
ARG ASWF_GLFW_VERSION
ARG ASWF_PYBIND11_VERSION
ARG ASWF_NUMPY_VERSION
ARG ASWF_PYTHON_VERSION
ARG ASWF_PYTHON_MAJOR_MINOR_VERSION
ARG ASWF_TBB_VERSION

ARG ASWF_ALEMBIC_VERSION
ARG ASWF_BLOSC_VERSION
ARG ASWF_OCIO_VERSION
ARG ASWF_OIIO_VERSION
ARG ASWF_OPENEXR_VERSION
ARG ASWF_IMATH_VERSION
ARG ASWF_OPENSUBDIV_VERSION
ARG ASWF_OPENVDB_VERSION
ARG ASWF_OSL_VERSION
ARG ASWF_OTIO_VERSION
ARG ASWF_PARTIO_VERSION
ARG ASWF_PTEX_VERSION
ARG ASWF_PYSIDE_VERSION
ARG ASWF_QT_VERSION
ARG ASWF_USD_VERSION

# Required base packages built in previous stages
FROM ${ASWF_ORG}/ci-package-cmake:${ASWF_VFXPLATFORM_VERSION}-${ASWF_CMAKE_VERSION} as ci-package-cmake-external
FROM ${ASWF_ORG}/ci-package-cppunit:${ASWF_VFXPLATFORM_VERSION}-${ASWF_CPPUNIT_VERSION} as ci-package-cppunit-external
FROM ${ASWF_ORG}/ci-package-python:${ASWF_VFXPLATFORM_VERSION}-${ASWF_PYTHON_VERSION} as ci-package-python-external
FROM ${ASWF_ORG}/ci-package-boost:${ASWF_VFXPLATFORM_VERSION}-${ASWF_BOOST_VERSION} as ci-package-boost-external
FROM ${ASWF_ORG}/ci-package-tbb:${ASWF_VFXPLATFORM_VERSION}-${ASWF_TBB_VERSION} as ci-package-tbb-external
FROM ${ASWF_ORG}/ci-package-qt:${ASWF_VFXPLATFORM_VERSION}-${ASWF_QT_VERSION} as ci-package-qt-external
FROM ${ASWF_ORG}/ci-package-pybind11:${ASWF_VFXPLATFORM_VERSION}-${ASWF_PYBIND11_VERSION} as ci-package-pybind11-external
FROM ${ASWF_ORG}/ci-package-pyside:${ASWF_VFXPLATFORM_VERSION}-${ASWF_PYSIDE_VERSION} as ci-package-pyside-external

FROM ${ASWF_ORG}/ci-package-imath:${ASWF_VFXPLATFORM_VERSION}-${ASWF_IMATH_VERSION} as ci-package-imath-external
FROM ${ASWF_ORG}/ci-package-openexr:${ASWF_VFXPLATFORM_VERSION}-${ASWF_OPENEXR_VERSION} as ci-package-openexr-external
FROM ${ASWF_ORG}/ci-package-blosc:${ASWF_VFXPLATFORM_VERSION}-${ASWF_BLOSC_VERSION} as ci-package-blosc-external
FROM ${ASWF_ORG}/ci-package-glew:${ASWF_VFXPLATFORM_VERSION}-${ASWF_GLEW_VERSION} as ci-package-glew-external
FROM ${ASWF_ORG}/ci-package-glfw:${ASWF_VFXPLATFORM_VERSION}-${ASWF_GLFW_VERSION} as ci-package-glfw-external
FROM ${ASWF_ORG}/ci-package-alembic:${ASWF_VFXPLATFORM_VERSION}-${ASWF_ALEMBIC_VERSION} as ci-package-alembic-external
FROM ${ASWF_ORG}/ci-package-openvdb:${ASWF_VFXPLATFORM_VERSION}-${ASWF_OPENVDB_VERSION} as ci-package-openvdb-external
FROM ${ASWF_ORG}/ci-package-oiio:${ASWF_VFXPLATFORM_VERSION}-${ASWF_OIIO_VERSION} as ci-package-oiio-external
FROM ${ASWF_ORG}/ci-package-ocio:${ASWF_VFXPLATFORM_VERSION}-${ASWF_OCIO_VERSION} as ci-package-ocio-external


#################### ci-base-builder ####################
FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${ASWF_CLANG_MAJOR_VERSION} as ci-base-builder

ARG ASWF_CMAKE_VERSION
ARG ASWF_PYTHON_VERSION
ARG ASWF_NUMPY_VERSION
ARG ASWF_BOOST_VERSION
ARG ASWF_PKG_ORG
ARG ASWF_CONAN_CHANNEL

ENV ASWF_CMAKE_VERSION=${ASWF_CMAKE_VERSION}
ENV ASWF_PYTHON_VERSION=${ASWF_PYTHON_VERSION}
ENV ASWF_NUMPY_VERSION=${ASWF_NUMPY_VERSION}
ENV ASWF_BOOST_VERSION=${ASWF_BOOST_VERSION}

# Copy local conan packages if any
COPY packages/conan/data/ /opt/conan_home/d/
COPY packages/conan/settings/ /opt/conan_home/.conan/

# Use conan to install MaterialX
COPY <<EOF /usr/local/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
cmake/${ASWF_CMAKE_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
python/${ASWF_PYTHON_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
boost/${ASWF_BOOST_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

RUN <<EOF
cd /usr/local/
cat /usr/local/conanfile.txt
conan install .
# Replace first line of pip to fix the hardcoded shebang line
sed -i "1s/.*/\#\!\/usr\/bin\/env python3/" /usr/local/bin/pip
EOF

COPY ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

ENV DOWNLOADS_DIR=/tmp/downloads \
     CCACHE_DIR=/tmp/ccache \
     ASWF_INSTALL_PREFIX=/usr/local \
     PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${ASWF_PYTHON_MAJOR_MINOR_VERSION}/site-packages:${PYTHONPATH}


#################### ci-partio-builder ####################
FROM ci-base-builder as ci-partio-builder

ARG ASWF_PARTIO_VERSION
ENV ASWF_PARTIO_VERSION=${ASWF_PARTIO_VERSION}

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
ARG ASWF_DTS_VERSION
ARG ASWF_PARTIO_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-partio"
LABEL org.opencontainers.image.title="Partio package built for ASWF Docker images"
LABEL org.opencontainers.image.description="Partio headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/wdas/partio"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_PARTIO_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.partio="${ASWF_PARTIO_VERSION}"

COPY --from=ci-partio-builder /package/. /


#################### ci-osl-builder ####################
FROM ci-partio-builder as ci-osl-builder

ARG ASWF_OSL_VERSION
ENV ASWF_OSL_VERSION=${ASWF_OSL_VERSION}

COPY --from=ci-package-imath-external /. /usr/local/
COPY --from=ci-package-openexr-external /. /usr/local/
COPY --from=ci-package-oiio-external /. /usr/local/
COPY --from=ci-package-pybind11-external /. /usr/local/
COPY --from=ci-package-openvdb-external /. /usr/local/
COPY --from=ci-package-tbb-external /. /usr/local/
COPY --from=ci-package-blosc-external /. /usr/local/

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
ARG ASWF_DTS_VERSION
ARG ASWF_OSL_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-osl"
LABEL org.opencontainers.image.title="OpenShadingLanguage package built for ASWF Docker images"
LABEL org.opencontainers.image.description="OpenShadingLanguage headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/imageworks/OpenShadingLanguage"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_OSL_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.osl="${ASWF_OSL_VERSION}"

COPY --from=ci-osl-builder /package/. /


#################### ci-ptex-builder ####################
FROM ci-base-builder as ci-ptex-builder

ARG ASWF_PTEX_VERSION
ENV ASWF_PTEX_VERSION=${ASWF_PTEX_VERSION}

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
ARG ASWF_DTS_VERSION
ARG ASWF_PTEX_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-ptex"
LABEL org.opencontainers.image.title="Ptex package built for ASWF Docker images"
LABEL org.opencontainers.image.description="Ptex headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/wdas/ptex"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_PTEX_VERSION}"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.ptex="${ASWF_PTEX_VERSION}"

COPY --from=ci-ptex-builder /package/. /


#################### ci-opensubdiv-builder ####################
FROM ci-ptex-builder as ci-opensubdiv-builder

ARG ASWF_OPENSUBDIV_VERSION
ENV ASWF_OPENSUBDIV_VERSION=${ASWF_OPENSUBDIV_VERSION}

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
ARG ASWF_DTS_VERSION
ARG ASWF_OPENSUBDIV_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-opensubdiv"
LABEL org.opencontainers.image.title="OpenSubdiv package built for ASWF Docker images"
LABEL org.opencontainers.image.description="OpenSubdiv headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/PixarAnimationStudios/OpenSubdiv"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_OPENSUBDIV_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.opensubdiv="${ASWF_OPENSUBDIV_VERSION}"

COPY --from=ci-opensubdiv-builder /package/. /


#################### ci-usd-builder ####################
FROM ci-opensubdiv-builder as ci-usd-builder

ARG ASWF_MATERIALX_VERSION
ARG ASWF_PKG_ORG
ARG ASWF_CONAN_CHANNEL
ARG ASWF_USD_VERSION
ARG ASWF_NUMPY_VERSION

ENV ASWF_USD_VERSION=${ASWF_USD_VERSION}
ENV ASWF_NUMPY_VERSION=${ASWF_NUMPY_VERSION}

COPY --from=ci-package-imath-external /. /usr/local/
COPY --from=ci-package-openexr-external /. /usr/local/
COPY --from=ci-package-glew-external /. /usr/local/
COPY --from=ci-package-alembic-external /. /usr/local/
COPY --from=ci-package-openvdb-external /. /usr/local/
COPY --from=ci-package-oiio-external /. /usr/local/
COPY --from=ci-package-ocio-external /. /usr/local/
COPY --from=ci-package-qt-external /. /usr/local/
COPY --from=ci-package-pyside-external /. /usr/local/

COPY ../scripts/vfx/build_usd.sh \
     /tmp/

# Use conan to install MaterialX
COPY <<EOF /usr/local/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
materialx/${ASWF_MATERIALX_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

RUN <<EOF
cd /usr/local/
conan install .
EOF

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
ARG ASWF_DTS_VERSION
ARG ASWF_USD_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-usd"
LABEL org.opencontainers.image.title="USD package built for ASWF Docker images"
LABEL org.opencontainers.image.description="USD (Universal Scene Description) headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/PixarAnimationStudios/USD"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_USD_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.usd="${ASWF_USD_VERSION}"

COPY --from=ci-usd-builder /package/. /


#################### ci-otio-builder ####################
FROM ci-base-builder as ci-otio-builder

ARG ASWF_OTIO_VERSION
ENV ASWF_OTIO_VERSION=${ASWF_OTIO_VERSION}

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
ARG ASWF_DTS_VERSION
ARG ASWF_OTIO_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-otio"
LABEL org.opencontainers.image.title="OpenTimelineIO package built for ASWF Docker images"
LABEL org.opencontainers.image.description="OpenTimelineIO headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/PixarAnimationStudios/OpenTimelineIO"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_OTIO_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.otio="${ASWF_OTIO_VERSION}"

COPY --from=ci-otio-builder /package/. /
