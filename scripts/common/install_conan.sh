#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex
mkdir python
cd python

curl --location "https://www.python.org/ftp/python/${ASWF_CONAN_PYTHON_VERSION}/Python-${ASWF_CONAN_PYTHON_VERSION}.tgz" | tar xfz -

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

# Trying to run pyinstaller on an installer version of Conan does not work well
# Instead we run pyinstaller directly on the source
pip3 install pyinstaller

cd ..
curl --location https://github.com/conan-io/conan/archive/refs/tags/${ASWF_CONAN_VERSION}.tar.gz | tar xfz -
cd conan-${ASWF_CONAN_VERSION}
pip3 install -r conans/requirements.txt
python3 pyinstaller.py
cp -r pyinstaller/dist/conan /opt

cat <<EOF > "${ASWF_INSTALL_PREFIX}/bin/conan"
#!/bin/sh
exec "${ASWF_CONAN_ROOT}/conan" "\$@"
EOF
chmod a+x "${ASWF_INSTALL_PREFIX}/bin/conan"

cd ../..
rm -rf python
rm -rf /tmp/pyconan
