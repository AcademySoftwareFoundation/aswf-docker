#!/usr/bin/env bash

set -ex

pypath=`which python`
if [[ $pypath != /usr/local/bin/python ]]
then
    echo "Wrong python location: $pypath"
    exit 1
fi

pyversion=`python --version`
if [[ $pyversion != Python\ 3.7* ]]
then
    echo "Wrong python version: $pyversion"
    exit 1
fi
