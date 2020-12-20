#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir qt
cd qt

ccache --max-size=10G
#ccache --clear

if [[ $ASWF_QT_VERSION == 5.6.1 ]]; then
    if [ ! -f "$DOWNLOADS_DIR/qt-${ASWF_QT_VERSION}.zip" ]; then
        curl --location "https://www.autodesk.com/content/dam/autodesk/www/Company/files/2019/qt561formaya2019.zip" -o "$DOWNLOADS_DIR/qt-${ASWF_QT_VERSION}.zip"
    fi
    unzip "$DOWNLOADS_DIR/qt-${ASWF_QT_VERSION}.zip"
    mv qt-adsk-5.6.1-vfx qt-src
    cd qt-src
    tar xf ../qt561-webkit.tgz
else
    QT_MAJOR_MINOR=$(echo "${ASWF_QT_VERSION}" | cut -d. -f-2)
    if [ ! -f "$DOWNLOADS_DIR/qt-${ASWF_QT_VERSION}.tar.xz" ]; then
        curl --location "http://download.qt.io/official_releases/qt/${QT_MAJOR_MINOR}/${ASWF_QT_VERSION}/single/qt-everywhere-src-${ASWF_QT_VERSION}.tar.xz" -o "$DOWNLOADS_DIR/qt-${ASWF_QT_VERSION}.tar.xz"
    fi
    tar xf "$DOWNLOADS_DIR/qt-${ASWF_QT_VERSION}.tar.xz"
    mv "qt-everywhere-src-${ASWF_QT_VERSION}" qt-src
    cd qt-src
    
fi

./configure \
    --prefix="${ASWF_INSTALL_PREFIX}" \
        -no-strip \
        -no-rpath \
        -opensource \
        -plugin-sql-sqlite \
        -verbose \
        -opengl desktop \
        -xcb \
        -no-warnings-are-errors \
        -no-libudev \
        -no-egl \
        -nomake examples \
        -nomake tests \
        -c++std c++14 \
        -confirm-license \
        -no-use-gold-linker \
        -release \
        -no-sql-mysql \
        -qt-libjpeg \
        -qt-libpng \
        -bundled-xcb-xinput \
        -sysconfdir /etc/xdg \
        -qt-pcre \
        -qt-harfbuzz \
        -R . \
        -icu \
        -skip qtnetworkauth \
        -skip qtpurchasing

make -j$(nproc)

sudo make install

cd ../..
rm -rf qt
