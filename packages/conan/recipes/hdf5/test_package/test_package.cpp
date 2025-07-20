/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5b17b876f2b6899f3cc8dbfb2282b361cd18a48a/recipes/hdf5/all/test_package/test_package.cpp
*/

#include <H5Cpp.h>

extern "C" void test_cxx_api()
{
    hsize_t dimensions[] = {4, 6};
	H5::H5File file("dataset.h5", H5F_ACC_TRUNC);
	H5::DataSpace dataspace(2, dimensions);
	H5::DataSet dataset = file.createDataSet("dataset", H5::PredType::STD_I32BE, dataspace);
}
