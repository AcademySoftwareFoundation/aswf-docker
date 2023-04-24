#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir pyside
cd pyside


# Workaround pyside issue with Qt headers within system location https://bugreports.qt.io/browse/PYSIDE-787
# Qt is temporarily moved to /tmp/qt5temp just to build pyside! So set up the
# environment so that it can be found (if it has NOT been moved, do nothing).
if [ -d /tmp/qt5temp ] ; then
    export PATH=/tmp/qt5temp/bin:$PATH
    export LD_LIBRARY_PATH=/tmp/qt5temp/lib:$LD_LIBRARY_PATH
    cat <<-EOF > /tmp/qt5temp/bin/qt.conf
		[Paths]
		Prefix = /tmp/qt5temp
	EOF
fi

if [[ $ASWF_PYSIDE_VERSION == 2.0.0 ]]; then
    curl --location "https://www.autodesk.com/content/dam/autodesk/www/Company/files/pyside2-maya2018.4.zip" -o "$DOWNLOADS_DIR/pyside-${ASWF_PYSIDE_VERSION}.zip"
    unzip "$DOWNLOADS_DIR/pyside-${ASWF_PYSIDE_VERSION}.zip"
    mv pyside-setup pyside
    cd pyside
    "${ASWF_INSTALL_PREFIX}/bin/python" setup.py build install --prefix "${ASWF_INSTALL_PREFIX}"
else
    # Naming scheme changed from "everywhere" to "opensource" with version 5.13.2
    PYSIDE_URL_SUFFIX=""
    if [[ $ASWF_PYSIDE_VERSION == 5.12.6 ]]; then
        PYSIDE_URL_NAME=pyside-setup-everywhere-src-${ASWF_PYSIDE_VERSION}
    else
       PYSIDE_URL_NAME=pyside-setup-opensource-src-${ASWF_PYSIDE_VERSION}
        if [[ $ASWF_PYSIDE_VERSION == 5.15.9 ]]; then
            # 5.15.9 added a -1 suffix to the distribution tarball
            PYSIDE_URL_SUFFIX="-1"
        fi
    fi
    if [ ! -f "$DOWNLOADS_DIR/pyside-${ASWF_PYSIDE_VERSION}.tar.xz" ]; then
        curl --location "https://download.qt.io/official_releases/QtForPython/pyside2/PySide2-${ASWF_PYSIDE_VERSION}-src/${PYSIDE_URL_NAME}${PYSIDE_URL_SUFFIX}.tar.xz" -o "$DOWNLOADS_DIR/pyside-${ASWF_PYSIDE_VERSION}.tar.xz"
    fi
    tar xf "$DOWNLOADS_DIR/pyside-${ASWF_PYSIDE_VERSION}.tar.xz"
    mv "${PYSIDE_URL_NAME}" pyside

    export LLVM_INSTALL_DIR=${ASWF_INSTALL_PREFIX}
    export CLANG_INSTALL_DIR=${ASWF_INSTALL_PREFIX}

    cd pyside

    if [[ $ASWF_PYSIDE_VERSION == 5.12.6 ]]; then
        # Apply typing patch
        curl --location "https://codereview.qt-project.org/changes/pyside%2Fpyside-setup~271412/revisions/4/patch?zip" -o "typing-patch.zip"
        unzip typing-patch.zip
        patch -p1 < 28958df.diff
    fi
    if [[ $ASWF_PYSIDE_VERSION == 5.12.6 ]]; then
        # Apply clang10 patch
        curl --location "https://codereview.qt-project.org/changes/pyside%2Fpyside-setup~296271/revisions/2/patch?zip" -o "clang10-patch.zip"
        unzip clang10-patch.zip
        patch -p1 < 9ae6382.diff
    fi
    if [[ $ASWF_PYSIDE_VERSION == 5.15.9 ]]; then
        # Fix for compiling against Numpy 1.23.x from
        # https://git.alpinelinux.org/aports/commit/?id=8936d82ae568ce7521427075be5599fcc3a409f0
        cat << EOF > shiboken_numpy_1_23.diff
--- a/sources/shiboken2/libshiboken/sbknumpyarrayconverter.cpp
+++ b/sources/shiboken2/libshiboken/sbknumpyarrayconverter.cpp
@@ -116,8 +116,8 @@ std::ostream &operator<<(std::ostream &str, PyArrayObject *o)
             str << " NPY_ARRAY_NOTSWAPPED";
         if ((flags & NPY_ARRAY_WRITEABLE) != 0)
             str << " NPY_ARRAY_WRITEABLE";
-        if ((flags & NPY_ARRAY_UPDATEIFCOPY) != 0)
-            str << " NPY_ARRAY_UPDATEIFCOPY";
+        if ((flags & NPY_ARRAY_WRITEBACKIFCOPY) != 0)
+            str << " NPY_ARRAY_WRITEBACKIFCOPY";
     } else {
         str << '0';
     }
EOF
        patch -p1 < shiboken_numpy_1_23.diff
    fi

    "${ASWF_INSTALL_PREFIX}/bin/python" setup.py install --parallel=$(nproc) --prefix "${ASWF_INSTALL_PREFIX}"

fi

cd ..
rm -rf pyside
