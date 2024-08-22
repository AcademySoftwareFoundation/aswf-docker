#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

# Rocky 8 needs PowerTools and Devel repos enabled for some of these packages

BASEOS_MAJORVERSION=$(sed -n  's/^.* release \([0-9]*\)\..*$/\1/p' /etc/redhat-release)
if [ "$BASEOS_MAJORVERSION" -gt "7" ]; then
    dnf -y install 'dnf-command(config-manager)'
    dnf config-manager --set-enabled powertools
    # libbluray-devel is in EPEL 9, we may no longer need devel repo then
    dnf config-manager --set-enabled devel
    # Rocky 8 base image doesn't have a system Python (3), install and make default
    dnf -y install python3
    alternatives --set python /usr/bin/python3
fi

yum install --setopt=tsflags=nodocs -y \
    alsa-lib \
    alsa-lib-devel \
    alsa-plugins-pulseaudio \
    alsa-utils \
    at-spi2-core-devel \
    autoconf \
    automake \
    bison \
    bzip2-devel \
    ca-certificates \
    csh \
    cups \
    cups-devel \
    dbus \
    dbus-devel \
    doxygen \
    expat-devel \
    file \
    flex \
    flite-devel \
    fontconfig \
    fontconfig-devel \
    freeglut \
    freeglut-devel \
    freetype \
    freetype-devel \
    frei0r-devel \
    gamin \
    gdbm-devel \
    giflib-devel \
    glib2-devel \
    glut-devel \
    glx-utils \
    gperf \
    gstreamer1 \
    gstreamer1-devel \
    gstreamer1-plugins-bad-free \
    gstreamer1-plugins-bad-free-devel \
    gstreamer1-plugins-base-devel \
    gstreamer1-plugins-good \
    gtk2-devel \
    harfbuzz-devel \
    java-1.8.0-openjdk \
    libbluray-devel \
    libcap-devel \
    libcdio-paranoia-devel \
    libcurl-devel \
    libdrm \
    libffi-devel \
    libfontenc-devel \
    libgcrypt-devel \
    libgudev1-devel \
    libicu-devel \
    libjpeg \
    libjpeg-devel \
    libmng-devel \
    libpcap-devel \
    libpng \
    libpng-devel \
    LibRaw-devel \
    libtheora-devel \
    libtiff \
    libtiff-devel \
    libv4l \
    libv4l-devel \
    libvdpau-devel \
    libvorbis-devel \
    libvpx-devel \
    libwebp-devel \
    libX11-devel \
    libXaw-devel \
    libxcb \
    libxcb-devel \
    libXcomposite \
    libXcomposite-devel \
    libXcursor \
    libXcursor-devel \
    libXdamage-devel \
    libXdmcp-devel \
    libXext-devel \
    libXfixes-devel \
    libXft-devel \
    libXi \
    libXi-devel \
    libXinerama \
    libXinerama-devel \
    libxkbcommon \
    libxkbcommon-devel \
    libxkbcommon-x11-devel \
    libxkbfile-devel \
    libxml2 \
    libxml2-devel \
    libXmu \
    libXmu-devel \
    libXp \
    libXp-devel \
    libXpm \
    libXpm-devel \
    libXrandr \
    libXrandr-devel \
    libXrender \
    libXrender-devel \
    libXres-devel \
    libXScrnSaver \
    libXScrnSaver-devel \
    libxshmfence-devel \
    libxslt \
    libxslt-devel \
    libXtst-devel \
    libXv-devel \
    libXvMC-devel \
    libXxf86vm-devel \
    lz4-devel \
    make \
    mesa-libEGL-devel \
    mesa-libGL-devel \
    mesa-libGLU-devel \
    mesa-libGLw-devel \
    motif \
    motif-devel \
    ncurses \
    ncurses-devel \
    nss \
    nss-devel \
    openjpeg2-devel \
    openssl-devel \
    opus-devel \
    PackageKit-gstreamer-plugin \
    patch \
    pciutils-devel \
    pkgconfig \
    procps-ng-devel \
    pulseaudio-libs \
    pulseaudio-libs-devel \
    readline \
    readline-devel \
    rsync \
    ruby \
    snappy-devel \
    speech-dispatcher-devel \
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
    xcb-util \
    xcb-util-devel \
    xcb-util-image \
    xcb-util-image-devel \
    xcb-util-keysyms \
    xcb-util-keysyms-devel \
    xcb-util-renderutil \
    xcb-util-renderutil-devel \
    xcb-util-wm \
    xcb-util-wm-devel \
    xkeyboard-config-devel \
    xorg-x11-server-Xvfb \
    xorg-x11-xkb-utils \
    xorg-x11-xkb-utils-devel \
    xorg-x11-xtrans-devel \
    xz-devel \
    zlib-devel \

# This is needed for Xvfb to function properly.
dbus-uuidgen > /etc/machine-id

yum -y groupinstall "Development Tools"

if [ "$BASEOS_MAJORVERSION" -gt "7" ]; then
    dnf -y install gcc-toolset-$ASWF_DTS_VERSION
else
    yum install -y --setopt=tsflags=nodocs centos-release-scl-rh

    if [[ $ASWF_DTS_VERSION == 6 ]]; then
        # Use the centos vault as the original devtoolset-6 is not part of CentOS-7 anymore
        sed -i 's/7/7.6.1810/g; s|^#\s*\(baseurl=http://\)mirror|\1vault|g; /mirrorlist/d' /etc/yum.repos.d/CentOS-SCLo-*.repo
    fi

    # Workaround for occasional error: "Not using downloaded centos-sclo-rh/repomd.xml because it is older than what we have"
    yum clean all

    yum install -y --setopt=tsflags=nodocs \
        "devtoolset-$ASWF_DTS_VERSION-toolchain"
fi

yum install -y epel-release

# Additional packages that are not found initially
yum install -y \
    audiofile-devel \
    lame-devel \
    libcaca-devel \
    libdc1394-devel \
    libdeflate-devel \
    opencl-headers \
    patchelf \
    p7zip \
    xcb-util-cursor \
    xcb-util-cursor-devel \
    yasm-devel \
    zvbi-devel

if [ "$BASEOS_MAJORVERSION" -gt "7" ]; then
    # Rocky 8 has git 2.31 and OpenSSL 1.1.1k by default
    # Recent Qt 5.15.x wants wayland-devel
    # Qt 6 wants python3-html5lib, python3-importlib-metadata, nodejs, brotli,
    # double-conversion, perl-IPC-Cmd, perl-Digest-SHA, python 3.9
    # An unknown dependency is pulling Python 3.11.5, might as well
    # have the devel package as well
    dnf -y install \
        git \
        wayland-devel \
        python3-importlib-metadata \
        brotli brotli-devel \
        double-conversion double-conversion-devel \
        perl-IPC-Cmd \
        perl-Digest-SHA \
        python39 \
        python39-devel \
        python3.11 \
        python3.11-devel \
        python3.11-setuptools
    dnf -y module install nodejs:18
    # If we really wanted libdb4 / libdb4-devel
    # dnf -y install
    #    https://pkgs.dyn.su/el8/base/x86_64/libdb4-4.8.30-30.el8.x86_64.rpm
    #    https://pkgs.dyn.su/el8/base/x86_64/libdb4-devel-4.8.30-30.el8.x86_64.rpm
    # If we really wanted openjpeg / openjpeg-libs / openjpeg-devel
    # dnf -y install
    #    https://pkgs.dyn.su/el8/base/x86_64/openjpeg-1.5.2-1.el8.x86_64.rpm
    #    https://pkgs.dyn.su/el8/base/x86_64/openjpeg-libs-1.5.2-1.el8.x86_64.rpm
    #    https://pkgs.dyn.su/el8/base/x86_64/openjpeg-devel-1.5.2-1.el8.x86_64.rpm

    # Make Python 3.11 the default Python
    alternatives --set python /usr/bin/python3
    alternatives --set python3 /usr/bin/python3.11
else
    yum install -y \
        libdb4-devel \
        openjpeg-devel \
        openssl11-devel \
        rh-git218
fi

yum clean all
