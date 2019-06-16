#!/usr/bin/env bash

set -ex

CPPUNIT_VERSION="$1"

wget http://dev-www.libreoffice.org/src/cppunit-${CPPUNIT_VERSION}.tar.gz
tar xf cppunit-${CPPUNIT_VERSION}.tar.gz
cd cppunit-${CPPUNIT_VERSION}

./configure --prefix=/usr/local
make -j4
make install

cd ..
rm -rf cppunit-${CPPUNIT_VERSION}
