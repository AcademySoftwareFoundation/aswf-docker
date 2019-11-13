#!/usr/bin/env bash

set -ex

mkdir pyside
cd pyside

if [[ $PYSIDE_VERSION == 2.0.0 ]]; then
    curl --location https://www.autodesk.com/content/dam/autodesk/www/Company/files/pyside2-maya2018.4.zip -o $DOWNLOADS_DIR/pyside-${PYSIDE_VERSION}.zip
    unzip $DOWNLOADS_DIR/pyside-${PYSIDE_VERSION}.zip
    mv pyside-setup pyside
    cd pyside
    ${ASWF_INSTALL_PREFIX}/bin/python setup.py build install --prefix ${ASWF_INSTALL_PREFIX}
else
    if [ ! -f $DOWNLOADS_DIR/pyside-${PYSIDE_VERSION}.tar.xz ]; then
        curl --location https://download.qt.io/official_releases/QtForPython/pyside2/PySide2-${PYSIDE_VERSION}-src/pyside-setup-everywhere-src-${PYSIDE_VERSION}.tar.xz -o $DOWNLOADS_DIR/pyside-${PYSIDE_VERSION}.tar.xz
    fi
    tar xf $DOWNLOADS_DIR/pyside-${PYSIDE_VERSION}.tar.xz
    mv pyside-setup-everywhere-src-${PYSIDE_VERSION} pyside

    export CLANG_INSTALL_DIR=${ASWF_INSTALL_PREFIX}
    
    cd pyside
    ${ASWF_INSTALL_PREFIX}/bin/python setup.py build --parallel=64
    ${ASWF_INSTALL_PREFIX}/bin/python setup.py install --prefix ${ASWF_INSTALL_PREFIX}

fi

cd ..
rm -rf pyside
