#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# The nvidia/cudagl images are no longer maintained, only the nvidia/cuda images are,
# this script is based on https://gitlab.com/nvidia/container-images/cuda/-/blob/master/build.sh
# to layer OpenGL, libglvnd and the GL development headers on top of the nvidia/cuda base container.
#
# We skip the 32 bit libraries since we only support a 64 bit build environment, this avoids ending up
# with 32 bit libraries in /usr/local/lib
# All prerequisites have already been installed by install_yumpackages.sh

set -ex

# Don't need to do this on centos7, cudagl container still available
if [ ${ASWF_BASEOS_DISTRO} == "centos7" ]; then
    exit 0
fi

mkdir /tmp/libglvnd
cd /tmp/libglvnd
git clone --branch="v${ASWF_GLVND_VERSION}" https://github.com/NVIDIA/libglvnd.git .
./autogen.sh
./configure --prefix=/usr/local --libdir=/usr/local/lib
make -j"$(nproc)" install-strip
find /usr/local/lib -type f -name 'lib*.la' -delete
cd /tmp
rm -rf libglvnd

# Setup runtime environment
mkdir -p /usr/local/share/glvnd/egl_vendor.d
cat << EOF > /usr/local/share/glvnd/egl_vendor.d/10_nvidia.json
{
    "file_format_version" : "1.0.0",
    "ICD" : {
        "library_path" : "libEGL_nvidia.so.0"
    }
}
EOF
echo '/usr/local/lib' >> /etc/ld.so.conf.d/glvnd.conf
ldconfig
echo '/usr/local/lib/libGL.so.1' >> /etc/ld.so.preload
echo '/usr/local/lib/libEGL.so.1' >> /etc/ld.so.preload

# Setup development environment
mkdir /tmp/gldev
cd /tmp/gldev
git clone https://github.com/KhronosGroup/OpenGL-Registry.git
cd /tmp/gldev/OpenGL-Registry
git checkout 681c365c012ac9d3bcadd67de10af4730eb460e0
cp -r api/GL /usr/local/include
cd /tmp/gldev
git clone https://github.com/KhronosGroup/EGL-Registry.git
cd /tmp/gldev/EGL-Registry
git checkout 0fa0d37da846998aa838ed2b784a340c28dadff3
cp -r api/EGL api/KHR /usr/local/include
cd /tmp/gldev
git clone --branch=mesa-17.3.3 --depth=1 https://gitlab.freedesktop.org/mesa/mesa.git
cd /tmp/gldev/mesa
mkdir -p /usr/local/include/GL
cp include/GL/gl.h include/GL/gl_mangle.h /usr/local/include/GL/
rm -rf /tmp/gldev

# install pkg-config definitions for EGL and EGL libs
mkdir -p /usr/local/lib/pkgconfig
cat << EOF > /usr/local/lib/pkgconfig/egl.pc
prefix=/usr/local
exec_prefix=${prefix}
libdir=${prefix}/lib
includedir=${prefix}/include

Name: egl
Description: glvnd EGL library
Requires.private:  x11 xcb xau xdmcp
Version: 1.0.0
Libs: -L${libdir} -lEGL
Libs.private: -lpthread -ldl
Cflags: -I${includedir}
EOF
cat << EOF > /usr/local/lib/pkgconfig/gl.pc
prefix=/usr/local
exec_prefix=${prefix}
libdir=${prefix}/lib
includedir=${prefix}/include

Name: gl
Description: glvnd OpenGL library
Requires.private:  x11 xcb xau xdmcp
Version: 1.0.0
Libs: -L${libdir} -lGL
Libs.private: -lpthread -ldl
Cflags: -I${includedir}
EOF

# Don't forget to set:
#
# ENV NVIDIA_VISIBLE_DEVICES \
#        ${NVIDIA_VISIBLE_DEVICES:-all}
# ENV NVIDIA_DRIVER_CAPABILITIES \
#        ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics
# ENV PKG_CONFIG_PATH /usr/local/lib/pkgconfig
#
# in the Dockerfile after this script is called.

