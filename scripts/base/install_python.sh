#!/usr/bin/env bash

set -ex

curl --location https://www.python.org/ftp/python/${PYTHON_VERSION_FULL}/Python-${PYTHON_VERSION_FULL}.tgz -o Python.tgz
tar xf Python.tgz && rm Python.tgz
cd Python-${PYTHON_VERSION_FULL}

./configure \
    --prefix=/usr/local \
    --enable-unicode=ucs4 \
    --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make -j4

sudo make install

cd ../..
rm -rf Python-${PYTHON_VERSION_FULL}

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" &&\
    python get-pip.py

pip install \
    nose \
    epydoc
