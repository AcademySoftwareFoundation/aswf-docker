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
ARG ASWF_CPYTHON_VERSION
ARG ASWF_PYTHON_MAJOR_MINOR_VERSION
ARG ASWF_ONETBB_VERSION

ARG ASWF_ALEMBIC_VERSION
ARG ASWF_BLOSC_VERSION
ARG ASWF_OCIO_VERSION
ARG ASWF_OIIO_VERSION
ARG ASWF_OPENEXR_VERSION
ARG ASWF_IMATH_VERSION
ARG ASWF_OPENRV_VERSION
ARG ASWF_OPENSUBDIV_VERSION
ARG ASWF_PARTIO_VERSION
ARG ASWF_PTEX_VERSION
ARG ASWF_PYSIDE_VERSION
ARG ASWF_QT_VERSION

# Required base packages built in previous stages

FROM ${ASWF_ORG}/ci-package-oiio:${ASWF_VFXPLATFORM_VERSION}-${ASWF_OIIO_VERSION} AS ci-package-oiio-external
FROM ${ASWF_ORG}/ci-package-ocio:${ASWF_VFXPLATFORM_VERSION}-${ASWF_OCIO_VERSION} AS ci-package-ocio-external

#################### ci-base-builder ####################
FROM ${ASWF_ORG}/ci-common:${CI_COMMON_VERSION}-clang${ASWF_CLANG_MAJOR_VERSION} AS ci-base-builder

ARG ASWF_CMAKE_VERSION
ARG ASWF_CPYTHON_VERSION
ARG ASWF_PYTHON_MAJOR_MINOR_VERSION
ARG ASWF_NUMPY_VERSION
ARG ASWF_BOOST_VERSION
ARG ASWF_ONETBB_VERSION
ARG ASWF_PKG_ORG
ARG ASWF_CONAN_CHANNEL
ARG ASWF_VFXPLATFORM_VERSION

ENV ASWF_CMAKE_VERSION=${ASWF_CMAKE_VERSION}
ENV ASWF_CPYTHON_VERSION=${ASWF_CPYTHON_VERSION}
ENV ASWF_PYTHON_MAJOR_MINOR_VERSION=${ASWF_PYTHON_MAJOR_MINOR_VERSION}
ENV ASWF_NUMPY_VERSION=${ASWF_NUMPY_VERSION}
ENV ASWF_BOOST_VERSION=${ASWF_BOOST_VERSION}
ENV ASWF_ONETBB_VERSION=${ASWF_ONETBB_VERSION}
ENV ASWF_VFXPLATFORM_VERSION=${ASWF_VFXPLATFORM_VERSION}

COPY scripts/common/install_conanpackages.sh /tmp

# Use conan to install some packages
COPY <<EOF /usr/local/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
cmake/${ASWF_CMAKE_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
cpython/${ASWF_CPYTHON_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
boost/${ASWF_BOOST_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
onetbb/${ASWF_ONETBB_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

RUN --mount=type=cache,target=/opt/conan_home/d \
    --mount=type=bind,rw,target=/opt/conan_home/.conan2,source=packages/conan/settings \
    /tmp/install_conanpackages.sh /usr/local vfx${ASWF_VFXPLATFORM_VERSION}

COPY ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

ENV DOWNLOADS_DIR=/tmp/downloads \
     CCACHE_DIR=/tmp/ccache \
     ASWF_INSTALL_PREFIX=/usr/local \
     PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${ASWF_PYTHON_MAJOR_MINOR_VERSION}/site-packages:${PYTHONPATH}

#################### ci-openrv-builder ####################
FROM ci-base-builder AS ci-openrv-builder

ARG ASWF_OPENRV_VERSION
ENV ASWF_OPENRV_VERSION=${ASWF_OPENRV_VERSION}
ARG ASWF_PKG_ORG
ARG ASWF_CONAN_CHANNEL
ARG CI_COMMON_VERSION
ENV CI_COMMON_VERSION=${CI_COMMON_VERSION}
ARG ASWF_VFXPLATFORM_VERSION
ENV ASWF_VFXPLATFORM_VERSION=${ASWF_VFXPLATFORM_VERSION}
ARG ASWF_PYSIDE_CLANG_VERSION
ENV ASWF_PYSIDE_CLANG_VERSION=${ASWF_PYSIDE_CLANG_VERSION}
ARG ASWF_CXX_STANDARD
ENV ASWF_CXX_STANDARD=${ASWF_CXX_STANDARD}
ARG ASWF_EXPAT_VERSION
ENV ASWF_EXPAT_VERSION=${ASWF_EXPAT_VERSION}
ARG ASWF_QT_VERSION
ENV ASWF_QT_VERSION=${ASWF_QT_VERSION}
ARG ASWF_IMATH_VERSION
ENV ASWF_IMATH_VERSION=${ASWF_IMATH_VERSION}
ARG ASWF_OPENEXR_VERSION
ENV ASWF_OPENEXR_VERSION=${ASWF_OPENEXR_VERSION}

COPY --from=ci-package-oiio-external /. /usr/local/
COPY --from=ci-package-ocio-external /. /usr/local/

COPY ../scripts/review/build_openrv.sh \
     /tmp/

COPY scripts/common/install_conanpackages.sh /tmp

# Use conan to install dependencies
COPY <<EOF /usr/local/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
expat/${ASWF_EXPAT_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
imath/${ASWF_IMATH_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
openexr/${ASWF_OPENEXR_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

RUN --mount=type=cache,target=/opt/conan_home/d \
    --mount=type=bind,rw,target=/opt/conan_home/.conan2,source=packages/conan/settings \
    /tmp/install_conanpackages.sh /usr/local vfx${ASWF_VFXPLATFORM_VERSION}

# Qt files are under /tmp/qttemp because OpenRV compiles its own PySide2 and it
# causes issues during the build when Qt is within system folder (e.g. /usr/local)

# Use conan to install dependencies
COPY <<EOF /tmp/qttemp/conanfile.txt
[generators]
[imports]
., * -> .
[requires]
qt/${ASWF_QT_VERSION}@${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}
EOF

RUN --mount=type=cache,target=/opt/conan_home/d \
    --mount=type=bind,rw,target=/opt/conan_home/.conan2,source=packages/conan/settings \
    /tmp/install_conanpackages.sh /tmp/qttemp vfx${ASWF_VFXPLATFORM_VERSION}

RUN --mount=type=cache,target=/tmp/ccache \
     --mount=type=cache,sharing=private,target=/tmp/downloads \
     /tmp/before_build.sh && \
     /tmp/build_openrv.sh && \
     /tmp/copy_new_files.sh && \
     ccache --show-stats


#################### ci-package-openrv ####################
FROM scratch AS ci-package-openrv

ARG ASWF_ORG
ARG CI_COMMON_VERSION
ARG ASWF_DTS_VERSION
ARG ASWF_DTS_PREFIX
ARG ASWF_OPENRV_VERSION
ARG ASWF_VFXPLATFORM_VERSION

LABEL org.opencontainers.image.name="$ASWF_ORG/ci-package-openrv"
LABEL org.opencontainers.image.title="OpenRV package built for ASWF Docker images"
LABEL org.opencontainers.image.description="OpenRV headers and binaries to be installed in ASWF Docker images"
LABEL org.opencontainers.image.authors="Built by aswf.io CI Working Group"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.url="https://github.com/AcademySoftwareFoundation/OpenRV"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker/blob/main/packages/Dockerfile"
LABEL org.opencontainers.image.version="${ASWF_OPENRV_VERSION}"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL io.aswf.docker.versions.ci-common="${CI_COMMON_VERSION}"
LABEL io.aswf.docker.versions.vfx-platform="${ASWF_VFXPLATFORM_VERSION}"
LABEL io.aswf.docker.versions.dts="${ASWF_DTS_VERSION}"
LABEL io.aswf.docker.versions.osl="${ASWF_OSL_VERSION}"

COPY --from=ci-openrv-builder /package/. /

