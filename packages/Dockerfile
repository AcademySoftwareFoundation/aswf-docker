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
     ../scripts/common/install_dev_cmake.sh \
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
    /tmp/install_dev_ccache.sh && \
    /tmp/install_dev_cmake.sh


#################### ci-common-clang-builder ####################
FROM ci-centos7-gl-packages as ci-common-clang-builder

ARG CI_COMMON_VERSION

COPY ../scripts/${CI_COMMON_VERSION}/versions_common.sh \
     ../scripts/common/build_clang.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,target=/tmp/downloads \
    source /tmp/versions_common.sh && \
    /tmp/before_build.sh && \
    /tmp/build_clang.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-common-clang-package ####################
# This build target is used to generate a packages of clang that 
# can be placed in a downloadable artifact

FROM scratch as ci-common-clang-package

COPY --from=ci-common-clang-builder /package/. /


#################### ci-base-python-builder ####################
FROM ci-centos7-gl-packages as ci-base-python-builder

ARG VFXPLATFORM_VERSION
ARG PYTHON_VERSION

ENV PYTHONPATH=${ASWF_INSTALL_PREFIX}/lib/python${PYTHON_VERSION}/site-packages:${PYTHONPATH}
ENV VFXPLATFORM_VERSION=${VFXPLATFORM_VERSION}

COPY ../scripts/${VFXPLATFORM_VERSION}/versions_base.sh \
     ../scripts/base/build_python.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_python.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-base-boost-package ####################
# This build target is used to generate a packages of boost that 
# can be placed in a downloadable artifact

FROM scratch as ci-base-python-package

COPY --from=ci-base-python-builder /package/. /


#################### ci-base-boost-builder ####################
FROM ci-base-python-builder as ci-base-boost-builder

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


#################### ci-base-boost-package ####################
# This build target is used to generate a packages of boost that 
# can be placed in a downloadable artifact

FROM scratch as ci-base-boost-package

COPY --from=ci-base-boost-builder /package/. /


#################### ci-base-tbb-builder ####################
FROM ci-base-python-builder as ci-base-tbb-builder

COPY ../scripts/base/build_tbb.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_tbb.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-base-tbb-package ####################
# This build target is used to generate a packages of tbb that 
# can be placed in a downloadable artifact

FROM scratch as ci-base-tbb-package

COPY --from=ci-base-tbb-builder /package/. /


#################### ci-base-cppunit-builder ####################
FROM ci-base-python-builder as ci-base-cppunit-builder

COPY ../scripts/base/build_cppunit.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_cppunit.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-base-cppunit-package ####################
# This build target is used to generate a packages of cppunit that 
# can be placed in a downloadable artifact

FROM scratch as ci-base-cppunit-package

COPY --from=ci-base-cppunit-builder /package/. /


#################### ci-base-log4cplus-builder ####################
FROM ci-base-python-builder as ci-base-log4cplus-builder

COPY ../scripts/base/build_log4cplus.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_log4cplus.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-base-log4cplus-package ####################
# This build target is used to generate a packages of log4cplus that 
# can be placed in a downloadable artifact

FROM scratch as ci-base-log4cplus-package

COPY --from=ci-base-log4cplus-builder /package/. /


#################### ci-base-glew-builder ####################
FROM ci-base-python-builder as ci-base-glew-builder

COPY ../scripts/base/build_glew.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_glew.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-base-glew-package ####################
# This build target is used to generate a packages of glew that 
# can be placed in a downloadable artifact

FROM scratch as ci-base-glew-package

COPY --from=ci-base-glew-builder /package/. /



#################### ci-base-glfw-builder ####################
FROM ci-base-python-builder as ci-base-glfw-builder

COPY ../scripts/base/build_glfw.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_glfw.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-base-glfw-package ####################
# This build target is used to generate a packages of glfw that 
# can be placed in a downloadable artifact

FROM scratch as ci-base-glfw-package

COPY --from=ci-base-glfw-builder /package/. /


#################### ci-base-qt-builder ####################
FROM ci-base-python-builder as ci-base-qt-builder

COPY ../scripts/base/build_qt.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    /tmp/before_build.sh && \
    /tmp/build_qt.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-base-qt-package ####################
# This build target is used to generate a packages of qt that 
# can be placed in a downloadable artifact

FROM scratch as ci-base-qt-package

COPY --from=ci-base-qt-builder /package/. /


#################### ci-base-pyside-builder ####################
FROM ci-base-python-builder as ci-base-pyside-builder

# Workaround pyside issue with Qt headers within system location https://bugreports.qt.io/browse/PYSIDE-787
COPY ../scripts/base/build_qt.sh /tmp/
RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    export ASWF_INSTALL_PREFIX=/tmp/qt5temp && \
    /tmp/build_qt.sh && \
    ccache --show-stats

COPY ../scripts/base/build_pyside.sh \
     /tmp/

COPY --from=ci-package-clang /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_base.sh && \
    export PATH=/tmp/qt5temp/bin:$PATH && \
    export LD_LIBRARY_PATH=/tmp/qt5temp/lib:$LD_LIBRARY_PATH && \
    /tmp/before_build.sh && \
    /tmp/build_pyside.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-base-pyside-package ####################
# This build target is used to generate a packages of pyside that 
# can be placed in a downloadable artifact

FROM scratch as ci-base-pyside-package

COPY --from=ci-base-pyside-builder /package/. /



#################### ci-vfx-openexr-builder ####################
FROM ci-base-boost-builder as ci-vfx-openexr-builder

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


#################### ci-vfx-openexr-package ####################
# This build target is used to generate a packages of openexr that 
# can be placed in a downloadable artifact

FROM scratch as ci-vfx-openexr-package

COPY --from=ci-vfx-openexr-builder /package/. /


#################### ci-vfx-blosc-builder ####################
FROM ci-base-python-builder as ci-vfx-blosc-builder

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


#################### ci-vfx-blosc-package ####################
# This build target is used to generate a packages of blosc that 
# can be placed in a downloadable artifact

FROM scratch as ci-vfx-blosc-package

COPY --from=ci-vfx-blosc-builder /package/. /


#################### ci-vfx-oiio-builder ####################
FROM ci-vfx-openexr-builder as ci-vfx-oiio-builder

COPY ../scripts/vfx/build_oiio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_oiio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-vfx-oiio-package ####################
# This build target is used to generate a packages of oiio that 
# can be placed in a downloadable artifact

FROM scratch as ci-vfx-oiio-package

COPY --from=ci-vfx-oiio-builder /package/. /


#################### ci-vfx-ocio-builder ####################
FROM ci-vfx-oiio-builder as ci-vfx-ocio-builder

COPY ../scripts/vfx/build_ocio.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_ocio.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-vfx-ocio-package ####################
# This build target is used to generate a packages of ocio that 
# can be placed in a downloadable artifact

FROM scratch as ci-vfx-ocio-package

COPY --from=ci-vfx-ocio-builder /package/. /


#################### ci-vfx-alembic-builder ####################
FROM ci-vfx-openexr-builder as ci-vfx-alembic-builder

COPY ../scripts/vfx/build_alembic.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_alembic.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-vfx-alembic-package ####################
# This build target is used to generate a packages of alembic that 
# can be placed in a downloadable artifact

FROM scratch as ci-vfx-alembic-package

COPY --from=ci-vfx-alembic-builder /package/. /



#################### ci-vfx-ptex-builder ####################
FROM ci-vfx-openexr-builder as ci-vfx-ptex-builder

COPY ../scripts/vfx/build_ptex.sh \
     /tmp/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_ptex.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-vfx-ptex-package ####################
# This build target is used to generate a packages of ptex that 
# can be placed in a downloadable artifact

FROM scratch as ci-vfx-ptex-package

COPY --from=ci-vfx-ptex-builder /package/. /




#################### ci-vfx-opensubdiv-builder ####################
FROM ci-vfx-ptex-builder as ci-vfx-opensubdiv-builder

COPY ../scripts/vfx/build_opensubdiv.sh \
     /tmp/

COPY --from=ci-base-glew-package /. /usr/local/
COPY --from=ci-base-tbb-package /. /usr/local/
COPY --from=ci-base-glfw-package /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_opensubdiv.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-vfx-opensubdiv-package ####################
# This build target is used to generate a packages of opensubdiv that 
# can be placed in a downloadable artifact

FROM scratch as ci-vfx-opensubdiv-package

COPY --from=ci-vfx-opensubdiv-builder /package/. /




#################### ci-vfx-openvdb-builder ####################
FROM ci-vfx-openexr-builder as ci-vfx-openvdb-builder

COPY ../scripts/vfx/build_openvdb.sh \
     /tmp/

COPY --from=ci-base-glew-package /. /usr/local/
COPY --from=ci-base-tbb-package /. /usr/local/
COPY --from=ci-base-cppunit-package /. /usr/local/
COPY --from=ci-base-glfw-package /. /usr/local/
COPY --from=ci-vfx-blosc-package /. /usr/local/

RUN --mount=type=cache,target=/tmp/ccache \
    --mount=type=cache,sharing=private,target=/tmp/downloads \
    source /tmp/versions_vfx.sh && \
    /tmp/before_build.sh && \
    /tmp/build_openvdb.sh && \
    /tmp/copy_new_files.sh && \
    ccache --show-stats


#################### ci-vfx-openvdb-package ####################
# This build target is used to generate a packages of openvdb that 
# can be placed in a downloadable artifact

FROM scratch as ci-vfx-openvdb-package

COPY --from=ci-vfx-openvdb-builder /package/. /




#################### ci-vfx-usd-builder ####################
FROM ci-vfx-opensubdiv-builder as ci-vfx-usd-builder

COPY --from=ci-base-glew-package /. /usr/local/
COPY --from=ci-vfx-alembic-package /. /usr/local/
COPY --from=ci-vfx-openvdb-package /. /usr/local/
COPY --from=ci-vfx-oiio-package /. /usr/local/
COPY --from=ci-vfx-ocio-package /. /usr/local/
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


#################### ci-vfx-usd-package ####################
# This build target is used to generate a packages of usd that 
# can be placed in a downloadable artifact

FROM scratch as ci-vfx-usd-package

COPY --from=ci-vfx-usd-builder /package/. /


