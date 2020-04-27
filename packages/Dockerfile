# syntax = docker/dockerfile:experimental

# "Global" ARGs
ARG CI_COMMON_VERSION=1
ARG VFXPLATFORM_VERSION=2019
ARG PYTHON_VERSION=2.7
ARG CUDA_VERSION=10.1
ARG ASWF_ORG=aswftesting

# Required packages built in previous passes to speed things up
FROM ${ASWF_ORG}/ci-package-clang:${CI_COMMON_VERSION} as ci-package-clang
FROM ${ASWF_ORG}/ci-package-qt:${VFXPLATFORM_VERSION} as ci-package-qt
FROM ${ASWF_ORG}/ci-package-pyside:${VFXPLATFORM_VERSION} as ci-package-pyside

#################### ci-centos7-gl-packages ####################
FROM nvidia/cudagl:${CUDA_VERSION}-devel-centos7 as ci-centos7-gl-packages

ARG CI_COMMON_VERSION

COPY ../scripts/common/install_yumpackages.sh \
     /tmp/

RUN --mount=type=cache,sharing=private,target=/var/cache/yum \
    /tmp/install_yumpackages.sh

COPY ../scripts/${CI_COMMON_VERSION}/versions_common.sh \
     ../scripts/common/install_dev_ccache.sh \
     ../scripts/common/before_build.sh \
     ../scripts/common/copy_new_files.sh \
     /tmp/

ENV CI_COMMON_VERSION=${CI_COMMON_VERSION} \
    DOWNLOADS_DIR=/tmp/downloads \
    CCACHE_DIR=/tmp/ccache \
    ASWF_INSTALL_PREFIX=/usr/local \
    LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:/opt/rh/devtoolset-6/root/usr/lib64:/opt/rh/devtoolset-6/root/usr/lib:${LD_LIBRARY_PATH} \
    PATH=/opt/aswfbuilder/bin:/usr/local/bin:/opt/rh/devtoolset-6/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-6/root/usr/bin/:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin

RUN --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_common.sh && \
    /tmp/install_dev_ccache.sh


#################### ci-clang-builder ####################
FROM ci-centos7-gl-packages as ci-clang-builder

ARG CI_COMMON_VERSION

COPY ../scripts/${CI_COMMON_VERSION}/versions_common.sh \
     ../scripts/common/build_clang.sh \
     ../scripts/common/install_dev_cmake.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,target=/tmp/downloads \
    source /tmp/versions_common.sh && \
    /tmp/install_dev_cmake.sh && \
    /tmp/before_build.sh && \
    /tmp/build_clang.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-clang-package ####################
# This build target is used to generate a packages of clang that 
# can be placed in a downloadable artifact

FROM scratch as ci-clang-package

COPY --from=ci-clang-builder /package/. /


#################### ci-ninja-builder ####################
FROM ci-centos7-gl-packages as ci-ninja-builder

ARG CI_COMMON_VERSION

COPY ../scripts/${CI_COMMON_VERSION}/versions_common.sh \
     ../scripts/common/build_ninja.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,target=/tmp/downloads \
    source /tmp/versions_common.sh && \
    /tmp/before_build.sh && \
    /tmp/build_ninja.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-ninja-package ####################
# This build target is used to generate a packages of ninja that 
# can be placed in a downloadable artifact

FROM scratch as ci-ninja-package

COPY --from=ci-ninja-builder /package/. /


#################### ci-python-builder ####################
FROM ci-centos7-gl-packages as ci-python-builder

ARG VFXPLATFORM_VERSION
ARG PYTHON_VERSION

ENV PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${PYTHON_VERSION}/site-packages:${PYTHONPATH}
ENV VFXPLATFORM_VERSION=${VFXPLATFORM_VERSION}

COPY ../scripts/${VFXPLATFORM_VERSION}/versions_base.sh \
     ../scripts/base/build_python.sh \
     ../scripts/base/install_cmake.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/install_cmake.sh && \
    /tmp/before_build.sh && \
    /tmp/build_python.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-boost-package ####################
# This build target is used to generate a packages of boost that 
# can be placed in a downloadable artifact

FROM scratch as ci-python-package

COPY --from=ci-python-builder /package/. /


#################### ci-boost-builder ####################
FROM ci-python-builder as ci-boost-builder

ARG VFXPLATFORM_VERSION
ARG PYTHON_VERSION

COPY ../scripts/base/build_boost.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_boost.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-boost-package ####################
# This build target is used to generate a packages of boost that 
# can be placed in a downloadable artifact

FROM scratch as ci-boost-package

COPY --from=ci-boost-builder /package/. /


#################### ci-tbb-builder ####################
FROM ci-python-builder as ci-tbb-builder

COPY ../scripts/base/build_tbb.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_tbb.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-tbb-package ####################
# This build target is used to generate a packages of tbb that 
# can be placed in a downloadable artifact

FROM scratch as ci-tbb-package

COPY --from=ci-tbb-builder /package/. /


#################### ci-cppunit-builder ####################
FROM ci-python-builder as ci-cppunit-builder

COPY ../scripts/base/build_cppunit.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_cppunit.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-cppunit-package ####################
# This build target is used to generate a packages of cppunit that 
# can be placed in a downloadable artifact

FROM scratch as ci-cppunit-package

COPY --from=ci-cppunit-builder /package/. /


#################### ci-log4cplus-builder ####################
FROM ci-python-builder as ci-log4cplus-builder

COPY ../scripts/base/build_log4cplus.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_log4cplus.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-log4cplus-package ####################
# This build target is used to generate a packages of log4cplus that 
# can be placed in a downloadable artifact

FROM scratch as ci-log4cplus-package

COPY --from=ci-log4cplus-builder /package/. /


#################### ci-glew-builder ####################
FROM ci-python-builder as ci-glew-builder

COPY ../scripts/base/build_glew.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_glew.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-glew-package ####################
# This build target is used to generate a packages of glew that 
# can be placed in a downloadable artifact

FROM scratch as ci-glew-package

COPY --from=ci-glew-builder /package/. /



#################### ci-glfw-builder ####################
FROM ci-python-builder as ci-glfw-builder

COPY ../scripts/base/build_glfw.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_glfw.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-glfw-package ####################
# This build target is used to generate a packages of glfw that 
# can be placed in a downloadable artifact

FROM scratch as ci-glfw-package

COPY --from=ci-glfw-builder /package/. /


#################### -qt-builder ####################
FROM ci-python-builder as ci-qt-builder

COPY ../scripts/base/build_qt.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_qt.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-qt-package ####################
# This build target is used to generate a packages of qt that 
# can be placed in a downloadable artifact

FROM scratch as ci-qt-package

COPY --from=ci-qt-builder /package/. /


#################### ci-pyside-builder ####################
FROM ci-python-builder as ci-pyside-builder

# Workaround pyside issue with Qt headers within system location https://bugreports.qt.io/browse/PYSIDE-787
COPY --from=ci-package-qt /. /tmp/qt5temp

COPY ../scripts/base/build_pyside.sh \
     /tmp/

COPY --from=ci-package-clang /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_pyside.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-pyside-package ####################
# This build target is used to generate a packages of pyside that 
# can be placed in a downloadable artifact

FROM scratch as ci-pyside-package

COPY --from=ci-pyside-builder /package/. /



#################### ci-openexr-builder ####################
FROM ci-boost-builder as ci-openexr-builder

COPY ../scripts/$VFXPLATFORM_VERSION/versions_vfx.sh \
     ../scripts/vfx/build_openexr.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_openexr.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-openexr-package ####################
# This build target is used to generate a packages of openexr that 
# can be placed in a downloadable artifact

FROM scratch as ci-openexr-package

COPY --from=ci-openexr-builder /package/. /


#################### ci-blosc-builder ####################
FROM ci-python-builder as ci-blosc-builder

COPY ../scripts/$VFXPLATFORM_VERSION/versions_vfx.sh \
     ../scripts/vfx/build_blosc.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_blosc.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-blosc-package ####################
# This build target is used to generate a packages of blosc that 
# can be placed in a downloadable artifact

FROM scratch as ci-blosc-package

COPY --from=ci-blosc-builder /package/. /


#################### ci-oiio-builder ####################
FROM ci-openexr-builder as ci-oiio-builder

COPY ../scripts/vfx/build_oiio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_oiio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-oiio-package ####################
# This build target is used to generate a packages of oiio that 
# can be placed in a downloadable artifact

FROM scratch as ci-oiio-package

COPY --from=ci-oiio-builder /package/. /


#################### ci-ocio-builder ####################
FROM ci-oiio-builder as ci-ocio-builder

COPY ../scripts/vfx/build_ocio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_ocio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-ocio-package ####################
# This build target is used to generate a packages of ocio that 
# can be placed in a downloadable artifact

FROM scratch as ci-ocio-package

COPY --from=ci-ocio-builder /package/. /


#################### ci-alembic-builder ####################
FROM ci-openexr-builder as ci-alembic-builder

COPY ../scripts/vfx/build_alembic.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_alembic.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-alembic-package ####################
# This build target is used to generate a packages of alembic that 
# can be placed in a downloadable artifact

FROM scratch as ci-alembic-package

COPY --from=ci-alembic-builder /package/. /



#################### ci-ptex-builder ####################
FROM ci-openexr-builder as ci-ptex-builder

COPY ../scripts/vfx/build_ptex.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_ptex.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-ptex-package ####################
# This build target is used to generate a packages of ptex that 
# can be placed in a downloadable artifact

FROM scratch as ci-ptex-package

COPY --from=ci-ptex-builder /package/. /




#################### ci-opensubdiv-builder ####################
FROM ci-ptex-builder as ci-opensubdiv-builder

COPY ../scripts/vfx/build_opensubdiv.sh \
     /tmp/

COPY --from=ci-glew-package /. /usr/local/
COPY --from=ci-tbb-package /. /usr/local/
COPY --from=ci-glfw-package /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_opensubdiv.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-opensubdiv-package ####################
# This build target is used to generate a packages of opensubdiv that 
# can be placed in a downloadable artifact

FROM scratch as ci-opensubdiv-package

COPY --from=ci-opensubdiv-builder /package/. /




#################### ci-openvdb-builder ####################
FROM ci-openexr-builder as ci-openvdb-builder

COPY ../scripts/vfx/build_openvdb.sh \
     /tmp/

COPY --from=ci-glew-package /. /usr/local/
COPY --from=ci-tbb-package /. /usr/local/
COPY --from=ci-cppunit-package /. /usr/local/
COPY --from=ci-glfw-package /. /usr/local/
COPY --from=ci-blosc-package /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_openvdb.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-openvdb-package ####################
# This build target is used to generate a packages of openvdb that 
# can be placed in a downloadable artifact

FROM scratch as ci-openvdb-package

COPY --from=ci-openvdb-builder /package/. /




#################### ci-usd-builder ####################
FROM ci-opensubdiv-builder as ci-usd-builder

COPY --from=ci-glew-package /. /usr/local/
COPY --from=ci-alembic-package /. /usr/local/
COPY --from=ci-openvdb-package /. /usr/local/
COPY --from=ci-oiio-package /. /usr/local/
COPY --from=ci-ocio-package /. /usr/local/
COPY --from=ci-package-qt /. /usr/local/
COPY --from=ci-package-pyside /. /usr/local/

COPY ../scripts/vfx/build_usd.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_usd.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-usd-package ####################
# This build target is used to generate a packages of usd that 
# can be placed in a downloadable artifact

FROM scratch as ci-usd-package

COPY --from=ci-usd-builder /package/. /


