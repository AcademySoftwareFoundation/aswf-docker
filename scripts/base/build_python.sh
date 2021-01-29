#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir python
cd python

curl -C - --location "https://www.python.org/ftp/python/${ASWF_PYTHON_VERSION}/Python-${ASWF_PYTHON_VERSION}.tgz" -o "$DOWNLOADS_DIR/Python-${ASWF_PYTHON_VERSION}.tgz"


mkdir -p "${ASWF_INSTALL_PREFIX}/bin"
echo "PATH=$PATH"

# Create script to allow use of system python
cat <<EOF > "${ASWF_INSTALL_PREFIX}/bin/run-with-system-python"
#!/bin/sh
# Unsets all environment variables so that the system python can function normally
# To use, just prefix any command with run-with-system-python
unset PYTHONPATH
unset LIBRARY_PATH
unset PKG_CONFIG_PATH
export LD_LIBRARY_PATH=/opt/rh/devtoolset-${ASWF_DTS_VERSION}/root/usr/lib64:/opt/rh/devtoolset-${ASWF_DTS_VERSION}/root/usr/lib
export PATH=/opt/rh/devtoolset-${ASWF_DTS_VERSION}/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-${ASWF_DTS_VERSION}/root/usr/bin/:/usr/sbin:/usr/bin:/sbin:/bin
exec "\$@"
EOF
chmod a+x "${ASWF_INSTALL_PREFIX}/bin/run-with-system-python"

# Create a yum wrapper that uses the system python
cat <<EOF > "${ASWF_INSTALL_PREFIX}/bin/yum"
#!/bin/sh
# This runs yum with system python
exec "${ASWF_INSTALL_PREFIX}/bin/run-with-system-python" /usr/bin/yum "\$@"
EOF
chmod a+x "${ASWF_INSTALL_PREFIX}/bin/yum"

tar xf "$DOWNLOADS_DIR/Python-${ASWF_PYTHON_VERSION}.tgz"
cd "Python-${ASWF_PYTHON_VERSION}"

# Ensure configure, build and install is done with no reference to ${ASWF_INSTALL_PREFIX} as this somehow messes up the system install
run-with-system-python ./configure \
    --prefix="${ASWF_INSTALL_PREFIX}" \
    --enable-unicode=ucs4 \
    --enable-shared
run-with-system-python make -j$(nproc)

run-with-system-python make install

if [[ $ASWF_PYTHON_VERSION == 3* ]]; then
    # Create symlink from python3 to python
    ln -s python3 "${ASWF_INSTALL_PREFIX}/bin/python"
    export PIP=pip3
else
    export PIP=pip
fi

cd ../..
rm -rf python

if [[ $ASWF_PYTHON_VERSION == 3* ]]; then
    curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
else
    curl "https://bootstrap.pypa.io/2.7/get-pip.py" -o "get-pip.py"
fi
python get-pip.py
rm get-pip.py

$PIP install \
    nose \
    coverage \
    docutils \
    epydoc \
    "numpy==${ASWF_NUMPY_VERSION}"
