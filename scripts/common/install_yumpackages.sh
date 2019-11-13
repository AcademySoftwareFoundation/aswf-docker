#!/usr/bin/env bash

set -ex

yum install -y \
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
    glx-utils \
    gperf \
    java-1.8.0-openjdk \
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
    libxkbcommon libxkbcommon-devel \
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
    rsync \
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
    xorg-x11-xkb-utils xorg-x11-xkb-utils-devel \
    Xvfb Xvfb-devel \
    xz-devel \
    zlib-devel

# This is needed for Xvfb to function properly.
dbus-uuidgen > /etc/machine-id

yum -y groupinstall "Development Tools"

yum install -y --setopt=tsflags=nodocs centos-release-scl-rh yum-utils

yum-config-manager --setopt=centos-sclo-rh.baseurl=http://vault.centos.org/centos/7.6.1810/sclo/\$basearch/rh/ --save

yum install -y --setopt=tsflags=nodocs devtoolset-6-toolchain --nogpgcheck

yum install -y epel-release
yum install -y p7zip
