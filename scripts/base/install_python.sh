#!/usr/bin/env bash

set -ex

# Create script to allow use of system python
cat <<EOF > /usr/local/bin/run-with-system-python
#!/bin/sh
# Unsets all environment variables so that the system python can function normally
# To use, just prefix any command with run-with-system-python
unset PYTHONPATH
unset LIBRARY_PATH
unset PKG_CONFIG_PATH
export LD_LIBRARY_PATH=/opt/rh/devtoolset-6/root/usr/lib64:/opt/rh/devtoolset-6/root/usr/lib
export PATH=/opt/rh/devtoolset-6/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-6/root/usr/bin/:/usr/sbin:/usr/bin:/sbin:/bin
exec "\$@"
EOF
chmod a+x /usr/local/bin/run-with-system-python

# Create a yum wrapper that uses the system python
cat <<EOF > /usr/local/bin/yum
#!/bin/sh
# This runs yum with system python
exec /usr/local/bin/run-with-system-python /usr/bin/yum "\$@"
EOF
chmod a+x /usr/local/bin/yum

curl --location https://www.python.org/ftp/python/${PYTHON_VERSION_FULL}/Python-${PYTHON_VERSION_FULL}.tgz -o Python.tgz
tar xf Python.tgz && rm Python.tgz
cd Python-${PYTHON_VERSION_FULL}

# Ensure configure, build and install is done with no reference to /usr/local as this somehow messes up the system install
run-with-system-python ./configure \
    --prefix=/usr/local \
    --enable-unicode=ucs4 \
    --enable-shared
run-with-system-python make -j4

run-with-system-python make altinstall

if [[ $PYTHON_VERSION == 3* ]]; then
    # Create symlink from python3 to python
    sudo ln -s /usr/local/bin/python3 /usr/local/bin/python
fi

cd ..
rm -rf Python-${PYTHON_VERSION_FULL}

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" &&\
    python get-pip.py
rm get-pip.py

pip install \
    nose \
    epydoc \
    coverage
