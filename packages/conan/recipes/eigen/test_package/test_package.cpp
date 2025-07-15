/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5f19361f49bc31a349b383c1f95c7f79627f728a/recipes/eigen/all/test_package/test_package.cpp
*/

#include <iostream>
#include <Eigen/Core>
#include <unsupported/Eigen/MatrixFunctions>


int main(void)
{
    int const N = 5;
    Eigen::MatrixXi A(N, N);
    A.setRandom();

    std::cout << "A =\n" << A << "\n\n"
              << "A(2..3,:) =\n" << A.middleRows(2, 2) << "\n";

    return 0;
}
