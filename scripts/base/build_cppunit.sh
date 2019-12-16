#!/usr/bin/env bash

set -ex

if [ ! -f $DOWNLOADS_DIR/cppunit-${CPPUNIT_VERSION}.tar.gz ]; then
    curl --location http://dev-www.libreoffice.org/src/cppunit-${CPPUNIT_VERSION}.tar.gz -o $DOWNLOADS_DIR/cppunit-${CPPUNIT_VERSION}.tar.gz
fi

tar xf $DOWNLOADS_DIR/cppunit-${CPPUNIT_VERSION}.tar.gz
cd cppunit-${CPPUNIT_VERSION}

./configure --prefix=${ASWF_INSTALL_PREFIX}
make -j4
make install

cd ..
rm -rf cppunit-${CPPUNIT_VERSION}
