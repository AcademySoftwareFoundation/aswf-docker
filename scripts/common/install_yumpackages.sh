#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex


GAMIN_RPM="gamin"
MESA_VULKAN_DEVEL_RPM="mesa-vulkan-devel"
XORG_X11_XKB_UTILS_RPM="xorg-x11-xkb-utils xorg-x11-xkb-utils-devel"
LIBXVMC_DEVEL_RPM="libXvMC-devel"

BASEOS_MAJORVERSION=$(sed -n  's/^.* release \([0-9]*\)\..*$/\1/p' /etc/redhat-release)
if [ "$BASEOS_MAJORVERSION" -gt "7" ]; then
    dnf -y install 'dnf-command(config-manager)'
    if [ "$BASEOS_MAJORVERSION" -eq "8" ]; then
        # Rocky 8 needs PowerTools and Devel repos enabled for some of these packages
        dnf config-manager --set-enabled powertools
        # The Rocky 8 mirror repos seem to be getting increasingly unreliable, prefer going to the source
        sed -i -e 's/^mirrorlist=/#mirrorlist=/g' -e 's/#baseurl=/baseurl=/g' /etc/yum.repos.d/Rocky-{BaseOS,AppStream,Extras,PowerTools}.repo
        # libbluray-devel is in EPEL 9, we may no longer need devel repo then
        # same for yasm-devel and libdc1394-devel
        # But the devel repo in Rocky 8 warns that "WARNING! FOR BUILDROOT AND KOJI USE"
        # And as of late August 2025 it is causing conflicts with BaseOS / AppStream.
        # So we will only enable it for specific installs.
        # dnf config-manager --set-enabled devel

        # Rocky 8 base image doesn't have a system Python (3), install and make default
        dnf -y install python3
        alternatives --set python /usr/bin/python3
    else
        # Rocky 9 needs CRB repo enabled for some of these packages
        dnf config-manager --set-enabled crb
        # Some packages are gone or renamed in EL 9
        GAMIN_RPM=""
        MESA_VULKAN_DEVEL_RPM="mesa-vulkan-drivers"
        # In Rocky 9 xkbcomp-devel is in the devel repo which we don't want, all it provides is a single
        # pkgconfig file we don't need.
        XORG_X11_XKB_UTILS_RPM="setxkbmap xkbcomp"
        LIBXVMC_DEVEL_RPM=""
    fi
    # Ignore any DNF metadata cached in base image
    dnf clean all
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
    dbus-tools \
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
    ${GAMIN_RPM} \
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
    jq \
    libaio-devel \
    libcap-devel \
    libcdio-paranoia-devel \
    libcurl-devel \
    libdrm \
    libffi-devel \
    libfontenc-devel \
    libgcrypt-devel \
    libgudev1-devel \
    libicu-devel \
    libinput-devel \
    libjpeg \
    libjpeg-devel \
    libmng-devel \
    libpcap-devel \
    libpng \
    libpng-devel \
    libsndfile-devel \
    libtheora-devel \
    libtiff \
    libtiff-devel \
    libuuid-devel \
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
    libxslt-devel \
    libXtst-devel \
    libXv-devel \
    ${LIBXVMC_DEVEL_RPM} \
    libXxf86vm-devel \
    lz4-devel \
    make \
    meson \
    mesa-libEGL-devel \
    mesa-libGL-devel \
    mesa-libGLU-devel \
    mesa-libGLw-devel \
    mesa-libOSMesa-devel \
    ${MESA_VULKAN_DEVEL_RPM} \
    mpdecimal-devel \
    mpg123-devel \
    motif \
    motif-devel \
    nasm \
    ncurses \
    ncurses-devel \
    nss \
    nss-devel \
    openal-soft \
    openal-soft-devel \
    openjpeg2-devel \
    openssl-devel \
    opus-devel \
    PackageKit-gstreamer-plugin \
    patch \
    pciutils-devel \
    pkgconfig \
    procps-ng-devel \
    pulseaudio-libs \
    pulseaudio-libs-glib2 \
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
    xorg-x11-proto-devel \
    xorg-x11-server-Xvfb \
    xorg-x11-util-macros \
    ${XORG_X11_XKB_UTILS_RPM} \
    xorg-x11-xtrans-devel \
    xz-devel \
    zlib-devel

# This is needed for Xvfb to function properly.
dbus-uuidgen > /etc/machine-id

yum -y groupinstall "Development Tools"

if [ "$BASEOS_MAJORVERSION" -gt "7" ]; then
    dnf -y install gcc-toolset-$ASWF_DTS_VERSION gcc-toolset-$ASWF_DTS_VERSION-libatomic-devel
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

# Additional packages, some moved to EPEL 9
yum install -y \
    alsa-lib \
    alsa-lib-devel \
    audiofile-devel \
    frei0r-devel \
    lame-devel \
    libaom-devel \
    libcaca-devel \
    libdeflate-devel \
    libdrm-devel \
    libdrm \
    libsquish-devel \
    libxshmfence \
    libxshmfence-devel \
    nss-devel \
    ocl-icd-devel \
    opencl-headers \
    patchelf \
    p7zip \
    portaudio \
    portaudio-devel \
    spdlog-devel \
    svt-av1-devel \
    xcb-util-cursor \
    xcb-util-cursor-devel \
    zvbi-devel

if [ "$BASEOS_MAJORVERSION" -eq "8" ]; then
    # For Rocky 8 these exist in the mostly off limits devel repo. In Rocky 9 they are in EPEL.
    dnf config-manager --set-enabled devel
fi

yum install -y \
    libbluray-devel \
    libdc1394-devel \
    yasm-devel

if [ "$BASEOS_MAJORVERSION" -eq "8" ]; then
    dnf config-manager --set-disabled devel
fi

if [ "$BASEOS_MAJORVERSION" -gt "7" ]; then
    # Rocky 8 has git 2.31 and OpenSSL 1.1.1k by default
    # Recent Qt 5.15.x wants wayland-devel
    # Qt 6 wants python3-html5lib, python3-importlib-metadata, nodejs, brotli,
    # double-conversion, perl-IPC-Cmd, perl-Digest-SHA, python 3.9
    # An unknown dependency is pulling Python 3.11.5, might as well
    # have the devel package as well

    # On EL 9 Python 3.9 is the default and perl-FindBin is no longer in
    # the perl-interpreter package, but instead in its own.
    if [ "$BASEOS_MAJORVERSION" -eq "8" ]; then
        PYTHON39_RPM="python39 python39-devel"
    else
        PERL_FIND_BIN_RPM="perl-FindBin"
    fi

    dnf -y install \
        git \
        wayland-devel \
        wayland-protocols-devel \
        python3-importlib-metadata \
        brotli brotli-devel \
        double-conversion double-conversion-devel \
        ${PERL_FIND_BIN_RPM} \
        perl-IPC-Cmd \
        perl-Digest-SHA \
        perl-open \
        ${PYTHON39_RPM} \
        python3.11 \
        python3.11-devel \
        python3.11-setuptools
    dnf -y module install nodejs:18

    # Make Python 3.11 the default Python. Can't change default system python on EL 9.
    if [ "$BASEOS_MAJORVERSION" -eq "8" ]; then
        alternatives --set python /usr/bin/python3
        alternatives --set python3 /usr/bin/python3.11
    fi
else
    yum install -y \
        libdb4-devel \
        openjpeg-devel \
        openssl11-devel \
        rh-git218
fi

yum clean all
