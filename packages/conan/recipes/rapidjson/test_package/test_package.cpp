/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/3c237f4a7e8f29eacae90b809e4f18e75dfc05a3/recipes/rapidjson/all/test_package/test_package.cpp
*/

#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"

#include <iostream>

using namespace rapidjson;

int main() {
    const char* json = "{\"working\":\"false\"}";
    Document d;
    d.Parse(json);

    Value& w = d["working"];
    w.SetString("true", 4);

    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    d.Accept(writer);

    std::cout << buffer.GetString() << std::endl;
    return 0;
}
