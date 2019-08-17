ARG CUDA_VERSION=10.1
FROM nvidia/cudagl:${CUDA_VERSION}-devel-centos7

ARG ASWF_ORG=aswf
ARG BUILD_DATE=dev
ARG VCS_REF=dev
ARG CI_COMMON_VERSION=1.0

LABEL maintainer="aloys.baillet@gmail.com"

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="$ASWF_ORG/base-ci"
LABEL org.label-schema.description="Common CI Docker Image"
LABEL org.label-schema.url="http://aswf.io/"
LABEL org.label-schema.vcs-url="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="AcademySoftwareFoundation"
LABEL org.label-schema.version="1.0"
LABEL org.label-schema.docker.cmd="docker run -v `pwd`:/tmp/project -it $ASWF_ORG/common-ci bash"


USER root

RUN yum install -y \
    alsa-lib alsa-lib-devel \
    automake autoconf \
    bison \
    bzip2-devel \
    ca-certificates \
    csh \
    db4-devel \
    dbus dbus-devel \
    doxygen \
    expat-devel \
    fam \
    file \
    fontconfig fontconfig-devel \
    freetype freetype-devel \
    gdbm-devel \
    git \
    glut-devel \
    gperf \
    java-1.8.0-openjdk \
    libcap-devel \
    libcap-devel \
    libffi-devel \
    libjpeg libjpeg-devel \
    libpcap-devel \
    libpng libpng-devel \
    libtiff libtiff-devel \
    libv4l libv4l-devel \
    libxcb libxcb-devel \
    libXcomposite libXcomposite-devel \
    libXcursor libXcursor-devel \
    libXi libXi-devel \
    libXinerama libXinerama-devel \
    libxml2 libxml2-devel \
    libXmu libXmu-devel \
    libXp libXp-devel \
    libXpm libXpm-devel \
    libXrandr libXrandr-devel \
    libXrender libXrender-devel \
    libXScrnSaver libXScrnSaver-devel \
    libxslt libxslt-devel \
    libXtst-devel \
    make \
    mesa-libEGL-devel \
    mesa-libGL-devel \
    ncurses ncurses-devel \
    nss nss-devel \
    openssl-devel \
    patch \
    pciutils-devel \
    pkgconfig \
    pulseaudio-libs pulseaudio-libs-devel \
    pulseaudio-libs-devel \
    readline readline-devel \
    ruby \
    sqlite-devel \
    sudo \
    tcsh \
    tk-devel \
    unzip \
    wget \
    which \
    xcb-util xcb-util-devel \
    xcb-util-image xcb-util-image-devel \
    xcb-util-keysyms xcb-util-keysyms-devel \
    xcb-util-wm xcb-util-wm-devel \
    xz-devel \
    zlib-devel \
    && \
    yum -y groupinstall "Development Tools" && \
    yum install -y --setopt=tsflags=nodocs centos-release-scl-rh && \
    yum install -y --setopt=tsflags=nodocs devtoolset-6-toolchain && \
    yum clean all -y &&\
    rm -rf /var/cache/yum/*

RUN mkdir /opt/aswf
WORKDIR /opt/aswf

ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:/opt/rh/devtoolset-6/root/usr/lib64:/opt/rh/devtoolset-6/root/usr/lib:${LD_LIBRARY_PATH} \
    PATH=/usr/local/bin:/opt/rh/devtoolset-6/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-6/root/usr/bin/:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin \
    CI_COMMON_VERSION=${CI_COMMON_VERSION}

COPY scripts/common/*.sh \
     /tmp/

RUN source /tmp/versions_common.sh && \
    /tmp/install_ninja.sh && \
    /tmp/install_sonar.sh && \
    /tmp/install_clang.sh
