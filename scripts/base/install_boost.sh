#!/usr/bin/env bash

set -ex

BOOST_MAJOR_MINOR=$(echo "${BOOST_VERSION}" | cut -d. -f-2)
BOOST_MAJOR=$(echo "${BOOST_VERSION}" | cut -d. -f-1)
BOOST_MINOR=$(echo "${BOOST_MAJOR_MINOR}" | cut -d. -f2-)
BOOST_PATCH=$(echo "${BOOST_VERSION}" | cut -d. -f3-)
BOOST_VERSION_U="${BOOST_MAJOR}_${BOOST_MINOR}_${BOOST_PATCH}"

if [[ $BOOST_VERSION != 1.61* ]]; then
    BOOST_EXTRA_ARGS="cxxstd=14"
else
    BOOST_EXTRA_ARGS=""
fi

if [[ $PYTHON_VERSION == 3* ]]; then
    # The unfortunate trick is the "m" in the python include path...
    echo "using python : ${PYTHON_VERSION} : /usr/local/bin/python${PYTHON_VERSION} : /usr/local/include/python${PYTHON_VERSION}m : /usr/local/lib ;" > ~/user-config.jam
    BOOTSTRAP_ARGS="--with-python=/usr/local/bin/python${PYTHON_VERSION} --with-python-version=${PYTHON_VERSION} --with-python-root=/usr/local/lib/python${PYTHON_VERSION}"
else
    BOOTSTRAP_ARGS=""
fi

mkdir _boost
cd _boost

curl --location https://sourceforge.net/projects/boost/files/boost/${BOOST_VERSION}/boost_${BOOST_VERSION_U}.tar.gz -o boost.tar.gz
tar -xzf boost.tar.gz

cd boost_${BOOST_VERSION_U}
sh bootstrap.sh ${BOOTSTRAP_ARGS}
./b2 install -j4 variant=release toolset=gcc \
    --with-atomic \
    --with-chrono \
    --with-container \
    --with-context \
    --with-coroutine \
    --with-date_time \
    --with-exception \
    --with-filesystem \
    --with-graph \
    --with-graph_parallel \
    --with-iostreams \
    --with-locale \
    --with-log \
    --with-math \
    --with-mpi \
    --with-program_options \
    --with-random \
    --with-regex \
    --with-serialization \
    --with-system \
    --with-test \
    --with-thread \
    --with-timer \
    --with-type_erasure \
    --with-wave \
    --prefix=/usr/local \
    --with-python \
    ${BOOST_EXTRA_ARGS}

cd ../..
rm -rf _boost
