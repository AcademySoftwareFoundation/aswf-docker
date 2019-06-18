#!/usr/bin/env bash

set -ex

PYTHON_VERSION_FULL="$1"

wget https://www.python.org/ftp/python/${PYTHON_VERSION_FULL}/Python-${PYTHON_VERSION_FULL}.tgz
tar xf Python-${PYTHON_VERSION_FULL}.tgz
cd Python-${PYTHON_VERSION_FULL}

./configure \
    --prefix=/usr/local \
    --enable-unicode=ucs4 \
    --enable-shared
make -j4
make install

cd ../..
rm -rf Python-${PYTHON_VERSION_FULL}

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" &&\
    python get-pip.py

pip install \
    nose \
    epydoc
