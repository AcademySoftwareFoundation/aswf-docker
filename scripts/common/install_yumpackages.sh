#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

yum install --setopt=tsflags=nodocs -y \
    alsa-lib alsa-lib-devel \
    automake autoconf \
    bison \
    bzip2-devel \
    ca-certificates \
    csh \
    cups cups-devel \
    dbus dbus-devel \
    doxygen \
    expat-devel \
    fam \
    file \
    flex \
    fontconfig fontconfig-devel \
    freeglut freeglut-devel \
    freetype freetype-devel \
    frei0r-devel \
    gdbm-devel \
    giflib-devel \
    git \
    glib2-devel \
    glut-devel \
    glx-utils \
    gperf \
    gstreamer1 gstreamer1-devel \
    gstreamer1-plugins-bad-free gstreamer1-plugins-bad-free-devel \
    gtk2-devel \
    harfbuzz-devel \
    java-1.8.0-openjdk \
    libbluray-devel \
    libcap-devel \
    libcdio-paranoia-devel \
    libcurl-devel \
    libffi-devel \
    libgcrypt-devel \
    libgudev1-devel \
    libicu-devel \
    libjpeg libjpeg-devel \
    libmng-devel \
    libpcap-devel \
    libpng libpng-devel \
    LibRaw-devel \
    libtheora-devel \
    libtiff libtiff-devel \
    libv4l libv4l-devel \
    libvdpau-devel \
    libvorbis-devel \
    libvpx-devel \
    libwebp-devel \
    libxcb libxcb-devel \
    libXcomposite libXcomposite-devel \
    libXcursor libXcursor-devel \
    libXi libXi-devel \
    libXinerama libXinerama-devel \
    libxkbcommon libxkbcommon-devel \
    libxkbcommon-x11-devel \
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
    mesa-libGLU-devel \
    motif motif-devel \
    ncurses ncurses-devel \
    nss nss-devel \
    openjpeg-devel \
    openjpeg2-devel \
    openssl-devel \
    opus-devel \
    patch \
    pciutils-devel \
    pkgconfig \
    procps-ng-devel \
    pulseaudio-libs pulseaudio-libs-devel \
    readline readline-devel \
    rsync \
    ruby \
    speex-devel \
    sqlite-devel \
    sudo \
    systemd-devel \
    tcsh \
    texinfo \
    tk-devel \
    unzip \
    wget \
    which \
    xcb-util xcb-util-devel \
    xcb-util-image xcb-util-image-devel \
    xcb-util-keysyms xcb-util-keysyms-devel \
    xcb-util-wm xcb-util-wm-devel \
    xkeyboard-config-devel \
    xorg-x11-xkb-utils xorg-x11-xkb-utils-devel \
    xorg-x11-server-Xvfb \
    xz-devel \
    zlib-devel                                                                                        

# This is needed for Xvfb to function properly.
dbus-uuidgen > /etc/machine-id

yum -y groupinstall "Development Tools"

yum install -y --setopt=tsflags=nodocs centos-release-scl-rh yum-utils

if [[ $DTS_VERSION == 6 ]]; then
    sed -i 's/7/7.6.1810/g; s|^#\s*\(baseurl=http://\)mirror|\1vault|g; /mirrorlist/d' /etc/yum.repos.d/CentOS-SCLo-*.repo
    yum install -y --setopt=tsflags=nodocs devtoolset-6-toolchain --nogpgcheck
else
    yum install -y --setopt=tsflags=nodocs devtoolset-$DTS_VERSION-toolchain --nogpgcheck
fi

yum install -y epel-release

# Additional package that are not found initially
yum install -y \
    lame-devel \
    libcaca-devel \
    libdb4-devel \
    libdc1394-devel \
    p7zip \
    yasm-devel \
    zvbi-devel
