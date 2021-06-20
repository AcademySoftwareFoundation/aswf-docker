# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG CUDA_VERSION=10.2
ARG ASWF_ORG=aswftesting
ARG ASWF_PKG_ORG=aswftesting
ARG CI_COMMON_VERSION=1
ARG VFXPLATFORM_VERSION=2019

ARG ASWF_ORG
ARG VFXPLATFORM_VERSION
ARG ASWF_VERSION
ARG PYTHON_VERSION=2.7

FROM ${ASWF_PKG_ORG}/ci-package-python:${VFXPLATFORM_VERSION} as ci-package-python
FROM ${ASWF_PKG_ORG}/ci-package-tbb:${VFXPLATFORM_VERSION} as ci-package-tbb

FROM nvidia/cudagl:${CUDA_VERSION}-devel-centos7 as builder

COPY --from=ci-package-python /. /usr/local/
COPY --from=ci-package-tbb /. /usr/local/

RUN rm -rf /usr/local/include

FROM nvidia/cudagl:${CUDA_VERSION}-devel-centos7 as rt-base

LABEL maintainer="aloys.baillet@gmail.com"
LABEL com.vfxplatform.version=$VFXPLATFORM_VERSION
LABEL org.opencontainers.image.name="$ASWF_ORG/rt-common"
LABEL org.opencontainers.image.description="Common image for runtime ASWF images"
LABEL org.opencontainers.image.url="http://aswf.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.version=$VFXPLATFORM_VERSION

ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:${LD_LIBRARY_PATH} \
    PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin \
    PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages:/usr/local/lib/python \
    VFXPLATFORM_VERSION=$VFXPLATFORM_VERSION \
    ASWF_VERSION=${ASWF_VERSION} \
    ASWF_ORG=${ASWF_ORG}

COPY --from=builder /usr/local /usr/local/

RUN yum install --setopt=tsflags=nodocs -y \
    alsa-lib \
    automake autoconf \
    bison \
    bzip2 \
    ca-certificates \
    csh \
    cups \
    dbus \
    doxygen \
    fam \
    file \
    fontconfig \
    freeglut \
    freetype \
    glx-utils \
    gstreamer1 \
    gstreamer1-plugins-bad-free \
    libgomp \
    libicu \
    libjpeg \
    libpng \
    libtiff \
    libv4l \
    libxcb \
    libXcomposite \
    libXcursor \
    libXi \
    libXinerama \
    libxkbcommon \
    libxkbcommon-x11 \
    libxml2 \
    libXmu \
    libXp \
    libXpm \
    libXrandr \
    libXrender \
    libXScrnSaver \
    libxslt \
    motif \
    ncurses \
    nss \
    patch \
    pkgconfig \
    pulseaudio-libs \
    readline \
    rsync \
    ruby \
    sudo \
    tcsh \
    texinfo \
    unzip \
    wget \
    which \
    xcb-util \
    xcb-util-image \
    xcb-util-keysyms \
    xcb-util-wm \
    xorg-x11-xkb-utils \
    xorg-x11-server-Xvfb && \
    rm -rf /var/cache/yum/*

RUN wget https://xpra.org/repos/CentOS/xpra.repo -P /etc/yum.repos.d/ && \
    yum install --setopt=tsflags=nodocs -y xpra python-paramiko python-inotify python2-uinput && \
    # Delete libGL installed by mesa... \
    rm -f /usr/lib64/libGL.so* /usr/lib64/libGLdispatch.so* /usr/lib64/libGLX_system.so* /usr/lib64/libGLX_mesa* /usr/lib64/libGLX.so* && \
    rm -rf /var/cache/yum/*

RUN wget https://sourceforge.net/projects/virtualgl/files/2.6.4/VirtualGL-2.6.4.x86_64.rpm/download -O /tmp/vgl.rpm && \
    yum install -y /tmp/vgl.rpm && \
    rm /tmp/vgl.rpm && \
    rm -rf /var/cache/yum/*

RUN yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum install -y dkms && \
    rm -rf /var/cache/yum/*

COPY rt-base/xpra-entry-point.sh /usr/local/bin/
COPY rt-base/xpra.conf /etc/xpra/

ENV NVIDIA_DRIVER_CAPABILITIES=${NVIDIA_DRIVER_CAPABILITIES},display

# xpra default port
EXPOSE 14500
