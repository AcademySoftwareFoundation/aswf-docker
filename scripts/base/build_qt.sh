#!/usr/bin/env bash

set -ex

mkdir qt
cd qt

ccache --max-size=10G
#ccache --clear

if [[ $QT_VERSION == 5.6.1 ]]; then
    if [ ! -f $DOWNLOADS_DIR/qt-${QT_VERSION}.zip ]; then
        curl --location https://www.autodesk.com/content/dam/autodesk/www/Company/files/2019/qt561formaya2019.zip -o $DOWNLOADS_DIR/qt-${QT_VERSION}.zip
    fi
    unzip $DOWNLOADS_DIR/qt-${QT_VERSION}.zip
    mv qt-adsk-5.6.1-vfx qt-src
    cd qt-src
    tar xf ../qt561-webkit.tgz
else
    QT_MAJOR_MINOR=$(echo "${QT_VERSION}" | cut -d. -f-2)
    if [ ! -f $DOWNLOADS_DIR/qt-${QT_VERSION}.tar.xz ]; then
        curl --location http://download.qt.io/official_releases/qt/${QT_MAJOR_MINOR}/${QT_VERSION}/single/qt-everywhere-src-${QT_VERSION}.tar.xz -o $DOWNLOADS_DIR/qt-${QT_VERSION}.tar.xz
    fi
    tar xf $DOWNLOADS_DIR/qt-${QT_VERSION}.tar.xz
    mv qt-everywhere-src-${QT_VERSION} qt-src
    cd qt-src
fi

./configure \
    --prefix=${ASWF_INSTALL_PREFIX} \
        -no-strip \
        -no-rpath \
        -opensource \
        -plugin-sql-sqlite \
        -openssl \
        -verbose \
        -opengl desktop \
        -qt-xcb \
        -no-warnings-are-errors \
        -no-libudev \
        -no-egl \
        -nomake examples \
        -nomake tests \
        -c++std c++14 \
        -confirm-license
make -j64

sudo make install

cd ../..
rm -rf qt
