#!/usr/bin/env bash

set -ex

mkdir pyside
cd pyside


# Workaround pyside issue with Qt headers within system location https://bugreports.qt.io/browse/PYSIDE-787
# Qt is temporarily moved to /tmp/qt5temp just to build pyside!
export PATH=/tmp/qt5temp/bin:$PATH
export LD_LIBRARY_PATH=/tmp/qt5temp/lib:$LD_LIBRARY_PATH
cat <<EOF > /tmp/qt5temp/bin/qt.conf
[Paths]
Prefix = /tmp/qt5temp
EOF

if [[ $PYSIDE_VERSION == 2.0.0 ]]; then
    curl --location https://www.autodesk.com/content/dam/autodesk/www/Company/files/pyside2-maya2018.4.zip -o $DOWNLOADS_DIR/pyside-${PYSIDE_VERSION}.zip
    unzip $DOWNLOADS_DIR/pyside-${PYSIDE_VERSION}.zip
    mv pyside-setup pyside
    cd pyside
    ${ASWF_INSTALL_PREFIX}/bin/python setup.py build install --prefix ${ASWF_INSTALL_PREFIX}
else
    if [[ $PYSIDE_VERSION == 5.12.6 ]]; then
        PYSIDE_URL_NAME=pyside-setup-everywhere-src-${PYSIDE_VERSION}
    else
        PYSIDE_URL_NAME=pyside-setup-opensource-src-${PYSIDE_VERSION}
    fi
    if [ ! -f $DOWNLOADS_DIR/pyside-${PYSIDE_VERSION}.tar.xz ]; then
        curl --location https://download.qt.io/official_releases/QtForPython/pyside2/PySide2-${PYSIDE_VERSION}-src/${PYSIDE_URL_NAME}.tar.xz -o $DOWNLOADS_DIR/pyside-${PYSIDE_VERSION}.tar.xz
    fi
    tar xf $DOWNLOADS_DIR/pyside-${PYSIDE_VERSION}.tar.xz
    mv ${PYSIDE_URL_NAME} pyside

    export CLANG_INSTALL_DIR=${ASWF_INSTALL_PREFIX}
    
    cd pyside

    if [[ $PYSIDE_VERSION == 5.12.6 ]]; then
        # Apply typing patch
        curl --location https://codereview.qt-project.org/changes/pyside%2Fpyside-setup~271412/revisions/4/patch?zip -o typing-patch.zip
        unzip typing-patch.zip
        patch -p1 < 28958df.diff
    fi

    ${ASWF_INSTALL_PREFIX}/bin/python setup.py build --parallel=$(nproc)
    ${ASWF_INSTALL_PREFIX}/bin/python setup.py install --prefix ${ASWF_INSTALL_PREFIX}

fi

cd ..
rm -rf pyside
