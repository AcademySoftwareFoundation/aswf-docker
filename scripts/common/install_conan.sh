#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex
mkdir python
cd python

curl -C - --location "https://www.python.org/ftp/python/${ASWF_CONAN_PYTHON_VERSION}/Python-${ASWF_CONAN_PYTHON_VERSION}.tgz" -o "$DOWNLOADS_DIR/Python-${ASWF_CONAN_PYTHON_VERSION}.tgz"

tar xf "$DOWNLOADS_DIR/Python-${ASWF_CONAN_PYTHON_VERSION}.tgz"
cd "Python-${ASWF_CONAN_PYTHON_VERSION}"

export LD_LIBRARY_PATH=/tmp/pyconan/lib:${LD_LIBRARY_PATH}
export PATH=/tmp/pyconan/bin:${PATH}

./configure \
    --prefix="/tmp/pyconan" \
    --enable-unicode=ucs4 \
    --enable-shared
make -j$(nproc)
make install

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python3 get-pip.py

pip3 install "conan==${ASWF_CONAN_VERSION}" pyinstaller

pyinstaller `which conan` --distpath /opt

cat <<EOF > "${ASWF_INSTALL_PREFIX}/bin/conan"
#!/bin/sh
exec "${ASWF_CONAN_ROOT}/conan" "\$@"
EOF
chmod a+x "${ASWF_INSTALL_PREFIX}/bin/conan"

cd ../..
rm -rf python
rm -rf /tmp/pyconan
