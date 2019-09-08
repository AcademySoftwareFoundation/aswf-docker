#!/usr/bin/env bash

set -ex

curl --location https://www.python.org/ftp/python/${PYTHON_VERSION_FULL}/Python-${PYTHON_VERSION_FULL}.tgz -o Python.tgz
tar xf Python.tgz && rm Python.tgz
cd Python-${PYTHON_VERSION_FULL}

PYTHONPATH_ORG=${PYTHONPATH}
LIBRARY_PATH_ORG=${LIBRARY_PATH}
PKG_CONFIG_PATH_ORG=${PKG_CONFIG_PATH}
PATH_ORG=${PATH}
LD_LIBRARY_PATH_ORG=${LD_LIBRARY_PATH}

# Restore environment to default to ensure python installs correctly
unset PYTHONPATH
unset LIBRARY_PATH
unset PKG_CONFIG_PATH
export PATH=/opt/rh/devtoolset-6/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-6/root/usr/bin/:/usr/sbin:/usr/bin:/sbin:/bin
export LD_LIBRARY_PATH=/opt/rh/devtoolset-6/root/usr/lib64:/opt/rh/devtoolset-6/root/usr/lib

./configure \
    --prefix=/usr/local \
    --enable-unicode=ucs4 \
    --enable-shared
make -j4

sudo make altinstall

if [[ $PYTHON_VERSION == 3* ]]; then
    # Create symlink from python3 to python
    sudo ln -s /usr/local/bin/python3 /usr/local/bin/python
fi

cd ..
rm -rf Python-${PYTHON_VERSION_FULL}

# Restore paths for pip to function
export PYTHONPATH=${PYTHONPATH_ORG}
export LIBRARY_PATH=${LIBRARY_PATH_ORG}
export PKG_CONFIG_PATH=${PKG_CONFIG_PATH_ORG}
export PATH=${PATH_ORG}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH_ORG}

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" &&\
    python get-pip.py
rm get-pip.py

pip install \
    nose \
    epydoc

# Create script to restore original yum functionality
cat <<EOF > /usr/local/bin/yum
#!/bin/sh
unset PYTHONPATH
unset LIBRARY_PATH
unset PKG_CONFIG_PATH
unset LD_LIBRARY_PATH
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
exec /usr/bin/yum "\$@"
EOF
chmod a+x /usr/local/bin/yum
