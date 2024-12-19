/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#(
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/yaml-cpp/all/test_package/test_package.cpp
*/

#include <string>
#include <iostream>

#include "yaml-cpp/yaml.h"

void parsing_nodes() {
    YAML::Node primes = YAML::Load("[2, 3, 5, 7, 11]");
    std::cout << "Size: " << primes.size() << '\n';
}

void building_nodes() {
    YAML::Emitter emitter;
    emitter << YAML::BeginMap;
    emitter << YAML::Key << "name";
    emitter << YAML::Value << "Ryan Braun";
    emitter << YAML::Key << "position";
    emitter << YAML::Value << "LF";
    emitter << YAML::EndMap;
    std::cout << emitter.c_str() << '\n';
}

int main() {
    parsing_nodes();
    building_nodes();
    return 0;
}
