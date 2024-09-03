# syntax = docker/dockerfile:1.4
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# "Global" ARGs
ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_CLANG_MAJOR_VERSION
ARG ASWF_PYSIDE_CLANG_VERSION
ARG ASWF_VFXPLATFORM_VERSION

ARG ASWF_BOOST_VERSION
ARG ASWF_CMAKE_VERSION
ARG ASWF_CPPUNIT_VERSION
ARG ASWF_EXPAT_VERSION
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

FROM ${ASWF_ORG}/ci-package-openvdb:${ASWF_VFXPLATFORM_VERSION}-${ASWF_OPENVDB_VERSION} AS ci-package-openvdb-external
FROM ${ASWF_ORG}/ci-package-oiio:${ASWF_VFXPLATFORM_VERSION}-${ASWF_OIIO_VERSION} AS ci-package-oiio-external
FROM ${ASWF_ORG}/ci-package-ocio:${ASWF_VFXPLATFORM_VERSION}-${ASWF_OCIO_VERSION} AS ci-package-ocio-external


#################### ci-base-builder ####################
FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${ASWF_CLANG_MAJOR_VERSION} AS ci-base-builder

ARG ASWF_CMAKE_VERSION
ARG ASWF_PYTHON_VERSION
ARG ASWF_PYTHON_MAJOR_MINOR_VERSION
ARG ASWF_NUMPY_VERSION
ARG ASWF_BOOST_VERSION
ARG ASWF_TBB_VERSION
ARG ASWF_PKG_ORG
ARG ASWF_CONAN_CHANNEL
ARG ASWF_VFXPLATFORM_VERSION

ENV ASWF_CMAKE_VERSION=${ASWF_CMAKE_VERSION}
ENV ASWF_PYTHON_VERSION=${ASWF_PYTHON_VERSION}
ENV ASWF_PYTHON_MAJOR_MINOR_VERSION=${ASWF_PYTHON_MAJOR_MINOR_VERSION}
ENV ASWF_NUMPY_VERSION=${ASWF_NUMPY_VERSION}
ENV ASWF_BOOST_VERSION=${ASWF_BOOST_VERSION}
ENV ASWF_TBB_VERSION=${ASWF_TBB_VERSION}
ENV ASWF_VFXPLATFORM_VERSION=${ASWF_VFXPLATFORM_VERSION}

COPY scripts/common/install_conanpackages.sh /tmp

# Use conan to install some packages
COPY <<EOF /usr/local/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
cmake/${ASWF_CMAKE_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
python/${ASWF_PYTHON_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
boost/${ASWF_BOOST_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
tbb/${ASWF_TBB_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

RUN --mount=type=cache,target=/opt/conan_home/d \
    --mount=type=bind,rw,target=/opt/conan_home/.conan,source=packages/conan/settings \
    /tmp/install_conanpackages.sh /usr/local vfx${ASWF_VFXPLATFORM_VERSION}

COPY ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

ENV DOWNLOADS_DIR=/tmp/downloads \
     CCACHE_DIR=/tmp/ccache \
     ASWF_INSTALL_PREFIX=/usr/local \
     PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${ASWF_PYTHON_MAJOR_MINOR_VERSION}/site-packages:${PYTHONPATH}

#################### ci-osl-builder ####################
FROM ci-base-builder AS ci-osl-builder

ARG ASWF_OSL_VERSION
ENV ASWF_OSL_VERSION=${ASWF_OSL_VERSION}
ARG ASWF_PKG_ORG
ARG ASWF_CONAN_CHANNEL
ARG CI_COMMON_VERSION
ENV CI_COMMON_VERSION=${CI_COMMON_VERSION}
ARG ASWF_VFXPLATFORM_VERSION
ENV ASWF_VFXPLATFORM_VERSION=${ASWF_VFXPLATFORM_VERSION}
ARG ASWF_PYSIDE_CLANG_VERSION
ENV ASWF_PYSIDE_CLANG_VERSION=${ASWF_PYSIDE_CLANG_VERSION}
ARG ASWF_TBB_VERSION
ENV ASWF_TBB_VERSION=${ASWF_TBB_VERSION}
ARG ASWF_CXX_STANDARD
ENV ASWF_CXX_STANDARD=${ASWF_CXX_STANDARD}
ARG ASWF_PARTIO_VERSION
ENV ASWF_PARTIO_VERSION=${ASWF_PARTIO_VERSION}
ARG ASWF_PYBIND11_VERSION
ENV ASWF_PYBIND11_VERSION=${ASWF_PYBIND11_VERSION}
ARG ASWF_EXPAT_VERSION
ENV ASWF_EXPAT_VERSION=${ASWF_EXPAT_VERSION}
ARG ASWF_QT_VERSION
ENV ASWF_QT_VERSION=${ASWF_QT_VERSION}
ARG ASWF_PYSIDE_VERSION
ENV ASWF_PYSIDE_VERSION=${ASWF_PYSIDE_VERSION}
ARG ASWF_BLOSC_VERSION
ENV ASWF_BLOSC_VERSION=${ASWF_BLOSC_VERSION}
ARG ASWF_PTEX_VERSION
ENV ASWF_PTEX_VERSION=${ASWF_PTEX_VERSION}
ARG ASWF_IMATH_VERSION
ENV ASWF_IMATH_VERSION=${ASWF_IMATH_VERSION}
ARG ASWF_OPENEXR_VERSION
ENV ASWF_OPENEXR_VERSION=${ASWF_OPENEXR_VERSION}

COPY --from=ci-package-openvdb-external /. /usr/local/
COPY --from=ci-package-oiio-external /. /usr/local/
COPY --from=ci-package-ocio-external /. /usr/local/

COPY ../scripts/vfx/build_osl.sh \
     /tmp/

COPY scripts/common/install_conanpackages.sh /tmp

# Use conan to install dependencies
COPY <<EOF /usr/local/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
expat/${ASWF_EXPAT_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
tbb/${ASWF_TBB_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
partio/${ASWF_PARTIO_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
pybind11/${ASWF_PYBIND11_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
qt/${ASWF_QT_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
pyside/${ASWF_PYSIDE_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
blosc/${ASWF_BLOSC_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
ptex/${ASWF_PTEX_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
imath/${ASWF_IMATH_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
openexr/${ASWF_OPENEXR_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

RUN --mount=type=cache,target=/opt/conan_home/d \
    --mount=type=bind,rw,target=/opt/conan_home/.conan,source=packages/conan/settings \
    /tmp/install_conanpackages.sh /usr/local vfx${ASWF_VFXPLATFORM_VERSION}

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_osl.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-osl ####################
FROM scratch AS ci-package-osl

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
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


#################### ci-usd-builder ####################
FROM ci-base-builder AS ci-usd-builder

ARG ASWF_PKG_ORG
ARG ASWF_CONAN_CHANNEL
ARG CI_COMMON_VERSION
ARG ASWF_PYSIDE_CLANG_VERSION
ARG ASWF_USD_VERSION
ARG ASWF_NUMPY_VERSION
ARG ASWF_EXPAT_VERSION
ARG ASWF_GLEW_VERSION
ARG ASWF_GLFW_VERSION
ARG ASWF_PYBIND11_VERSION
ARG ASWF_MATERIALX_VERSION
ARG ASWF_QT_VERSION
ARG ASWF_PYSIDE_VERSION
ARG ASWF_ALEMBIC_VERSION
ARG ASWF_IMATH_VERSION
ARG ASWF_OPENEXR_VERSION
ARG ASWF_OPENSUBDIV_VERSION
ARG ASWF_PARTIO_VERSION
ARG ASWF_PTEX_VERSION

ENV CI_COMMON_VERSION=${CI_COMMON_VERSION}
ENV ASWF_PYSIDE_CLANG_VERSION=${ASWF_PYSIDE_CLANG_VERSION}
ENV ASWF_USD_VERSION=${ASWF_USD_VERSION}
ENV ASWF_NUMPY_VERSION=${ASWF_NUMPY_VERSION}
ENV ASWF_EXPAT_VERSION=${ASWF_EXPAT_VERSION}
ENV ASWF_GLEW_VERSION=${ASWF_GLEW_VERSION}
ENV ASWF_GLFW_VERSION=${ASWF_GLFW_VERSION}
ENV ASWF_PYBIND11_VERSION=${ASWF_PYBIND11_VERSION}
ENV ASWF_MATERIALIX_VERSION=${ASWF_MATERIALX_VERSION}
ENV ASWF_QT_VERSION=${ASWF_PYSIDE_VERSION}
ENV ASWF_PYSIDE_VERSION=${ASWF_PYSIDE_VERSION}
ENV ASWF_ALEMBIC_VERSION=${ASWF_ALEMBIC_VERSION}
ENV ASWF_IMATH_VERSION=${ASWF_IMATH_VERSION}
ENV ASWF_OPENEXR_VERSION=${ASWF_OPENEXR_VERSION}
ENV ASWF_OPENSUBDIV_VERSION=${ASWF_OPENSUBDIV_VERSION}
ENV ASWF_PARTIO_VERSION=${ASWF_PARTIO_VERSION}
ENV ASWF_PTEX_VERSION=${ASWF_PTEX_VERSION}

COPY --from=ci-package-openvdb-external /. /usr/local/
COPY --from=ci-package-oiio-external /. /usr/local/
COPY --from=ci-package-ocio-external /. /usr/local/

COPY ../scripts/vfx/build_usd.sh \
     /tmp/

COPY scripts/common/install_conanpackages.sh /tmp

# Use conan to install dependencies
COPY <<EOF /usr/local/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
alembic/${ASWF_ALEMBIC_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
expat/${ASWF_EXPAT_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
glew/${ASWF_GLEW_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
qt/${ASWF_QT_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
pyside/${ASWF_PYSIDE_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
opensubdiv/${ASWF_OPENSUBDIV_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
partio/${ASWF_PARTIO_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
imath/${ASWF_IMATH_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
openexr/${ASWF_OPENEXR_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
materialx/${ASWF_MATERIALX_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

RUN --mount=type=cache,target=/opt/conan_home/d \
    --mount=type=bind,rw,target=/opt/conan_home/.conan,source=packages/conan/settings \
    /tmp/install_conanpackages.sh /usr/local vfx${ASWF_VFXPLATFORM_VERSION}

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_usd.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-usd ####################
FROM scratch AS ci-package-usd

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
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
FROM ci-base-builder AS ci-otio-builder

ARG CI_COMMON_VERSION
ARG ASWF_PYSIDE_CLANG_VERSION
ARG ASWF_OTIO_VERSION
ARG ASWF_EXPAT_VERSION
ARG ASWF_QT_VERSION
ARG ASWF_PYSIDE_VERSION

ENV CI_COMMON_VERSION=${CI_COMMON_VERSION}
ENV ASWF_PYSIDE_CLANG_VERSION=${ASWF_PYSIDE_CLANG_VERSION}
ENV ASWF_OTIO_VERSION=${ASWF_OTIO_VERSION}
ENV ASWF_EXPAT_VERSION=${ASWF_EXPAT_VERSION}
ENV ASWF_QT_VERSION=${ASWF_QT_VERSION}
ENV ASWF_PYSIDE_VERSION=${ASWF_PYSIDE_VERSION}

COPY scripts/common/install_conanpackages.sh /tmp

# Use conan to install some packages
COPY <<EOF /usr/local/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
expat/${ASWF_EXPAT_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
qt/${ASWF_QT_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
pyside/${ASWF_PYSIDE_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

COPY ../scripts/vfx/build_otio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_otio.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-otio ####################
FROM scratch AS ci-package-otio

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
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
