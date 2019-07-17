#!/usr/bin/env bash

set -ex

curl --location http://dev-www.libreoffice.org/src/cppunit-${CPPUNIT_VERSION}.tar.gz -o cppunit.tar.gz
tar xf cppunit.tar.gz && rm cppunit.tar.gz
cd cppunit-${CPPUNIT_VERSION}

./configure --prefix=/usr/local
make -j4
make install

cd ..
rm -rf cppunit-${CPPUNIT_VERSION}
