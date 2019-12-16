#!/usr/bin/env bash

set -ex

mkdir alembic
cd alembic

#if [ ! -f $DOWNLOADS_DIR/hdf5-${HDF5_VERSION}.tar.gz ]; then
    curl --location https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8/hdf5-${HDF5_VERSION}/src/hdf5-${HDF5_VERSION}.tar.gz -o $DOWNLOADS_DIR/hdf5-${HDF5_VERSION}.tar.gz
#fi

tar -zxf $DOWNLOADS_DIR/hdf5-${HDF5_VERSION}.tar.gz
cd hdf5-${HDF5_VERSION}
./configure \
    --prefix=${ASWF_INSTALL_PREFIX} \
    --enable-threadsafe \
    --disable-hl \
    --with-pthread=/usr/include
make -j 4
make install

cd ..

if [ ! -f $DOWNLOADS_DIR/alembic-${ALEMBIC_VERSION}.tar.gz ]; then
    curl --location https://github.com/alembic/alembic/archive/${ALEMBIC_VERSION}.tar.gz -o $DOWNLOADS_DIR/alembic-${ALEMBIC_VERSION}.tar.gz
fi
tar -zxf $DOWNLOADS_DIR/alembic-${ALEMBIC_VERSION}.tar.gz
cd alembic-${ALEMBIC_VERSION}
cmake \
    -D CMAKE_INSTALL_PREFIX=${ASWF_INSTALL_PREFIX} \
    -D CMAKE_PREFIX_PATH=${ASWF_INSTALL_PREFIX} \
    -D BOOST_ROOT=${ASWF_INSTALL_PREFIX} \
    -D ILMBASE_ROOT=${ASWF_INSTALL_PREFIX} \
    -D USE_PYILMBASE=TRUE \
    -D USE_PYALEMBIC=TRUE \
    -D USE_ARNOLD=FALSE \
    -D USE_PRMAN=FALSE \
    -D USE_MAYA=FALSE \
    .
make -j 4
make install

cd ../..
rm -rf alembic
