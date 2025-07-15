/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5f19361f49bc31a349b383c1f95c7f79627f728a/recipes/nlohmann_json/all/test_package/test_package.cpp
*/

#include <iostream>

#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
    const json data = {
        {"pi", 3.141},
        {"happy", true},
        {"name", "Niels"},
        {"nothing", nullptr},
        {"answer", {
            {"everything", 42}
        }},
        {"list", {1, 0, 2}},
        {"object", {
            {"currency", "USD"},
            {"value", 42.99}
        }}
    };

#if JSON_USE_IMPLICIT_CONVERSIONS
    float f = data["pi"];
#else
    auto f = data["pi"].get<float>();
#endif
    std::cout << data.dump(4) << "\n";
    return 0;
}